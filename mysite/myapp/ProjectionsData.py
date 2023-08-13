class ProjectionsData:
    """
    A class that contains projections data from Fantasy Football Scout.

    Attributes
    ----------
    fantasyFootballScoutUsername : str
        The username used to authenticate.
    fantasyFootballScoutPassword : str
        The password used to authenticate.
    sixGameProjections : list
        The season projections data.
    seasonProjections : list
        The six game projections data.

    Methods
    -------
    align_six_game_projections_with_official()
        Align team names and player names from projectionsData.sixGameProjections to OfficialAPIData.players.
    """

    def __init__(self, API_results):
        self.sixGameProjections = API_results[0]
        self.seasonProjections = API_results[1]
        self.align_six_game_projections_with_official()

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
            self.sixGameProjections[0]['Team'] == 'WHM'] = 'WHU'
        self.sixGameProjections[0]['Pos'].loc[
            self.sixGameProjections[0]['Pos'] == 'GK'] = 'GKP'
        self.sixGameProjections[0]['Team'].loc[
            self.sixGameProjections[0]['Team'] == 'NOT'] = 'NFO'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('White')
            & self.sixGameProjections[0]['Team'].str.contains('ARS')
            & self.sixGameProjections[0]['Pos'].str.contains('DEF')] = 'White'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Chambers')
            & self.sixGameProjections[0]['Team'].str.contains('ARS')
            & self.sixGameProjections[0]['Pos'].str.contains('DEF')] = 'Chambers'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Jacob Ramsey')
            & self.sixGameProjections[0]['Team'].str.contains('AVL')
            & self.sixGameProjections[0]['Pos'].str.contains('MID')] = 'J.Ramsey'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Smith')
            & self.sixGameProjections[0]['Team'].str.contains('BOU')
            & self.sixGameProjections[0]['Pos'].str.contains('DEF')] = 'Smith'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('James')
            & self.sixGameProjections[0]['Team'].str.contains('CHE')
            & self.sixGameProjections[0]['Pos'].str.contains('DEF')] = 'James'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Ayew')
            & self.sixGameProjections[0]['Team'].str.contains('CRY')
            & self.sixGameProjections[0]['Pos'].str.contains('MID')] = 'J.Ayew'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Richards')
            & self.sixGameProjections[0]['Team'].str.contains('CRY')
            & self.sixGameProjections[0]['Pos'].str.contains('DEF')] = 'C.Richards'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Ward')
            & self.sixGameProjections[0]['Team'].str.contains('CRY')
            & self.sixGameProjections[0]['Pos'].str.contains('DEF')] = 'Ward'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Doucoure')
            & self.sixGameProjections[0]['Team'].str.contains('EVE')
            & self.sixGameProjections[0]['Pos'].str.contains('MID')] = 'A.Doucoure'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Gray')
            & self.sixGameProjections[0]['Team'].str.contains('EVE')
            & self.sixGameProjections[0]['Pos'].str.contains('MID')] = 'Gray'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Wilson')
            & self.sixGameProjections[0]['Team'].str.contains('FUL')
            & self.sixGameProjections[0]['Pos'].str.contains('MID')] = 'Wilson'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Jones')
            & self.sixGameProjections[0]['Team'].str.contains('LIV')
            & self.sixGameProjections[0]['Pos'].str.contains('MID')] = 'Jones'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Phillips')
            & self.sixGameProjections[0]['Team'].str.contains('LIV')
            & self.sixGameProjections[0]['Pos'].str.contains('MID')] = 'Phillips'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Alvarez')
            & self.sixGameProjections[0]['Team'].str.contains('MCI')
            & self.sixGameProjections[0]['Pos'].str.contains('FWD')] = 'J.Alvarez'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Lewis')
            & self.sixGameProjections[0]['Team'].str.contains('MCI')
            & self.sixGameProjections[0]['Pos'].str.contains('MID')] = 'R.Lewis'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Phillips')
            & self.sixGameProjections[0]['Team'].str.contains('MCI')
            & self.sixGameProjections[0]['Pos'].str.contains('MID')] = 'Phillips'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Williams')
            & self.sixGameProjections[0]['Team'].str.contains('MUN')
            & self.sixGameProjections[0]['Pos'].str.contains('DEF')] = 'B.Williams'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Bruno Guimaraes')
            & self.sixGameProjections[0]['Team'].str.contains('NEW')
            & self.sixGameProjections[0]['Pos'].str.contains('MID')] = 'Bruno G.'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Longstaff')
            & self.sixGameProjections[0]['Team'].str.contains('NEW')
            & self.sixGameProjections[0]['Pos'].str.contains('MID')] = 'Longstaff (Sean)'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Wilson')
            & self.sixGameProjections[0]['Team'].str.contains('NEW')
            & self.sixGameProjections[0]['Pos'].str.contains('FWD')] = 'Wilson'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Davies')
            & self.sixGameProjections[0]['Team'].str.contains('TOT')
            & self.sixGameProjections[0]['Pos'].str.contains('DEF')] = 'Davies'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Sanchez')
            & self.sixGameProjections[0]['Team'].str.contains('TOT')
            & self.sixGameProjections[0]['Pos'].str.contains('DEF')] = 'Sanchez'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Neto')
            & self.sixGameProjections[0]['Team'].str.contains('WOL')
            & self.sixGameProjections[0]['Pos'].str.contains('MID')] = 'Neto'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Chambers')
            & self.sixGameProjections[0]['Team'].str.contains('AVL')
            & self.sixGameProjections[0]['Pos'].str.contains('DEF')] = 'Chambers'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Traore')
            & self.sixGameProjections[0]['Team'].str.contains('AVL')
            & self.sixGameProjections[0]['Pos'].str.contains('MID')] = 'Bertrand Traore'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Cook')
            & self.sixGameProjections[0]['Team'].str.contains('BOU')
            & self.sixGameProjections[0]['Pos'].str.contains('MID')] = 'L.Cook'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Neto')
            & self.sixGameProjections[0]['Team'].str.contains('BOU')
            & self.sixGameProjections[0]['Pos'].str.contains('GKP')] = 'Neto'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Ferguson')
            & self.sixGameProjections[0]['Team'].str.contains('BHA')
            & self.sixGameProjections[0]['Pos'].str.contains('FWD')] = 'Ferguson'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Sanchez')
            & self.sixGameProjections[0]['Team'].str.contains('CHE')
            & self.sixGameProjections[0]['Pos'].str.contains('GKP')] = 'Sanchez'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Chalobah')
            & self.sixGameProjections[0]['Team'].str.contains('CHE')
            & self.sixGameProjections[0]['Pos'].str.contains('DEF')] = 'Chalobah'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Doucoure')
            & self.sixGameProjections[0]['Team'].str.contains('CRY')
            & self.sixGameProjections[0]['Pos'].str.contains('MID')] = 'C.Doucoure'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Virginia')
            & self.sixGameProjections[0]['Team'].str.contains('EVE')
            & self.sixGameProjections[0]['Pos'].str.contains('GKP')] = 'J.Virginia'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Phillips')
            & self.sixGameProjections[0]['Team'].str.contains('LIV')
            & self.sixGameProjections[0]['Pos'].str.contains('DEF')] = 'Phillips'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Lewis')
            & self.sixGameProjections[0]['Team'].str.contains('MCI')
            & self.sixGameProjections[0]['Pos'].str.contains('DEF')] = 'R.Lewis'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Henderson')
            & self.sixGameProjections[0]['Team'].str.contains('MUN')
            & self.sixGameProjections[0]['Pos'].str.contains('GKP')] = 'Henderson'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Longstaff')
            & self.sixGameProjections[0]['Team'].str.contains('NEW')
            & self.sixGameProjections[0]['Pos'].str.contains('MID')] = 'Longstaff'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Dennis')
            & self.sixGameProjections[0]['Team'].str.contains('NFO')
            & self.sixGameProjections[0]['Pos'].str.contains('FWD')] = 'Dennis'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Johnson')
            & self.sixGameProjections[0]['Team'].str.contains('NFO')
            & self.sixGameProjections[0]['Pos'].str.contains('MID')] = 'Johnson'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Richards')
            & self.sixGameProjections[0]['Team'].str.contains('NFO')
            & self.sixGameProjections[0]['Pos'].str.contains('DEF')] = 'O.Richards'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Williams')
            & self.sixGameProjections[0]['Team'].str.contains('NFO')
            & self.sixGameProjections[0]['Pos'].str.contains('DEF')] = 'Williams'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Sessegnon')
            & self.sixGameProjections[0]['Team'].str.contains('TOT')
            & self.sixGameProjections[0]['Pos'].str.contains('DEF')] = 'Sessegnon'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Johnson')
            & self.sixGameProjections[0]['Team'].str.contains('WHU')
            & self.sixGameProjections[0]['Pos'].str.contains('DEF')] = 'Johnson'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Lucas Paqueta')
            & self.sixGameProjections[0]['Team'].str.contains('WHU')
            & self.sixGameProjections[0]['Pos'].str.contains('MID')] = 'L.Paqueta'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Sa')
            & self.sixGameProjections[0]['Team'].str.contains('WOL')
            & self.sixGameProjections[0]['Pos'].str.contains('GKP')] = 'Jose Sa'
        return
