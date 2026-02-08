import time

from fastapi import FastAPI
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
from src.metrics import (
    recommendation_response_time,
    recommendations_total,
)
from fastapi.middleware.cors import CORSMiddleware

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
        # faudra faire le traitement ici j'imagine, appeler les fonctions de games_service etc.

        result = {"steam_id": request.steam_id, "game": "Half-Life 3", "score": 0.95}

        recommendations_total.labels(status="success").inc()

        return result

    except Exception:
        recommendations_total.labels(status="error").inc()
        raise

    finally:
        duration = time.time() - start_time
        recommendation_response_time.observe(duration)


Instrumentator().instrument(app).expose(app)
