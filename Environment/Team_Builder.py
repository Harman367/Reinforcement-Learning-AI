#Imports
import numpy as np
from poke_env.teambuilder import Teambuilder

#Class to build Pokemon Teams.
class Team_Builder(Teambuilder):
    def __init__(self, teams):
        self.teams = [self.join_team(self.parse_showdown_team(team)) for team in teams]

    def yield_team(self):
        return np.random.choice(self.teams)