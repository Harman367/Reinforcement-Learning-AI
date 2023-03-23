#Imports
import json
import random

with open('Modules\Environment\Pokemon.json', 'r') as data:
    #Source: "https://github.com/Honko/pokemon-team-generator/blob/master/js/data/smogon-sets/dpp_ou.js",
    data = json.load(data)

#for pokemon in data:
#    print(data[pokemon])

#print(data['Abomasnow'][0])

#for key in random.choice(data['Abomasnow']):
#    if key in ["moves", "item", "ability", "nature"]:
#        print(key)

print(random.choice(data['Abomasnow'][0]["moves"])[0])
print(len(data))