import requests
import requests
from requests import post
import time




teamNames = ['MIL','TOR','BOS','MIA','IND','PHI','BRK','ORL','WAS','CHO','CHI','NYK','DET','ATL','CLE']
teamNames += ['LAL','LAC','DEN','UTA','OKC','HOU','DAL','MEM','POR','NOP','SAC','SAS','PHO','MIN','GSW']

counter = 0
for team in teamNames:
    counter += 1
    percentage = (counter/30)*100
    print(f'{percentage} completed')
    url = f'http://127.0.0.1:5000/team/contracts?team={team}'
    r = requests.post(url=url)