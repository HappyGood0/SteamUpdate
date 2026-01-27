from steam_web_api import Steam
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import numpy as np

# Charge les variables du fichier .env situé dans le même dossier
load_dotenv()

# Récupère la clé
KEY = os.getenv("STEAM_API_KEY")

    
    # Utilisation de la variable KEY ici
steam = Steam(KEY)




#------------------------------------------------------------------#


usergame = steam.users.get_owned_games("76561198205309263")

usergamelist = usergame.get("games")

# for game in usergamelist:
#     gameid = game.get("appid")
#     url = f"https://steamspy.com/api.php?request=appdetails&appid={gameid}"
#     response = requests.get(url).json().get("price")
#     print(response == "0")

gamedata = []
useravgprice = 1
nbpaidgame = 1
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
        useravgprice += int(response.get("price"))
        nbpaidgame += 1
        print(useravgprice)
        print(response.get("price"))

    print(gamename)
    print(avgplaytime4ever, avgplaytime2weeks)
    print(gameplaytime4ever, gameplaytime2weeks)
    print("----")
    if avgplaytime4ever != 0:
        score = 0.7*np.log(1+gameplaytime4ever)/np.log(1+(avgplaytime4ever + k)) + 0.3*np.log(1+gameplaytime2weeks)/np.log(1+avgplaytime2weeks) if avgplaytime2weeks > 0 else 0.7*np.log(1+gameplaytime4ever)/np.log(1+(avgplaytime4ever + k))
        gamedata.append([gameid, gamename, gameplaytime4ever, gameplaytime2weeks, avgplaytime4ever, avgplaytime2weeks, score])

useravgprice = useravgprice/nbpaidgame

gamedata.sort(key=lambda x: x[6], reverse=True)
for game in gamedata:
    print(game)

print(useravgprice)





usergametags = []

for i in range(0,5):
    gameid = gamedata[i][0]
    url = f"https://steamspy.com/api.php?request=appdetails&appid={gameid}"
    response = requests.get(url).json()
    tags = response.get("tags")
    usergametags.append([gameid, gamedata[i][1], tags])

for game in usergametags:
    print(game)
