import httpx
from fastapi import APIRouter, HTTPException, Query
from src.models.Games import GamesRecommendationResponse

# Router pour les endpoints météo
router = APIRouter(prefix="/games", tags=["Games"])


@router.get("/current", response_model=GamesRecommendationResponse)
async def get_game_structure(
    id: int = Query(..., description="ID du jeu de référence", ge=0),
):
    """
    Récupère les recommandations de jeux basées sur un jeu de référence.

    Args:
        id: ID du jeu de référence

    Returns:
        GamesRecommendationResponse: Données des jeux recommandés

    Raises:
        HTTPException: 404 si le jeu n'est pas trouvé, 500 en cas d'erreur serveur
    """
    try:
        # Logique pour récupérer les recommandations de jeux
        # Ceci est un exemple fictif, remplacez-le par la logique réelle
        recommanded_games = await get_game_structure(id)
        return recommanded_games

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"Jeu avec ID '{id}' non trouvé.",
            ) from e
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Erreur lors de la récupération des données de jeu: {str(e)}",
        ) from e
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur de connexion à l'API de jeux: {str(e)}"
        ) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}") from e
