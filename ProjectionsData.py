import pandas as pd
import requests


class ProjectionsData:
    """
    A class that contains projections data from Fantasy Football Scout.

    Attributes
    ----------
    fantasyFootballScoutUsername : str
        The username used to authenticate.
    fantasyFootballScoutPassword : str
        The password used to authenticate.
    sixGameProjections : object
        The season projections data.
    seasonProjections : object
        The six game projections data.

    Methods
    -------
    import_data()
        Import projections data from Fantasy Football Scout.
    align_six_game_projections_with_official()
        Align team names and player names from projectionsData.sixGameProjections to OfficialAPIData.players.
    """

    def __init__(self, fantasyFootballScoutUsername, fantasyFootballScoutPassword):
        self.fantasyFootballScoutUsername = fantasyFootballScoutUsername
        self.fantasyFootballScoutPassword = fantasyFootballScoutPassword
        self.sixGameProjections, self.seasonProjections = self.import_data(self.fantasyFootballScoutUsername,
                                                                           self.fantasyFootballScoutPassword)
        self.align_six_game_projections_with_official()

    @staticmethod
    def import_data(fantasyFootballScoutUsername, fantasyFootballScoutPassword):
        """Import projections data from Fantasy Football Scout.

        Parameters
        ----------
        fantasyFootballScoutUsername : str
            The username used to authenticate.
        fantasyFootballScoutPassword : str
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
                    data={'username': fantasyFootballScoutUsername, 'password': fantasyFootballScoutPassword,
                          'login': '>+Log+In'})
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
        """Align team names and player names from projectionsData.sixGameProjections to OfficialAPIData.players. The
        team name acronyms and other data details do not always align.

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
        self.sixGameProjections[0]['Team'].loc[
            self.sixGameProjections[0]['Team'] == 'NOT'] = 'NFO'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Peri')
            & self.sixGameProjections[0]['Team'].str.contains('TOT')
            & self.sixGameProjections[0]['Pos'].str.contains('DEF')] = 'Perisic'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Gomes') &
            self.sixGameProjections[0]['Team'].str.contains('EVE')] = 'Andre Gomes'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Mari') &
            self.sixGameProjections[0]['Team'].str.contains('ARS')] = 'Pablo Mari'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Doucoure') &
            self.sixGameProjections[0]['Team'].str.contains('EVE')] = 'A.Doucoure'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Jacob Ramsey') &
            self.sixGameProjections[0]['Team'].str.contains('AVL')] = 'Ramsey'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Sorensen') &
            self.sixGameProjections[0]['Team'].str.contains('BRE')] = 'Bech'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Traore') &
            self.sixGameProjections[0]['Team'].str.contains('WOL')] = 'Adama'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('C.DoucourÃ©')] = 'C.Doucoure'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('MartÃ­nez')] = 'Martinez'
        return
