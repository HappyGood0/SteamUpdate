from turtle import pd
import httpx
from typing import Dict, List, Optional
from datetime import datetime
from matplotlib.path import Path
from mlflow.tracking import MlflowClient
import mlflow
import mlflow.sklearn
from src.models.Games import (
    GamesRecommendationRequest,
    GamesRecommendationResponse,
    VALIDTAG,
    GamesStructure,
)
from steam_web_api import Steam
import os
from dotenv import load_dotenv
import requests
import numpy as np
import time
from src.metrics import (
    external_api_duration,
    external_api_errors_total,
    games_processed_per_recommendation
)

class GamesService:
    """Service pour récupérer les recommandations de jeux depuis une API fictive"""

    def __init__(self,idSteam: int):
        # Configuration de l'API de jeux (exemple fictif)
        self.idSteam = idSteam
        load_dotenv()
        KEY = os.getenv("STEAM_API_KEY")
        self.steam = Steam(KEY)
        try:
            self.model = mlflow.sklearn.load_model("models:/topGamesUser_regressor/Staging")
            print("✅ Modèle MLflow chargé avec succès")
        except Exception as e:
            print(f"⚠️ Erreur lors du chargement du modèle: {e}")
            self.model = None

        csv_path = Path(__file__).resolve().parents[3] / "bdd" / "steamgames.csv"
        try:
            self.games_db = pd.read_csv(csv_path, sep=',')
            print(f"✅ Base de données chargée: {len(self.games_db)} jeux")
        except Exception as e:
            print(f"⚠️ Erreur lors du chargement de la BDD: {e}")
            self.games_db = None
    
    def getBestGamesWithScores(self, game: GamesStructure, top_n: int = 3) -> List[Dict]:
        """
        Compare un jeu avec tous les jeux de la base de données et retourne les meilleurs matchs
        
        Args:
            game: Instance de GamesStructure à comparer
            top_n: Nombre de recommandations à retourner
            
        Returns:
            Liste de dictionnaires contenant 'game' (GamesStructure) et 'similarity_score' (float)
            Exemple: [
                {
                    'game': GamesStructure(...),
                    'similarity_score': 95.5
                },
                ...
            ]
        """
        
        if self.model is None:
            raise Exception("Modèle MLflow non disponible")
        
        if self.games_db is None or self.games_db.empty:
            raise Exception("Base de données de jeux non disponible")
        
        # Convertir GamesStructure en dictionnaire pour faciliter l'accès
        game_dict = game.model_dump()
        
        # Extraire UNIQUEMENT les features (tags) du jeu d'entrée (sans id et nom)
        game_features = {}
        for tag in self.VALIDTAG:
            game_features[tag] = game_dict.get(tag, 0)
        
        predictions = []
        
        # Calculer le score de similarité pour chaque jeu de la base
        for idx, db_game in self.games_db.iterrows():
            try:
                # Calculer la différence absolue entre les tags du jeu d'entrée et ceux de la BDD
                # IMPORTANT : Ne créer le DataFrame qu'avec les colonnes de tags
                features = {}
                for tag in self.VALIDTAG:
                    db_value = db_game.get(tag, 0)
                    
                    # Gérer les valeurs manquantes (NaN)
                    if pd.isna(db_value):
                        db_value = 0
                        
                    # Calculer la différence absolue
                    features[tag] = abs(game_features[tag] - db_value)
                
                # Créer un DataFrame UNIQUEMENT avec les colonnes de tags (pas de 'id' ni 'nom')
                df_features = pd.DataFrame([features], columns=self.VALIDTAG)
                
                # Prédire le score de similarité avec le modèle MLflow
                similarity_score = self.model.predict(df_features)[0]
                
                # Construire le dictionnaire de données pour GamesStructure
                game_data = {
                    'id': int(idx),  # Utiliser l'index comme ID
                    'nom': str(db_game.get('nom', db_game.get('name', f'Game {idx}')))
                }
                
                # Ajouter tous les tags avec leurs valeurs
                for tag in self.VALIDTAG:
                    tag_value = db_game.get(tag, 0)
                    
                    # Gérer les valeurs manquantes
                    if pd.isna(tag_value):
                        tag_value = 0
                        
                    game_data[tag] = float(tag_value)
                
                # Créer l'instance GamesStructure
                game_structure = GamesStructure(**game_data)
                
                # Ajouter à la liste des prédictions
                predictions.append({
                    'game': game_structure,
                    'similarity_score': float(similarity_score)
                })
                
            except Exception as e:
                print(f"⚠️ Erreur pour le jeu à l'index {idx}: {e}")
                print(f"   Détails: {str(e)}")
                continue
        
        # Vérifier qu'on a au moins des résultats
        if not predictions:
            raise Exception("Aucune prédiction n'a pu être générée")
        
        # Trier par score de similarité décroissant (meilleurs matchs en premier)
        predictions.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        # Retourner les top N meilleurs matchs
        return predictions[:top_n]

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
        start_time = time.time()
        try:
            usergame = self.steam.users.get_owned_games(self.idSteam)
            external_api_duration.labels(api='steam').observe(time.time() - start_time)
        except Exception as e:
            external_api_errors_total.labels(api='steam', error_type='error').inc()
            raise
    
        usergamelist = usergame.get("games")
        gamedata = []
        
        for game in usergamelist:
            gameid = game.get("appid")
            gamename = game.get("name")
            gameplaytime4ever = game.get("playtime_forever")
            gameplaytime2weeks = game.get("playtime_2weeks") if game.get("playtime_2weeks")!=None else 0

            url = f"https://steamspy.com/api.php?request=appdetails&appid={gameid}"
            start_time = time.time()
            try:
                response = requests.get(url).json()
                external_api_duration.labels(api='steamspy').observe(time.time() - start_time)
            except Exception as e:
                external_api_errors_total.labels(api='steamspy', error_type='error').inc()
                continue

            avgplaytime4ever = response.get("median_forever")
            avgplaytime2weeks = response.get("median_2weeks")
            k = 480

            if response.get("price") != "0" and response.get("price") != None:
                k = 0

            if avgplaytime4ever != 0:
                score = 0.7*np.log(1+gameplaytime4ever)/np.log(1+(avgplaytime4ever + k)) + 0.3*np.log(1+gameplaytime2weeks)/np.log(1+avgplaytime2weeks) if avgplaytime2weeks > 0 else 0.7*np.log(1+gameplaytime4ever)/np.log(1+(avgplaytime4ever + k))
                gamedata.append([gameid, gamename, gameplaytime4ever, gameplaytime2weeks, avgplaytime4ever, avgplaytime2weeks, score])

        games_processed_per_recommendation.observe(len(gamedata))
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
        i=0
        j=0
        while i < 5:
            gameid = gamedata[j][0]
            url = f"https://steamspy.com/api.php?request=appdetails&appid={gameid}"
            response = requests.get(url).json()
            tags = response.get("tags", {})
            if isinstance(tags, dict) and tags!={}:

                filtered_tags = {
                    key: value for key, value in tags.items() 
                    if key in VALIDTAG
                }


                i += 1
                usergametags.append([gamedata[i], filtered_tags])
                
            
            j += 1

        return usergametags
    

    def get_user_profil(self, usergametags) -> list:
        sumLabels = 0
        userscore = {}
        for game in usergametags:
            sumLabels += (sum(list(game[1].values())))
            for label in game[1].items():
                if label[0] in userscore.keys():
                    userscore[label[0]] += round(label[1]/sumLabels,2)
                else:
                    userscore.update({label[0]:round(label[1]/sumLabels,2)})
            

            
        userprofil = []

        
        userprofil.append(self.idSteam)
        userprofil.append(usergametags)
        userprofil.append(userscore)
        return userprofil
    


    def get_game_structure(self) -> GamesStructure:
        profil = GamesStructure
        usergames = self.get_user_game_list()
        topgametags = self.get_favorite_game_tags(usergames)
        userprofil = self.get_user_profil(topgametags)
        player_data = self.steam.users.get_user_details(self.idSteam).get("player", {})
        profil.nom = (player_data.get("personaname"),"none")
        for field_name, value in profil.model_dump().items():
        
            if isinstance(value, float):

                if field_name in userprofil[2]:

                    setattr(profil, field_name, userprofil[2][field_name])
        return profil