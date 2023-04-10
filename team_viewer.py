import json

#Load JSON file.
with open("Modules\Environment\Teams.json", "r") as teams:
    data = json.load(teams)

for team_name in data.keys():
    print(team_name)
    for team in data[team_name]:
        print(team)