import pandas as pd
from tabulate import tabulate


class Fixture:
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
    def __init__(self, GameWeek):
        self.nextGameWeek = GameWeek

    def get_formation_for_team(self, team):
        """Return team formations in descending order with the highest scoring at the top.

        Parameters
        ----------

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
        self.team.sort(key=lambda x: (x['position_name'], -x[self.nextGameWeek]))
        for formation in formations:
            team_copy = team.copy()
            while current_formation != formation and len(team_copy) > player_index:
                current_player = team_copy[player_index]
                # This approach assumes the team is sorted by projected points in the next game week
                if self.add_player_to_formation(current_player, current_formation, formation):
                    total_points += current_player[self.nextGameWeek]
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

    @staticmethod
    def predict_fixtures(consolidatedData):
        """Predict the next fixture using the formation with the highest projected points.

        Parameters
        ----------
        consolidatedData : object
            TBC

        Raises
        ------

        """
        fixtures = []
        game_count = 0
        nextGameWeekHeader = consolidatedData.ProjectionsData.sixGameProjections[0].columns.values[-8]
        for match in consolidatedData.OfficialAPIData.league['matches']:
            # assuming league size is 12
            if game_count < 6 and match['finished'] is False:
                player_one_players = Fixture.get_players_for_team(consolidatedData)
                player_two_players = Fixture.get_players_for_team(consolidatedData)
                fixture = {
                    "player_one": consolidatedData.OfficialAPIData.id_to_entry_id(match['league_entry_1'],
                                                                                  consolidatedData.OfficialAPIData.league),
                    "player_one_score": consolidatedData.get_formations(player_one_players, nextGameWeekHeader)[0]['Score'],
                    "player_two": consolidatedData.OfficialAPIData.id_to_entry_id(match['league_entry_2'],
                                                                                  consolidatedData.OfficialAPIData.league),
                    "player_two_score": consolidatedData.get_formations(player_two_players, nextGameWeekHeader)[0]['Score']
                }
                fixtures.append(fixture)
                game_count = game_count + 1
        print(tabulate(fixtures, headers="keys", tablefmt="github"))
        return

    @staticmethod
    def get_players_for_team(teamName, consolidatedData):
        """Return the players in the team.

        Parameters
        ----------
        teamName : object
            TBC
        consolidatedData : object
            TBC

        Raises
        ------

        """
        team = []
        for i in range(len(consolidatedData.OfficialAPIData.players['elements'])):
            if consolidatedData.OfficialAPIData.players['elements'][i]['selected'] == teamName:
                consolidatedData.team.append(consolidatedData.OfficialAPIData.players['elements'][i])
        return team
