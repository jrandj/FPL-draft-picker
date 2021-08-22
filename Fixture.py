import pandas as pd
from tabulate import tabulate
from Team import Team


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

    @staticmethod
    def predict_fixtures(consolidatedData):
        """Predict the next fixture using the formation with the highest projected points.

        Parameters
        ----------
        consolidatedData : object
            TBC
        teamID : object
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
                player_one_players = Team.get_players_for_team(
                    consolidatedData.OfficialAPIData.id_to_entry_id(match['league_entry_1'], consolidatedData.OfficialAPIData),
                    consolidatedData)
                player_two_players = Team.get_players_for_team(
                    consolidatedData.OfficialAPIData.id_to_entry_id(match['league_entry_2'], consolidatedData.OfficialAPIData),
                    consolidatedData)
                fixture = {
                    "player_one": consolidatedData.OfficialAPIData.id_to_entry_name(match['league_entry_1'],
                                                                                  consolidatedData.OfficialAPIData),
                    "player_one_score": consolidatedData.get_formations(player_one_players, nextGameWeekHeader)[0][
                        'Score'],
                    "player_two": consolidatedData.OfficialAPIData.id_to_entry_name(match['league_entry_2'],
                                                                                  consolidatedData.OfficialAPIData),
                    "player_two_score": consolidatedData.get_formations(player_two_players, nextGameWeekHeader)[0][
                        'Score']
                }
                fixtures.append(fixture)
                game_count = game_count + 1
        print(tabulate(fixtures, headers="keys", tablefmt="github"))
        return
