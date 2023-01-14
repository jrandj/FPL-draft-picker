import math
from collections import OrderedDict
from tabulate import tabulate


class Team:
    """
    A class that represents a team.

    Attributes
    ----------
    teamName : str
        The name of the team.
    teamID : str
        The unique identifier of the team.
    consolidatedData : object
        An instance of ConsolidatedData.
    playersInTeam : sequence
        A list of the players in the team.
    formations : sequence
        A list of the possible formations for the team and their projected points total in the next fixture.
    candidates_representation:
        A subset of players with six game projections added.
    formations_representation: str
        A representation of the formations of the team.

    Methods
    -------
    get_players_for_team()
        Return the players in the team.
    get_formations_for_team()
        Return team formations in descending order with the highest scoring at the top.
    add_player_to_formation
        Attempt to add a player to a formation.
    generate_candidates_representation():
        Generate a representation of the candidates.
    generate_formations_representation():
        Generate a representation of the formations of the team.
    """

    def __init__(self, teamName, teamID, consolidatedData):
        self.teamName = teamName
        self.teamID = teamID
        self.consolidatedData = consolidatedData
        self.playersInTeam = self.get_players_for_team(self.teamID, self.consolidatedData)
        self.formations = self.get_formations_for_team(self.playersInTeam, self.consolidatedData)
        self.candidates_representation = self.generate_candidates_representation()
        self.formations_representation = self.generate_formations_representation()

    @staticmethod
    def get_players_for_team(teamID, consolidatedData):
        """Return the players in the team.

        Parameters
        ----------
        teamID : str
            The unique identifier of the team.
        consolidatedData : object
            An instance of ConsolidatedData.

        Raises
        ------

        """
        team = []
        for i in range(len(consolidatedData.officialAPIData.players['elements'])):
            if consolidatedData.officialAPIData.players['elements'][i]['selected'] == teamID:
                team.append(consolidatedData.officialAPIData.players['elements'][i])
        return team

    @staticmethod
    def get_formations_for_team(playersInTeam, consolidatedData):
        """Return team formations in descending order with the highest scoring at the top.

        Parameters
        ----------
        playersInTeam : sequence
            A list of the players in the team.
        consolidatedData : object
            An instance of ConsolidatedData.

        Raises
        ------

        """
        formations = [{'GKP': 1, 'DEF': 5, 'MID': 3, 'FWD': 2, 'Score': 0},
                      {'GKP': 1, 'DEF': 5, 'MID': 4, 'FWD': 1, 'Score': 0},
                      # {'GKP': 1, 'DEF': 5, 'MID': 2, 'FWD': 3, 'Score': 0},
                      {'GKP': 1, 'DEF': 4, 'MID': 3, 'FWD': 3, 'Score': 0},
                      {'GKP': 1, 'DEF': 4, 'MID': 5, 'FWD': 1, 'Score': 0},
                      {'GKP': 1, 'DEF': 4, 'MID': 4, 'FWD': 2, 'Score': 0},
                      {'GKP': 1, 'DEF': 3, 'MID': 5, 'FWD': 2, 'Score': 0},
                      {'GKP': 1, 'DEF': 3, 'MID': 4, 'FWD': 3, 'Score': 0}]
        player_index = 0
        total_points = 0
        current_formation = {'GKP': 0, 'DEF': 0, 'MID': 0, 'FWD': 0}
        nextGameWeek = consolidatedData.nextGameWeek
        playersInTeam.sort(key=lambda x: (x['position_name'], -x[nextGameWeek]))
        for formation in formations:
            team_copy = playersInTeam.copy()
            while current_formation != formation and len(team_copy) > player_index:
                current_player = team_copy[player_index]
                # This approach assumes the team is sorted by projected points in the next game week
                if Team.add_player_to_formation(current_player, current_formation, formation):
                    total_points += current_player[nextGameWeek]
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

    @staticmethod
    def add_player_to_formation(current_player, current_formation, formation):
        """Attempt to add a player to a formation.

        Parameters
        ----------
        current_player : dict
            The proposed player.
        current_formation : dict
            The current formation.
        formation : dict
            The current formation for which the player is proposed.

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

    def generate_candidates_representation(self):
        """Generate a representation of the candidates.

        Parameters
        ----------

        Raises
        ------

        """
        printListPoints = []
        printListIctIndex = []
        sixGameProjectionHeader = self.consolidatedData.projectionsData.sixGameProjections[0].columns.values[-2]
        nextGameWeekHeader = self.consolidatedData.nextGameWeek

        for i in self.playersInTeam:
            printDictPoints = OrderedDict((k, i[k]) for k in (
                'web_name', 'team_name', 'position_name', sixGameProjectionHeader, nextGameWeekHeader,
                str(sixGameProjectionHeader + ' Candidates'),
                str(nextGameWeekHeader + ' Pts Candidates')))
            printListPoints.append(printDictPoints)
            printDictIctIndex = OrderedDict(
                (k, i[k]) for k in ('web_name', 'team_name', 'position_name', 'ict_index', 'ict_index_candidates'))
            printListIctIndex.append(printDictIctIndex)

        sortedPrintListPoints = sorted(printListPoints, key=lambda x: (x['position_name'], -x[sixGameProjectionHeader]))
        sortedPrintListIctIndex = sorted(printListIctIndex, key=lambda x: (x['position_name'], -float(x['ict_index'])))
        # print(tabulate(sortedPrintListPoints, headers="keys", tablefmt="github"))
        # print(tabulate(sortedPrintListIctIndex, headers="keys", tablefmt="github"))

        expected_results = [i for i in self.consolidatedData.officialAPIData.players['elements'] if i['status'] != 'u']
        failed_merge = [i for i in self.consolidatedData.officialAPIData.players['elements'] if
                        i['merge_status_six_game'] != 'both' and i['status'] != 'u']
        no_projections = [i for i in self.consolidatedData.officialAPIData.players['elements'] if
                          math.isnan(i[sixGameProjectionHeader]) and i['status'] != 'u' and i[
                              'merge_status_six_game'] == 'both']
        failed_merge_player_info = [
            [i["web_name_clean"], i["team_name"], i["position_name"], i["merge_status_six_game"]]
            for i in failed_merge]
        no_projections_player_info = [
            [i["web_name_clean"], i["team_name"], i["position_name"], i["merge_status_six_game"]]
            for i in no_projections]

        candidates_representation = str(
            tabulate(sortedPrintListPoints, headers="keys", tablefmt="html", stralign="left", numalign="left",
                     colalign="left") + "<br>" +
            tabulate(sortedPrintListIctIndex, headers="keys", tablefmt="html", stralign="left", numalign="left",
                     colalign="left") +
            "<br>" + str(len(expected_results))
            + " active players from the Official Fantasy Premier League API have been matched to "
            + str(len(expected_results) - len(failed_merge) - len(no_projections))
            + " Fantasy Football Scout six game projections."
            + "<br>" + "The following merge failures occurred between the official Fantasy Premier League API and "
                       "the Fantasy Football Scout six game projections: "
            + str(failed_merge_player_info)
            + "<br> The following players were matched but have an invalid Fantasy Football Scout six game projection: "
            + str(no_projections_player_info)) + "<br>"

        return candidates_representation

    def generate_formations_representation(self):
        """Generate a representation of the formations of the team.

        Parameters
        ----------

        Raises
        ------

        """
        formations_representation = "Formations and their scores: " + str(
            sorted(self.formations, key=lambda x: (x['Score']), reverse=True)) + "<br>"
        return formations_representation
