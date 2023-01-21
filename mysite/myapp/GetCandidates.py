import pandas as pd
import os

from .Team import Team
from .ConsolidatedData import ConsolidatedData

pd.options.mode.chained_assignment = None

class GetCandidates:
    def __init__(self, leagueID, teamName):
        self.fantasyFootballScoutUsername = os.getenv('PROJECTIONS_USERNAME')
        self.fantasyFootballScoutPassword = os.getenv('PROJECTIONS_PASSWORD')
        self.teamName = teamName
        self.leagueID = leagueID
        self.consolidatedData = ConsolidatedData(self.fantasyFootballScoutUsername, self.fantasyFootballScoutPassword,
                                                 self.teamName, self.leagueID)
        self.team = Team(self.teamName, self.consolidatedData.teamID, self.consolidatedData)
        print("DONE")
