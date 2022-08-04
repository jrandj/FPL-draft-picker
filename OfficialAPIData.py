import requests


class OfficialAPIData:
    """
    A class that contains data from the official API.

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
        Import Official API data.
    add_availability_to_players()
        Augment player data with information from playerAvailability.
    id_to_entry_id():
        Gets the entry ID from the entity ID.
    id_to_entry_name():
        Gets the entry name from the entity ID.
    """

    def __init__(self, leagueID):
        self.leagueID = leagueID
        self.players, self.playerAvailability, self.league = self.import_data(leagueID)
        self.add_availability_to_players()

    @staticmethod
    def import_data(leagueID):
        """Import Official API data.

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

    def add_availability_to_players(self):
        """Augment player data with information from playerAvailability.

        Parameters
        ----------

        Raises
        ------

        """
        for i in range(len(self.players['elements'])):
            self.players['elements'][i]['web_name_clean'] = self.players['elements'][i]['web_name'].translate(
                str.maketrans({'í': 'i', 'ï': 'i', 'ß': 'ss', 'á': 'a', 'ä': 'a', 'é': 'e', 'ñ': 'n',
                               'ć': 'c', 'š': 's', 'Ö': 'O', 'Ø': 'O', 'ø': 'o', 'ö': 'o', 'ó': 'o', 'ü': 'u',
                               'ç': 'c', 'ú': 'u', 'Ü': 'U', 'ş': 's', 'ğ': 'g', 'ã': 'a', 'Ñ': 'N', 'Š': 'S',
                               'ł': 'l', 'Á': 'A'}))
            self.players['elements'][i]['selected'] = 'No'
            self.players['elements'][i]['available'] = 'No'

            for j in self.players['teams']:
                if self.players['elements'][i]['team'] == j['id']:
                    self.players['elements'][i]['team_name'] = j['short_name']

            for j in self.players['element_types']:
                if self.players['elements'][i]['element_type'] == j['id']:
                    self.players['elements'][i]['position_name'] = j['singular_name_short']

            for j in self.playerAvailability['element_status']:
                if self.players['elements'][i]['id'] == j['element']:
                    if j['owner'] is not None:
                        self.players['elements'][i]['selected'] = j['owner']
                    if self.players['elements'][i]['status'] != 'u' and j['owner'] is None:
                        self.players['elements'][i]['available'] = 'Yes'
        return

    def id_to_entry_id(self, pid):
        """Gets the entry ID from the entity ID.

        Parameters
        ----------
        pid : int
            The entity id.

        Raises
        ------
        SystemExit:
            If the entry ID cannot be found for the entity ID.
        """
        for entry in self.league['league_entries']:
            if entry['id'] == pid:
                entity_id = entry['entry_id']
                return entity_id
        print("No entry_id found for ID: " + pid + " in league.")
        raise SystemExit()

    def id_to_entry_name(self, pid):
        """Gets the entry name from the entity ID.

        Parameters
        ----------
        pid : int
            The entity ID.

        Raises
        ------
        SystemExit:
            If the entry name cannot be found for the entity ID.
        """
        for entry in self.league['league_entries']:
            if entry['id'] == pid:
                entry_name = entry['entry_name']
                return entry_name
        print("No entry_name found for ID: " + pid + " in league.")
        raise SystemExit()
