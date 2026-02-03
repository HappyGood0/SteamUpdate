import json
import time
from steam_web_api import Steam
import os
from dotenv import load_dotenv
import requests
import numpy as np

# Charge les variables du fichier .env situé dans le même dossier
load_dotenv()

# Récupère la clé
KEY = os.getenv("STEAM_API_KEY")

    
    # Utilisation de la variable KEY ici
steam = Steam(KEY)

i=0
testid = 76561198000047504
with open("userid.json", "a", encoding="utf-8") as f:
    while i < 100:
        print(testid)
        owned_games = steam.users.get_owned_games(str(testid))

        if owned_games is not None:
            games_list = owned_games.get("games", [])
    
        if len(games_list) > 20:
        
            json.dump(testid, f)
            f.write("\n")
            print("sucess")
            i += 1
            pass
        testid += 1
        print(i)
        time.sleep(1)