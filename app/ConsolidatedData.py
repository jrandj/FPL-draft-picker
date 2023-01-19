import pandas as pd
import ssl
import aiohttp
import asyncio

from Team import Team
from OfficialAPIData import OfficialAPIData
from ProjectionsData import ProjectionsData


class ConsolidatedData:
    """
    A class that contains projections data from Fantasy Football Scout.

    Attributes
    ----------
    teamName : str
        The name of the team.
    leagueID : sequence
        The unique identifier for the league.
    fantasyFootballScoutUsername : str
        The username used to authenticate to Fantasy Football Scout.
    fantasyFootballScoutPassword : str
        The password used to authenticate to Fantasy Football Scout.
    officialAPIData : object
        An instance of OfficialAPIData.
    projectionsData : object
        An instance of ProjectionsData.
    teamID : object
        The players associated with teamName.
    nextGameWeek : str
        The upcoming game week.

    Methods
    -------
    load_official_data()
        Load the data from the official FPL APIs.
    load_projections_data()
        Load the data from the projection APIs.
    fetch_projection()
	    Make an API call for a projections URL.
    fetch_all_projections()
        Import projections data from Fantasy Football Scout
    fetch_official()
        Make an API call for an official URL.
    fetch_all_official()
        Import data from the official FPL API.
    get_formations()
        Return team formations in descending order with the highest scoring at the top.
    add_candidates_to_players_based_on_projections()
        Find candidates who have a better six game projection than existing players in the team and add the list
        to the players object.
    get_teamID_from_teamName()
        Gets the unique identifier for the team from the teamName.
    """

    def __init__(self, fantasyFootballScoutUsername, fantasyFootballScoutPassword, teamName, leagueID):
        self.teamName = teamName
        self.leagueID = leagueID
        self.fantasyFootballScoutUsername = fantasyFootballScoutUsername
        self.fantasyFootballScoutPassword = fantasyFootballScoutPassword
        official_response_data = self.load_official_data()
        projections_response_data = self.load_projections_data()
        self.officialAPIData = OfficialAPIData(self.leagueID, official_response_data)
        self.projectionsData = ProjectionsData(projections_response_data)
        self.teamID = self.get_teamID_from_teamName()
        self.add_candidates_to_players_based_on_projections()
        self.nextGameWeek = 'GW' + str(self.officialAPIData.players['events']['next'])

    def load_official_data(self):
        """Load Official API data.

        Parameters
        ----------

        Raises
        ------

        """
        loop = asyncio.get_event_loop()
        urls = ["https://draft.premierleague.com/api/bootstrap-static",
                "https://draft.premierleague.com/api/league/" + str(self.leagueID) + "/element-status",
                "https://draft.premierleague.com/api/league/" + str(self.leagueID) + "/details"]
        results = loop.run_until_complete(ConsolidatedData.fetch_all_official(urls, loop))
        return results

    def load_projections_data(self):
        """Load projections data from Fantasy Football Scout.

        Parameters
        ----------

        Raises
        ------
        ValueError:
            If the projections API responses cannot be parsed.
        """
        # try:
        loop = asyncio.get_event_loop()
        urls = ["https://members.fantasyfootballscout.co.uk/projections/six-game-projections/",
                "https://members.fantasyfootballscout.co.uk/projections/season-projections/"]
        results = loop.run_until_complete(self.fetch_all_projections(urls, loop))

        try:
            results[0] = pd.read_html(results[0])
            results[1] = pd.read_html(results[1])
        except ValueError as err:
            # Todo: Figure out how to catch authentication failure when posting to the session instead.
            print("No data can be read from Fantasy Football Scout, please check your credentials.")
            raise SystemExit(err)

        return results

    @staticmethod
    async def fetch_projection(session, url):
        """Make an API call for a projections URL.

        Parameters
        ----------
        url : str
            The current URL to request from.
        loop : aiohttp.client.ClientSession
            The session object.

        Raises
        ------

        """
        async with session.get(url, ssl=ssl.SSLContext()) as response:
            return await response.text()

    async def fetch_all_projections(self, urls, loop):
        """Import projections data from Fantasy Football Scout.

        Parameters
        ----------
        urls : list
            The JSON containing player data from a team.
        loop : asyncio.windows_events.ProactorEventLoop
            The asyncio loop object.

        Raises
        ------
        SystemExit:
            If a response cannot be obtained from the API.
        """
        try:
            async with aiohttp.ClientSession(loop=loop) as session:
                await session.post('https://members.fantasyfootballscout.co.uk/',
                                   data={'username': self.fantasyFootballScoutUsername,
                                         'password': self.fantasyFootballScoutPassword,
                                         'login': '>+Log+In'})
                results = await asyncio.gather(*[ConsolidatedData.fetch_projection(session, url) for url in urls],
                                               return_exceptions=True)
                return results
        except ValueError as err:
            print("Error calling projections API.")
            raise SystemExit(err)

    @staticmethod
    async def fetch_official(session, url):
        """Make an API call for an official URL.

        Parameters
        ----------
        url : str
            The current URL to request from.
        loop : aiohttp.client.ClientSession
            The session object.

        Raises
        ------

        """
        async with session.get(url, ssl=ssl.SSLContext()) as response:
            return await response.json()

    @staticmethod
    async def fetch_all_official(urls, loop):
        """Import data from the official FPL API.

        Parameters
        ----------
        urls : list
            The JSON containing player data from a team.
        loop : asyncio.windows_events.ProactorEventLoop
            The asyncio loop object.

        Raises
        ------
        SystemExit:
            If a response cannot be obtained from the API.
        """
        try:
            async with aiohttp.ClientSession(loop=loop) as session:
                results = await asyncio.gather(*[ConsolidatedData.fetch_official(session, url) for url in urls],
                                               return_exceptions=True)
                return results
        except ValueError as err:
            print("Error calling official API.")
            raise SystemExit(err)

    @staticmethod
    def get_formations(team, nextGameWeekHeader):
        """Return team formations in descending order with the highest scoring at the top.

        Parameters
        ----------
        team : dict
            The JSON containing player data from a team.
        nextGameWeekHeader : string
            The key for the projected points of the upcoming game week.

        Raises
        ------

        """
        formations = [{'GKP': 1, 'DEF': 5, 'MID': 3, 'FWD': 2, 'Score': 0},
                      {'GKP': 1, 'DEF': 5, 'MID': 4, 'FWD': 1, 'Score': 0},
                      {'GKP': 1, 'DEF': 4, 'MID': 3, 'FWD': 3, 'Score': 0},
                      {'GKP': 1, 'DEF': 4, 'MID': 5, 'FWD': 1, 'Score': 0},
                      {'GKP': 1, 'DEF': 4, 'MID': 4, 'FWD': 2, 'Score': 0},
                      {'GKP': 1, 'DEF': 3, 'MID': 5, 'FWD': 2, 'Score': 0},
                      {'GKP': 1, 'DEF': 3, 'MID': 4, 'FWD': 3, 'Score': 0}]
        player_index = 0
        total_points = 0
        current_formation = {'GKP': 0, 'DEF': 0, 'MID': 0, 'FWD': 0}
        team.sort(key=lambda x: (x['position_name'], -x[nextGameWeekHeader]))
        for formation in formations:
            team_copy = team.copy()
            while current_formation != formation and len(team_copy) > player_index:
                current_player = team_copy[player_index]
                # This approach assumes the team is sorted by projected points in the next game week
                if Team.add_player_to_formation(current_player, current_formation, formation):
                    total_points += current_player[nextGameWeekHeader]
                    del team_copy[player_index]
                    player_index = 0
                else:
                    player_index = player_index + 1

            formation['Score'] = round(total_points, 2)
            total_points = 0
            player_index = 0
            current_formation = {'GKP': 0, 'DEF': 0, 'MID': 0, 'FWD': 0}
        formations.sort(key=lambda x: (-x['Score']))
        return formations

    def add_candidates_to_players_based_on_projections(self):
        """Find candidates who have a better six game projection than existing players in the team and add the list
        to the players object.

        Parameters
        ----------

        Raises
        ------

        """
        df = pd.DataFrame.from_dict(self.officialAPIData.players['elements'])
        sixGameProjectionHeader = self.projectionsData.sixGameProjections[0].columns.values[-2]
        numberOfRemainingGameWeeks = 39 - self.officialAPIData.players['events']['next']
        nextGameWeekName = 'GW' + str(self.officialAPIData.players['events']['next'])
        GameWeekName = []

        # I will need to validate this behaviour in the last 6 GWs
        # at GW37 there is only GW38 at position -3 (the columns shrink)
        lower_bound = 6  # for e.g. at start of season -3 -5 is GW1
        if numberOfRemainingGameWeeks < 5:
            upper_bound = -3 - (5 - numberOfRemainingGameWeeks)
        else:
            upper_bound = 0  # for e.g. at start of season -3 is GW6

        for i in range(upper_bound, lower_bound):
            GameWeekName.append(self.projectionsData.sixGameProjections[0].columns.values[-3 - i])

        # Left join fplPlayerData onto six game projections using a key of player name, team name, and position name.
        # We need to drop duplicates because the projections data does not have additional data to ensure a 1:1 join.
        # df.to_csv('players.csv')/self.projectionsData.sixGameProjections[0].to_csv('projections.csv') allow analysis
        df1 = df.merge(self.projectionsData.sixGameProjections[0], how='left',
                       left_on=['web_name_clean', 'team_name', 'position_name'],
                       right_on=['Name', 'Team', 'Pos'], indicator='merge_status_six_game').drop_duplicates(
            subset=['id'])
        d1 = df1.to_dict(orient='records')

        for i in range(len(d1)):
            candidates = {}
            candidates_this_gw = {}
            ict_index_candidates = {}
            self.officialAPIData.players['elements'][i]['6GW Pts Projection'] = d1[i][sixGameProjectionHeader]
            self.officialAPIData.players['elements'][i]['NGW Pts Projection'] = d1[i][GameWeekName[-1]]
            for ii in range(upper_bound, lower_bound - 1):
                self.officialAPIData.players['elements'][i][GameWeekName[ii]] = d1[i][GameWeekName[ii]]
            self.officialAPIData.players['elements'][i]['merge_status_six_game'] = d1[i]['merge_status_six_game']
            if d1[i]['selected'] == self.teamID:
                for j in range(len(d1)):
                    if (d1[j][sixGameProjectionHeader] > d1[i][sixGameProjectionHeader]) and (
                            d1[i]['Pos'] == d1[j]['Pos']) and \
                            (d1[j]['selected'] == 'No') and (d1[j]['available'] == 'Yes'):
                        candidates[d1[j]['web_name']] = d1[j][sixGameProjectionHeader]
                    if (d1[j][nextGameWeekName] > d1[i][nextGameWeekName]) and (d1[i]['Pos'] == d1[j]['Pos']) and \
                            (d1[j]['selected'] == 'No') and (d1[j]['available'] == 'Yes'):
                        candidates_this_gw[d1[j]['web_name']] = d1[j][nextGameWeekName]
                    if (float(d1[j]['ict_index']) > float(d1[i]['ict_index'])) and (d1[i]['Pos'] == d1[j]['Pos']) and \
                            (d1[j]['selected'] == 'No') and (d1[j]['available'] == 'Yes'):
                        ict_index_candidates[d1[j]['web_name']] = float(d1[j]['ict_index'])
                sorted_candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
                sorted_candidates_this_gw = sorted(candidates_this_gw.items(), key=lambda x: x[1], reverse=True)
                ict_index_candidates = sorted(ict_index_candidates.items(), key=lambda x: x[1], reverse=True)
                self.officialAPIData.players['elements'][i]['6GW Candidates'] = sorted_candidates
                self.officialAPIData.players['elements'][i]['NGW Candidates'] = sorted_candidates_this_gw
                self.officialAPIData.players['elements'][i]['ict_index_candidates'] = ict_index_candidates
        return

    def get_teamID_from_teamName(self):
        """Gets the unique identifier for the team from the teamName.

        Parameters
        ----------

        Raises
        ------
        SystemExit:
            If the teamName cannot be found in the leagueID.
        """
        found = 0
        for i in self.officialAPIData.league['league_entries']:
            if i['entry_name'] == self.teamName:
                teamID = i['entry_id']
                found = 1
        if found == 0:
            print("Team " + self.teamName + " not found in league " + self.leagueID + ".")
            raise SystemExit()
        return teamID
