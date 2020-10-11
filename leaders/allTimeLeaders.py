from bs4 import BeautifulSoup
import requests
import time
import unicodedata

allTimeCareerLeaderReferenceDict = {
'Games':'https://www.basketball-reference.com//leaders/g_career.html',
'MinutesPlayed':'https://www.basketball-reference.com//leaders/mp_career.html',
'FieldGoals':'https://www.basketball-reference.com//leaders/fg_career.html',
'FieldGoalAttempts':'https://www.basketball-reference.com//leaders/fga_career.html',
'2-PtFieldGoals':'https://www.basketball-reference.com//leaders/fg2_career.html',
'2-PtFieldGoalAttempts':'https://www.basketball-reference.com//leaders/fg2a_career.html',
'3-PtFieldGoals':'https://www.basketball-reference.com//leaders/fg3_career.html',
'3-PtFieldGoalAttempts':'https://www.basketball-reference.com//leaders/fg3a_career.html',
'FieldGoalsMissed':'https://www.basketball-reference.com//leaders/fgx_career.html',
'FreeThrows':'https://www.basketball-reference.com//leaders/ft_career.html',
'FreeThrowAttempts':'https://www.basketball-reference.com//leaders/fta_career.html',
'OffensiveRebounds':'https://www.basketball-reference.com//leaders/orb_career.html',
'DefensiveRebounds':'https://www.basketball-reference.com//leaders/drb_career.html',
'TotalRebounds':'https://www.basketball-reference.com//leaders/trb_career.html',
'Assists':'https://www.basketball-reference.com//leaders/ast_career.html',
'Steals':'https://www.basketball-reference.com//leaders/stl_career.html',
'Blocks':'https://www.basketball-reference.com//leaders/blk_career.html',
'Turnovers':'https://www.basketball-reference.com//leaders/tov_career.html',
'PersonalFouls':'https://www.basketball-reference.com//leaders/pf_career.html',
'Points':'https://www.basketball-reference.com//leaders/pts_career.html',
'Triple-Doubles':'https://www.basketball-reference.com//leaders/trp_dbl_career.html',
'FieldGoalPct':'https://www.basketball-reference.com//leaders/fg_pct_career.html',
'2-PtFieldGoalPct':'https://www.basketball-reference.com//leaders/fg2_pct_career.html',
'3-PtFieldGoalPct':'https://www.basketball-reference.com//leaders/fg3_pct_career.html',
'FreeThrowPct':'https://www.basketball-reference.com//leaders/ft_pct_career.html',
'MinutesPerGame':'https://www.basketball-reference.com//leaders/mp_per_g_career.html',
'PointsPerGame':'https://www.basketball-reference.com//leaders/pts_per_g_career.html',
'ReboundsPerGame':'https://www.basketball-reference.com//leaders/trb_per_g_career.html',
'AssistsPerGame':'https://www.basketball-reference.com//leaders/ast_per_g_career.html',
'StealsPerGame':'https://www.basketball-reference.com//leaders/stl_per_g_career.html',
'BlocksPerGame':'https://www.basketball-reference.com//leaders/blk_per_g_career.html',
'PlayerEfficiencyRating':'https://www.basketball-reference.com//leaders/per_career.html',
'TrueShootingPct':'https://www.basketball-reference.com//leaders/ts_pct_career.html',
'EffectiveFieldGoalPct':'https://www.basketball-reference.com//leaders/efg_pct_career.html',
'OffensiveReboundPct':'https://www.basketball-reference.com//leaders/orb_pct_career.html',
'DefensiveReboundPct':'https://www.basketball-reference.com//leaders/drb_pct_career.html',
'TotalReboundPct':'https://www.basketball-reference.com//leaders/trb_pct_career.html',
'AssistPct':'https://www.basketball-reference.com//leaders/ast_pct_career.html',
'StealPct':'https://www.basketball-reference.com//leaders/stl_pct_career.html',
'BlockPct':'https://www.basketball-reference.com//leaders/blk_pct_career.html',
'TurnoverPct':'https://www.basketball-reference.com//leaders/tov_pct_career.html',
'UsagePct':'https://www.basketball-reference.com//leaders/usg_pct_career.html',
'OffensiveRating':'https://www.basketball-reference.com//leaders/off_rtg_career.html',
'DefensiveRating':'https://www.basketball-reference.com//leaders/def_rtg_career.html',
'OffensiveWinShares':'https://www.basketball-reference.com//leaders/ows_career.html',
'DefensiveWinShares':'https://www.basketball-reference.com//leaders/dws_career.html',
'WinShares':'https://www.basketball-reference.com//leaders/ws_career.html',
'WinSharesPer48Minutes':'https://www.basketball-reference.com//leaders/ws_per_48_career.html',
'BoxPlus/Minus':'https://www.basketball-reference.com//leaders/bpm_career.html',
'OffensiveBoxPlus/Minus':'https://www.basketball-reference.com//leaders/obpm_career.html',
'DefensiveBoxPlus/Minus':'https://www.basketball-reference.com//leaders/dbpm_career.html',
'ValueOverReplacementPlayer':'https://www.basketball-reference.com//leaders/vorp_career.html',

}

def allTimeCareerLeaders(type):

    url = allTimeCareerLeaderReferenceDict[type]

    # Create a beautifulSoup object
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    div = soup.find('div',id='all_nba')


    soup = (div.find_all('table'))[0]


    # Get the headers from the table
    mainTableHeaders = [unicodedata.normalize('NFD',th.get_text().replace(u'\xa0', u' ')) for th in soup.findAll('tr',limit=2)[0].findAll('th')]
    rows = soup.findAll('tr')[1:]

    # Get the actual stats from the table
    teamStats = [[td.getText().replace(u'\xa0', u' ').replace('\n','') for td in rows[i].findAll('td')[1:]] for i in range(len(rows))]
 

    # Get row headers
    rowHeaders = []
    for row in rows:
        rowHeaders += [row.findAll('td')[0].text.replace(u'\xa0', u' ')]

    # Create Dictionary
    stats = {}

    # Add stats to the dictionary
    counter  = 0
    stats['Legend'] = mainTableHeaders
    counter = 1
    for row in rowHeaders:
        if counter == 50:
            break
        stats[row] = teamStats[counter]
        counter += 1

    print(stats)



    # Return the dictionaries
    return(stats)
    

    return


