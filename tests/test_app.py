from app import app

import pandas as pd


# Test that selected players are correctly tagged in fplPlayerData
def test_selected_players():
    myLeague = 48188
    myTeamName = "wearetherunnersup"
    myTeam = app.get_team(myLeague, myTeamName)
    fplAvailabilityData, fplPlayerData, projectionsData = app.import_data(myLeague)
    fplPlayerData = app.consolidate_data(fplAvailabilityData, fplPlayerData, myTeam)

    testTeam = [525, 186, 527, 5, 333, 30, 152, 172, 347, 371, 67, 367, 410, 401, 12]
    for i in testTeam:
        assert (fplPlayerData['elements'][i-1]['selected'] == 'Yes')


# Test that strip_unicode handles all non-ASCII characters in player names in fplPlayerData
def test_web_name_clean():
    myLeague = 48188
    fplAvailabilityData, fplPlayerData, projectionsData = app.import_data(myLeague)

    for i in range(len(fplPlayerData['elements'])):
        assert app.strip_unicode(fplPlayerData['elements'][i]['web_name']).isascii()


# Test that merge between fplPlayerData and projectionsData is 1-1 based on the key
def test_one_to_one_merge():
    myLeague = 48188
    myTeamName = "wearetherunnersup"
    myTeam = app.get_team(myLeague, myTeamName)
    fplAvailabilityData, fplPlayerData, projectionsData = app.import_data(myLeague)
    fplPlayerData = app.consolidate_data(fplAvailabilityData, fplPlayerData, myTeam)

    df = pd.DataFrame.from_dict(fplPlayerData['elements'])
    projectionsData = app.clean_projections(projectionsData)
    df1 = df.merge(projectionsData[0], how='left', left_on=['web_name_clean', 'team_name', 'position_name'],
                   right_on=['Name', 'Team', 'Pos'], validate='1:1')

