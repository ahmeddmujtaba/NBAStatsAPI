from bs4 import BeautifulSoup
import requests
import time
import unicodedata



def getCoachStats(teamName):
    # Get the team URL
    url = 'https://www.basketball-reference.com/teams/INSERTTEAMNAMEHERE/coaches.html'
    url = url.replace('INSERTTEAMNAMEHERE',teamName)
    page = requests.get(url)

    # Create beautiful soup object
    soup = BeautifulSoup(page.text, 'html.parser')

    # Get the table
    soup = soup.find_all('div',class_='table_outer_container')[0]
    soup = (soup.find_all('table'))[0]


    # Get the headers from the table
    mainTableHeaders = [th.getText() for th in soup.findAll('tr',limit=2)[1].findAll('th')][1:]
    rows = soup.findAll('tr')[1:]

    # Get the actual stats
    coachStats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]

    

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
        stats[row] = coachStats[counter]
        counter += 1

    print(stats)
    return(stats)


