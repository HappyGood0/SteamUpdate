import httpx
from typing import Optional
from datetime import datetime
from mlflow.tracking import MlflowClient
import mlflow
import mlflow.sklearn
from src.models.Games import (
    GamesRecommendationRequest,
    GamesRecommendationResponse,
    VALIDTAG,
)
from steam_web_api import Steam
import os
from dotenv import load_dotenv
import requests
import numpy as np



class GamesService:
    """Service pour récupérer les recommandations de jeux depuis une API fictive"""

    def __init__(self,idSteam: int):
        # Configuration de l'API de jeux (exemple fictif)
        self.idSteam = idSteam
        load_dotenv()
        KEY = os.getenv("STEAM_API_KEY")
        self.steam = Steam(KEY)

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
    
    def get_user_game_list(self) -> list:
        usergame = self.steam.users.get_owned_games("76561198205309263")
        usergamelist = usergame.get("games")
        gamedata = []
        
        for game in usergamelist:
            
            gameid = game.get("appid")
            gamename = game.get("name")
            gameplaytime4ever = game.get("playtime_forever")
            gameplaytime2weeks = game.get("playtime_2weeks") if game.get("playtime_2weeks")!=None else 0

            url = f"https://steamspy.com/api.php?request=appdetails&appid={gameid}"
            response = requests.get(url).json()

            avgplaytime4ever = response.get("median_forever")
            avgplaytime2weeks = response.get("median_2weeks")

            k = 480

            if response.get("price") != "0" and response.get("price") != None:
                k = 0


            if avgplaytime4ever != 0:
                score = 0.7*np.log(1+gameplaytime4ever)/np.log(1+(avgplaytime4ever + k)) + 0.3*np.log(1+gameplaytime2weeks)/np.log(1+avgplaytime2weeks) if avgplaytime2weeks > 0 else 0.7*np.log(1+gameplaytime4ever)/np.log(1+(avgplaytime4ever + k))
                gamedata.append([gameid, gamename, gameplaytime4ever, gameplaytime2weeks, avgplaytime4ever, avgplaytime2weeks, score])


        gamedata.sort(key=lambda x: x[6], reverse=True)

        return gamedata
    
    def get_avg_price(self,usergamelist) -> float:
        useravgprice = 1
        nbpaidgame = 1
        for game in usergamelist:
            gameid = game[0]
            url = f"https://steamspy.com/api.php?request=appdetails&appid={gameid}"
            response = requests.get(url).json()

            if response.get("price") != "0" and response.get("price") != None:
                    useravgprice += int(response.get("price"))
                    nbpaidgame += 1

        return useravgprice/nbpaidgame
    

    def get_favorite_game_tags(self, gamedata) -> list:
        usergametags = []

        for i in range(0,5):
            gameid = gamedata[i][0]
            url = f"https://steamspy.com/api.php?request=appdetails&appid={gameid}"
            response = requests.get(url).json()
            tags = response.get("tags")

            for tag in list(tags.keys()):
                if tag not in VALIDTAG:
                    del tags[tag]
            usergametags.append([gameid, gamedata[i][1], gamedata[i][6], tags])

        return usergametags