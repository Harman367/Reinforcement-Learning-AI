#Imports
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
    
#Method to create random teams
def create_random_teams(number_of_teams, file_name):
    #Load JSON file.
    with open('Modules\Environment\Pokemon.json', 'r') as data:
        #Source: "https://github.com/Honko/pokemon-team-generator/blob/master/js/data/smogon-sets/dpp_ou.js",
        data = json.load(data)

    teams = []

    #Loop through number of teams.
    for i in range(number_of_teams):
        #Get random team.
        team = random.sample(list(data), 6)

        #Add team to list.
        teams.append(build_team(team, data))

        #Create JSON file.
        teams_json = {}

        #Add teams to JSON file.
        for i, team in enumerate(teams):
            teams_json[f"team_{i+1}"] = team

        teams_json = json.dumps(teams_json)

        #Write to JSON file.
        with open(f"Modules\Environment\{file_name}.json", "w") as outfile:
            outfile.write(teams_json)

#Method to load team.
def load_team(file_name):
    #Load JSON file.
    with open(f"Modules\Environment\{file_name}", "r") as infile:
        data = json.load(infile)

    #Teams
    teams = []

    #Shuffle teams.
    for key in data.keys():
        #Shuffle Pokemon.
        random.shuffle(data[key])

        team = ""

        #Loop through team and join Pokemon.
        for x in data[key]:
            team += x

        teams.append(team)

    return teams

#Method to build a team.
def build_team(team, data):
    built_team = []

    #Loop through team.
    for pokemon in team:
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

                #Check if move is already in list.
                if m in moves:
                    m = random.choice(move)

                    if "Hidden Power" in str(m):
                        m = "Hidden Power"

                moves.append(m)

            else:
                #Check if move is Hidden Power.
                if "Hidden Power" in str(move[0]):
                    move[0] = "Hidden Power"
                moves.append(move[0])

        #Get random item from list of items.
        item = random.choice(build["item"])
        
        #Get random ability from list of abilities.
        ability = random.choice(build["ability"])

        #Get random nature from list of natures.
        nature = random.choice(build["nature"])

        #Get random EVs from list of EVs.
        evs = build["evs"]

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

        built_team.append(pokemon_build)

    return built_team