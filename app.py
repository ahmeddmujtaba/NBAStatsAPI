import flask
from firebase import firebase
import collections
from flask_sqlalchemy import SQLAlchemy
import marshmallow
from firebase import firebase
import os
from flask import request, jsonify, Flask
from team.depthChart import depthChart
from playerID import getPlayerId
from player.playerStats import getStats
from player.playerImage import playerImage
from player.gameLogs import gameLogs
from player.gameLogsPlayoffs import gameLogsPlayoffs
from player.lineupsPlayoffs import lineupPlayoffs
from player.onoff import onoff
from player.onoffPlayoffs import onoffPlayoffs
from player.playerLineups import playerLineups
from player.shooting import shooting
from player.splits import splits
from player.playerLineups import playerLineups
from main.urlMaker import strip_accents
from firebase_admin import db
from requests.exceptions import HTTPError
from main.playerInfo import playerInfo
from team.franchiseStats import franchiseStats,teamStatsReferenceDict
from team.contracts import getContractStats
from team.coachStats import getCoachStats
from team.franchiseLeaders import getFranchiseLeadersStats,teamLeadersDict
from team.seasonLeaders import getFranchiseSeasonLeadersStats
from team.teamSeasonStats import teamSeasonStats,teamSeasonStatsreferenceDict
from team.gameLog import getTeamGameLog
from team.schedule import getTeamSchedule
from team.startingLineups import getTeamStartingLineups
from team.startingLineups2 import getTeamStartingLineups2
from team.teamLineups import teamLineupsReferenceDict,getTeamLineups
from team.teamOnOff import getTeamOnOff
from team.teamSplits import getTeamSplits
from seasons.allStarRoster import getAllStarRosters,allStarReferenceDict
from seasons.leagueIndex import getLeagueIndex
from seasons.leaguePer100 import getLeaguePer100
from seasons.leaguePerGame import getLeaguePerGame
from seasons.seasonPlayerStats import getSeasonPlayerStats, seasonPlayerStatsReferenceDict
from seasons.leagueSeasonLeaders import getSeasonLeadersStats
from seasons.leagueTotals import getLeagueTotals
from seasons.seasonStats import getSeasonStats,seasonStatsReferenceDict
from leaders.allTimeLeaders import allTimeCareerLeaderReferenceDict,allTimeCareerLeaders
from leaders.allTimePlayoffLeaders import allTimePlayoffLeaderReferenceDict,allTimePlayoffLeaders
from leaders.seasonLeaders import seasonLeaderReferenceDict,allTimeSeasonLeaders
from leaders.seasonPlayoffLeaders import seasonPlayoffLeaderReferenceDict,playoffSeasonLeaders


firebase = firebase.FirebaseApplication("https://bballdb-88bae.firebaseio.com/", None)



app = flask.Flask(__name__)

app.config["DEBUG"] = True


stats = {}

#region

def getRidOfAllAccents(stats):
    for key in stats.keys():
        for entry in stats[key]:
            entry = strip_accents(entry)

    for key in stats.keys():
        key = strip_accents(key)

    return(stats)



# MARK: PLAYER
# Gives yearly stats for a player
# Stat options are pergame,totals, advanced and more
# Example: http://127.0.0.1:5000/player/stats?name=stephencurry&type=advanced
@app.route('/player/stats', methods=['GET'])
def playerStatsF():
    playerID = getPlayerId(request.args['name'])
    statType = request.args['type']
    answer = firebase.get(f'/bballdb-88bae/seasons/player/{playerID}/stats', statType)
    if answer == None:
        try:
            answer = getStats(playerID,statType)
        except (HTTPError,KeyError,TypeError):
            answer = {"N/A":["N/A","N/A","N/A","N/A","N/A","N/A"],"NA":["N/A","N/A","N/A","N/A","N/A","N/A","N/A"],"Legend":["N/A","N/A","N/A","N/A","N/A","N/A","N/A"]}
        try:
            result = firebase.put(f'/bballdb-88bae/seasons/player/{playerID}/stats', statType,answer)
        except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
    try:
        del answer[""]
        answer = {"N/A":["N/A","N/A","N/A","N/A","N/A","N/A"],"NA":["N/A","N/A","N/A","N/A","N/A","N/A","N/A"],"Legend":["N/A","N/A","N/A","N/A","N/A","N/A","N/A"]}
    except KeyError:
        pass
    return(answer)


@app.route('/player/image' ,methods=['GET'])
def imageURLFetcher():
    player = request.args['name']
    playerID = getPlayerId(player)
    answer = firebase.get(f'/bballdb-88bae/seasons/player/{player}', 'src')
    if answer == None:
        try:
            answer = playerImage(playerID)
            try:
                result = firebase.put(f'/bballdb-88bae/player/{player}/imageURL/', 'src', answer)
            except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)



    



# Gives gamelogs for certain year, game are numbered as keys
# Example: http://127.0.0.1:5000/player/gamelogs?name=stephencurry&year=2016
@app.route('/player/gamelogs', methods=['GET'])
def gameLogsF():
    playerID = getPlayerId(request.args['name'])
    year = request.args['year']
    answer = gameLogs(playerID,year)
    return(answer)

# Gives playoff gamelogs for certain year, game are numbered as keys
# Example: http://127.0.0.1:5000/player/gamelogs?name=stephencurry&year=2016
@app.route('/player/playoffsgamelogs', methods=['GET'])
def playoffsGameLogsF():
    playerID = getPlayerId(request.args['name'])
    year = request.args['year']
    try:
        answer = gameLogsPlayoffs(playerID,year)
    except (KeyError,IndexError) as e:
        return({'N/A':'N/A'})
    answer = gameLogsPlayoffs(playerID,year)
    return(answer)

# Gives stats for a player and different lineups
# Option for either 2,3,4,5 man lineups 
# Example: http://127.0.0.1:5000/player/lineups?name=stephencurry&year=2016&man=2
@app.route('/player/lineups', methods=['GET'])
def lineupsF():
    playerID = getPlayerId(request.args['name'])
    year = request.args['year']
    man = request.args['man']
    try:
        answer = playerLineups(playerID,year,man)
    except (KeyError,IndexError) as e:
        return({'N/A':'N/A'})
    return(answer)

# Gives stats for a player and different lineups
# Option for either 2,3,4,5 man lineups 
# Example: http://127.0.0.1:5000/player/playoffslineups?name=stephencurry&year=2016&man=2
@app.route('/player/playoffslineups', methods=['GET'])
def playoffLineupsF():
    playerID = getPlayerId(request.args['name'])
    year = request.args['year']
    man = request.args['man']
    try:
        answer = lineupPlayoffs(playerID,year,man)
    except (KeyError,IndexError) as e:
        return({'N/A':'N/A'})
    return(answer)

# Gives stats comparing the impact of a player on team stats when on vs off
# Example: http://127.0.0.1:5000/player/onoff?name=stephencurry&year=2017
@app.route('/player/onoff', methods=['GET'])
def onoffF():
    playerID = getPlayerId(request.args['name'])
    year = request.args['year']
    try:
        answer = onoff(playerID,year)
    except (KeyError,IndexError) as e:
        return({'N/A':'N/A'})
    return(answer)

# Gives stats comparing the impact of a player on team stats when on vs off
# Example: http://127.0.0.1:5000/player/playoffsonoff?name=stephencurry&year=2017
@app.route('/player/playoffsonoff', methods=['GET'])
def onoffPlayoffsF():
    playerID = getPlayerId(request.args['name'])
    year = request.args['year']
    try:
        answer = onoffPlayoffs(playerID,year)
    except (KeyError,IndexError) as e:
        return({'N/A':'N/A'})
    return(answer)
    


    
# Returns shootings splits for a certain player during a certain year
# Example: http://127.0.0.1:5000/player/shooting?name=stephencurry&year=2016
@app.route('/player/shooting', methods=['GET'])
def shootingF():
    playerID = getPlayerId(request.args['name'])
    year = request.args['year']
    try:
        answer = shooting(playerID,year)
    except (KeyError,IndexError) as e:
        return({'N/A':'N/A'})
    return(answer)
   
# Returns splits for a certain player during a certain year
# Example: http://127.0.0.1:5000/player/splits?name=stephencurry&year=2016
@app.route('/player/splits', methods=['GET'])
def splitsF():
    playerID = getPlayerId(request.args['name'])
    year = request.args['year']
    try:
        answer = splits(playerID,year)
    except (KeyError,IndexError) as e:
        return({'N/A':'N/A'})
    return(answer)



@app.route('/player/POST', methods=['POST','GET'])
def postPlayerInfo():
    playerName = request.args['name']
    playerID = getPlayerId(request.args['name'])
    statType = request.args['type']
    if request.method == 'POST':
        answer = getStats(playerID,statType)
        try:
            del answer[""]
        except KeyError:
            pass
        try:
            playerName = str(playerName).replace('*','')
            result = firebase.put(f'/bballdb-88bae/player/{playerName}/stats/',statType,answer)
        except HTTPError:
            print("HTTP Exception Occured")
            pass
        
        return(answer)
    else:
        answer = firebase.get(f'/bballdb-88bae/player/{playerName}/stats/',statType)
        return(answer)


# Returns basic player information
# Example: http://127.0.0.1:5000/player/information?name=kobebryant
@app.route('/player/information', methods=['POST','GET'])
def postPlayerInformation():
    playerName = request.args['name']
    playerId = getPlayerId(playerName)
    if request.method == 'POST':
        answer = playerInfo(playerId)
        try:
            playerName = str(playerName).replace('*','')
            result = firebase.put(f'/bballdb-88bae/player/{playerName}/', 'Info',answer)
        except HTTPError:
            print("HTTP Exception Occured")
            pass

        return(answer)
    else:
        answer = firebase.get(f'/bballdb-88bae/player/{playerName}/','Info')
        return(answer)

# Returns certain stat of a certain type for a franchise for all its years
# Check the teamStatsReferenceDict to figure out available statTypes
# Example: http://127.0.0.1:5000/team/franchiseStats?team=DAL&statType=Basic&stat=TeamStats
@app.route('/team/franchiseStats', methods=['POST','GET'])
def postTeamFranchiseStats():
    teamName = request.args['team']
    statType = request.args['statType']
    stat = request.args['stat']
    if request.method == 'POST':
        answer = franchiseStats(teamStatsReferenceDict[statType][stat],teamName)
        try:
            result = firebase.put(f'/bballdb-88bae/teams/{teamName}/franchisestats/{statType}/', f'{stat}',answer)
        except HTTPError:
            print("HTTP Exception Occured")
            pass

        return(answer)
    else:
        answer = firebase.get(f'/bballdb-88bae/teams/{teamName}/franchisestats/{statType}/', f'{stat}')
        return(answer)


# Returns depthChart of a team organized by positions
# Includes playerNames and their stats
# Example: http://127.0.0.1:5000/team/depthChart?team=DAL&year=2020
@app.route('/team/depthChart', methods=['POST','GET'])
def postTeamDepthChart():
    teamName = request.args['team']
    year = request.args['year']
    if request.method == 'POST':
        answer = depthChart(teamName,year)
        try:
            result = firebase.put(f'/bballdb-88bae/teams/{teamName}/depthChart', str(year),answer)
        except HTTPError:
            print("HTTP Exception Occured")
            pass

        return(answer)
    else:
        answer = firebase.get(f'/bballdb-88bae/teams/{teamName}/depthChart', str(year))
        return(answer)

# Gives current contracts organized by names
# Example: http://127.0.0.1:5000/team/contracts?team=TOR
@app.route('/team/contracts', methods=['POST','GET'])
def postTeamContracts():
    teamName = request.args['team']
    if request.method == 'POST':
        answer = getContractStats(teamName)
        try:
            result = firebase.put(f'/bballdb-88bae/teams/{teamName}/', 'Contracts',answer)
        except AttributeError:
            print("Exception Occured")
            pass

        return(answer)
    else:
        answer = firebase.get(f'/bballdb-88bae/teams/{teamName}/', 'Contracts')
        if answer == None:
            answer = getContractStats(teamName)
        return(answer)

# Returns all the stats for every coach of that franchise, organized alphabetically
# Example: http://127.0.0.1:5000/team/coachStats?team=TOR
@app.route('/team/coachStats', methods=['POST','GET'])
def postCoachStats():
    teamName = request.args['team']
    if request.method == 'POST':
        answer = getCoachStats(teamName)
        try:
            result = firebase.put(f'/bballdb-88bae/teams/{teamName}', 'CoachStats',answer)
        except HTTPError:
            print("HTTP Exception Occured")
            pass

        return(answer)
    else:
        answer = firebase.get(f'/bballdb-88bae/teams/{teamName}', 'CoachStats')
        if answer == None:
            answer = getCoachStats(teamName)
        return(answer)

# Returns either career leaders or single season leadeers for a stats
# type = CareerLeaders | SeasonLeaders
# Example: http://127.0.0.1:5000/team/franchiseLeaders?team=TOR&type=SeasonLeaders
@app.route('/team/franchiseLeaders', methods=['POST','GET'])
def postFranchiseLeaders():
    teamName = request.args['team']
    statType = request.args['type']
    if request.method == 'POST':
        answer = getFranchiseLeadersStats(teamLeadersDict[statType],teamName)
        try:
            result = firebase.put(f'/bballdb-88bae/teams/{teamName}/franchiseLeaders/', statType,answer)
        except HTTPError:
            print("HTTP Exception Occured")
            pass

        return(answer)
    else:
        answer = firebase.get(f'/bballdb-88bae/teams/{teamName}/franchiseLeaders', statType)
        if answer == None:
            answer = getFranchiseLeadersStats(teamLeadersDict[statType],teamName)
        return(answer)

# Gives the leader for each category in current franchise season
# Example: http://127.0.0.1:5000/team/seasonLeaders?team=TOR&year=2020
@app.route('/team/seasonLeaders', methods=['POST','GET'])
def postSeasonLeaders():
    teamName = request.args['team']
    year = request.args['year']
    if request.method == 'POST':
        answer = getFranchiseSeasonLeadersStats(year,teamName)
        try:
            result = firebase.put(f'/bballdb-88bae/teams/{teamName}/seasonLeaders', str(year),answer)
        except HTTPError:
            print("HTTP Exception Occured")
            pass

        return(answer)
    else:
        answer = firebase.get(f'/bballdb-88bae/teams/{teamName}/seasonLeaders', str(year))
        if answer == None:
            answer = getFranchiseSeasonLeadersStats(year,teamName)
        return(answer)

# Gives player stats for each player on the team
# Check teamSeasonsStatsReferenceDict for the actual stat categories
# Example: http://127.0.0.1:5000/team/playerStats?team=TOR&stat=Advanced
@app.route('/team/playerStats', methods=['GET'])
def postTeamSeasonStats():
    teamName = request.args['team']
    stat = request.args['stat']
    answer = firebase.get(f'/bballdb-88bae/teams/{teamName}/seasonStats', stat)
    if answer == None:
        try:
            answer = teamSeasonStats(teamName,teamSeasonStatsreferenceDict[stat][0], teamSeasonStatsreferenceDict[stat][1])
            try:
                result = firebase.put(f'/bballdb-88bae/teams/{teamName}/seasonStats/', stat, answer)
            except HTTPError:
                print("HTTP Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)

# Returns gamelogs for all games of the current season
# Example: http://127.0.0.1:5000/team/gamelog?team=DAL
@app.route('/team/gamelog', methods=['GET'])
def postTeamGameLog():
    teamName = request.args['team']
    answer = firebase.get(f'/bballdb-88bae/teams/{teamName}/', 'gamelog')
    if answer == None:
        try:
            answer = getTeamGameLog(teamName)
            try:
                result = firebase.put(f'/bballdb-88bae/teams/{teamName}/', 'gamelog', answer)
            except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)

# Returns full schedule for the current season
# Example: http://127.0.0.1:5000/team/schedule?team=DAL
@app.route('/team/schedule', methods=['GET'])
def postTeamSchedule():
    teamName = request.args['team']
    answer = firebase.get(f'/bballdb-88bae/teams/{teamName}/', 'schedule')
    if answer == None:
        try:
            answer = getTeamSchedule(teamName)
            try:
                result = firebase.put(f'/bballdb-88bae/teams/{teamName}/', 'schedule', answer)
            except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)

# Returns starting lineup for each game of the season
# Example: http://127.0.0.1:5000/team/startinglineups?team=DAL&year=2020
@app.route('/team/startinglineups', methods=['GET'])
def postTeamStartingLineups():
    teamName = request.args['team']
    year = request.args['year']
    answer = firebase.get(f'/bballdb-88bae/teams/{teamName}/startinglineups', year)
    if answer == None:
        try:
            answer = getTeamStartingLineups(teamName,year)
            try:
                result = firebase.put(f'/bballdb-88bae/teams/{teamName}/startinglineups', year, answer)
            except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)


# Returns each starting lineup and winning percentage
# Example: http://127.0.0.1:5000/team/startinglineups2?team=DAL&year=2020
@app.route('/team/startinglineups2', methods=['GET'])
def postTeamStartingLineups2():
    teamName = request.args['team']
    year = request.args['year']
    answer = firebase.get(f'/bballdb-88bae/teams/{teamName}/startinglineups2', year)
    if answer == None:
        try:
            answer = getTeamStartingLineups2(teamName,year)
            try:
                result = firebase.put(f'/bballdb-88bae/teams/{teamName}/startinglineups2', year, answer)
            except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)

# Returns on-off stats for each player in the team
# Example: http://127.0.0.1:5000/team/onoff?team=DAL&year=2019
@app.route('/team/onoff', methods=['GET'])
def postTeamOnOff():
    teamName = request.args['team']
    year = request.args['year']
    answer = firebase.get(f'/bballdb-88bae/teams/{teamName}/onoff', year)
    if answer == None:
        try:
            answer = getTeamOnOff(teamName,year)
            try:
                result = firebase.put(f'/bballdb-88bae/teams/{teamName}/onoff', year, answer)
            except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)

# Returns the splits of the team throughout the current season
# Example: http://127.0.0.1:5000/team/splits?team=DAL&year=2019
@app.route('/team/splits', methods=['GET'])
def postTeamSplits():
    teamName = request.args['team']
    year = request.args['year']
    answer = firebase.get(f'/bballdb-88bae/teams/{teamName}/splits', year)
    if answer == None:
        try:
            answer = getTeamSplits(teamName,year)
            try:
                result = firebase.put(f'/bballdb-88bae/teams/{teamName}/splits', year, answer)
            except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)

# Return the different man lineups and their stats, sorted by playing time
# Example: http://127.0.0.1:5000/team/lineups?team=DAL&year=2020&man=2
@app.route('/team/lineups', methods=['GET'])
def postTeamLineups():
    teamName = request.args['team']
    year = request.args['year']
    stat = request.args['man']
    answer = firebase.get(f'/bballdb-88bae/teams/{teamName}/lineups/{year}', stat)
    if answer == None:
        try:
            answer = getTeamLineups(teamName,teamLineupsReferenceDict[stat],year)
            try:
                result = firebase.put(f'/bballdb-88bae/teams/{teamName}/lineups/{year}', stat, answer)
            except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)

# LEAGUE/SEASON SECTION

# Returns the awards team for the certain year
# Example: http://127.0.0.1:5000/season/allstarrosters?year=2010&stat=All-NBA
@app.route('/season/allstarrosters', methods=['GET'])
def postSeasonAllStars():
    year = request.args['year']
    stat = request.args['stat']
    answer = firebase.get(f'/bballdb-88bae/seasons/allstarrosters/{year}', stat)
    if answer == None:
        try:
            answer = getAllStarRosters(year, stat)
            try:
                result = firebase.put(f'/bballdb-88bae/seasons/allstarrosters/{year}', stat, answer)
            except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)

# Returns all the leaders for certain year
# Example: http://127.0.0.1:5000/season/leagueleaders?year=2020
@app.route('/season/leagueleaders', methods=['GET'])
def postLeagueLeaders():
    year = request.args['year']
    answer = firebase.get(f'/bballdb-88bae/seasons/leagueseasonleaders', year)
    if answer == None:
        try:
            answer = getSeasonLeadersStats(year)
            try:
                result = firebase.put(f'/bballdb-88bae/seasons/leagueseasonleaders', year, answer)
            except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)

# Returns every players stats, ordered alphabetically
# Example: http://127.0.0.1:5000/season/playerstats?year=2020&stat=PerGame
@app.route('/season/playerstats', methods=['GET'])
def postPlayerStats():
    year = request.args['year']
    stat = request.args['stat']
    answer = firebase.get(f'/bballdb-88bae/seasons/playerstats/{year}', stat)
    if answer == None:
        try:
            answer = getSeasonPlayerStats(year, stat)
            try:
                result = firebase.put(f'/bballdb-88bae/seasons/playerstats/{year}', stat, answer)
            except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)

# Returns team stats for current year
# Example: http://127.0.0.1:5000/season/teamstats?year=2020&stat=PerGame
@app.route('/season/teamstats', methods=['GET'])
def postSeasonStats():
    year = request.args['year']
    stat = request.args['stat']
    answer = firebase.get(f'/bballdb-88bae/seasons/stats/{year}', stat)
    if answer == None:
        try:
            answer = getSeasonStats(year, stat)
            try:
                result = firebase.put(f'/bballdb-88bae/seasons/stats/{year}', stat, answer)
            except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)

# Returns champion, awards, leaders for all seasons
# Example: http://127.0.0.1:5000/season/leagueindex
@app.route('/season/leagueindex', methods=['GET'])
def postSeasonLeagueIndex():
    answer = firebase.get(f'/bballdb-88bae/seasons', 'leagueindex')
    if answer == None:
        try:
            answer = getLeagueIndex()
            try:
                result = firebase.put(f'/bballdb-88bae/seasons', 'leagueindex' ,answer)
            except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)

# Returns per100 stats for all the seasons
@app.route('/season/leagueper100', methods=['GET'])
def postSeasonPer100():
    answer = firebase.get(f'/bballdb-88bae/seasons', 'leagueper100')
    if answer == None:
        try:
            answer = getLeaguePer100()
            try:
                result = firebase.put(f'/bballdb-88bae/seasons', 'leagueper100' ,answer)
            except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)

# Returns pergame stats for all the seasons
@app.route('/season/leaguepergame', methods=['GET'])
def postSeasonLeaguePerGame():
    answer = firebase.get(f'/bballdb-88bae/seasons', 'leaguepergame')
    if answer == None:
        try:
            answer = getLeaguePerGame()
            try:
                result = firebase.put(f'/bballdb-88bae/seasons', 'leaguepergame' ,answer)
            except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)

# Returns all time leaders for a certain stat
# Example: http://127.0.0.1:5000/leaders/alltime?type=Points
@app.route('/leaders/alltime', methods=['GET'])
def allTimeLeaders():
    stat = request.args['type']
    answer = firebase.get(f'/bballdb-88bae/leaders/alltime', stat)
    if answer == None:
        try:
            answer = allTimeCareerLeaders(stat)
            try:
                result = firebase.put(f'/bballdb-88bae/leaders/alltime', stat ,answer)
            except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)

# Returns all time leaders for a certain stat in the playoffs
# Example: http://127.0.0.1:5000/leaders/alltimeplayoffs?type=Points
@app.route('/leaders/alltimeplayoffs', methods=['GET'])
def postSeasonAllTimeLeaders():
    stat = request.args['type']
    answer = firebase.get(f'/bballdb-88bae/leaders/alltimeplayoffs', stat)
    if answer == None:
        try:
            answer = allTimePlayoffLeaders(stat)
            try:
                result = firebase.put(f'/bballdb-88bae/leaders/alltimeplayoffs', stat ,answer)
            except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)


# Returns single season leaders for a certain stat
# Example: http://127.0.0.1:5000/leaders/singleseson?type=Points
@app.route('/leaders/singleseason', methods=['GET'])
def singleSeasonLeaders():
    stat = request.args['type']
    answer = firebase.get(f'/bballdb-88bae/leaders/singleseason', stat)
    if answer == None:
        try:
            answer = allTimeSeasonLeaders(stat)
            try:
                result = firebase.put(f'/bballdb-88bae/leaders/singleseason', stat ,answer)
            except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)


# Returns single season leaders for a certain stat in the playoffs
# Example: http://127.0.0.1:5000/leaders/singleseasonplayoffs?type=Points
@app.route('/leaders/singleseasonplayoffs', methods=['GET'])
def singleSeasonPlayoffLeaders():
    stat = request.args['type']
    answer = firebase.get(f'/bballdb-88bae/leaders/singleseasonplayoffs', stat)
    if answer == None:
        try:
            answer = playoffSeasonLeaders(stat)
            try:  
                result = firebase.put(f'/bballdb-88bae/leaders/singleseasonplayoffs', stat ,answer)
            except (HTTPError,TypeError) as e:
                print(e, " - Exception Occured")
        except AttributeError:
            answer = 'N/A'
        
    return(answer)

if __name__ == '__main__':
    app.run()