from bs4 import BeautifulSoup
import requests
import time
import unicodedata
 

# Make a referenceDict
teamLeadersDict = {
    'SeasonLeaders': 'https://www.basketball-reference.com/teams/INSERTTEAMNAMEHERE/leaders_season.html',
    'CareerLeaders': 'https://www.basketball-reference.com/teams/INSERTTEAMNAMEHERE/leaders_career.html'
}

def getFranchiseLeadersStats(url,teamName):

    # Get the team URL
    url = url.replace('INSERTTEAMNAMEHERE',teamName)
    page = requests.get(url)

    # Create beautiful soup object
    soup = BeautifulSoup(page.text, 'html.parser')

    # Get the individual sections
    divs = soup.find_all('div',class_='data_grid_box')

    # Create dictionary to return
    stats = {}

    # Go through all the divs
    for div in divs:

        # Get the title 
        title = div.find('table').find('caption').text
        
        
        # Change the div so that all the stats become visible
        div['class'] = 'data_grid_box show_all'

        statsToAdd = []

        # Go through all the table rows
        for tr in div.find_all('tr'):
            name = tr.find('td',class_='who').text
            value = tr.find('td',class_='value').text

            
            statsToAdd += [(name,value.strip())]

        
        stats[title] = statsToAdd

            
            

    return(stats)
