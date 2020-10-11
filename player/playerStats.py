from bs4 import BeautifulSoup
import requests
import time
from main.urlMaker import strip_accents


# Create dictionary to keep reference of div names and headerRow numbers
referenceDict  = {
    'pergame': ('all_per_game',0),
    'totals': ('all_totals',0),
    'per36': ('all_per_minute',0),
    'per100poss':('all_per_poss',0),
    'advanced': ('all_advanced',0),
    'adjustedshooting':('all_adj-shooting',1),
    'shooting':('all_shooting',1),
    'playbyplay':('all_pbp',1),
    'gamehighs': ('all_year-and-career-highs',1),
    'playoffspergame':('all_playoffs_per_game',0),
    'playoffstotals': ('all_playoffs_totals',0),
    'playoffsper36': ('all_playoffs_per_minute',0),
    'playoffsper100poss':('all_playoffs_per_poss',0),
    'playoffsadvanced': ('all_playoffs_advanced',0),
    'playoffsshooting': ('all_playoffs_shooting',1),
    'playoffsplaybyplay':('all_playoffs_pbp',1),
    'playoffsgamehighs':('all_year-and-career-highs-po',1),
}


def getStats(playerID,type):

    url = f'https://www.basketball-reference.com/players/{playerID}.html'
    page = requests.get(url)

    print

    firstdiv = referenceDict[type][0]
    print(firstdiv)

    headerRow = referenceDict[type][1]

    # Create a beautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')

    # Get the commented out parts
    soup = str(soup)
    soup = soup.replace('-->','')
    soup = soup.replace('<--','')
    soup = soup.replace('!--','')

    soup = BeautifulSoup(soup , 'html.parser')
    
    # Get the specific div
    try:
        div = str(soup.find_all('div',id=firstdiv)[0])
    except IndexError:
        return({'N/A':'N/A'})

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
    mainTableHeaders = [strip_accents(th.getText().replace(u'\xa0', u' ')) for th in soup.findAll('tr',limit=3)[headerRow].findAll('th')][1:]
    rows = soup.findAll('tr')[1:]

    # Get the actual stats
    playerStats = [[strip_accents(td.getText().replace(u'\xa0', u' ')) for td in rows[i].findAll('td')] for i in range(len(rows))]

    

    # Get row headers
    rowHeaders = []
    for row in rows:
        try:
            rowHeaders += [strip_accents(row.find('th').text)]
        except AttributeError:
            rowHeaders += []

    # Create Dictionary
    stats = {}

    # Add stats to the dictionary
    counter  = 0
    stats['Legend'] = mainTableHeaders
    for row in rowHeaders:
        stats[row] = playerStats[counter]
        counter += 1



    # Return the dictionaries
    return(stats)



