from bs4 import BeautifulSoup
import requests
import time


# Create dictionary to keep reference of div names and headerRow numbers
teamSeasonStatsreferenceDict  = {
    'Roster': ('all_roster',0),
    'TeamAndOpponentStats':('all_team_and_opponent',0),
    'TeamMisc':('all_team_misc',1),
    'Totals': ('all_totals',0),
    'Per36': ('all_per_minute',0),
    'Per100Poss':('all_per_poss',0),
    'Advanced': ('all_advanced',0),
    'AdjustedShooting':('all_adj-shooting',0),
    'Shooting':('all_shooting',2),
    'PlayByPlay':('all_pbp',1),
    'Salaries': ('all_salaries2',0)
}


def teamSeasonStats(teamName,firstdiv,headerRow):

    url =  f'https://www.basketball-reference.com/teams/{teamName}/2020.html'
    page = requests.get(url)

    # Create a beautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Get the specific div
    div = str(soup.find_all('div',id=firstdiv)[0])

    # Get the commented out parts
    div = div.replace('-->','')
    div = div.replace('<--','')
    div = div.replace('!--','')


    # Get uncommented parts and put it into beautiful soup again
    soup = BeautifulSoup(div,'html.parser')
    
    # Get the table
    soup = soup.find_all('div',class_='table_outer_container')[0]
    soup = (soup.find_all('table'))[0]


    # Get the headers from the table
    mainTableHeaders = [th.getText().replace(u'\xa0', u' ') for th in soup.findAll('tr',limit=3)[headerRow].findAll('th')][1:]
    rows = soup.findAll('tr')[1:]

    # Get the actual stats
    playerStats = [[td.getText().replace(u'\xa0', u' ') for td in rows[i].findAll('td')] for i in range(len(rows))]

    

    # Get row headers
    rowHeaders = []
    for row in rows:
        rowHeaders += [row.find('th').text]

    # Create Dictionary
    stats = {}

    # Add stats to the dictionary
    counter  = 0
    stats['Legend'] = mainTableHeaders
    

    rowsUsed = []
    for row in rowHeaders:
        if row in rowsUsed:
            stats[row + '*'] = playerStats[counter]
            counter += 1
            rowsUsed += [row + '*']
        else:
            stats[row] = playerStats[counter]
            counter += 1
            rowsUsed += [row]
        


    print(stats)

    # Return the dictionaries
    return(stats)
'''
from firebase import firebase
from requests.exceptions import HTTPError


teamNames = ['MIL','TOR','BOS','MIA','IND','PHI','BRK','ORL','WAS','CHO','CHI','NYK','DET','ATL','CLE']
teamNames += ['LAL','LAC','DEN','UTA','OKC','HOU','DAL','MEM','POR','NOP','SAC','SAS','PHO','MIN','GSW']

firebase = firebase.FirebaseApplication("https://bballdb-88bae.firebaseio.com/", None)

counter = 0
for team in teamNames:
    for stat in teamSeasonStatsreferenceDict.keys():
        counter += 1
        percentage = (counter/(30*11))*100
        print(f'{percentage} DONE {team}.{stat}')
        answer = teamSeasonStats(team,teamSeasonStatsreferenceDict[stat][0],teamSeasonStatsreferenceDict[stat][1])
        try:
            result = firebase.put(f'/bballdb-88bae/teams/{team}/seasonStats/', stat, answer)
        except HTTPError:
            print('pass')

        print()
        print()
        time.sleep(2)
'''