from bs4 import BeautifulSoup
import requests
import time
import unicodedata

seasonLeaderReferenceDict={
"Games":'https://www.basketball-reference.com//leaders/g_season.html',
'MinutesPlayed':'https://www.basketball-reference.com//leaders/mp_season.html',
'FieldGoals':'https://www.basketball-reference.com//leaders/fg_season.html',
'FieldGoalAttempts':'https://www.basketball-reference.com//leaders/fga_season.html',
'2-PtFieldGoals':'https://www.basketball-reference.com//leaders/fg2_season.html',
'2-PtFieldGoalAttempts':'https://www.basketball-reference.com//leaders/fg2a_season.html',
'3-PtFieldGoals':'https://www.basketball-reference.com//leaders/fg3_season.html',
'3-PtFieldGoalAttempts':'https://www.basketball-reference.com//leaders/fg3a_season.html',
'FieldGoalsMissed':'https://www.basketball-reference.com//leaders/fgx_season.html',
'FreeThrows':'https://www.basketball-reference.com//leaders/ft_season.html',
'FreeThrowAttempts':'https://www.basketball-reference.com//leaders/fta_season.html',
'OffensiveRebounds':'https://www.basketball-reference.com//leaders/orb_season.html',
'DefensiveRebounds':'https://www.basketball-reference.com//leaders/drb_season.html',
'TotalRebounds':'https://www.basketball-reference.com//leaders/trb_season.html',
'Assists':'https://www.basketball-reference.com//leaders/ast_season.html',
'Steals':'https://www.basketball-reference.com//leaders/stl_season.html',
'Blocks':'https://www.basketball-reference.com//leaders/blk_season.html',
'Turnovers':'https://www.basketball-reference.com//leaders/tov_season.html',
'PersonalFouls':'https://www.basketball-reference.com//leaders/pf_season.html',
'Points':'https://www.basketball-reference.com//leaders/pts_season.html',
'Triple-Doubles':'https://www.basketball-reference.com//leaders/trp_dbl_season.html',
'FieldGoalPct':'https://www.basketball-reference.com//leaders/fg_pct_season.html',
'2-PtFieldGoalPct':'https://www.basketball-reference.com//leaders/fg2_pct_season.html',
'3-PtFieldGoalPct':'https://www.basketball-reference.com//leaders/fg3_pct_season.html',
'FreeThrowPct':'https://www.basketball-reference.com//leaders/ft_pct_season.html',
'MinutesPerGame':'https://www.basketball-reference.com//leaders/mp_per_g_season.html',
'PointsPerGame':'https://www.basketball-reference.com//leaders/pts_per_g_season.html',
'ReboundsPerGame':'https://www.basketball-reference.com//leaders/trb_per_g_season.html',
'AssistsPerGame':'https://www.basketball-reference.com//leaders/ast_per_g_season.html',
'StealsPerGame':'https://www.basketball-reference.com//leaders/stl_per_g_season.html',
'BlocksPerGame':'https://www.basketball-reference.com//leaders/blk_per_g_season.html',
'PlayerEfficiencyRating':'https://www.basketball-reference.com//leaders/per_season.html',
'TrueShootingPct':'https://www.basketball-reference.com//leaders/ts_pct_season.html',
'EffectiveFieldGoalPct':'https://www.basketball-reference.com//leaders/efg_pct_season.html',
'OffensiveReboundPct':'https://www.basketball-reference.com//leaders/orb_pct_season.html',
'DefensiveReboundPct':'https://www.basketball-reference.com//leaders/drb_pct_season.html',
'TotalReboundPct':'https://www.basketball-reference.com//leaders/trb_pct_season.html',
'AssistPct':'https://www.basketball-reference.com//leaders/ast_pct_season.html',
'StealPct':'https://www.basketball-reference.com//leaders/stl_pct_season.html',
'BlockPct':'https://www.basketball-reference.com//leaders/blk_pct_season.html',
'TurnoverPct':'https://www.basketball-reference.com//leaders/tov_pct_season.html',
'UsagePct':'https://www.basketball-reference.com//leaders/usg_pct_season.html',
'OffensiveRating':'https://www.basketball-reference.com//leaders/off_rtg_season.html',
'DefensiveRating':'https://www.basketball-reference.com//leaders/def_rtg_season.html',
'OffensiveWinShares':'https://www.basketball-reference.com//leaders/ows_season.html',
'DefensiveWinShares':'https://www.basketball-reference.com//leaders/dws_season.html',
'WinShares':'https://www.basketball-reference.com//leaders/ws_season.html',
'WinSharesPer48Minutes':'https://www.basketball-reference.com//leaders/ws_per_48_season.html',
'BoxPlus/Minus':'https://www.basketball-reference.com//leaders/bpm_season.html',
'OffensiveBoxPlus/Minus':'https://www.basketball-reference.com//leaders/obpm_season.html',
'DefensiveBoxPlus/Minus':'https://www.basketball-reference.com//leaders/dbpm_season.html',
'ValueOverReplacementPlayer':'https://www.basketball-reference.com//leaders/vorp_season.html',



}

def allTimeSeasonLeaders(type):


    url = seasonLeaderReferenceDict[type]

    # Create a beautifulSoup object
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    div = soup.find('div',id='all_stats_NBA')


    soup = (div.find_all('table'))[0]


    # Get the headers from the table
    mainTableHeaders = [th.get_text().replace(u'\xa0', u' ') for th in soup.findAll('tr',limit=2)[0].findAll('th')]
    rows = soup.findAll('tr')[1:]

    # Get the actual stats from the table
    teamStats = [[td.getText().replace(u'\xa0', u' ') for td in rows[i].findAll('td')[1:]] for i in range(len(rows))]
 

    # Get row headers
    rowHeaders = []
    for row in rows:
        rowHeaders += [row.findAll('td')[0].text.replace(u'\xa0', u' ')]

    # Create Dictionary
    stats = {}

    # Add stats to the dictionary
    counter  = 1
    stats['Legend'] = mainTableHeaders
    for row in rowHeaders:
        if counter == 51:
            break
        stats[counter] = teamStats[counter]
        counter += 1



    # Return the dictionaries
    return(stats)
    

    return


