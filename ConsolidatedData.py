import pandas as pd

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
    get_formations()
        Return team formations in descending order with the highest scoring at the top.
    add_total_points_to_players()
        Add the total projected scores to the players object.
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
        # OfficialAPIData.__init__(self, self.leagueID)
        # ProjectionsData.__init__(self, self.fantasyFootballScoutUsername, self.fantasyFootballScoutPassword)
        self.officialAPIData = OfficialAPIData(self.leagueID)
        self.projectionsData = ProjectionsData(self.fantasyFootballScoutUsername, self.fantasyFootballScoutPassword)
        self.teamID = self.get_teamID_from_teamName()
        self.add_candidates_to_players_based_on_projections()
        self.nextGameWeek = self.projectionsData.sixGameProjections[0].columns.values[-8]

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
                      {'GKP': 1, 'DEF': 5, 'MID': 2, 'FWD': 3, 'Score': 0},
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

    def add_total_points_to_players(self):
        """Add the total projected scores to the players object.

        Parameters
        ----------

        Raises
        ------

        """
        df = pd.DataFrame.from_dict(self.officialAPIData.players['elements'])
        # Left join fplPlayerData onto season projections using a key of player name, team name and position name.
        # We need to drop duplicates because the projections data does not have additional data to ensure a 1:1 join.
        df1 = df.merge(self.projectionsData.seasonProjections[0], how='left',
                       left_on=['web_name_clean', 'team_name', 'position_name'],
                       right_on=['Name', 'Team', 'Pos'], indicator='merge_status_season').drop_duplicates(
            subset=['id']).drop(columns=['Name', 'Team', 'Pos', 'FPL Price', 'Mins', 'G', 'A', 'CS', 'Bonus', 'YC'])
        d1 = df1.to_dict(orient='records')

        for i in range(len(d1)):
            self.officialAPIData.players['elements'][i]['merge_status_season'] = d1[i]['merge_status_season']
            self.officialAPIData.players['elements'][i]['FPL_Pts'] = d1[i]['FPL Pts']
        return

    def add_candidates_to_players_based_on_projections(self):
        """Find candidates who have a better six game projection than existing players in the team and add the list
        to the players object.

        Parameters
        ----------

        Raises
        ------

        """
        df = pd.DataFrame.from_dict(self.officialAPIData.players['elements'])
        sixGameProjection = self.projectionsData.sixGameProjections[0].columns.values[-2]
        nextGameWeek = self.projectionsData.sixGameProjections[0].columns.values[-8]
        nextGameWeekPlusOne = self.projectionsData.sixGameProjections[0].columns.values[-7]
        nextGameWeekPlusTwo = self.projectionsData.sixGameProjections[0].columns.values[-6]
        nextGameWeekPlusThree = self.projectionsData.sixGameProjections[0].columns.values[-5]
        nextGameWeekPlusFour = self.projectionsData.sixGameProjections[0].columns.values[-4]
        nextGameWeekPlusFive = self.projectionsData.sixGameProjections[0].columns.values[-3]

        # Left join fplPlayerData onto six game projections using a key of player name, team name and position name.
        # We need to drop duplicates because the projections data does not have additional data to ensure a 1:1 join.
        df1 = df.merge(self.projectionsData.sixGameProjections[0], how='left',
                       left_on=['web_name_clean', 'team_name', 'position_name'],
                       right_on=['Name', 'Team', 'Pos'], indicator='merge_status_six_game').drop_duplicates(
            subset=['id'])
        d1 = df1.to_dict(orient='records')

        for i in range(len(d1)):
            candidates = {}
            candidates_this_gw = {}
            ict_index_candidates = {}
            self.officialAPIData.players['elements'][i][sixGameProjection] = d1[i][sixGameProjection]
            self.officialAPIData.players['elements'][i][nextGameWeek] = d1[i][nextGameWeek]
            self.officialAPIData.players['elements'][i][nextGameWeekPlusOne] = d1[i][nextGameWeekPlusOne]
            self.officialAPIData.players['elements'][i][nextGameWeekPlusTwo] = d1[i][nextGameWeekPlusTwo]
            self.officialAPIData.players['elements'][i][nextGameWeekPlusThree] = d1[i][nextGameWeekPlusThree]
            self.officialAPIData.players['elements'][i][nextGameWeekPlusFour] = d1[i][nextGameWeekPlusFour]
            self.officialAPIData.players['elements'][i][nextGameWeekPlusFive] = d1[i][nextGameWeekPlusFive]
            self.officialAPIData.players['elements'][i]['merge_status_six_game'] = d1[i]['merge_status_six_game']
            if d1[i]['selected'] == self.teamID:
                for j in range(len(d1)):
                    if (d1[j][sixGameProjection] > d1[i][sixGameProjection]) and (d1[i]['Pos'] == d1[j]['Pos']) and \
                            (d1[j]['selected'] == 'No') and (d1[j]['available'] == 'Yes'):
                        candidates[d1[j]['web_name']] = d1[j][sixGameProjection]
                    if (d1[j][nextGameWeek] > d1[i][nextGameWeek]) and (d1[i]['Pos'] == d1[j]['Pos']) and \
                            (d1[j]['selected'] == 'No') and (d1[j]['available'] == 'Yes'):
                        candidates_this_gw[d1[j]['web_name']] = d1[j][nextGameWeek]
                    if (float(d1[j]['ict_index']) > float(d1[i]['ict_index'])) and (d1[i]['Pos'] == d1[j]['Pos']) and \
                            (d1[j]['selected'] == 'No') and (d1[j]['available'] == 'Yes'):
                        ict_index_candidates[d1[j]['web_name']] = float(d1[j]['ict_index'])
                sorted_candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
                sorted_candidates_this_gw = sorted(candidates_this_gw.items(), key=lambda x: x[1], reverse=True)
                ict_index_candidates = sorted(ict_index_candidates.items(), key=lambda x: x[1], reverse=True)
                self.officialAPIData.players['elements'][i]['candidates'] = sorted_candidates
                self.officialAPIData.players['elements'][i]['candidates_this_gw'] = sorted_candidates_this_gw
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
