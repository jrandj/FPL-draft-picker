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
    print_fixture_predictions():
        Print the fixtures.
    """

    def __init__(self, consolidatedData):
        self.consolidatedData = consolidatedData
        self.fixtures = self.predict_fixtures()

    def predict_fixtures(self):
        """Generate the fixtures object to show the highest projected points for each team.

        Parameters
        ----------

        Raises
        ------

        """
        fixtures = []
        game_count = 0
        nextGameWeekHeader = self.consolidatedData.projectionsData.sixGameProjections[0].columns.values[-8]
        for match in self.consolidatedData.officialAPIData.league['matches']:
            # assuming league size is 12
            if game_count < 6 and match['finished'] is False:
                player_one_players = Team.get_players_for_team(
                    self.consolidatedData.officialAPIData.id_to_entry_id(match['league_entry_1']),
                    self.consolidatedData)
                player_two_players = Team.get_players_for_team(
                    self.consolidatedData.officialAPIData.id_to_entry_id(match['league_entry_2']),
                    self.consolidatedData)
                fixture = {
                    "player_one": self.consolidatedData.officialAPIData.id_to_entry_name(match['league_entry_1']),
                    "player_one_score": self.consolidatedData.get_formations(player_one_players,
                                                                             nextGameWeekHeader)[
                        0]['Score'],
                    "player_two": self.consolidatedData.officialAPIData.id_to_entry_name(match['league_entry_2']),
                    "player_two_score": self.consolidatedData.get_formations(player_two_players,
                                                                             nextGameWeekHeader)[
                        0][
                        'Score']
                }
                fixtures.append(fixture)
                game_count = game_count + 1
        return fixtures

    def print_fixture_predictions(self):
        """Print the fixtures.

        Parameters
        ----------

        Raises
        ------

        """
        print(tabulate(self.fixtures, headers="keys", tablefmt="github"))
