from unittest.mock import MagicMock, patch

import pandas as pd
from src.services.games_service import GamesService


@patch("src.services.games_service.pd.read_csv")
@patch("src.services.games_service.mlflow.sklearn.load_model")
def test_games_service_initialization(mock_load_model, mock_read_csv):
    """Test d'initialisation du service de jeux avec mocks simples"""
    mock_read_csv.return_value = pd.DataFrame(
        [
            {"nom": "Game 1", "Action": 0.9, "RPG": 0.8, "prix": 1999},
        ]
    )
    mock_load_model.return_value = MagicMock()
    with patch.dict("os.environ", {"STEAM_API_KEY": "fake_key"}):
        service = GamesService(steam_identifier=76561198167767436)
        assert service.id_steam == 76561198167767436
        assert service.games_db is not None
        assert service.model is not None
