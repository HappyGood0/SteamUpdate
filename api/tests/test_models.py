import pytest
from pydantic import ValidationError
from src.models.Games import (
    GamesRecommendationRequest,
    GamesRecommendationResponse,
    GamesStructure,
)


def test_games_recommendation_request_valid():
    """Test de création valide d'une requête de recommandation"""
    request = GamesRecommendationRequest(id=123)
    assert request.id == 123


def test_games_recommendation_request_negative_id():
    """Test qu'un ID négatif est rejeté"""
    with pytest.raises(ValidationError):
        GamesRecommendationRequest(id=-1)


def test_games_recommendation_response_valid():
    """Test de création valide d'une réponse de recommandation"""
    response = GamesRecommendationResponse(
        img="https://example.com/game.jpg",
        prix="1999",  # Correction: string
        tags=["Action", "RPG"],
        nom="Test Game",
        lien="https://store.steampowered.com/app/123",
    )
    assert response.prix == "1999"
    assert "Action" in response.tags


def test_games_recommendation_response_empty_name():
    """Test qu'un nom vide est rejeté"""
    with pytest.raises(ValidationError):
        GamesRecommendationResponse(
            img="https://example.com/game.jpg",
            prix=1999,
            tags=["Action"],
            nom="",
            lien="https://store.steampowered.com",
        )


def test_games_structure_valid():
    """Test de création valide d'une structure de jeu"""
    game = GamesStructure(
        nom="Half-Life",
        Atmospheric=0.8,
        Fantasy=0.2,
        Relaxing=0.0,
        Funny=0.1,
        Horror=0.6,
        Sci_fi=0.9,
        Futuristic=0.8,
        Retro=0.3,
        Dark=0.7,
        Mystery=0.5,
        Survival=0.4,
        Psychological_Horror=0.3,
        Medieval=0.0,
        Management=0.0,
        Sports=0.0,
        Building=0.0,
        Tactical=0.5,
        Drama=0.4,
        Space=0.2,
        Romance=0.0,
        Racing=0.0,
        Dark_Fantasy=0.0,
        Logic=0.6,
        Emotional=0.3,
        Nature=0.0,
        Post_apocalyptic=0.6,
        War=0.4,
        Historical=0.0,
        Zombies=0.5,
        Stealth=0.3,
        Investigation=0.2,
        Dark_Humor=0.1,
        Parkour=0.0,
        Flight=0.0,
        Pirates=0.0,
        Steampunk=0.0,
        Indie=0.0,
        Action=0.9,
        Casual=0.0,
        Adventure=0.7,
        Simulation=0.0,
        RPG=0.0,
        Strategy=0.0,
        Action_Adventure=0.8,
        _3D=1.0,
        _2D=0.0,
        First_Person=1.0,
        Third_Person=0.0,
        Top_Down=0.0,
        Realistic=0.8,
        Cartoony=0.0,
        Hand_drawn=0.0,
        Text_Based=0.0,
        Isometric=0.0,
        PvP=0.2,
        PvE=0.8,
        Open_World=0.0,
        Story_Rich=0.9,
        Combat=0.9,
        Turn_Based_Combat=0.0,
        Turn_Based_Tactics=0.0,
        Hack_and_Slash=0.0,
        Deckbuilding=0.0,
        Team_Based=0.0,
        Puzzle=0.7,
        Platformer=0.0,
        Shooter=1.0,
        Arcade=0.0,
        Visual_Novel=0.0,
        Roguelike=0.0,
        Sandbox=0.0,
        Point_Click=0.0,
        RTS=0.0,
        Tower_Defense=0.0,
        Rhythm=0.0,
        Singleplayer=1.0,
        Multiplayer=0.3,
        Online_Co_op=0.0,
        Local_Co_op=0.0,
        d3=1.0,
        d2=0.0,
    )
    assert game.nom == "Half-Life"
    assert game.Shooter == 1.0
