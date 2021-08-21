import pandas as pd
import requests


class ProjectionsData:
    """
    A class that contains projections data from Fantasy Football Scout.

    Attributes
    ----------
    username : str
        The username used to authenticate.
    password : str
        The password used to authenticate.
    seasonProjections : object
        The season projections data.
    sixGameProjections : object
        The six game projections data.

    Methods
    -------
    import_data()
        Returns the projections data from Fantasy Football Scout.
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.sixGameProjections, self.seasonProjections = self.import_data(self.username, self.password)
        self.align_six_game_projections_with_official()

    @staticmethod
    def import_data(username, password):
        """Imports data from draft.premierleague and fantasyfootballscout.

        Parameters
        ----------
        username : str
            The username used to authenticate.
        password : str
            The password used to authenticate.

        Raises
        ------
        requests.exceptions.HTTPError:
            If any HTTP errors are encountered when retrieving data.
        ValueError:
            If the projections cannot be parsed.

        """
        try:
            s1 = requests.session()
            s1.post('https://members.fantasyfootballscout.co.uk/',
                    data={'username': username, 'password': password, 'login': '>+Log+In'})
            r1 = s1.get('https://members.fantasyfootballscout.co.uk/projections/six-game-projections/')
            r2 = s1.get('https://members.fantasyfootballscout.co.uk/projections/season-projections/')
            r1.raise_for_status()
            r2.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        try:
            sixGameProjections = pd.read_html(r1.content)
            seasonProjections = pd.read_html(r2.content)
        except ValueError as err:
            # Todo: Figure out how to catch authentication failure when posting to the session instead.
            print("No data can be read from Fantasy Football Scout, please check your credentials.")
            raise SystemExit(err)

        return sixGameProjections, seasonProjections

    def align_six_game_projections_with_official(self):
        """Align team names and player names from projectionsData.sixGameProjections to OfficialAPIData.players.

        Parameters
        ----------

        Raises
        ------

        """
        self.sixGameProjections[0]['Team'].loc[
            self.sixGameProjections[0]['Team'] == 'BRI'] = 'BHA'
        self.sixGameProjections[0]['Team'].loc[
            self.sixGameProjections[0]['Team'] == 'SOT'] = 'SOU'
        self.sixGameProjections[0]['Team'].loc[
            self.sixGameProjections[0]['Team'] == 'WHM'] = 'WHU'
        self.sixGameProjections[0]['Pos'].loc[
            self.sixGameProjections[0]['Pos'] == 'GK'] = 'GKP'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Buend<ed>a')] = 'Buendia'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Femenia') &
            self.sixGameProjections[0]['Team'].str.contains('WAT')] = 'Kiko Femenia'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Gomes') &
            self.sixGameProjections[0]['Team'].str.contains('EVE')] = 'Andre Gomes'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Sanchez') &
            self.sixGameProjections[0]['Team'].str.contains('WHU')] = 'Carlos Sanchez'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Rodriguez') &
            self.sixGameProjections[0]['Team'].str.contains('EVE')] = 'James'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Rodri') &
            self.sixGameProjections[0]['Team'].str.contains('MCI')] = 'Rodrigo'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Kiko Femenia') &
            self.sixGameProjections[0]['Team'].str.contains('WAT')] = 'Femenia'
        return
