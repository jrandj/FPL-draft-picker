import pandas as pd


class ConsolidatedData:
    """
    A class that contains projections data from Fantasy Football Scout.

    Attributes
    ----------
    username : str
        The username used to authenticate.
    password : str
        The password used to authenticate.
    seasonProjections : object
        The season projections data.
    sixGameProjections : object
        The six game projections data.

    Methods
    -------
    import_data()
        Returns the projections data from Fantasy Football Scout.
    """
    def __init__(self, OfficialAPIData, ProjectionsData, teamName, leagueID):
        self.teamName = teamName
        self.leagueID = leagueID
        self.OfficialAPIData = OfficialAPIData
        self.ProjectionsData = ProjectionsData
        self.teamID = self.get_teamID_from_teamName()
        self.add_candidates_to_players_based_on_projections()
        self.team = self.get_players_for_team()
        self.nextGameWeek = self.ProjectionsData.sixGameProjections[0].columns.values[-8]
        #self.formations = self.get_formations(self.nextGameWeek, self.team)


    @staticmethod
    def add_player_to_formation(current_player, current_formation, formation):
        """Attempt to add a player to a formation.

        Parameters
        ----------
        current_player : dict
            The proposed player
        current_formation : dict
            The current formation
        formation : dict
            The formation that we are working towards

        Raises
        ------

        """
        player_added = True

        if current_player['position_name'] == 'GKP' and current_formation.get('GKP') + 1 <= formation.get('GKP'):
            current_formation['GKP'] = current_formation['GKP'] + 1
        elif current_player['position_name'] == 'DEF' and current_formation.get('DEF') + 1 <= formation.get('DEF'):
            current_formation['DEF'] = current_formation['DEF'] + 1
        elif current_player['position_name'] == 'MID' and current_formation.get('MID') + 1 <= formation.get('MID'):
            current_formation['MID'] = current_formation['MID'] + 1
        elif current_player['position_name'] == 'FWD' and current_formation.get('FWD') + 1 <= formation.get('FWD'):
            current_formation['FWD'] = current_formation['FWD'] + 1
        else:
            player_added = False

        return player_added

    def get_teamID_from_teamName(self):
        """Gets the unique identifier for the team from the team name.

        Parameters
        ----------

        Raises
        ------
        SystemExit:
            If the teamName cannot be found in the leagueID.
        """
        found = 0
        for i in self.OfficialAPIData.league['league_entries']:
            if i['entry_name'] == self.teamName:
                teamID = i['entry_id']
                found = 1
        if found == 0:
            print("Team " + self.teamName + " not found in league " + self.leagueID + ".")
            raise SystemExit()
        return teamID

    def add_total_points_to_players(self):
        """Add the total projected scores to the self.OfficialAPIData.players object.

        Parameters
        ----------

        Raises
        ------

        """
        df = pd.DataFrame.from_dict(self.OfficialAPIData.players['elements'])
        # Left join fplPlayerData onto season projections using a key of player name, team name and position name.
        # We need to drop duplicates because the projections data does not have additional data to ensure a 1:1 join.
        df1 = df.merge(self.ProjectionsData.seasonProjections[0], how='left',
                       left_on=['web_name_clean', 'team_name', 'position_name'],
                       right_on=['Name', 'Team', 'Pos'], indicator='merge_status_season').drop_duplicates(
            subset=['id']).drop(columns=['Name', 'Team', 'Pos', 'FPL Price', 'Mins', 'G', 'A', 'CS', 'Bonus', 'YC'])
        d1 = df1.to_dict(orient='records')

        for i in range(len(d1)):
            self.OfficialAPIData.players['elements'][i]['merge_status_season'] = d1[i]['merge_status_season']
            self.OfficialAPIData.players['elements'][i]['FPL_Pts'] = d1[i]['FPL Pts']
        return

    def add_candidates_to_players_based_on_projections(self):
        """Find candidates who have a better six game projection than the players in self.teamName.

        Parameters
        ----------

        Raises
        ------

        """
        df = pd.DataFrame.from_dict(self.OfficialAPIData.players['elements'])
        sixGameProjection = self.ProjectionsData.sixGameProjections[0].columns.values[-2]
        nextGameWeek = self.ProjectionsData.sixGameProjections[0].columns.values[-8]
        nextGameWeekPlusOne = self.ProjectionsData.sixGameProjections[0].columns.values[-7]
        nextGameWeekPlusTwo = self.ProjectionsData.sixGameProjections[0].columns.values[-6]
        nextGameWeekPlusThree = self.ProjectionsData.sixGameProjections[0].columns.values[-5]
        nextGameWeekPlusFour = self.ProjectionsData.sixGameProjections[0].columns.values[-4]
        nextGameWeekPlusFive = self.ProjectionsData.sixGameProjections[0].columns.values[-3]

        # Left join fplPlayerData onto six game projections using a key of player name, team name and position name.
        # We need to drop duplicates because the projections data does not have additional data to ensure a 1:1 join.
        df1 = df.merge(self.ProjectionsData.sixGameProjections[0], how='left', left_on=['web_name_clean', 'team_name', 'position_name'],
                       right_on=['Name', 'Team', 'Pos'], indicator='merge_status_six_game').drop_duplicates(
            subset=['id'])
        d1 = df1.to_dict(orient='records')

        for i in range(len(d1)):
            candidates = {}
            candidates_this_gw = {}
            ict_index_candidates = {}
            self.OfficialAPIData.players['elements'][i][sixGameProjection] = d1[i][sixGameProjection]
            self.OfficialAPIData.players['elements'][i][nextGameWeek] = d1[i][nextGameWeek]
            self.OfficialAPIData.players['elements'][i][nextGameWeekPlusOne] = d1[i][nextGameWeekPlusOne]
            self.OfficialAPIData.players['elements'][i][nextGameWeekPlusTwo] = d1[i][nextGameWeekPlusTwo]
            self.OfficialAPIData.players['elements'][i][nextGameWeekPlusThree] = d1[i][nextGameWeekPlusThree]
            self.OfficialAPIData.players['elements'][i][nextGameWeekPlusFour] = d1[i][nextGameWeekPlusFour]
            self.OfficialAPIData.players['elements'][i][nextGameWeekPlusFive] = d1[i][nextGameWeekPlusFive]
            self.OfficialAPIData.players['elements'][i]['merge_status_six_game'] = d1[i]['merge_status_six_game']
            if d1[i]['selected'] == self.teamName:
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
                self.OfficialAPIData.fplPlayerData['elements'][i]['candidates'] = sorted_candidates
                self.OfficialAPIData.fplPlayerData['elements'][i]['candidates_this_gw'] = sorted_candidates_this_gw
                self.OfficialAPIData.fplPlayerData['elements'][i]['ict_index_candidates'] = ict_index_candidates
        return

