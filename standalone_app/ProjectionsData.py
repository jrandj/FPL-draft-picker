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
            self.sixGameProjections[0]['Name'].str.contains('Estupi') &
            self.sixGameProjections[0]['Team'].str.contains('BHA')] = 'Estupinan'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Ferguson \(Evan\)') &
            self.sixGameProjections[0]['Team'].str.contains('BHA')] = 'Ferguson'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Gomes') &
            self.sixGameProjections[0]['Team'].str.contains('EVE')] = 'Andre Gomes'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Jaku') &
            self.sixGameProjections[0]['Pos'].str.contains('GKP') &
            self.sixGameProjections[0]['Team'].str.contains('EVE')] = 'Jakupovic'
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
            self.sixGameProjections[0]['Name'].str.contains('Traore \(Adama\)') &
            self.sixGameProjections[0]['Pos'].str.contains('MID') &
            self.sixGameProjections[0]['Team'].str.contains('WOL')] = 'Adama'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Traore \(Boubacar\)') &
            self.sixGameProjections[0]['Pos'].str.contains('MID') &
            self.sixGameProjections[0]['Team'].str.contains('WOL')] = 'Traore'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('C.Douco')] = 'C.Doucoure'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Martínez')] = 'Martinez'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Dennis \(Emmanuel\)') &
            self.sixGameProjections[0]['Team'].str.contains('NFO')] = 'Dennis'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Bad') &
            self.sixGameProjections[0]['Pos'].str.contains('DEF') &
            self.sixGameProjections[0]['Team'].str.contains('NFO')] = 'Bade'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Caf') &
            self.sixGameProjections[0]['Team'].str.contains('NFO')] = 'Cafu'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('White \(Ben\)') &
            self.sixGameProjections[0]['Team'].str.contains('ARS')] = 'White'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Smith \(Matthew\)') &
            self.sixGameProjections[0]['Team'].str.contains('ARS')] = 'Smith'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Chambers \(Calum\)') &
            self.sixGameProjections[0]['Team'].str.contains('AVL')] = 'Chambers'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Neto \(Murara\)') &
            self.sixGameProjections[0]['Team'].str.contains('BOU')] = 'Neto'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Smith \(Adam\)') &
            self.sixGameProjections[0]['Team'].str.contains('BOU')] = 'Smith'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Cook \(Lewis\)') &
            self.sixGameProjections[0]['Team'].str.contains('BOU')] = 'Cook'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Sanchez \(Robert\)') &
            self.sixGameProjections[0]['Team'].str.contains('BHA')] = 'Sanchez'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Chalobah \(Trevoh\)') &
            self.sixGameProjections[0]['Team'].str.contains('CHE')] = 'Chalobah'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('James \(Reece\)') &
            self.sixGameProjections[0]['Team'].str.contains('CHE')] = 'James'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Mendy \(Edouard\)') &
            self.sixGameProjections[0]['Team'].str.contains('CHE')] = 'Mendy'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Richards \(Chris\)') &
            self.sixGameProjections[0]['Team'].str.contains('CRY')] = 'Richards'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Phillips \(Killian\)') &
            self.sixGameProjections[0]['Team'].str.contains('CRY')] = 'Phillips'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Ward \(Joel\)') &
            self.sixGameProjections[0]['Team'].str.contains('CRY')] = 'Ward'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Ayew \(Jordan\)') &
            self.sixGameProjections[0]['Team'].str.contains('CRY')] = 'Ayew'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Ferguson \(Nathan\)') &
            self.sixGameProjections[0]['Team'].str.contains('CRY')] = 'Ferguson'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('JakupoviÄ‡') &
            self.sixGameProjections[0]['Team'].str.contains('EVE')] = 'Jakupovic'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Gray \(Demarai\)') &
            self.sixGameProjections[0]['Team'].str.contains('EVE')] = 'Gray'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Vin') &
            self.sixGameProjections[0]['Pos'].str.contains('FWD') &
            self.sixGameProjections[0]['Team'].str.contains('FUL')] = 'Vinicius'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Chalobah \(Nathaniel\)') &
            self.sixGameProjections[0]['Team'].str.contains('FUL')] = 'Chalobah'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Wilson \(Harry\)') &
            self.sixGameProjections[0]['Team'].str.contains('FUL')] = 'Wilson'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('James \(Daniel\)') &
            self.sixGameProjections[0]['Team'].str.contains('FUL')] = 'James'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Ward \(Danny\)') &
            self.sixGameProjections[0]['Team'].str.contains('LEI')] = 'Ward'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Mendy \(Nampalys\)') &
            self.sixGameProjections[0]['Team'].str.contains('LEI')] = 'Mendy'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Henderson \(Jordan\)') &
            self.sixGameProjections[0]['Team'].str.contains('LIV')] = 'Henderson'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Jones \(Curtis\)') &
            self.sixGameProjections[0]['Team'].str.contains('LIV')] = 'Jones'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Williams \(Neco\)') &
            self.sixGameProjections[0]['Team'].str.contains('NFO')] = 'N.Williams'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Rico \(Lewis\)') &
            self.sixGameProjections[0]['Team'].str.contains('MCI')] = 'Lewis'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Sergio') &
            self.sixGameProjections[0]['Pos'].str.contains('DEF') &
            self.sixGameProjections[0]['Team'].str.contains('MCI')] = 'Sergio Gomez'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Phillips \(Kalvin\)') &
            self.sixGameProjections[0]['Team'].str.contains('MCI')] = 'Phillips'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Williams \(Brandon\)') &
            self.sixGameProjections[0]['Team'].str.contains('MUN')] = 'B.Williams'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Wilson \(Callum\)') &
            self.sixGameProjections[0]['Team'].str.contains('NEW')] = 'Wilson'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Longstaff \(Sean\)') &
            self.sixGameProjections[0]['Team'].str.contains('NEW')] = 'S.Longstaff'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Lewis \(Jamal\)') &
            self.sixGameProjections[0]['Team'].str.contains('NEW')] = 'Lewis'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Cook \(Steve\)') &
            self.sixGameProjections[0]['Team'].str.contains('NFO')] = 'Cook'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Johnson \(Brennan\)') &
            self.sixGameProjections[0]['Team'].str.contains('NFO')] = 'Johnson'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Henderson \(Dean\)') &
            self.sixGameProjections[0]['Team'].str.contains('NFO')] = 'Henderson'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Armstrong \(Stuart\)') &
            self.sixGameProjections[0]['Team'].str.contains('SOU')] = 'S.Armstrong'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Armstrong \(Adam\)') &
            self.sixGameProjections[0]['Team'].str.contains('SOU')] = 'A.Armstrong'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Adams \(Che\)') &
            self.sixGameProjections[0]['Team'].str.contains('SOU')] = 'Adams'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Davies \(Ben\)') &
            self.sixGameProjections[0]['Team'].str.contains('TOT')] = 'Davies'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Sanchez \(Davinson\)') &
            self.sixGameProjections[0]['Team'].str.contains('TOT')] = 'Sanchez'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Sessegnon \(Ryan\)') &
            self.sixGameProjections[0]['Team'].str.contains('TOT')] = 'R.Sessegnon'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('White \(Harvey\)') &
            self.sixGameProjections[0]['Team'].str.contains('TOT')] = 'White'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Johnson \(Ben\)') &
            self.sixGameProjections[0]['Team'].str.contains('WHU')] = 'Johnson'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Lucas Paqueta') &
            self.sixGameProjections[0]['Team'].str.contains('WHU')] = 'Paqueta'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Neto \(Pedro\)') &
            self.sixGameProjections[0]['Team'].str.contains('WOL')] = 'Neto'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Smith \(Jackson\)') &
            self.sixGameProjections[0]['Team'].str.contains('WOL')] = 'Smith'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Kalaj') &
            self.sixGameProjections[0]['Pos'].str.contains('FWD') &
            self.sixGameProjections[0]['Team'].str.contains('WOL')] = 'Kalajdžic'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Chambers \(Luke\)') &
            self.sixGameProjections[0]['Team'].str.contains('LIV')] = 'Chambers'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Davies \(Harvey\)') &
            self.sixGameProjections[0]['Team'].str.contains('LIV')] = 'H.Davies'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Phillips \(Nathaniel\)') &
            self.sixGameProjections[0]['Team'].str.contains('LIV')] = 'Phillips'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Gray \(Archie\)') &
            self.sixGameProjections[0]['Team'].str.contains('LEE')] = 'Gray'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Adams \(Tyler\)') &
            self.sixGameProjections[0]['Team'].str.contains('LEE')] = 'Adams'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Richards \(Omar\)') &
            self.sixGameProjections[0]['Team'].str.contains('NFO')] = 'Richards'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Doucoure \(Cheick\)') &
            self.sixGameProjections[0]['Team'].str.contains('CRY')] = 'C.Doucoure'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Richards \(Chris\)') &
            self.sixGameProjections[0]['Team'].str.contains('CRY')] = 'Richards'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('João Félix')] = 'Joao Felix'
        self.sixGameProjections[0]['Name'].loc[
            self.sixGameProjections[0]['Name'].str.contains('Wöber')] = 'Wober'
        return
