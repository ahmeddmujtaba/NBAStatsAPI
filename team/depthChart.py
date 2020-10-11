from bs4 import BeautifulSoup
import requests
import time
import unicodedata


# Make a referenceDict
teamLeadersDict = {
    'SeasonLeaders': 'https://www.basketball-reference.com/teams/INSERTTEAMNAMEHERE/leaders_season.html',
    'CareerLeaders': 'https://www.basketball-reference.com/teams/INSERTTEAMNAMEHERE/leaders_career.html'
}

def depthChart(teamName, year):

    # Get the team URL
    url = f'https://www.basketball-reference.com/teams/{teamName}/{year}_depth.html'
    
    page = requests.get(url)

    # Create beautiful soup object
    soup = BeautifulSoup(page.text, 'html.parser')

    # Get the individual sections
    divs = soup.find_all('div', class_='data_grid_box')

    # Create dictionary to return
    stats = {}


    
    player =  []
    names = []
    values = []

    # Go through all the divs
    for div in divs:

        # Get the title 
        title = div.find('table').find('caption').text
        statsToAdd = []

        for i in range(len(div.find_all('a'))):
            statsToAdd += [div.find_all('a')[i].text,div.find_all('span')[i].text]

        stats[title] = statsToAdd

        

    return(stats)
