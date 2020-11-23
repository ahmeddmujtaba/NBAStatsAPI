import requests
from bs4 import BeautifulSoup

def playerImage(playerID):
    url = f'https://www.basketball-reference.com/players/{playerID}.html'
    
    page = requests.get(url)

    # Create beautiful soup object
    soup = BeautifulSoup(page.text, 'html.parser')
    try:
        div = soup.find('div',id='info')
    except AttributeError:
        div = None
    

    try:
        image = div.find('img')['src']
    except (AttributeError,TypeError) as e:
        image = 'N/A'

    '''
    print((counter/1510)*100,'%',f'   {player}')

    stats[player] = image

    player = str(player).replace('*','')
    try:
        result = firebase.put(f'/bballdb-88bae/player/{player}/imageURL/', 'src', image)
    except HTTPError:
        print("Exception Occured")
    print()
    print()'''

    return ({'URL': image})

