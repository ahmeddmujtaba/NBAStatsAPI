from bs4 import BeautifulSoup
import requests
import time
import unicodedata



def playerInfo(playerID):

    url = f'https://www.basketball-reference.com/players/{playerID}.html'
    print(url)
    page = requests.get(url)

    name = ''

    # Create a beautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')

    div = soup.find('div',id='meta')

    try:
        name = div.find('h1',itemprop='name').text.replace('\n','')
    except AttributeError:
        name = playerID
    

    counter = 0
    team = 'N/A'
    fullname =''
    pronunciation = ''
    position = ''
    measurements = ''
    team = ''
    dob = ''
    college = ''
    draft = 'UnDrafted'
    experience = ''

    for p in div.findAll('p'):
        counter += 1
        if counter == 1:
            if p.text.find('Pronunciation:') != -1:
                pronunciation = p.text.replace('\n','')
                fullname = ''
            else:
                fullname = p.text.replace('\n','')
                pronunciation = ''
        
        if counter == 2 and fullname == '':
            fullname = p.text.replace('\n','')

        if p.text.find('Position') != -1:
            position = p.text.replace('\n','')

        if p.text.find('lb') != -1 and p.text.find('kg') != -1:
            measurements = p.text.replace('\n','')

        if p.text.find('Team') != -1:
            team = p.text.replace('\n','')

        if p.text.find('Born') != -1:
            dob = p.text.replace('\n','').replace('  ',' ')

        if p.text.find('College') != -1:
            college = p.text.replace('\n','').replace(' ','').replace(':',': ')

        if p.text.find('Draft') != -1:
            draft = p.text.replace('\n','').replace('  ','').replace(':',': ')

        if p.text.find('Experience') != -1:
            experience = p.text.replace('\n','').replace(' ','').replace(':',': ')


    social = ""
    for a in div.findAll('a'):
        if str(a).find("https://twitter.com/") != -1:
            social = str(a).replace("<a href=","").split(">")[0].replace('"','')

    print(social)

    accolades = []

    try:
        for li in soup.find('ul',id='bling').findAll('li'):
            accolades += [li.text]
    except AttributeError:
        pass

    info = {}

    counter = 0
    career = []
    season = []

    for p in soup.find('div',class_='stats_pullout').findAll('p'):
        counter += 1
        if counter%2 == 0:
            career += [p.text]
        else:
            season += [p.text]
        
    try:
        imgURL = div.find("img")['src']
    except TypeError:
        imgURL = "N/A"
    


        
    info['StatsLegend'] = ['G','PTS','REB','AST','FG%','3FG%','FT%','eFG%','PER','WS']
    info['Season'] = season[1:]
    info['Career'] = career[1:]
    info['Name'] = name
    info['Fullname'] = fullname.split('Twitter')[0].split('▪')[0].replace('  ','')
    info['Pronunciation'] = pronunciation
    info['Position'] = position.replace('Position:','').split('▪')[0].replace('  ',' ')
    info['Measurements'] = measurements.replace(u'\xa0', u' ')
    info['Team'] = team.replace('Team: ','')
    info['DOB'] = dob.replace(u'\xa0', u' ').replace('  ',' ').replace('Born: ','')[:-2]
    info['College'] = college.replace('College:','')
    info['Draft'] = draft.replace('Draft: ','')
    info['Experience'] = experience.replace('Experience:','').replace('years',' years')
    info['Accolades'] = accolades
    info['ImageURL'] = imgURL
    info['Twitter'] = social
    return(info)



playerInfo('d/duranke01')