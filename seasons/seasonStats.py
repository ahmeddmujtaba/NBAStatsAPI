from bs4 import BeautifulSoup
import requests
import time


# Create dictionary to keep reference of div names and headerRow numbers
seasonStatsReferenceDict  = {
    'EasternConference': ('all_confs_standings_E',0),
    'WesternConference': ('all_confs_standings_W',0),
    'PerGame': ('all_team-stats-per_game',0),
    'OpponentPerGame': ('all_opponent-stats-per_game',0),
    'TeamPer100Poss':('all_team-stats-per_poss',0),
    'OpponentPer100Poss':('all_opponent-stats-per_poss',0),
    'TeamStats':('all_team-stats-base',0),
    'OpponentStats':('all_opponent-stats-base',0),
    'TeamPerPoss':('all_team-stats-per_poss',0),
    'OpponentPerPoss':('all_opponent-stats-per_poss',0),
    'Misc':('all_misc_stats',1),
    'TeamShooting':('all_team_shooting',2),
    'OpponentShooting':('all_opponent_shooting',2),
}


def getSeasonStats(year,table):
    # Constuct proper URL and make a request
    url = f'https://www.basketball-reference.com/leagues/NBA_{year}.html'
    page = requests.get(url)


    # Get the first div name and the headerRow position
    firstdiv = seasonStatsReferenceDict[table][0]
    headerRow = seasonStatsReferenceDict[table][1]
    # Create a beautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')

    # Get the commented out parts
    soup = str(soup)
    soup = soup.replace('-->','')
    soup = soup.replace('<--','')
    soup = soup.replace('!--','')

    soup = BeautifulSoup(soup , 'html.parser')
    
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
        rowHeaders += [row.find('th').text.replace(u'\xa0', u' ')]

    # Create Dictionary
    stats = {}

    # Add stats to the dictionary
    counter  = 0
    stats['Legend'] = mainTableHeaders
    for row in rowHeaders:
        stats[row] = playerStats[counter]
        counter += 1


    print(stats)

    # Return the dictionaries
    return(stats)


