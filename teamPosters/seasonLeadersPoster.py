import requests
import requests
from requests import post
import time



teamNames = ['MIL','TOR','BOS','MIA','IND','PHI','BRK','ORL','WAS','CHO','CHI','NYK','DET','ATL','CLE']
teamNames += ['LAL','LAC','DEN','UTA','OKC','HOU','DAL','MEM','POR','NOP','SAC','SAS','PHO','MIN','GSW']


counter = 0
for team in teamNames:
    for year in range(1980,2021):
        counter += 1
        year = 2020
        percentage = counter*100/(30*40)
        print(f'{percentage}% DONE..........')
        print(team,year)
        print()
        print()

        url = f'http://127.0.0.1:5000/team/seasonLeaders?team={team}&year={year}'
        r = requests.post(url=url)
        time.sleep(2)



