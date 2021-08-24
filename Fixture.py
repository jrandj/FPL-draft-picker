from tabulate import tabulate
from Team import Team


class Fixture:
    """
    A class that represents a fixture.

    Attributes
    ----------
    nextGameWeek : str
        The upcoming game week.

    Methods
    -------
    predict_fixtures()
        Predict the next fixture using the formation with the highest projected points for each team.
    """

    def __init__(self, nextGameWeek):
        self.nextGameWeek = nextGameWeek

    @staticmethod
    def predict_fixtures(consolidatedData):
        """Predict the next fixture using the formation with the highest projected points for each team.

        Parameters
        ----------
        consolidatedData : object
            An instance of ConsolidatedData.

        Raises
        ------

        """
        fixtures = []
        game_count = 0
        nextGameWeekHeader = consolidatedData.projectionsData.sixGameProjections[0].columns.values[-8]
        for match in consolidatedData.officialAPIData.league['matches']:
            # assuming league size is 12
            if game_count < 6 and match['finished'] is False:
                player_one_players = Team.get_players_for_team(
                    consolidatedData.officialAPIData.id_to_entry_id(match['league_entry_1']),
                    consolidatedData)
                player_two_players = Team.get_players_for_team(
                    consolidatedData.officialAPIData.id_to_entry_id(match['league_entry_2']),
                    consolidatedData)
                fixture = {
                    "player_one": consolidatedData.officialAPIData.id_to_entry_name(match['league_entry_1']),
                    "player_one_score": consolidatedData.get_formations(player_one_players, nextGameWeekHeader)[0][
                        'Score'],
                    "player_two": consolidatedData.officialAPIData.id_to_entry_name(match['league_entry_2']),
                    "player_two_score": consolidatedData.get_formations(player_two_players, nextGameWeekHeader)[0][
                        'Score']
                }
                fixtures.append(fixture)
                game_count = game_count + 1
        print(tabulate(fixtures, headers="keys", tablefmt="github"))
        return
