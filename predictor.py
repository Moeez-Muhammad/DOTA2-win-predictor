import opendota
import json
from joblib import load

api = opendota.API()
api.get_heroes()
api.generate_hero_ids_dict()
api.generate_hero_dict()

#random_forest = load()
dire = []
radiant = []

print("Enter Radiant Team: ")
while len(radiant) != 5:
	hero = input(str(len(radiant) + 1) + ": ")
	if hero not in api.heroes_dict:
		print("Invalid hero")
		continue
	if hero not in radiant and hero not in dire:
		radiant.append(hero)
	else:
		print("NO duplicate heroes")
		continue
print(radiant)

print("Enter Dire team: ")
while len(dire) != 5:
	hero = input(str(len(dire) + 1) + ": ")
	if hero not in api.heroes_dict:
		print("Invalid hero!")
		continue
	if hero not in dire and hero not in radiant:
		dire.append(hero)
	else:
		print("No duplicate heroes")
		continue
print(dire)
