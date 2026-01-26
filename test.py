from steam_web_api import Steam
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

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

usergame = steam.users.get_owned_games("76561198205309263")

usergamelist = usergame.get("games")

tabgame = []
for game in usergamelist:
    tabgame.append([game.get("appid"), game.get("name"), int(game.get("playtime_forever"))])

tabgame.sort(key=lambda x: x[2], reverse=True)

#print(usergame)

#for game in tabgame:
    #print(game[0],"--", game[1], ":" , game[2]//60, "h", game[2]%60, "min")

url = f"https://steamspy.com/api.php?request=appdetails&appid={tabgame[0][0]}"

response = requests.get(url)

#print(response.json().get("tags"))

