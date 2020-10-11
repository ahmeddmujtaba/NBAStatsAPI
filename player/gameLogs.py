from bs4 import BeautifulSoup
import requests
import time
import unicodedata

def gameLogs(playerID,year):
    # Add year to the end of the URL
    url = f'https://www.basketball-reference.com/players/{playerID}/gamelog/{year}'
    page = requests.get(url)

    # Create a beautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Get the specific div
    try:
        div = str(soup.find_all('div',id='all_pgl_basic')[0])
    except IndexError:
        return({'N/A':'N/A'})


    # Get uncommented parts and put it into beautiful soup again
    soup = BeautifulSoup(div,'html.parser')
    
    # Get the table
    soup = soup.find_all('div',class_='table_outer_container')[0]
    soup = (soup.find_all('table'))[0]


    # Get the headers from the table
    mainTableHeaders = [th.getText().replace(u'\xa0', u' ') for th in soup.findAll('tr',limit=2)[0].findAll('th')][1:]
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
    for row in rowHeaders:
        stats[row] = playerStats[counter]
        counter += 1


    print(stats['43'])

    # Return the dictionaries
    return(stats)

