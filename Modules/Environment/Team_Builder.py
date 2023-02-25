#Imports
import numpy as np
from poke_env.teambuilder import Teambuilder
import json
import random

#Class to build Pokemon Teams.
class Team_Builder(Teambuilder):

    #Constructor
    def __init__(self, teams):
        self.teams = [self.join_team(self.parse_showdown_team(team)) for team in teams]


    def yield_team(self):
        return np.random.choice(self.teams)

    #Method to format JSON.
    def format_JSON():
        with open('Pokemon.json', 'r') as data:
            #Source: "https://github.com/Honko/pokemon-team-generator/blob/master/js/data/smogon-sets/dpp_ou.js",
            data = json.load(data)

        print(list(data)[0])