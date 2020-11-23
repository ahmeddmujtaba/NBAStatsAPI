#from ..team.teamSeasonStats import teamSeasonStats, referenceDict
from refscraper.
from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
import time
from firebase import firebase
from requests.exceptions import HTTPError


teamNames = ['MIL','TOR','BOS','MIA','IND','PHI','BRK','ORL','WAS','CHO','CHI','NYK','DET','ATL','CLE']
teamNames += ['LAL','LAC','DEN','UTA','OKC','HOU','DAL','MEM','POR','NOP','SAC','SAS','PHO','MIN','GSW']

firebase = firebase.FirebaseApplication("https://bballdb-88bae.firebaseio.com/", None)

counter = 0
for team in teamNames:
    for stat in referenceDict.keys():
        counter += 1
        percentage = (counter/30*11)*100
        print(f'{percentage} DONE {team}.{stat}')
        answer = teamSeasonStats(team,referenceDict[stat][0],referenceDict[stat][1])
        try:
            result = firebase.put(f'/bballdb-88bae/team/{team}/seasonStats/', stat, answer)
        except HTTPError:
            print("Exception Occured")

        print()
        print()

