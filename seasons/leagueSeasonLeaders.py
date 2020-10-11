from bs4 import BeautifulSoup
import requests
import time
import unicodedata




def getSeasonLeadersStats(year):

    # Get the team URL
    url = f'https://www.basketball-reference.com/leagues/NBA_{year}_leaders.html'
    page = requests.get(url)

    # Create beautiful soup object
    soup = BeautifulSoup(page.text, 'html.parser')
    soup = soup.find('div',class_='leaderboard_wrapper')


    soup = str(soup)


    # Get the commented out parts
    soup = soup.replace('-->','')
    soup = soup.replace('<--','')
    soup = soup.replace('!--','')

    soup = BeautifulSoup(soup , 'html.parser')


    


    # Get the individual sections
    divs = soup.findAll('div',class_='data_grid_box')




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
            try:
                name = tr.find('td',class_='who').text
                value = tr.find('td',class_='value').text
            except AttributeError:
                name = ''
            

            
            statsToAdd += [(name,value)]

        
        stats[title] = statsToAdd

            
            
    print(stats['Minutes Played'])

    return(stats)

