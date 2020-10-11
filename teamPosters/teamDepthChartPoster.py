import requests
from player.playerStats import getStats
from playerID import getPlayerId,playerID
import requests
from requests import post
import time
from team.depthChart import depthChart


teamNames = ['MIL','TOR','BOS','MIA','IND','PHI','BRK','ORL','WAS','CHO','CHI','NYK','DET','ATL','CLE']
teamNames += ['LAL','LAC','DEN','UTA','OKC','HOU','DAL','MEM','POR','NOP','SAC','SAS','PHO','MIN','GSW']


counter = 0
for team in teamNames:
    counter += 1
    year = 2020
    percentage = counter*100/(30*40)
    print(f'{percentage}% DONE..........')
    print(team,year)
    print()
    print()

    url = f'http://127.0.0.1:5000/team/depthChart?team={team}&year=2020'
    r = requests.post(url=url)
    time.sleep(2)

for year in range(1980,2012):
    url = f'http://127.0.0.1:5000/team/depthChart?team=NJN&year={year}'
    r = requests.post(url=url)
