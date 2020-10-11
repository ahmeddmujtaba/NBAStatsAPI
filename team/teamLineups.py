from bs4 import BeautifulSoup
import requests
import time
import unicodedata

teamLineupsReferenceDict = {
    '5': 'all_lineups_5-man_',
    '4': 'all_lineups_4-man_',
    '3': 'all_lineups_3-man_',
    '2': 'all_lineups_2-man_',
}

def getTeamLineups(teamName,divid,year):
    # Construc the proper URL
    url = f'https://www.basketball-reference.com/teams/{teamName}/{year}/lineups/'



    # Make request using URL
    page = requests.get(url)

    # Create a beautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')
    soup = str(soup.find('div',id='content'))

    # Get the commented out parts
    soup = soup.replace('-->','')
    soup = soup.replace('<--','')
    soup = soup.replace('!--','')
    

    soup = BeautifulSoup(soup, 'html.parser')
    

    

    # Get the specific div
    div = str(soup.find_all('div',id=divid)[0])


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
        if row == '':
            row = 'Team Average'
            stats[row] = playerStats[counter][1:]
        else:
            stats[row] = playerStats[counter]
        counter += 1

    
    print(stats)

    for key in stats.keys():
        print(key)
        print(stats[key])

    # Return the dictionaries
    return(stats)
