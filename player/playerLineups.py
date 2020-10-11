from bs4 import BeautifulSoup
import requests
import time
import unicodedata
from main.urlMaker import strip_accents

referenceDict = {
    '5': 'all_lineups-5-man',
    '4': 'all_lineups-4-man',
    '3': 'all_lineups-3-man',
    '2': 'all_lineups-2-man',
}

def playerLineups(playerID,year,man):
    # Add year to the end of the URL
    url = f'https://www.basketball-reference.com/players/{playerID}/lineups/{year}'
    page = requests.get(url)
    

    try:
        divid = referenceDict[man]
    except KeyError:
        return({'N/A':'N/A'})



    # Create a beautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')
    

    # Get the specific div
    try:
        div = str(soup.find_all('div',id=divid)[0])
    except KeyError:
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
    mainTableHeaders = [strip_accents(th.getText().replace(u'\xa0', u' ')) for th in soup.findAll('tr',limit=2)[1].findAll('th')][1:]
    rows = soup.findAll('tr')[1:]

    # Get the actual stats
    playerStats = [[strip_accents(td.getText().replace(u'\xa0', u' ')) for td in rows[i].findAll('td')] for i in range(len(rows))]

    

    # Get row headers
    rowHeaders = []
    for row in rows:
        rowHeaders += [strip_accents(row.find('th').text)]

    # Create Dictionary
    stats = {}

    # Add stats to the dictionary
    counter  = 0
    stats['Legend'] = mainTableHeaders
    for row in rowHeaders:
        if row == '':
            row = 'Player Average'
            stats[row] = playerStats[counter][1:]
        else:
            stats[row] = playerStats[counter]
        counter += 1

    
    print(stats)

    # Return the dictionaries
    return(stats)


