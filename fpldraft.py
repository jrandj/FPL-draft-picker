import pandas as pd
import argparse
from ConsolidatedData import ConsolidatedData
from Fixture import Fixture
from Team import Team

pd.options.mode.chained_assignment = None  # default='warn'


class Draft:
    """
    The top level class for the FPL-Draft application.

    Attributes
    ----------
    leagueID : sequence
        The unique identifier for the league.
    teamName : str
        The name of the team.
    fantasyFootballScoutUsername : str
        The username used to authenticate to Fantasy Football Scout.
    fantasyFootballScoutPassword : str
        The password used to authenticate to Fantasy Football Scout.
    consolidatedData : object
        An instance of ConsolidatedData.
    fixture : object
        An instance of Fixture.
    team : object
        An instance of Team.

    Methods
    -------
    parse_input()
        Parse the user input.
    """

    def __init__(self):
        self.leagueID, self.teamName, self.fantasyFootballScoutUsername, self.fantasyFootballScoutPassword = \
            self.parse_input()
        self.consolidatedData = ConsolidatedData(self.fantasyFootballScoutUsername, self.fantasyFootballScoutPassword,
                                                 self.teamName,
                                                 self.leagueID)
        self.fixture = Fixture(self.consolidatedData.nextGameWeek)
        self.team = Team(self.teamName, self.consolidatedData.teamID, self.consolidatedData)

    @staticmethod
    def parse_input():
        ap = argparse.ArgumentParser()
        ap.add_argument("-leagueID", required=True, help="The minileague")
        ap.add_argument("-teamName", required=True, help="The team")
        ap.add_argument("-fantasyFootballScoutUsername", required=True, help="Username for Fantasy Football Scout")
        ap.add_argument("-fantasyFootballScoutPassword", required=True, help="Password for Fantasy Football Scout")
        args = vars(ap.parse_args())
        leagueID = args.get('leagueID')
        teamName = args.get('teamName')
        fantasyFootballScoutUsername = args.get('fantasyFootballScoutUsername')
        fantasyFootballScoutPassword = args.get('fantasyFootballScoutPassword')
        return leagueID, teamName, fantasyFootballScoutUsername, fantasyFootballScoutPassword


def main():
    draft = Draft()
    draft.fixture.predict_fixtures(draft.consolidatedData)
    draft.team.print_candidates()
    draft.team.print_formations()


if __name__ == "__main__":
    main()