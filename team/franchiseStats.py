from bs4 import BeautifulSoup
import requests
import time
import unicodedata

# Make dictionary for all the team html pages
teamStatsReferenceDict = {
    'Basic': {
        'TeamStats':'https://www.basketball-reference.com/teams/INSERTTEAMNAMEHERE/stats_basic_totals.html',
        'TeamStatsPerGame':'https://www.basketball-reference.com/teams/INSERTTEAMNAMEHERE/stats_per_game_totals.html',
        'OpponentStats':'https://www.basketball-reference.com/teams/INSERTTEAMNAMEHERE/opp_stats_basic_totals.html',
        'OpponentStatsPerGame':'https://www.basketball-reference.com/teams/INSERTTEAMNAMEHERE/opp_stats_per_game_totals.html'
    },
    
    'LeagueRanks': {
        'TeamStats':'https://www.basketball-reference.com/teams/INSERTTEAMNAMEHERE/stats_basic_ranks.html',
        'TeamStatsPerGame':'https://www.basketball-reference.com/teams/INSERTTEAMNAMEHERE/stats_per_game_ranks.html',
        'OpponentStats':'https://www.basketball-reference.com/teams/INSERTTEAMNAMEHERE/opp_stats_basic_ranks.html',
        'OpponentStatsPerGame':'https://www.basketball-reference.com/teams/INSERTTEAMNAMEHERE/opp_stats_per_game_ranks.html'
    }, 
    'YearOverYear': {
        'TeamStats':'https://www.basketball-reference.com/teams/INSERTTEAMNAMEHERE/stats_basic_yr_yr.html',
        'TeamStatsPerGame':'https://www.basketball-reference.com/teams/INSERTTEAMNAMEHERE/stats_per_game_yr_yr.html',
        'OpponentStats':'https://www.basketball-reference.com/teams/INSERTTEAMNAMEHERE/opp_stats_basic_yr_yr.html',
        'OpponentStatsPerGame':'https://www.basketball-reference.com/teams/INSERTTEAMNAMEHERE/opp_stats_per_game_yr_yr.html'
    }

}


def franchiseStats(url, teamName):

    # Get the team URL
    url = url.replace('INSERTTEAMNAMEHERE',teamName)
    page = requests.get(url)

    # Create beautiful soup object
    soup = BeautifulSoup(page.text, 'html.parser')

    # Get the table
    soup = soup.find_all('div',class_='table_outer_container')[0]
    soup = (soup.find_all('table'))[0]


    # Get the headers from the table
    mainTableHeaders = [th.get_text().replace(u'\xa0', u' ') for th in soup.findAll('tr',limit=2)[0].findAll('th')]
    rows = soup.findAll('tr')[1:]

    # Get the actual stats from the table
    teamStats = [[td.getText().replace(u'\xa0', u' ') for td in rows[i].findAll('td')] for i in range(len(rows))]

    # Get row headers
    rowHeaders = []
    for row in rows:
        rowHeaders += [row.find('th').text.replace(u'\xa0', u' ')]

    # Create Dictionary
    stats = {}

    # Add stats to the dictionary
    counter  = 0
    stats['Legend'] = mainTableHeaders
    for row in rowHeaders:
        stats[row] = teamStats[counter]
        counter += 1

    return(stats)



