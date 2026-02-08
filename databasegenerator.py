import csv
import os

import requests
from dotenv import load_dotenv
from steam_web_api import Steam

# Charge les variables du fichier .env situé dans le même dossier
load_dotenv()

# Récupère la clé
KEY = os.getenv("STEAM_API_KEY")


# Utilisation de la variable KEY ici
steam = Steam(KEY)

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

colonne_user = [
    "ID",
    "nom",
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


i = 0
testid = 76561198000047504


def createbddtopgame():
    url = "https://steamspy.com/api.php?request=top100forever"
    response = requests.get(url).json()
    with open("top100games.csv", "a", encoding="utf-8") as topgame:
        writer_user = csv.DictWriter(topgame, fieldnames=colonne_user)
        for game in response:
            url = f"https://steamspy.com/api.php?request=appdetails&appid={str(game)}"
            currentgame = requests.get(url).json()
            gameprofil = {"ID": game, "nom": currentgame.get("name")}

            tags = currentgame.get("tags", {})

            if isinstance(tags, dict) and tags != {}:
                filtered_tags = {key: value for key, value in tags.items() if key in VALIDTAG}
            total = round(sum(list(filtered_tags.values())), 2)
            for tags in VALIDTAG:
                value = filtered_tags.get(tags)

                if value is not None:
                    gameprofil.update({tags: value / total})
                else:
                    gameprofil.update({tags: 0})
            writer_user.writerow(gameprofil)
            gameprofil = {}


createbddtopgame()
