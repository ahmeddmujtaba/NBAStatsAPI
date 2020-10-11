import requests
from player.playerStats import getStats
from playerID import getPlayerId,playerID
#from player.playerStats import getStats,referenceDict
import requests
from requests import post
import time
from team.franchiseStats import franchiseStats,teamStatsReferenceDict

teamNames = ['MIL','TOR','BOS','MIA','IND','PHI','BRK','ORL','WAS','CHO','CHI','NYK','DET','ATL','CLE']
teamNames += ['LAL','LAC','DEN','UTA','OKC','HOU','DAL','MEM','POR','NOP','SAC','SAS','PHO','MIN','GSW']


print(len(teamNames))

counter = 0
for team in teamNames:
    for statType in teamStatsReferenceDict.keys():
        for stat in teamStatsReferenceDict[statType].keys():
            counter += 1
            percentage = counter*100/(30*3*4)
            print(f'{percentage}% DONE..........')
            print(team,statType,stat)
            print()
            print()
            url = f'http://127.0.0.1:5000/team/franchiseStats?team={team}&statType={statType}&stat={stat}'
            r = requests.post(url=url)
            time.sleep(5)
            

print('done')


