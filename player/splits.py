from bs4 import BeautifulSoup
import requests
import time
import unicodedata

def splits(playerID,year):
    # Add year to the end of the URL
    url = f'https://www.basketball-reference.com/players/{playerID}/splits/{year}'
    page = requests.get(url)

    # Create a beautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Get the specific div
    div = str(soup.find_all('div',id='all_splits')[0])


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
    mainTableHeaders = [th.getText().replace(u'\xa0', u' ') for th in soup.findAll('tr',limit=2)[1].findAll('th')][1:]
    rows = soup.findAll('tr')[:]

    # Get the actual stats
    playerStats = [[td.getText().replace(u'\xa0', u' ') for td in rows[i].findAll('td')[1:]] for i in range(len(rows))]

    

    # Get row headers
    rowHeaders = []
    for row in rows:
        
        try:

            rowHeaders += [row.find('td',class_='left').text]
        except AttributeError:
            pass


    # Create Dictionary
    stats = {}

    # Add stats to the dictionary
    counter  = 1
    stats['Legend'] = mainTableHeaders
    for row in rowHeaders:
        if playerStats[counter] != []:
            stats[row] = playerStats[counter]
        else:
            counter += 1
            stats[row] = playerStats[counter]
        counter += 1


    print(stats['Legend'])

    # Return the dictionaries
    return(stats)


