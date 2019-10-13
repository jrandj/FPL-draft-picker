from app import app


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


test_selected_players()
test_web_name_clean()


