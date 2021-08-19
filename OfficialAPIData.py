import requests


class OfficialAPIData:
    """
    A class used to represent a Result.

    Attributes
    ----------
    leagueID : sequence
        The unique identifier for the league.
    players : object
        The player data.
    playerAvailability : object
        The player availability data.
    league : object
        The league data.

    Methods
    -------
    import_data()
        Returns the performance results in a dictionary.
    """
    def __init__(self, leagueID):
        self.leagueID = leagueID
        self.players, self.playerAvailability, self.league = self.import_data(leagueID)

    @staticmethod
    def import_data(leagueID):
        """Imports data from the official draft.premierleague APIs.

        Parameters
        ----------
        leagueID : sequence
            The unique identifier for the league.

        Raises
        ------
        requests.exceptions.HTTPError:
            If any HTTP errors are encountered when retrieving data.

        """

        try:
            r1 = requests.get(url='https://draft.premierleague.com/api/bootstrap-static')
            r1.raise_for_status()
            players = r1.json()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        try:
            r2 = requests.get(url="https://draft.premierleague.com/api/league/" + str(leagueID) + "/element-status")
            r2.raise_for_status()
            playerAvailability = r2.json()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        try:
            r3 = requests.get(url="https://draft.premierleague.com/api/league/" + str(leagueID) + "/details")
            r3.raise_for_status()
            league = r3.json()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        return players, playerAvailability, league
