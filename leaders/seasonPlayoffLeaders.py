from bs4 import BeautifulSoup
import requests
import time
import unicodedata


seasonPlayoffLeaderReferenceDict  = {
'Games':'https://www.basketball-reference.com//leaders/g_season_p.html',
'MinutesPlayed':'https://www.basketball-reference.com//leaders/mp_season_p.html',
'FieldGoals':'https://www.basketball-reference.com//leaders/fg_season_p.html',
'FieldGoalAttempts':'https://www.basketball-reference.com//leaders/fga_season_p.html',
'2-PtFieldGoals':'https://www.basketball-reference.com//leaders/fg2_season_p.html',
'2-PtFieldGoalAttempts':'https://www.basketball-reference.com//leaders/fg2a_season_p.html',
'3-PtFieldGoals':'https://www.basketball-reference.com//leaders/fg3_season_p.html',
'3-PtFieldGoalAttempts':'https://www.basketball-reference.com//leaders/fg3a_season_p.html',
'FieldGoalsMissed':'https://www.basketball-reference.com//leaders/fgx_season_p.html',
'FreeThrows':'https://www.basketball-reference.com//leaders/ft_season_p.html',
'FreeThrowAttempts':'https://www.basketball-reference.com//leaders/fta_season_p.html',
'OffensiveRebounds':'https://www.basketball-reference.com//leaders/orb_season_p.html',
'DefensiveRebounds':'https://www.basketball-reference.com//leaders/drb_season_p.html',
'TotalRebounds':'https://www.basketball-reference.com//leaders/trb_season_p.html',
'Assists':'https://www.basketball-reference.com//leaders/ast_season_p.html',
'Steals':'https://www.basketball-reference.com//leaders/stl_season_p.html',
'Blocks':'https://www.basketball-reference.com//leaders/blk_season_p.html',
'Turnovers':'https://www.basketball-reference.com//leaders/tov_season_p.html',
'PersonalFouls':'https://www.basketball-reference.com//leaders/pf_season_p.html',
'Points':'https://www.basketball-reference.com//leaders/pts_season_p.html',
'Triple-Doubles':'https://www.basketball-reference.com//leaders/trp_dbl_season_p.html',
'FieldGoalPct':'https://www.basketball-reference.com//leaders/fg_pct_season_p.html',
'2-PtFieldGoalPct':'https://www.basketball-reference.com//leaders/fg2_pct_season_p.html',
'3-PtFieldGoalPct':'https://www.basketball-reference.com//leaders/fg3_pct_season_p.html',
'FreeThrowPct':'https://www.basketball-reference.com//leaders/ft_pct_season_p.html',
'MinutesPerGame':'https://www.basketball-reference.com//leaders/mp_per_g_season_p.html',
'PointsPerGame':'https://www.basketball-reference.com//leaders/pts_per_g_season_p.html',
'ReboundsPerGame':'https://www.basketball-reference.com//leaders/trb_per_g_season_p.html',
'AssistsPerGame':'https://www.basketball-reference.com//leaders/ast_per_g_season_p.html',
'StealsPerGame':'https://www.basketball-reference.com//leaders/stl_per_g_season_p.html',
'BlocksPerGame':'https://www.basketball-reference.com//leaders/blk_per_g_season_p.html',
'PlayerEfficiencyRating':'https://www.basketball-reference.com//leaders/per_season_p.html',
'TrueShootingPct':'https://www.basketball-reference.com//leaders/ts_pct_season_p.html',
'EffectiveFieldGoalPct':'https://www.basketball-reference.com//leaders/efg_pct_season_p.html',
'OffensiveReboundPct':'https://www.basketball-reference.com//leaders/orb_pct_season_p.html',
'DefensiveReboundPct':'https://www.basketball-reference.com//leaders/drb_pct_season_p.html',
'TotalReboundPct':'https://www.basketball-reference.com//leaders/trb_pct_season_p.html',
'AssistPct':'https://www.basketball-reference.com//leaders/ast_pct_season_p.html',
'StealPct':'https://www.basketball-reference.com//leaders/stl_pct_season_p.html',
'BlockPct':'https://www.basketball-reference.com//leaders/blk_pct_season_p.html',
'TurnoverPct':'https://www.basketball-reference.com//leaders/tov_pct_season_p.html',
'UsagePct':'https://www.basketball-reference.com//leaders/usg_pct_season_p.html',
'OffensiveRating':'https://www.basketball-reference.com//leaders/off_rtg_season_p.html',
'DefensiveRating':'https://www.basketball-reference.com//leaders/def_rtg_season_p.html',
'OffensiveWinShares':'https://www.basketball-reference.com//leaders/ows_season_p.html',
'DefensiveWinShares':'https://www.basketball-reference.com//leaders/dws_season_p.html',
'WinShares':'https://www.basketball-reference.com//leaders/ws_season_p.html',
'WinSharesPer48Minutes':'https://www.basketball-reference.com//leaders/ws_per_48_season_p.html',
'BoxPlus/Minus':'https://www.basketball-reference.com//leaders/bpm_season_p.html',
'OffensiveBoxPlus/Minus':'https://www.basketball-reference.com//leaders/obpm_season_p.html',
'DefensiveBoxPlus/Minus':'https://www.basketball-reference.com//leaders/dbpm_season_p.html',
'ValueOverReplacementPlayer':'https://www.basketball-reference.com//leaders/vorp_season_p.html',

}


def playoffSeasonLeaders(type):

    url = seasonPlayoffLeaderReferenceDict[type]

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

