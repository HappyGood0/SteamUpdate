from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@patch("src.services.games_service.GamesService.resolve_vanity_url", return_value=76561198167767436)
@patch("src.services.games_service.mlflow.sklearn.load_model")
@patch("src.services.games_service.Steam")
@patch("src.services.games_service.pd.read_csv")
@patch("src.services.games_service.GamesService.get_user_game_list")
def test_recommend_endpoint_valid_pseudo(
    mock_get_user_game_list, mock_read_csv, mock_steam, mock_load_model, mock_resolve_vanity_url
):
    """Test du endpoint /api/recommend avec un pseudo Steam (mocké)"""
    mock_read_csv.return_value = pd.DataFrame(
        [
            {"nom": "Game 1", "Action": 0.9, "RPG": 0.8, "prix": 1999},
            {"nom": "Game 2", "Action": 0.7, "RPG": 0.6, "prix": 1499},
            {"nom": "Game 3", "Action": 0.5, "RPG": 0.4, "prix": 999},
        ]
    )
    steam_mock = MagicMock()
    steam_mock.users.get_user_details.return_value = {"player": {"personaname": "TestUser"}}
    search_games_mock = MagicMock()
    search_games_mock.get.side_effect = (
        lambda key: [
            {
                "img": "https://example.com/game.jpg",
                "lien": "https://store.steampowered.com/app/1",
                "nom": "Game 1",
                "prix": 1999,
            }
        ]
        if key == "apps"
        else None
    )
    steam_mock.apps.search_games.return_value = search_games_mock
    mock_steam.return_value = steam_mock
    mock_load_model.return_value.predict.return_value = [0.95, 0.85, 0.75]
    mock_get_user_game_list.return_value = [
        [1, "Game 1", 100, 10, 100, 10, 1.0],
        [2, "Game 2", 80, 8, 80, 8, 0.8],
        [3, "Game 3", 60, 6, 60, 6, 0.6],
    ]
    response = client.post("/api/recommend", json={"pseudo": "monPseudoSteam"})
    assert response.status_code == 200
    data = response.json()
    assert "steam_id" in data
    assert "recommendations" in data
    assert data["steam_id"] == "76561198167767436"
    assert isinstance(data["recommendations"], list)
    assert len(data["recommendations"]) > 0


def test_health_endpoint():
    """Test du endpoint /api/health"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("src.services.games_service.GamesService.get_user_game_list")
@patch("src.services.games_service.pd.read_csv")
@patch("src.services.games_service.Steam")
@patch("src.services.games_service.mlflow.sklearn.load_model")
def test_recommend_endpoint_valid(
    mock_load_model, mock_steam, mock_read_csv, mock_get_user_game_list
):
    """Test du endpoint /api/recommend avec une requête valide (mocké)"""
    # Mock de la base de données
    mock_read_csv.return_value = pd.DataFrame(
        [
            {"nom": "Game 1", "Action": 0.9, "RPG": 0.8, "prix": 1999},
            {"nom": "Game 2", "Action": 0.7, "RPG": 0.6, "prix": 1499},
            {"nom": "Game 3", "Action": 0.5, "RPG": 0.4, "prix": 999},
        ]
    )
    # Mock Steam
    steam_mock = MagicMock()
    steam_mock.users.get_user_details.return_value = {"player": {"personaname": "TestUser"}}
    search_games_mock = MagicMock()
    search_games_mock.get.side_effect = (
        lambda key: [
            {
                "img": "https://example.com/game.jpg",
                "lien": "https://store.steampowered.com/app/1",
                "nom": "Game 1",
                "prix": 1999,
            }
        ]
        if key == "apps"
        else None
    )
    steam_mock.apps.search_games.return_value = search_games_mock
    mock_steam.return_value = steam_mock
    # Mock modèle MLflow
    mock_load_model.return_value.predict.return_value = [0.95, 0.85, 0.75]
    # Mock jeux utilisateur
    mock_get_user_game_list.return_value = [
        [1, "Game 1", 100, 10, 100, 10, 1.0],
        [2, "Game 2", 80, 8, 80, 8, 0.8],
        [3, "Game 3", 60, 6, 60, 6, 0.6],
    ]

    response = client.post("/api/recommend", json={"steam_id": "76561198167767436"})
    assert response.status_code == 200
    data = response.json()
    assert "steam_id" in data
    assert "recommendations" in data
    assert data["steam_id"] == "76561198167767436"
    assert isinstance(data["recommendations"], list)
    assert len(data["recommendations"]) > 0


def test_recommend_endpoint_missing_steam_id():
    """Test du endpoint /api/recommend sans steam_id"""
    try:
        response = client.post("/api/recommend", json={})
        assert response.status_code in (400, 422)
    except ValueError as e:
        assert "steam_id ou pseudo requis" in str(e)


def test_recommend_endpoint_invalid_payload():
    """Test du endpoint /api/recommend avec payload invalide"""
    try:
        response = client.post("/api/recommend", json={"invalid": "data"})
        assert response.status_code in (400, 422)
    except ValueError as e:
        assert "steam_id ou pseudo requis" in str(e)


@pytest.mark.asyncio
async def test_metrics_exposed():
    """Test que les métriques Prometheus sont exposées"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "Health_check_requests_total" in response.text
