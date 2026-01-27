from pydantic import BaseModel, Field
from typing import List, Optional

VALIDTAG = ["Atmospheric", "Fantasy", "Relaxing", "Funny", "Horror", "Sci-fi", "Futuristic", "Retro", "Dark", "Mystery", "Survival", "Psychological Horror",
"Medieval", "Management", "Sports", "Building", "Tactical", "Drama", "Space", "Romance", "Racing", "Dark Fantasy", "Logic", "Emotional", "Nature",
"Post-apocalyptic", "War", "Historical", "Zombies", "Stealth", "Investigation", "Dark Humor", "Parkour", "Flight", "Pirates", "Steampunk",
"Indie", "Action", "Casual", "Adventure", "Simulation", "RPG", "Strategy", "Action-Adventure",
"3D", "2D", "First-Person", "Third-Person", "Top-Down", "Realistic", "Cartoony", "Hand-drawn", "Text-Based", "Isometric",
"PvP", "PvE", "Open World", "Story Rich", "Combat", "Controller", "Choices Matter", "Linear", "Turn-Based Combat", "Turn-Based Tactics", "Hack and Slash",
"Deckbuilding", "Team-Based",
"Puzzle", "Platformer", "Shooter", "Arcade", "Visual Novel", "Roguelike", "Sandbox", "Point & Click", "RTS", "Tower Defense", "Rhythm",
"Singleplayer", "Multiplayer", "Online Co-op", "Local Co-op"]

class GamesRecommendationResponse(BaseModel):
    """DTO pour la requête de recommandations de jeux"""
    
    img : str = Field(..., description="URL de l'image du jeu", min_length=1)
    prix : int = Field(..., description="Prix du jeu en centimes", ge=0)
    tags : List[str] = Field(..., description="Liste des tags associés au jeu") 
    nom : str = Field(..., description="Nom du jeu", min_length=1)
    lien : str = Field(..., description="URL du jeu", min_length=1)
    
class GamesRecommendationRequest(BaseModel):
    """DTO pour la réponse de recommandations de jeux"""
    
    id : int = Field(..., description="ID du jeu de référence", ge=0)
