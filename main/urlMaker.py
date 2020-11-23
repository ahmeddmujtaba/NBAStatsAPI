from bs4 import BeautifulSoup
import requests
import time
import unicodedata
import sys
import json
import urllib3

def strip_accents(text):

    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass

    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)



def urlMaker():
    url = 'https://www.basketball-reference.com/players/a/'

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    #f = open('playerID.txt','w+')
    for letter in letters:
        url = 'https://www.basketball-reference.com/players/' + letter + '/'

        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        div = soup.find('div',id='all_players')
        tbody = div.find('tbody')
        

        for tr in tbody.findAll('tr'):
            currentPlayer = False
            th = tr.find('th')
            position = tr.findAll('td')[2].text
            height = tr.findAll('td')[3].text
            weight = tr.findAll('td')[4].text
            
            firstYear = int(tr.findAll('td')[1].text)
            lastYear = int(tr.findAll('td')[0].text)
            yearsInNba = lastYear - firstYear
            firstYear = int(tr.findAll('td')[1].text)
            if th.find('strong'):
                currentPlayer = True

            if currentPlayer == True:
                playerName = strip_accents(th.text).lower().replace(' ','')
                playerId = th.a['href'].split('/')[3].replace('.html','')
                name = th.text
                


                apiURL = "http://127.0.0.1:5000/player/information?name=" + strip_accents(name.lower().strip().replace(" ","").replace("*",""))
                try:
                    team = requests.get(apiURL).json()['Team']
                except ValueError:
                    team = 'N/A'
                    print("ERROR")

                if team == "" :
                    if lastYear < 2020:
                        team = "Retired"
                    else:
                        team = "Free Agent"

                else:
                    team = team


                '''f = open('playerNames1.txt','a')
                f.write(f' "{name} {weight} {height} {position}", ')
                f.close()


                f = open('playerNames2.txt','a')
                f.write(f' "{name}", ')
                f.close()

                f = open('playerNames3.txt','a')
                f.write(f' "{name} {position}", ')
                f.close() '''

                f = open('namesAsDict.txt','a')
                f.write(f' "{name}": "{weight}, {height}, {position}, {team}, {firstYear}, {lastYear} " , ')
                f.close()

                


                st1 = '"' + playerName + '" :'
                st2 = f'"{letter}/' + playerId + '",' 
                #f.write(st1 + st2)
                #print(st1 + st2)
            

        
        time.sleep(5)

        
    #f.close()


    return

