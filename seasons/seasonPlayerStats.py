from bs4 import BeautifulSoup
import requests
import time


# Create dictionary to keep reference of div names and headerRow numbers
seasonPlayerStatsReferenceDict  = {
    'PerGame': ('https://www.basketball-reference.com/leagues/NBA_YEAR_per_game.html','all_per_game_stats',0),
    'Totals': ('https://www.basketball-reference.com/leagues/NBA_YEAR_totals.html','all_totals_stats',0),
    'Per36': ('https://www.basketball-reference.com/leagues/NBA_YEAR_per_minute.html','all_per_minute_stats',0),
    'Per100Poss':('https://www.basketball-reference.com/leagues/NBA_YEAR_per_poss.html','all_per_poss_stats',0),
    'Advanced': ('https://www.basketball-reference.com/leagues/NBA_YEAR_advanced.html','all_advanced_stats',0),
    'AdjustedShooting':('https://www.basketball-reference.com/leagues/NBA_YEAR_adj_shooting.html','all_adj-shooting',1),
    'Shooting':('https://www.basketball-reference.com/leagues/NBA_YEAR_shooting.html','all_shooting_stats',1),
    'PlayByPlay':('https://www.basketball-reference.com/leagues/NBA_YEAR_play-by-play.html','all_pbp_stats',1),
}


def getSeasonPlayerStats(year,statType):
    url = seasonPlayerStatsReferenceDict[statType][0].replace('YEAR',str(year))
    firstdiv = seasonPlayerStatsReferenceDict[statType][1]
    headerRow = seasonPlayerStatsReferenceDict[statType][2]
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
    mainTableHeaders = [th.getText().replace(u'\xa0', u' ') for th in soup.findAll('tr',limit=2)[headerRow].findAll('th')][1:]
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

