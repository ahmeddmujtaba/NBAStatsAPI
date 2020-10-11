import requests
from player.playerStats import getStats
from playerID import getPlayerId,playerID
#from player.playerStats import getStats,referenceDict
import requests
from requests import post
import time

from team.teamSeasonStats import teamSeasonStats, referenceDict


start = False
counter = 0
for player in playerID.keys():
    print(player,playerID[player])
    counter += 1
    if player == 'guerschonyabusele':
        start = True
    print((counter/1510)*100,'%')

    if start == True:
        for statType in referenceDict.keys():
            URL = f'http://0.0.0.0:5000/player/POST?name={player}&type={statType}'
            print(URL)
            data = getStats(getPlayerId(player),statType)
            #print(data)
            r = requests.post(url=URL,data=data)
            time.sleep(2)
        

