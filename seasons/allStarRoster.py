from bs4 import BeautifulSoup
import requests
import time
import unicodedata

allStarReferenceDict = {
    'All-NBA': 'div_all-nba',
    'All-Defensive': 'div_all-defensive',
    'All-Rookie': 'all_all-rookie',
    'All-Star': 'div_all_star_game_rosters'
}

def getAllStarRosters(year,type):
    page = requests.get(f'https://www.basketball-reference.com/leagues/NBA_{year}.html')

    divid =  allStarReferenceDict[type]

    # Create a beautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')

    # Get the commented out parts
    soup = str(soup)
    soup = soup.replace('-->','')
    soup = soup.replace('<--','')
    soup = soup.replace('!--','')

    soup = BeautifulSoup(soup , 'html.parser')

    div = soup.find('div',id=divid)

    rosters = div.findAll('div',class_='data_grid_box')

    stats = {}

    for roster in rosters:
        captain = roster.find('caption').text
        print(captain)

        statsToAdd = []

        for a in roster.findAll('a'):
            statsToAdd += [(a.text)]

        stats[captain] = statsToAdd

    print(stats)

    return(stats)




