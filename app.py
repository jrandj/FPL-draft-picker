import pandas as pd
import argparse
from ConsolidatedData import ConsolidatedData
from OfficialAPIData import OfficialAPIData
from ProjectionsData import ProjectionsData
from Fixture import Fixture
from Team import Team

pd.options.mode.chained_assignment = None  # default='warn'


def main():
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

    officialAPIData = OfficialAPIData(leagueID)
    projectionsData = ProjectionsData(fantasyFootballScoutUsername, fantasyFootballScoutPassword)
    consolidatedData = ConsolidatedData(officialAPIData, projectionsData, teamName, leagueID)
    fixture = Fixture(consolidatedData.nextGameWeek)
    fixture.predict_fixtures(consolidatedData)
    team = Team(teamName, consolidatedData.teamID, consolidatedData)
    team.print_candidates()
    team.print_formations()


main()
