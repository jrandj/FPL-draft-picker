from tabulate import tabulate
from Team import Team


class Fixture:
    """
    A class that represents a fixture.

    Attributes
    ----------
    consolidatedData : object
        An instance of ConsolidatedData.
    fixtures : sequence
        The fixtures and their projected scores.
    representation : str
        A representation of the results.

    Methods
    -------
    predict_fixtures()
        Predict the next fixture using the formation with the highest projected points for each team.
    print_fixture_predictions():
        Print the fixtures.
    generate_representation():
        Generate a representation of the results.
    """

    def __init__(self, consolidatedData):
        self.consolidatedData = consolidatedData
        self.fixtures = self.predict_fixtures()
        self.representation = self.generate_representation()

    def predict_fixtures(self):
        """Generate the fixtures object to show the highest projected points for each team.

        Parameters
        ----------

        Raises
        ------

        """
        fixtures = []
        game_count = 0
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
                                                                             self.consolidatedData.nextGameWeek)[
                        0]['Score'],
                    "player_two": self.consolidatedData.officialAPIData.id_to_entry_name(match['league_entry_2']),
                    "player_two_score": self.consolidatedData.get_formations(player_two_players,
                                                                             self.consolidatedData.nextGameWeek)[
                        0][
                        'Score']
                }
                fixtures.append(fixture)
                game_count = game_count + 1
        return fixtures

    def generate_representation(self):
        """Generate a representation of the results.

        Parameters
        ----------

        Raises
        ------

        """
        return str(tabulate(self.fixtures, headers="keys", tablefmt="html", stralign="left", numalign="left",
                            colalign="left") + "<br>")
