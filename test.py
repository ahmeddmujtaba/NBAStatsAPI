
from app import app
import unittest



class FlaskTest(unittest.TestCase):
    def test__playerInfo(self):
        tester = app.test_client(self)
        response = tester.get("/player/information?name=kobebryant")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test__playerStats(self):
        tester = app.test_client(self)
        response = tester.get("/player/stats?name=stephencurry&type=advanced")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test__Image(self):
        tester = app.test_client(self)
        response = tester.get("/player/image?name=stephencurry")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test__playerLineups(self):
        tester = app.test_client(self)
        response = tester.get("/player/lineups?name=stephencurry&year=2016&man=2")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test__playerGameLogs(self):
        tester = app.test_client(self)
        response = tester.get("/player/gamelogs?name=stephencurry&year=2016")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test__playerOnOff(self):
        tester = app.test_client(self)
        response = tester.get("/player/onoff?name=stephencurry&year=2017")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test__playerShooting(self):
        tester = app.test_client(self)
        response = tester.get("/player/shooting?name=stephencurry&year=2016")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    

    def test__playerSplits(self):
        tester = app.test_client(self)
        response = tester.get("/player/splits?name=stephencurry&year=2016")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    def test__teamFranchiseStats(self):
        tester = app.test_client(self)
        response = tester.get("/team/franchiseStats?team=DAL&statType=Basic&stat=TeamStats")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    def test__teamDepthChart(self):
        tester = app.test_client(self)
        response = tester.get("/team/depthChart?team=DAL&year=2020")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test__teamContracts(self):
        tester = app.test_client(self)
        response = tester.get("/team/contracts?team=TOR")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    
    def test__teamFranchiseLeaders(self):
        tester = app.test_client(self)
        response = tester.get("/team/franchiseLeaders?team=TOR&type=SeasonLeaders")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test__teamSeasonLeadersLeaders(self):
        tester = app.test_client(self)
        response = tester.get("/team/seasonLeaders?team=TOR&year=2020")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test__teamPlayerStats(self):
        tester = app.test_client(self)
        response = tester.get("/team/playerStats?team=TOR&stat=Advanced")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test__teamGameLogs(self):
        tester = app.test_client(self)
        response = tester.get("/team/gamelog?team=DAL")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    def test__teamSchedule(self):
        tester = app.test_client(self)
        response = tester.get("/team/schedule?team=DAL")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    def test__teamStartingLineups(self):
        tester = app.test_client(self)
        response = tester.get("/team/startinglineups?team=DAL&year=2020")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    def test__teamOnOff(self):
        tester = app.test_client(self)
        response = tester.get("/team/onoff?team=DAL&year=2019")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    def test__teamSplits(self):
        tester = app.test_client(self)
        response = tester.get("/team/splits?team=DAL&year=2019")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test__teamLineups(self):
        tester = app.test_client(self)
        response = tester.get("/team/lineups?team=DAL&year=2020&man=2")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    
    def test__seasonAllStarRosters(self):
        tester = app.test_client(self)
        response = tester.get("/season/allstarrosters?year=2010&stat=All-NBA")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test__seasonLeagueLeaders(self):
        tester = app.test_client(self)
        response = tester.get("/season/leagueleaders?year=2020")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test__seasonLeagueLeaders(self):
        tester = app.test_client(self)
        response = tester.get("/season/leagueleaders?year=2020")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test__seasonPlayerStats(self):
        tester = app.test_client(self)
        response = tester.get("/season/playerstats?year=2020&stat=PerGame")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)


    def test__seasonStats(self):
        tester = app.test_client(self)
        response = tester.get("/season/teamstats?year=2020&stat=PerGame")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)


    def test__seasonLeagueIndex(self):
        tester = app.test_client(self)
        response = tester.get("/season/leagueindex")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)


    def test__leaguePerGame(self):
        tester = app.test_client(self)
        response = tester.get("/season/leaguepergame")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test__leaderAllTime(self):
        tester = app.test_client(self)
        response = tester.get("/leaders/alltime?type=Points")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test__seasonAllTimeLeaders(self):
        tester = app.test_client(self)
        response = tester.get("leaders/alltimeplayoffs?type=Points")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test__leaderSingleSeason(self):
        tester = app.test_client(self)
        response = tester.get("/leaders/singleseason?type=Points")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test__leaderSingleSeasonPLayoffs(self):
        tester = app.test_client(self)
        response = tester.get("/leaders/singleseasonplayoffs?type=Points")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    


    
    
    
unittest.main()