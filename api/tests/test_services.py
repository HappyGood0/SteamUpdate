from unittest.mock import MagicMock, patch

import pytest
from src.services.games_service import GamesService


@pytest.fixture
def mock_dependencies():
    """Mock de toutes les dépendances externes"""
    with (
        patch("src.services.games_service.Steam"),
        patch("src.services.games_service.mlflow.sklearn.load_model") as mock_model,
        patch("pandas.read_csv") as mock_csv,
    ):
        mock_model.return_value = MagicMock()
        mock_csv.return_value = MagicMock()
        yield


def test_games_service_initialization(mock_dependencies):
    """Test d'initialisation du service de jeux"""
    with patch.dict("os.environ", {"STEAM_API_KEY": "fake_key"}):
        service = GamesService(id_steam=76561198167767436)
        assert service.id_steam == 76561198167767436


def test_get_game_recommendations(mock_dependencies):
    """Test de récupération des recommandations"""
    with patch.dict("os.environ", {"STEAM_API_KEY": "fake_key"}):
        service = GamesService(id_steam=123456)
        recommendations = service.get_game_recommendations()

        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        # Vérification que les recommandations contiennent les attributs attendus
        if len(recommendations) > 0:
            assert hasattr(recommendations[0], "nom")
            assert hasattr(recommendations[0], "prix")
