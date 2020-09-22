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
    myLeague : sequence
        The mini-league identifier.
    ffsusername : sequence
        The username used to authenticate to members.fantasyfootballscout.co.uk.
    ffspassword : sequence
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


def strip_special_characters(myString):
    """Strips out special characters as these are not in the fantasyfootballscout.co.uk data.

    Parameters
    ----------
    myString : sequence
        The string to remove unicode characters from.

    Raises
    ------

    """
    myString = myString.translate(str.maketrans({'í': 'i', 'ï': 'i', 'ß': 'ss', 'á': 'a', 'ä': 'a', 'é': 'e', 'ñ': 'n',
                                                 'ć': 'c', 'š': 's', 'Ö': 'o', 'ö': 'o', 'ó': 'o', 'ø': 'o', 'ü': 'u',
                                                 'ç': 'c'}))
    return myString


def align_projections_data_to_official(projectionsData):
    """Fix differences between fantasyfootballscout.co.uk projections and draft.premierleague.com data.

    Parameters
    ----------
    projectionsData : dictionary
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
    return projectionsData


def find_candidates(fplPlayerData, projectionsData):
    """Find candidates who have a better six game projection than the players in the selected team.

    Parameters
    ----------
    fplPlayerData : dictionary
        The JSON containing player data from draft.premierleague.com
    projectionsData : dictionary
        The projections JSON from fantasyfootballscout.co.uk.

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
        fplPlayerData['elements'][i][sixGameProjection] = d1[i][sixGameProjection]
        fplPlayerData['elements'][i][nextGameWeek] = d1[i][nextGameWeek]
        fplPlayerData['elements'][i][nextGameWeekPlusOne] = d1[i][nextGameWeekPlusOne]
        fplPlayerData['elements'][i][nextGameWeekPlusTwo] = d1[i][nextGameWeekPlusTwo]
        fplPlayerData['elements'][i][nextGameWeekPlusThree] = d1[i][nextGameWeekPlusThree]
        fplPlayerData['elements'][i][nextGameWeekPlusFour] = d1[i][nextGameWeekPlusFour]
        fplPlayerData['elements'][i][nextGameWeekPlusFive] = d1[i][nextGameWeekPlusFive]
        fplPlayerData['elements'][i]['merge_status'] = d1[i]['merge_status']
        if d1[i]['selected'] == 'Yes':
            for j in range(len(d1)):
                if (d1[j][sixGameProjection] > d1[i][sixGameProjection]) and (d1[i]['Pos'] == d1[j]['Pos']) and \
                        (d1[j]['selected'] == 'No') and (d1[j]['available'] == 'Yes'):
                    candidates[d1[j]['web_name']] = d1[j][sixGameProjection]
            sorted_candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
            fplPlayerData['elements'][i]['candidates'] = sorted_candidates
    return fplPlayerData


def consolidate_data(fplAvailabilityData, fplPlayerData, myTeam):
    """Augment fplPlayerData with information about availability from fplAvailabilityData.

    Parameters
    ----------
    fplAvailabilityData : dictionary
        The JSON containing data from the mini-league from draft.premierleague.com.
    fplPlayerData : dictionary
        The JSON containing player data from draft.premierleague.com
    myTeam : sequence
        The selected team identifier.

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
                if j['owner'] == myTeam:
                    fplPlayerData['elements'][i]['selected'] = 'Yes'
                if fplPlayerData['elements'][i]['status'] != 'u' and j['owner'] is None:
                    fplPlayerData['elements'][i]['available'] = 'Yes'
    return fplPlayerData


def add_player_to_formation(current_player, current_formation, formation):
    """Attempt to add a player to a formation.

    Parameters
    ----------
    current_player : dictionary
        The proposed player
    current_formation : dictionary
        The current formation
    formation : dictionary
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
    team : dictionary
        The JSON containing player data from a team
    nextGameWeekHeader : string
        The key for the projected points of the next game week

    Raises
    ------

    """
    formations = [{'GKP': 1, 'DEF': 5, 'MID': 3, 'FWD': 2, 'Score': 0},
                  {'GKP': 1, 'DEF': 5, 'MID': 4, 'FWD': 1, 'Score': 0},
                  {'GKP': 1, 'DEF': 4, 'MID': 3, 'FWD': 3, 'Score': 0},
                  {'GKP': 1, 'DEF': 4, 'MID': 5, 'FWD': 1, 'Score': 0},
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


def print_candidates(fplPlayerData, projectionsData):
    """Print the players in the selected team along with candidates with a better projection.

    Parameters
    ----------
    fplPlayerData : dictionary
        The JSON containing player data from draft.premierleague.com
    projectionsData : dictionary
        The projections JSON from fantasyfootballscout.co.uk.

    Raises
    ------

    """
    myTeam = []
    printList = []
    nanCount = 0
    inactiveCount = 0
    sixGameProjectionHeader = projectionsData[0].columns.values[-2]
    nextGameWeekHeader = projectionsData[0].columns.values[-8]
    nextGameWeekPlusOneHeader = projectionsData[0].columns.values[-7]
    nextGameWeekPlusTwoHeader = projectionsData[0].columns.values[-6]
    nextGameWeekPlusThreeHeader = projectionsData[0].columns.values[-5]
    nextGameWeekPlusFourHeader = projectionsData[0].columns.values[-4]
    nextGameWeekPlusFiveHeader = projectionsData[0].columns.values[-3]

    for i in range(len(fplPlayerData['elements'])):
        if fplPlayerData['elements'][i]['selected'] == 'Yes':
            myTeam.append(fplPlayerData['elements'][i])
        if math.isnan(fplPlayerData['elements'][i][sixGameProjectionHeader]):
            nanCount = nanCount + 1
        if fplPlayerData['elements'][i]['status'] == 'u':
            inactiveCount = inactiveCount + 1

    for i in myTeam:
        printDict = {k: v for k, v in i.items() if k in {'web_name', 'team_name', 'position_name',
                                                         sixGameProjectionHeader, nextGameWeekHeader,
                                                         nextGameWeekPlusOneHeader, nextGameWeekPlusTwoHeader,
                                                         nextGameWeekPlusThreeHeader, nextGameWeekPlusFourHeader,
                                                         nextGameWeekPlusFiveHeader, 'candidates'}}
        printList.append(printDict)

    sortedPrintList = sorted(printList, key=lambda x: (x['position_name'], -x[sixGameProjectionHeader]))
    print(tabulate(sortedPrintList, headers="keys", tablefmt="github"))

    formations = get_formations(myTeam, nextGameWeekHeader)

    # Print the number of matched players
    print(str(len(fplPlayerData['elements']) - inactiveCount)
          + " active players from the official API have been matched to "
          + str(len(fplPlayerData['elements']) - nanCount) + " Scout projections, with a difference of "
          + str(len(fplPlayerData['elements']) - inactiveCount - (len(fplPlayerData['elements']) - nanCount)) + ".")

    failed_merge = [i for i in fplPlayerData['elements'] if i['merge_status'] != 'both' and i['status'] != 'u']
    failed_merge_player_info = [[i["web_name_clean"], i["team_name"], i["position_name"], i["merge_status"]]
                                for i in failed_merge]
    print("The " + str(len(fplPlayerData['elements']) - inactiveCount - (len(fplPlayerData['elements']) - nanCount))
          + " differences are due to the following merge failures: " + str(failed_merge_player_info))
    print("Formations and their scores: " + str(sorted(formations, key=lambda x: (x['Score']), reverse=True)))


def get_team(myLeague, myTeamName):
    """Gets the unique identifier for the team from the team name.

    Parameters
    ----------
    myLeague : sequence
        The mini-league identifier.
    myTeamName : sequence
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
    fplPlayerData = consolidate_data(fplAvailabilityData, fplPlayerData, myTeam)
    fplPlayerData = find_candidates(fplPlayerData, projectionsData)
    print_candidates(fplPlayerData, projectionsData)


main()
