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


def get_game_tags(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&l=english"
    response = requests.get(url)
    data = response.json()

    if data and data[str(app_id)]['success']:
        game_data = data[str(app_id)]['data']
        
        # Steam sépare 'categories' (ex: Solo) et 'genres' (ex: RPG)
        genres = [genre['description'] for genre in game_data.get('genres', [])]
        categories = [cat['description'] for cat in game_data.get('categories', [])]
        
        return genres + categories
    return []

# Exemple pour Elden Ring (AppID: 1245620)
tags = get_game_tags(1262350)


# def scrape_steam_tags(app_id):
#     url = f"https://store.steampowered.com/app/{app_id}/"
#     # Il faut parfois simuler un navigateur pour éviter les blocages
#     headers = {'User-Agent': 'Mozilla/5.0'}
#     
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')
    
    # Les tags sont généralement dans des balises <a> avec la classe 'app_tag'
#     tags = []
#     tag_elements = soup.find_all('a', class_='app_tag')
    
#     for el in tag_elements:
#         tags.append(el.text.strip())
        
#     return tags

# Test
#print(scrape_steam_tags(1262350))


#tabgame = []
#for game in usergamelist:
#    tabgame.append([game.get("appid"), game.get("name"), float(game.get("playtime_forever")), float(game.get("playtime_2weeks", 0))])

#tabgame.sort(key=lambda x: x[2], reverse=True)

#print(usergame)

#for game in tabgame:
    #print(game[0],"--", game[1], ":" , game[2]//60, "h", game[2]%60, "min")

#usergamelistdata = []

#for game in tabgame:
#    gameid = game[0]
#    url = f"https://steamspy.com/api.php?request=appdetails&appid={gameid}"
#    response = requests.get(url).json()
#    usergamelistdata.append([response.get("appid"), response.get("name"), float(response.get("average_forever")), float(response.get("average_2weeks"))])



#for game in usergamelistdata:
#    print(game)

#print("----- SCORES -----")



#





#usergamescores = []
#for i in range(len(tabgame)):
#    game = usergamelistdata[i]
#    score = 0.7*tabgame[i][2]/game[i][2] + 0.3*tabgame[i][3]/game[i][3] if game[i][3] > 0 else 0.7*tabgame[i][2]/game[i][2]#
#    usergamescores.append([game[0], game[1], score])#

#for game in sorted(usergamescores, key=lambda x: x[2], reverse=True):
#    print(game)


#------------------------------------------------------------------#


usergame = steam.users.get_owned_games("76561198205309263")

usergamelist = usergame.get("games")

# for game in usergamelist:
#     gameid = game.get("appid")
#     url = f"https://steamspy.com/api.php?request=appdetails&appid={gameid}"
#     response = requests.get(url).json().get("price")
#     print(response == "0")

gamedata = []

for game in usergamelist:
    
    gameid = game.get("appid")
    gamename = game.get("name")
    gameplaytime4ever = game.get("playtime_forever")
    gameplaytime2weeks = game.get("playtime_2weeks") if game.get("playtime_2weeks")!=None else 0
    url = f"https://steamspy.com/api.php?request=appdetails&appid={gameid}"
    avgplaytime4ever = requests.get(url).json().get("median_forever")
    avgplaytime2weeks = requests.get(url).json().get("median_2weeks")
    k = 0
    if requests.get(url).json().get("price") == "0":
        k = 480
    print(gamename)
    print(avgplaytime4ever, avgplaytime2weeks)
    print(gameplaytime4ever, gameplaytime2weeks)
    print("----")
    if avgplaytime4ever != 0:
        score = 0.7*np.log(1+gameplaytime4ever)/np.log(1+(avgplaytime4ever + k)) + 0.3*np.log(1+gameplaytime2weeks)/np.log(1+avgplaytime2weeks) if avgplaytime2weeks > 0 else 0.7*np.log(1+gameplaytime4ever)/np.log(1+(avgplaytime4ever + k))
        gamedata.append([gameid, gamename, gameplaytime4ever, gameplaytime2weeks, avgplaytime4ever, avgplaytime2weeks, score])
    

gamedata.sort(key=lambda x: x[6], reverse=True)
for game in gamedata:
    print(game)
