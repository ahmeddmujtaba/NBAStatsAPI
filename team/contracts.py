from bs4 import BeautifulSoup
import requests
import time
import unicodedata

def getContractStats(teamName):
    url = f'https://www.basketball-reference.com/contracts/{teamName}.html'
    page = requests.get(url)
    firstdiv = 'div_contracts'
    headerRow = 1

    # Create a beautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Get the specific div
    div = str(soup.find_all('div',id=firstdiv)[0])

    # Get uncommented parts and put it into beautiful soup again
    soup = BeautifulSoup(div,'html.parser')
    
    # Get the table
    #soup = soup.find_all('div',class_='table_outer_container')[0]
    soup = (soup.find_all('table'))[0]


    # Get the headers from the table
    mainTableHeaders = [th.getText().replace(u'\xa0', u' ') for th in soup.findAll('tr',limit=2)[headerRow].findAll('th')][1:]
    rows = soup.findAll('tr')[1:]

    # Get the actual stats
    playerStats = [[td for td in rows[i].findAll('td')] for i in range(len(rows))]
    
    #.

    for i in range(len(playerStats)):
        for j in range(len(playerStats[i])):
            try:
                if 'salary-pl' in playerStats[i][j]['class']:
                    playerStats[i][j] = playerStats[i][j].getText().replace(u'\xa0', u' ') + '(PO)'
                elif 'salary-tm' in playerStats[i][j]['class']:
                    playerStats[i][j] = playerStats[i][j].getText().replace(u'\xa0', u' ') + '(TO)'
                elif 'salary-fa' in playerStats[i][j]['class']:
                    playerStats[i][j] = playerStats[i][j].getText().replace(u'\xa0', u' ') + '(FA)'
                elif 'salary-et' in playerStats[i][j]['class']:
                    playerStats[i][j] = playerStats[i][j].getText().replace(u'\xa0', u' ') + '(ET)'
                else:
                    playerStats[i][j] = playerStats[i][j].getText().replace(u'\xa0', u' ')
            except  KeyError:
                playerStats[i][j] = playerStats[i][j].getText()
            

    # Get row headers
    rowHeaders = []
    for row in rows:

        if row.find('th'):
            rowHeaders += [row.find('th').text]
        else:
            rowHeaders += []

    # Create Dictionary
    stats = {}

    # Add stats to the dictionary
    counter  = 0
    stats['Legend'] = mainTableHeaders
    for row in rowHeaders:
        if row == 'Team Totals':
            stats[row] = (playerStats[len(rowHeaders)])
        else:
            if playerStats[counter] == ['']:
                counter += 1
            stats[row] = playerStats[counter]
        counter += 1



    # Return the dictionaries
    print(stats)
    return(stats)


