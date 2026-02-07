from steam_web_api import Steam
import os
from dotenv import load_dotenv
import requests
import numpy as np
import csv

# Charge les variables du fichier .env situé dans le même dossier
load_dotenv()

# Récupère la clé
KEY = os.getenv("STEAM_API_KEY")

    
    # Utilisation de la variable KEY ici
steam = Steam(KEY)
 #



VALIDTAG = ["Atmospheric", "Fantasy", "Relaxing", "Funny", "Horror", "Sci-fi", "Futuristic", "Retro", "Dark", "Mystery", "Survival", "Psychological Horror",
"Medieval", "Management", "Sports", "Building", "Tactical", "Drama", "Space", "Romance", "Racing", "Dark Fantasy", "Logic", "Emotional", "Nature",
"Post-apocalyptic", "War", "Historical", "Zombies", "Stealth", "Investigation", "Dark Humor", "Parkour", "Flight", "Pirates", "Steampunk",
"Indie", "Action", "Casual", "Adventure", "Simulation", "RPG", "Strategy", "Action-Adventure",
"3D", "2D", "First-Person", "Third-Person", "Top-Down", "Realistic", "Cartoony", "Hand-drawn", "Text-Based", "Isometric",
"PvP", "PvE", "Open World", "Story Rich", "Combat", "Controller", "Choices Matter", "Linear", "Turn-Based Combat", "Turn-Based Tactics", "Hack and Slash",
"Deckbuilding", "Team-Based",
"Puzzle", "Platformer", "Shooter", "Arcade", "Visual Novel", "Roguelike", "Sandbox", "Point & Click", "RTS", "Tower Defense", "Rhythm",
"Singleplayer", "Multiplayer", "Online Co-op", "Local Co-op"]

#------------------------------------------------------------------#

colonneUser = ['ID', 'Atmospheric', 'Fantasy', 'Relaxing', 'Funny', 'Horror', 'Sci-fi', 'Futuristic', 'Retro', 'Dark', 'Mystery', 'Survival', 'Psychological Horror', 'Medieval', 'Management', 'Sports', 'Building', 'Tactical', 'Drama', 'Space', 'Romance', 'Racing', 'Dark Fantasy', 'Logic', 'Emotional', 'Nature', 'Post-apocalyptic', 'War', 'Historical', 'Zombies', 'Stealth', 'Investigation', 'Dark Humor', 'Parkour', 'Flight', 'Pirates', 'Steampunk', 'Indie', 'Action', 'Casual', 'Adventure', 'Simulation', 'RPG', 'Strategy', 'Action-Adventure', '3D', '2D', 'First-Person', 'Third-Person', 'Top-Down', 'Realistic', 'Cartoony', 'Hand-drawn', 'Text-Based', 'Isometric', 'PvP', 'PvE', 'Open World', 'Story Rich', 'Combat', 'Controller', 'Choices Matter', 'Linear', 'Turn-Based Combat', 'Turn-Based Tactics', 'Hack and Slash', 'Deckbuilding', 'Team-Based', 'Puzzle', 'Platformer', 'Shooter', 'Arcade', 'Visual Novel', 'Roguelike', 'Sandbox', 'Point & Click', 'RTS', 'Tower Defense', 'Rhythm', 'Singleplayer', 'Multiplayer', 'Online Co-op', 'Local Co-op']
colonneGame = ['Utilisateur','Nom','Score', 'Atmospheric', 'Fantasy', 'Relaxing', 'Funny', 'Horror', 'Sci-fi', 'Futuristic', 'Retro', 'Dark', 'Mystery', 'Survival', 'Psychological Horror', 'Medieval', 'Management', 'Sports', 'Building', 'Tactical', 'Drama', 'Space', 'Romance', 'Racing', 'Dark Fantasy', 'Logic', 'Emotional', 'Nature', 'Post-apocalyptic', 'War', 'Historical', 'Zombies', 'Stealth', 'Investigation', 'Dark Humor', 'Parkour', 'Flight', 'Pirates', 'Steampunk', 'Indie', 'Action', 'Casual', 'Adventure', 'Simulation', 'RPG', 'Strategy', 'Action-Adventure', '3D', '2D', 'First-Person', 'Third-Person', 'Top-Down', 'Realistic', 'Cartoony', 'Hand-drawn', 'Text-Based', 'Isometric', 'PvP', 'PvE', 'Open World', 'Story Rich', 'Combat', 'Controller', 'Choices Matter', 'Linear', 'Turn-Based Combat', 'Turn-Based Tactics', 'Hack and Slash', 'Deckbuilding', 'Team-Based', 'Puzzle', 'Platformer', 'Shooter', 'Arcade', 'Visual Novel', 'Roguelike', 'Sandbox', 'Point & Click', 'RTS', 'Tower Defense', 'Rhythm', 'Singleplayer', 'Multiplayer', 'Online Co-op', 'Local Co-op']

with open('userid.csv', 'r', encoding='utf-8') as f:
     #open('topGamesUser.csv', 'a', encoding='utf-8') as gamefile, \
     #open('usersProfil.csv', 'a', encoding='utf-8') as userfile:
        
    #writerUser = csv.DictWriter(userfile, fieldnames=colonneUser)
    #writerGame = csv.DictWriter(gamefile, fieldnames=colonneGame)

    idlist = csv.reader(f)
    for id in idlist:
            
        iduser = id

        usergame = steam.users.get_owned_games(iduser)
        user = steam.users.get_user_details("76561198167767436").get("player").get("personaname")
        print(user)
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
            medplaytime4ever = response.get("median_forever")
            medplaytime2weeks = response.get("median_2weeks")
            k = 660
            if response.get("price") != "0" and response.get("price") != None:
                k = 0
                useravgprice += int(response.get("price"))
                nbpaidgame += 1
                print(useravgprice)
                print(response.get("price"))

            print(gamename)
            print(medplaytime4ever, medplaytime2weeks)
            print(gameplaytime4ever, gameplaytime2weeks)
            print("----")
            if medplaytime4ever != 0:
                score = np.log(1+gameplaytime4ever)/np.log(1+(medplaytime4ever + k)) + 0.3*np.log(1+gameplaytime2weeks)/np.log(1+medplaytime2weeks) if medplaytime2weeks > 0 else np.log(1+gameplaytime4ever)/np.log(1+(medplaytime4ever + k))
                gamedata.append([gameid, gamename, gameplaytime4ever, gameplaytime2weeks, medplaytime4ever, medplaytime2weeks, score])

        useravgprice = useravgprice/nbpaidgame

        gamedata.sort(key=lambda x: x[6], reverse=True)
        for game in gamedata:
            print(game)






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
                print(filtered_tags)
                print("__________________") 
                i += 1
                usergametags.append([gamedata[i], filtered_tags])
                
            
            j += 1

        print(usergametags)
        print("----------------------")
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

        
        userprofil.append(iduser)
        userprofil.append(usergametags)
        userprofil.append(userscore)

        print(userprofil)
        user_profil = {
            'ID': iduser,
        }

        for game in userprofil[1]:
            game_profil = {
                'Utilisateur': id,
                'Nom': game[0][1],
                'Score': float(game[0][6])
            }
            for label in VALIDTAG:
                if label in game[1].keys():
                    game_profil.update({label:round(game[1].get(label)/sum(list(game[1].values())),2)})
                else:
                    game_profil.update({label:0})
            #writerGame.writerow(game_profil)
            
        for label in VALIDTAG:
            if label in userprofil[2].keys():
                user_profil.update({label:userprofil[2].get(label)})
            else:
                user_profil.update({label:0})

        #writerUser.writerow(user_profil)
        
        



            

            





