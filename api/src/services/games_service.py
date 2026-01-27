import httpx
from typing import Optional
from datetime import datetime
from mlflow.tracking import MlflowClient
import mlflow
import mlflow.sklearn
from src.models.Games import (
    GamesRecommendationRequest,
    GamesRecommendationResponse,
)

class GamesService:
    """Service pour récupérer les recommandations de jeux depuis une API fictive"""

    def __init__(self,idSteam: int):
        # Configuration de l'API de jeux (exemple fictif)
        self.idSteam = idSteam
    def get_game_recommendations(self) -> GamesRecommendationResponse:

        # Logique fictive pour récupérer les recommandations de jeux
        # Remplacez ceci par la logique réelle pour interagir avec une API de jeux
        recommended_games = [
            GamesRecommendationResponse(
                img="https://example.com/game1.jpg",
                prix=1999,
                tags=["Action", "Aventure"],
                nom="Jeu A",
                lien="https://store.steampowered.com/app/123456/Jeu_A/"
            ),
            GamesRecommendationResponse(
                img="https://example.com/game2.jpg",
                prix=2999,
                tags=["RPG", "Multijoueur"],
                nom="Jeu B",
                lien="https://store.steampowered.com/app/654321/Jeu_B/"
            ),
        ]
        return recommended_games
    