from collections import OrderedDict

import requests
import pandas as pd
from tabulate import tabulate
import math
import argparse

pd.options.mode.chained_assignment = None  # default='warn'


def import_data(myLeague, ffsusername, ffspassword):
    """Imports data from draft.premierleague and fantasyfootballscout.

    Parameters
    ----------
    myLeague : str
        The mini-league identifier.
    ffsusername : str
        The username used to authenticate to members.fantasyfootballscout.co.uk.
    ffspassword : str
        The password used to authenticate to members.fantasyfootballscout.co.uk.

    Raises
    ------
    requests.exceptions.HTTPError:
        If any HTTP errors are encountered when retrieving data.
    ValueError:
        If the six game projections cannot be parsed.

    """
    try:
        r1 = requests.get(url="https://draft.premierleague.com/api/league/" + str(myLeague) + "/element-status")
        r1.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    try:
        r2 = requests.get(url='https://draft.premierleague.com/api/bootstrap-static')
        r2.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    try:
        s1 = requests.session()
        s1.post('https://members.fantasyfootballscout.co.uk/',
                data={'username': ffsusername, 'password': ffspassword, 'login': '>+Log+In'})
        r3 = s1.get('https://members.fantasyfootballscout.co.uk/projections/six-game-projections/')
        r3.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    fplAvailabilityData = r1.json()
    fplPlayerData = r2.json()
    try:
        projectionsData = pd.read_html(r3.content)
    except ValueError as err:
        # Todo: Figure out how to catch authentication failure when posting to the session instead.
        print("No data can be read from fantasyfootballscout, please check your credentials.")
        raise SystemExit(err)

    return fplAvailabilityData, fplPlayerData, projectionsData


def strip_special_characters(name):
    """Strips out special characters from names as these are not in the fantasyfootballscout.co.uk data.

    Parameters
    ----------
    name : str
        The name to remove unicode characters from.

    Raises
    ------

    """
    name = name.translate(str.maketrans({'í': 'i', 'ï': 'i', 'ß': 'ss', 'á': 'a', 'ä': 'a', 'é': 'e', 'ñ': 'n',
                                         'ć': 'c', 'š': 's', 'Ö': 'O', 'ö': 'o', 'ó': 'o', 'ø': 'o', 'ü': 'u',
                                         'ç': 'c', 'ú': 'u', 'Ü': 'U', 'ş': 's', 'ğ': 'g', 'ã': 'a'}))
    return name


def align_projections_data_to_official(projectionsData):
    """Fix differences between fantasyfootballscout.co.uk projections and draft.premierleague.com data.

    Parameters
    ----------
    projectionsData : dict
        The projections JSON from fantasyfootballscout.co.uk to be modified.

    Raises
    ------

    """
    projectionsData[0]['Team'].loc[projectionsData[0]['Team'] == 'BRI'] = 'BHA'
    projectionsData[0]['Team'].loc[projectionsData[0]['Team'] == 'SOT'] = 'SOU'
    projectionsData[0]['Team'].loc[projectionsData[0]['Team'] == 'WHM'] = 'WHU'
    projectionsData[0]['Pos'].loc[projectionsData[0]['Pos'] == 'GK'] = 'GKP'
    projectionsData[0]['Name'].loc[projectionsData[0]['Name'].str.contains('Buend<ed>a')] = 'Buendia'
    projectionsData[0]['Name'].loc[projectionsData[0]['Name'].str.contains('Femenia') &
                                   projectionsData[0]['Team'].str.contains('WAT')] = 'Kiko Femenia'
    projectionsData[0]['Name'].loc[projectionsData[0]['Name'].str.contains('Gomes') &
                                   projectionsData[0]['Team'].str.contains('EVE')] = 'Andre Gomes'
    projectionsData[0]['Name'].loc[projectionsData[0]['Name'].str.contains('Sanchez') &
                                   projectionsData[0]['Team'].str.contains('WHU')] = 'Carlos Sanchez'
    projectionsData[0]['Name'].loc[projectionsData[0]['Name'].str.contains('Rodriguez') &
                                   projectionsData[0]['Team'].str.contains('EVE')] = 'James'
    projectionsData[0]['Name'].loc[projectionsData[0]['Name'].str.contains('Rodri') &
                                   projectionsData[0]['Team'].str.contains('MCI')] = 'Rodrigo'
    projectionsData[0]['Name'].loc[projectionsData[0]['Name'].str.contains('Kiko Femenia') &
                                   projectionsData[0]['Team'].str.contains('WAT')] = 'Femenia'
    return projectionsData


def find_candidates(fplPlayerData, projectionsData, team):
    """Find candidates who have a better six game projection than the players in the selected team.

    Parameters
    ----------
    fplPlayerData : dict
        The JSON containing player data from draft.premierleague.com
    projectionsData : dict
        The projections JSON from fantasyfootballscout.co.uk.
    team : String
        The team that candidates are being found for

    Raises
    ------

    """
    df = pd.DataFrame.from_dict(fplPlayerData['elements'])
    projectionsData = align_projections_data_to_official(projectionsData)
    sixGameProjection = projectionsData[0].columns.values[-2]
    nextGameWeek = projectionsData[0].columns.values[-8]
    nextGameWeekPlusOne = projectionsData[0].columns.values[-7]
    nextGameWeekPlusTwo = projectionsData[0].columns.values[-6]
    nextGameWeekPlusThree = projectionsData[0].columns.values[-5]
    nextGameWeekPlusFour = projectionsData[0].columns.values[-4]
    nextGameWeekPlusFive = projectionsData[0].columns.values[-3]
    # Left join fplPlayerData onto projections using a key of player name, team name and position name
    df1 = df.merge(projectionsData[0], how='left', left_on=['web_name_clean', 'team_name', 'position_name'],
                   right_on=['Name', 'Team', 'Pos'], indicator='merge_status')
    d1 = df1.to_dict(orient='records')

    for i in range(len(d1)):
        candidates = {}
        candidates_this_gw = {}
        ict_index_candidates = {}
        fplPlayerData['elements'][i][sixGameProjection] = d1[i][sixGameProjection]
        fplPlayerData['elements'][i][nextGameWeek] = d1[i][nextGameWeek]
        fplPlayerData['elements'][i][nextGameWeekPlusOne] = d1[i][nextGameWeekPlusOne]
        fplPlayerData['elements'][i][nextGameWeekPlusTwo] = d1[i][nextGameWeekPlusTwo]
        fplPlayerData['elements'][i][nextGameWeekPlusThree] = d1[i][nextGameWeekPlusThree]
        fplPlayerData['elements'][i][nextGameWeekPlusFour] = d1[i][nextGameWeekPlusFour]
        fplPlayerData['elements'][i][nextGameWeekPlusFive] = d1[i][nextGameWeekPlusFive]
        fplPlayerData['elements'][i]['merge_status'] = d1[i]['merge_status']
        if d1[i]['selected'] == team:
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
            fplPlayerData['elements'][i]['candidates'] = sorted_candidates
            fplPlayerData['elements'][i]['candidates_this_gw'] = sorted_candidates_this_gw
            fplPlayerData['elements'][i]['ict_index_candidates'] = ict_index_candidates
    return fplPlayerData


def consolidate_data(fplAvailabilityData, fplPlayerData):
    """Augment fplPlayerData with information about availability from fplAvailabilityData.

    Parameters
    ----------
    fplAvailabilityData : dict
        The JSON containing data from the mini-league from draft.premierleague.com.
    fplPlayerData : dict
        The JSON containing player data from draft.premierleague.com

    Raises
    ------

    """
    for i in range(len(fplPlayerData['elements'])):
        fplPlayerData['elements'][i]['web_name_clean'] = strip_special_characters(
            fplPlayerData['elements'][i]['web_name'])
        fplPlayerData['elements'][i]['selected'] = 'No'
        fplPlayerData['elements'][i]['available'] = 'No'

        for j in fplPlayerData['teams']:
            if fplPlayerData['elements'][i]['team'] == j['id']:
                fplPlayerData['elements'][i]['team_name'] = j['short_name']

        for j in fplPlayerData['element_types']:
            if fplPlayerData['elements'][i]['element_type'] == j['id']:
                fplPlayerData['elements'][i]['position_name'] = j['singular_name_short']

        for j in fplAvailabilityData['element_status']:
            if fplPlayerData['elements'][i]['id'] == j['element']:
                if j['owner'] is not None:
                    fplPlayerData['elements'][i]['selected'] = j['owner']
                if fplPlayerData['elements'][i]['status'] != 'u' and j['owner'] is None:
                    fplPlayerData['elements'][i]['available'] = 'Yes'
    return fplPlayerData


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


def get_formations(team, nextGameWeekHeader):
    """Print team formations in order of highest scoring.

    Parameters
    ----------
    team : dict
        The JSON containing player data from a team
    nextGameWeekHeader : string
        The key for the projected points of the next game week

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
            if add_player_to_formation(current_player, current_formation, formation):
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


def get_players_for_team(fplPlayerData, projectionsData, team):
    """Print the players in the selected team along with candidates with a better projection.

    Parameters
    ----------
    fplPlayerData : dict
        The JSON containing player data from draft.premierleague.com
    projectionsData : dict
        The projections JSON from fantasyfootballscout.co.uk.
    team : String
        The JSON containing player data from a team

    Raises
    ------

    """
    myTeam = []
    nanCount = 0
    inactiveCount = 0
    sixGameProjectionHeader = projectionsData[0].columns.values[-2]
    for i in range(len(fplPlayerData['elements'])):
        if fplPlayerData['elements'][i]['selected'] == team:
            myTeam.append(fplPlayerData['elements'][i])
        if math.isnan(fplPlayerData['elements'][i][sixGameProjectionHeader]):
            nanCount = nanCount + 1
        if fplPlayerData['elements'][i]['status'] == 'u':
            inactiveCount = inactiveCount + 1
    return myTeam, nanCount, inactiveCount


def print_candidates(fplPlayerData, projectionsData, team, nanCount, inactiveCount):
    """Print the players in the selected team along with candidates with a better projection.

    Parameters
    ----------
    fplPlayerData : dict
        The JSON containing player data from draft.premierleague.com
    projectionsData : dict
        The projections JSON from fantasyfootballscout.co.uk.
    team : dict
        The team that candidates are printed for
    nanCount : int
        The number of players that have a NaN fantasyfootballscout.co.uk projection.
    inactiveCount : int
        The number of inactive players.

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

    print(str(len(fplPlayerData['elements']) - inactiveCount)
          + " active players from the official API have been matched to " + str(len(fplPlayerData['elements'])
                                                                                - inactiveCount + (
                                                                                        inactiveCount - nanCount)) + " valid Scout projections.")
    failed_merge = [i for i in fplPlayerData['elements'] if i['merge_status'] != 'both' and i['status'] != 'u']
    no_projections = [i for i in fplPlayerData['elements'] if
                      math.isnan(i[sixGameProjectionHeader]) and i['status'] != 'u']
    failed_merge_player_info = [[i["web_name_clean"], i["team_name"], i["position_name"], i["merge_status"]]
                                for i in failed_merge]
    no_projections_player_info = [[i["web_name_clean"], i["team_name"], i["position_name"], i["merge_status"]]
                                  for i in no_projections]
    print("The following merge failures occurred between the official API and the Scout projections: "
          + str(failed_merge_player_info))
    print("The following players were matched but have an invalid Scout projection: "
          + str(no_projections_player_info))
    return


def get_team(myLeague, myTeamName):
    """Gets the unique identifier for the team from the team name.

    Parameters
    ----------
    myLeague : str
        The mini-league identifier.
    myTeamName : str
        The team name.

    Raises
    ------
    requests.exceptions.HTTPError:
        If any HTTP errors are encountered when retrieving data.

    """
    url = "https://draft.premierleague.com/api/league/" + str(myLeague) + "/details"
    try:
        r1 = requests.get(url=url)
        r1.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    leagueData = r1.json()
    found = 0
    for i in leagueData['league_entries']:
        if i['entry_name'] == myTeamName:
            myTeam = i['entry_id']
            found = 1
    if found == 0:
        print("Team " + myTeamName + " not found in league " + myLeague + ".")
        raise SystemExit()
    return myTeam


def get_league_details(league):
    """Gets the league details.

    Parameters
    ----------
    league : str
        The mini-league identifier.

    Raises
    ------
    requests.exceptions.HTTPError:
        If any HTTP errors are encountered when retrieving data.

    """
    url = "https://draft.premierleague.com/api/league/" + str(league) + "/details"
    try:
        r1 = requests.get(url=url)
        r1.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    league_details = r1.json()
    return league_details


def id_to_entry_id(id, league_details):
    """Gets the entry id from the entity id.

    Parameters
    ----------
    id : int
        The entity id.
    league_details : dict
        The mini-league details.

    Raises
    ------

    """
    for entry in league_details['league_entries']:
        if entry['id'] == id:
            entity_id = entry['entry_id']
            return entity_id
    print("Id " + id + " not found in league.")
    raise SystemExit()


def id_to_entry_name(id, league_details):
    """Gets the entity name from the entity id.

    Parameters
    ----------
    id : int
        The entity id.
    league_details : dict
        The mini-league details.

    Raises
    ------

    """
    for entry in league_details['league_entries']:
        if entry['id'] == id:
            entry_name = entry['entry_name']
            return entry_name
    print("Id " + id + " not found in league.")
    raise SystemExit()


def predict_fixtures(fplPlayerData, projectionsData, league_details):
    """Print the players in the selected team along with candidates with a better projection.

    Parameters
    ----------
    fplPlayerData : dict
        The JSON containing player data from draft.premierleague.com
    projectionsData : dict
        The projections JSON from fantasyfootballscout.co.uk.
    league_details : dict
        The mini-league details.

    Raises
    ------

    """
    fixtures = []
    game_count = 0
    nextGameWeekHeader = projectionsData[0].columns.values[-8]
    for match in league_details['matches']:
        # assuming league size is 12
        if game_count < 6 and match['finished'] == False:
            player_one_players, nanCount, inactiveCount = get_players_for_team(fplPlayerData, projectionsData,
                                                                               id_to_entry_id(match['league_entry_1'],
                                                                                              league_details))
            player_two_players, nanCount, inactiveCount = get_players_for_team(fplPlayerData, projectionsData,
                                                                               id_to_entry_id(match['league_entry_2'],
                                                                                              league_details))
            fixture = {
                "player_one": id_to_entry_name(match['league_entry_1'], league_details),
                "player_one_score": get_formations(player_one_players, nextGameWeekHeader)[0]['Score'],
                "player_two": id_to_entry_name(match['league_entry_2'], league_details),
                "player_two_score": get_formations(player_two_players, nextGameWeekHeader)[0]['Score']
            }
            fixtures.append(fixture)
            game_count = game_count + 1
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
    ap.add_argument("-myLeague", required=True, help="The minileague")
    ap.add_argument("-myTeamName", required=True, help="The team")
    ap.add_argument("-ffslogin", required=True, help="Username for fantasyfootballscout")
    ap.add_argument("-ffspassword", required=True, help="Password for fantasyfootballscout")
    args = vars(ap.parse_args())

    myTeam = get_team(args.get('myLeague'), args.get('myTeamName'))
    fplAvailabilityData, fplPlayerData, projectionsData = \
        import_data(args.get('myLeague'), args.get('ffslogin'), args.get('ffspassword'))
    fplPlayerData = consolidate_data(fplAvailabilityData, fplPlayerData)
    fplPlayerData = find_candidates(fplPlayerData, projectionsData, myTeam)
    league_details = get_league_details(args.get('myLeague'))
    predict_fixtures(fplPlayerData, projectionsData, league_details)
    myPlayers, nanCount, inactiveCount = get_players_for_team(fplPlayerData, projectionsData, myTeam)
    nextGameWeek = projectionsData[0].columns.values[-8]
    myFormations = get_formations(myPlayers, nextGameWeek)
    print_candidates(fplPlayerData, projectionsData, myPlayers, nanCount, inactiveCount)
    print_formations(myFormations)


main()
