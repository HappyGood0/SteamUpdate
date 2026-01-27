from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import httpx
from src.models.Games import GamesRecommendationRequest, GamesRecommendationResponse

# Router pour les endpoints météo
router = APIRouter(prefix="/weather", tags=["Weather"])


# @router.get("/current", response_model=GamesRecommendationResponse)
# async def get_game_recommendations(