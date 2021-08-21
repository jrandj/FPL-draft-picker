from collections import OrderedDict

import pandas as pd
from tabulate import tabulate
import math
import argparse
from ConsolidatedData import ConsolidatedData
from OfficialAPIData import OfficialAPIData
from ProjectionsData import ProjectionsData
from Fixture import Fixture

pd.options.mode.chained_assignment = None  # default='warn'


def print_candidates(fplPlayerData, projectionsData, team):
    """Print the players in the selected team along with candidates with a better projection.

    Parameters
    ----------
    fplPlayerData : dict
        The JSON containing player data from draft.premierleague.com
    projectionsData : dict
        The six game projections JSON from fantasyfootballscout.co.uk.
    team : dict
        The team that candidates are printed for

    Raises
    ------

    """
    printListPoints = []
    printListIctIndex = []
    sixGameProjectionHeader = projectionsData[0].columns.values[-2]
    nextGameWeekHeader = projectionsData[0].columns.values[-8]

    for i in team:
        printDictPoints = OrderedDict((k, i[k]) for k in (
            'web_name', 'team_name', 'position_name', sixGameProjectionHeader, nextGameWeekHeader, 'candidates',
            'candidates_this_gw'))
        printListPoints.append(printDictPoints)
        printDictIctIndex = OrderedDict(
            (k, i[k]) for k in ('web_name', 'team_name', 'position_name', 'ict_index', 'ict_index_candidates'))
        printListIctIndex.append(printDictIctIndex)

    sortedPrintListPoints = sorted(printListPoints, key=lambda x: (x['position_name'], -x[sixGameProjectionHeader]))
    sortedPrintListIctIndex = sorted(printListIctIndex, key=lambda x: (x['position_name'], -float(x['ict_index'])))
    print(tabulate(sortedPrintListPoints, headers="keys", tablefmt="github"))
    print(tabulate(sortedPrintListIctIndex, headers="keys", tablefmt="github"))

    expected_results = [i for i in fplPlayerData['elements'] if i['status'] != 'u']
    failed_merge = [i for i in fplPlayerData['elements'] if i['merge_status_six_game'] != 'both' and i['status'] != 'u']
    no_projections = [i for i in fplPlayerData['elements'] if
                      math.isnan(i[sixGameProjectionHeader]) and i['status'] != 'u' and i[
                          'merge_status_six_game'] == 'both']
    failed_merge_player_info = [[i["web_name_clean"], i["team_name"], i["position_name"], i["merge_status_six_game"]]
                                for i in failed_merge]
    no_projections_player_info = [[i["web_name_clean"], i["team_name"], i["position_name"], i["merge_status_six_game"]]
                                  for i in no_projections]

    print(str(len(expected_results))
          + " active players from the official API have been matched to " + str(
        len(expected_results) - len(failed_merge) - len(no_projections)) + " valid Scout projections.")
    print("The following merge failures occurred between the official API and the Scout projections: "
          + str(failed_merge_player_info))
    print("The following players were matched but have an invalid Scout projection: "
          + str(no_projections_player_info))
    return


def get_players_for_team(consolidatedData):
    """Return the players in a particular team.

    Parameters
    ----------
    consolidatedData : dict
        The JSON containing player data from draft.premierleague.com

    Raises
    ------

    """
    myTeam = []
    for i in range(len(consolidatedData.OfficialAPIData.players['elements'])):
        if consolidatedData.OfficialAPIData.players['elements'][i]['selected'] == consolidatedData.teamName:
            myTeam.append(consolidatedData.OfficialAPIData.players['elements'][i])
    return myTeam


def predict_league(fplPlayerData, projectionsDataSeason, consolidatedData):
    """Compare the season results using the formation with the highest projected points.

    Parameters
    ----------
    fplPlayerData : dict
        The JSON containing player data from draft.premierleague.com
    projectionsDataSeason : dict
        The season projections JSON from fantasyfootballscout.co.uk.

    Raises
    ------

    """
    fixtures = []
    nextGameWeekHeader = projectionsDataSeason[0].columns.values[-8]
    players = []
    formations = []

    for i in fplPlayerData['teams']:
        players[i] = get_players_for_team(fplPlayerData, i)
        formations[i] = get_formations(i, nextGameWeekHeader)

    print(tabulate(fixtures, headers="keys", tablefmt="github"))
    return





def print_formations(formations):
    """Print the formations for a player.

    Parameters
    ----------
    formations : list
        The list of formations.

    Raises
    ------

    """
    print("Formations and their scores: " + str(sorted(formations, key=lambda x: (x['Score']), reverse=True)))
    return


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


    print_candidates(consolidatedData.OfficialAPIData.players, consolidatedData.ProjectionsData.sixGameProjections,
                     consolidatedData.team)
    print_formations(consolidatedData.formations)


main()
