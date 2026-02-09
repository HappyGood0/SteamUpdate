from pydantic import BaseModel, ConfigDict, Field

VALIDTAG = [
    "Atmospheric",
    "Fantasy",
    "Relaxing",
    "Funny",
    "Horror",
    "Sci-fi",
    "Futuristic",
    "Retro",
    "Dark",
    "Mystery",
    "Survival",
    "Psychological Horror",
    "Medieval",
    "Management",
    "Sports",
    "Building",
    "Tactical",
    "Drama",
    "Space",
    "Romance",
    "Racing",
    "Dark Fantasy",
    "Logic",
    "Emotional",
    "Nature",
    "Post-apocalyptic",
    "War",
    "Historical",
    "Zombies",
    "Stealth",
    "Investigation",
    "Dark Humor",
    "Parkour",
    "Flight",
    "Pirates",
    "Steampunk",
    "Indie",
    "Action",
    "Casual",
    "Adventure",
    "Simulation",
    "RPG",
    "Strategy",
    "Action-Adventure",
    "3D",
    "2D",
    "First-Person",
    "Third-Person",
    "Top-Down",
    "Realistic",
    "Cartoony",
    "Hand-drawn",
    "Text-Based",
    "Isometric",
    "PvP",
    "PvE",
    "Open World",
    "Story Rich",
    "Combat",
    "Controller",
    "Choices Matter",
    "Linear",
    "Turn-Based Combat",
    "Turn-Based Tactics",
    "Hack and Slash",
    "Deckbuilding",
    "Team-Based",
    "Puzzle",
    "Platformer",
    "Shooter",
    "Arcade",
    "Visual Novel",
    "Roguelike",
    "Sandbox",
    "Point & Click",
    "RTS",
    "Tower Defense",
    "Rhythm",
    "Singleplayer",
    "Multiplayer",
    "Online Co-op",
    "Local Co-op",
]
VALIDTAGBDD = [
    "Atmospheric",
    "Fantasy",
    "Relaxing",
    "Funny",
    "Horror",
    "Sci_fi",
    "Futuristic",
    "Retro",
    "Dark",
    "Mystery",
    "Survival",
    "Psychological_Horror",
    "Medieval",
    "Management",
    "Sports",
    "Building",
    "Tactical",
    "Drama",
    "Space",
    "Romance",
    "Racing",
    "Dark_Fantasy",
    "Logic",
    "Emotional",
    "Nature",
    "Post_apocalyptic",
    "War",
    "Historical",
    "Zombies",
    "Stealth",
    "Investigation",
    "Dark_Humor",
    "Parkour",
    "Flight",
    "Pirates",
    "Steampunk",
    "Indie",
    "Action",
    "Casual",
    "Adventure",
    "Simulation",
    "RPG",
    "Strategy",
    "Action_Adventure",
    "_3D",
    "_2D",
    "First_Person",
    "Third_Person",
    "Top_Down",
    "Realistic",
    "Cartoony",
    "Hand_drawn",
    "Text_Based",
    "Isometric",
    "PvP",
    "PvE",
    "Open_World",
    "Story_Rich",
    "Combat",
    "Controller",
    "Choices_Matter",
    "Linear",
    "Turn_Based_Combat",
    "Turn_Based_Tactics",
    "Hack_and_Slash",
    "Deckbuilding",
    "Team_Based",
    "Puzzle",
    "Platformer",
    "Shooter",
    "Arcade",
    "Visual_Novel",
    "Roguelike",
    "Sandbox",
    "Point_&_Click",
    "RTS",
    "Tower_Defense",
    "Rhythm",
    "Singleplayer",
    "Multiplayer",
    "Online_Co_op",
    "Local_Co_op",
]


class GamesRecommendationResponse(BaseModel):
    """DTO pour la requête de recommandations de jeux"""

    img: str = Field(description="URL de l'image du jeu", min_length=1, default="")
    prix: str = Field(description="Prix du jeu en dollar", default="")
    tags: list[str] = Field(description="Liste des tags associés au jeu", default=[])
    nom: str = Field(description="Nom du jeu", min_length=1, default="")
    lien: str = Field(description="URL du jeu", min_length=1, default="")
    score: float = Field(description="Score de similarité du jeu recommandé", ge=0.0, default=0.0)


class GamesRecommendationRequest(BaseModel):
    """DTO pour la réponse de recommandations de jeux"""

    id: int = Field(..., description="ID du jeu de référence", ge=0)


class GamesStructure(BaseModel):
    """DTO pour la structure d'un jeu dans la liste de jeux de l'utilisateur"""

    model_config = ConfigDict(populate_by_name=True)

    nom: str = Field(default="", description="Nom du jeu")
    Atmospheric: float = Field(default=0.0, description="Score du tag Atmospheric", ge=0)
    Fantasy: float = Field(default=0.0, description="Score du tag Fantasy", ge=0)
    Relaxing: float = Field(default=0.0, description="Score du tag Relaxing", ge=0)
    Funny: float = Field(default=0.0, description="Score du tag Funny", ge=0)
    Horror: float = Field(default=0.0, description="Score du tag Horror", ge=0)
    Sci_fi: float = Field(default=0.0, description="Score du tag Sci-fi", ge=0)
    Futuristic: float = Field(default=0.0, description="Score du tag Futuristic", ge=0)
    Retro: float = Field(default=0.0, description="Score du tag Retro", ge=0)
    Dark: float = Field(default=0.0, description="Score du tag Dark", ge=0)
    Mystery: float = Field(default=0.0, description="Score du tag Mystery", ge=0)
    Survival: float = Field(default=0.0, description="Score du tag Survival", ge=0)
    Psychological_Horror: float = Field(
        default=0.0, description="Score du tag Psychological Horror", ge=0
    )
    Medieval: float = Field(default=0.0, description="Score du tag Medieval", ge=0)
    Management: float = Field(default=0.0, description="Score du tag Management", ge=0)
    Sports: float = Field(default=0.0, description="Score du tag Sports", ge=0)
    Building: float = Field(default=0.0, description="Score du tag Building", ge=0)
    Tactical: float = Field(default=0.0, description="Score du tag Tactical", ge=0)
    Drama: float = Field(default=0.0, description="Score du tag Drama", ge=0)
    Space: float = Field(default=0.0, description="Score du tag Space", ge=0)
    Romance: float = Field(default=0.0, description="Score du tag Romance", ge=0)
    Racing: float = Field(default=0.0, description="Score du tag Racing", ge=0)
    Dark_Fantasy: float = Field(default=0.0, description="Score du tag Dark Fantasy", ge=0)
    Logic: float = Field(default=0.0, description="Score du tag Logic", ge=0)
    Emotional: float = Field(default=0.0, description="Score du tag Emotional", ge=0)
    Nature: float = Field(default=0.0, description="Score du tag Nature", ge=0)
    Post_apocalyptic: float = Field(default=0.0, description="Score du tag Post-apocalyptic", ge=0)
    War: float = Field(default=0.0, description="Score du tag War", ge=0)
    Historical: float = Field(default=0.0, description="Score du tag Historical", ge=0)
    Zombies: float = Field(default=0.0, description="Score du tag Zombies", ge=0)
    Stealth: float = Field(default=0.0, description="Score du tag Stealth", ge=0)
    Investigation: float = Field(default=0.0, description="Score du tag Investigation", ge=0)
    Dark_Humor: float = Field(default=0.0, description="Score du tag Dark Humor", ge=0)
    Parkour: float = Field(default=0.0, description="Score du tag Parkour", ge=0)
    Flight: float = Field(default=0.0, description="Score du tag Flight", ge=0)
    Pirates: float = Field(default=0.0, description="Score du tag Pirates", ge=0)
    Steampunk: float = Field(default=0.0, description="Score du tag Steampunk", ge=0)
    Indie: float = Field(default=0.0, description="Score du tag Indie", ge=0)
    Action: float = Field(default=0.0, description="Score du tag Action", ge=0)
    Casual: float = Field(default=0.0, description="Score du tag Casual", ge=0)
    Adventure: float = Field(default=0.0, description="Score du tag Adventure", ge=0)
    Simulation: float = Field(default=0.0, description="Score du tag Simulation", ge=0)
    RPG: float = Field(default=0.0, description="Score du tag RPG", ge=0)
    Strategy: float = Field(default=0.0, description="Score du tag Strategy", ge=0)
    Action_Adventure: float = Field(default=0.0, description="Score du tag Action-Adventure", ge=0)
    d3: float = Field(default=0.0, description="Score du tag 3D", ge=0)
    d2: float = Field(default=0.0, description="Score du tag 2D", ge=0)
    First_Person: float = Field(default=0.0, description="Score du tag First-Person", ge=0)
    Third_Person: float = Field(default=0.0, description="Score du tag Third-Person", ge=0)
    Top_Down: float = Field(default=0.0, description="Score du tag Top-Down", ge=0)
    Realistic: float = Field(default=0.0, description="Score du tag Realistic", ge=0)
    Cartoony: float = Field(default=0.0, description="Score du tag Cartoony", ge=0)
    Hand_drawn: float = Field(default=0.0, description="Score du tag Hand-drawn", ge=0)
    Text_Based: float = Field(default=0.0, description="Score du tag Text-Based", ge=0)
    Isometric: float = Field(default=0.0, description="Score du tag Isometric", ge=0)
    PvP: float = Field(default=0.0, description="Score du tag PvP", ge=0)
    PvE: float = Field(default=0.0, description="Score du tag PvE", ge=0)
    Open_World: float = Field(default=0.0, description="Score du tag Open World", ge=0)
    Story_Rich: float = Field(default=0.0, description="Score du tag Story Rich", ge=0)
    Combat: float = Field(default=0.0, description="Score du tag Combat", ge=0)
    Turn_Based_Combat: float = Field(
        default=0.0, description="Score du tag Turn-Based Combat", ge=0
    )
    Turn_Based_Tactics: float = Field(
        default=0.0, description="Score du tag Turn-Based Tactics", ge=0
    )
    Hack_and_Slash: float = Field(default=0.0, description="Score du tag Hack and Slash", ge=0)
    Deckbuilding: float = Field(default=0.0, description="Score du tag Deckbuilding", ge=0)
    Team_Based: float = Field(default=0.0, description="Score du tag Team-Based", ge=0)
    Puzzle: float = Field(default=0.0, description="Score du tag Puzzle", ge=0)
    Platformer: float = Field(default=0.0, description="Score du tag Platformer", ge=0)
    Shooter: float = Field(default=0.0, description="Score du tag Shooter", ge=0)
    Arcade: float = Field(default=0.0, description="Score du tag Arcade", ge=0)
    Visual_Novel: float = Field(default=0.0, description="Score du tag Visual Novel", ge=0)
    Roguelike: float = Field(default=0.0, description="Score du tag Roguelike", ge=0)
    Sandbox: float = Field(default=0.0, description="Score du tag Sandbox", ge=0)
    Point_Click: float = Field(default=0.0, description="Score du tag Point & Click", ge=0)
    RTS: float = Field(default=0.0, description="Score du tag RTS", ge=0)
    Tower_Defense: float = Field(default=0.0, description="Score du tag Tower Defense", ge=0)
    Rhythm: float = Field(default=0.0, description="Score du tag Rhythm", ge=0)
    Singleplayer: float = Field(default=0.0, description="Score du tag Singleplayer", ge=0)
    Multiplayer: float = Field(default=0.0, description="Score du tag Multiplayer", ge=0)
    Online_Co_op: float = Field(default=0.0, description="Score du tag Online Co-op", ge=0)
    Local_Co_op: float = Field(default=0.0, description="Score du tag Local Co-op", ge=0)
