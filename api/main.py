from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter

app = FastAPI()

health_counter = Counter('Health_check_requests', 'Number of health check requests received')

class SteamRequest(BaseModel):
    steam_id: str

@app.get("/api/health")
async def health():
    health_counter.inc()
    return {"status": "ok"}

@app.post("/api/recommend")
async def recommend(request: SteamRequest):
    return {
        "steam_id": request.steam_id,
        "game": "Half-Life 3",
        "score": 0.95
    }

Instrumentator().instrument(app).expose(app)