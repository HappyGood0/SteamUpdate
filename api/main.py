import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
from src.metrics import (
    recommendation_response_time,
    recommendations_total,
)
from src.services.games_service import GamesService

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://happygood0.github.io",
        "http://localhost:5173",
        "http://localhost",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


health_counter = Counter("Health_check_requests_total", "Number of health check requests received")


class SteamRequest(BaseModel):
    steam_id: str


@app.get("/api/health")
async def health():
    health_counter.inc()
    return {"status": "ok"}


@app.post("/api/recommend")
async def recommend(request: SteamRequest):
    start_time = time.time()

    try:
        service = GamesService(id_steam=int(request.steam_id))
        profil = service.get_game_structure()
        recommended = service.get_best_games_with_scores(profil, top_n=3)
        result = {
            "steam_id": request.steam_id,
            "recommendations": recommended,
        }
        result["build"] = "46799e6"

        recommendations_total.labels(status="success").inc()

        return result

    except Exception:
        recommendations_total.labels(status="error").inc()
        raise

    finally:
        duration = time.time() - start_time
        recommendation_response_time.observe(duration)


Instrumentator().instrument(app).expose(app)
