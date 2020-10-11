import requests
#from playerID import getPlayerId,playerID
#from player.playerStats import getStats,referenceDict
import requests

from requests import post
import time
import main.playerInfo.playerInfo
#from main.playerInfo import playerInfo
from team.teamSeasonStats import teamSeasonStats, referenceDict
import playerPosters.playerTag


start = False
counter = 0
for player in playerID.keys():
    print(player,playerID[player])
    counter += 1
    print((counter/1510)*100,'%')
    start = True

    if start == True:
        URL = f'http://127.0.0.1:5000/player/Information?name={player}'
        print(URL)
        data = playerInfo(playerID[player])
        #print(data)
        r = requests.post(url=URL,data=data)
        time.sleep(2)
        

