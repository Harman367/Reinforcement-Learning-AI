#Imports
import numpy as np
from poke_env.teambuilder import Teambuilder
import json
import random

#Class to build Pokemon Teams.
class Team_Builder(Teambuilder):

    #Constructor
    def __init__(self, team):
        self.team = self.join_team(self.parse_showdown_team(team))

    #Method to yield team.
    def yield_team(self):
        return self.team

#Method to format JSON.
def format_JSON():
    with open('Modules\Environment\Pokemon.json', 'r') as data:
        #Source: "https://github.com/Honko/pokemon-team-generator/blob/master/js/data/smogon-sets/dpp_ou.js",
        data = json.load(data)

    #Get random team.
    team = random.sample(list(data), 6)

    #Create empty lists.
    team_1 = []
    team_2 = []
    
    #Loop through team.
    for pokemon in team:
        #print("\n" + pokemon)
        name = pokemon

        #Get random build from list of builds.
        build = random.choice(data[pokemon])

        #Get random moves from list of moves.
        moves = []
        for move in build["moves"]:
            #Check if move is a list.
            if len(move) != 1:
                m = random.choice(move)

                #Check if move is Hidden Power.
                if "Hidden Power" in str(m):
                    m = "Hidden Power"

                
                moves.append(m)
                #print(m)
            else:
                #Check if move is Hidden Power.
                if "Hidden Power" in str(move[0]):
                    move[0] = "Hidden Power"
                moves.append(move[0])
                #print(move[0])

        #Get random item from list of items.
        item = random.choice(build["item"])
        #print(item)
        
        #Get random ability from list of abilities.
        ability = random.choice(build["ability"])
        #print(ability)

        #Get random nature from list of natures.
        nature = random.choice(build["nature"])
        #print(nature)

        #Get random EVs from list of EVs.
        evs = build["evs"]
        #print(evs)

        #Format EVs.
        ev = ""
        for key, val in evs.items():
            ev += str(val) + " " + key + " / "
        ev = ev[:-3]
        
        #Format Pokemon.
        pokemon_build = f"""
{name} @ {item}
Ability: {ability}
EVs: {ev}
{nature} Nature
- {moves[0]}
- {moves[1]}
- {moves[2]}
- {moves[3]}
"""
        #Add Pokemon to team.
        team_1.append(pokemon_build)

    #Copy and shuffle team.
    team_2 = team_1.copy()
    random.shuffle(team_2)

    #Create JSON file.
    teams = {
        "team_1": team_1,
        "team_2": team_2
    }
    teams_json = json.dumps(teams)

    #Write to JSON file.
    with open("Modules\Environment\Teams.json", "w") as outfile:
        outfile.write(teams_json)

    #print(t1)
    #print(t2)

    return join_pokemon(team_1, team_2)

#Method to load team.
def load_team():
    #Load JSON file.
    with open("Modules\Environment\Teams.json", "r") as infile:
        data = json.load(infile)

    #Shuffle teams.
    random.shuffle(data["team_1"])
    random.shuffle(data["team_2"])

    return join_pokemon(data["team_1"], data["team_2"])

#Method to join Pokemon.
def join_pokemon(team1, team2):
    #Join Pokemon.
    t1, t2 = "", ""
    for x, y in zip(team1, team2):
        t1 += x
        t2 += y

    return t1, t2