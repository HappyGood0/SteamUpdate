from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

class SteamRequest(BaseModel):
    steam_id: str

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.post("/api/recommend")
async def recommend(request: SteamRequest):
    return {
        "steam_id": request.steam_id,
        "game": "Half-Life 3",
        "score": 0.95
    }

Instrumentator().instrument(app).expose(app)