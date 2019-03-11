import opendota
import json

api = opendota.API()
api.get_heroes()
api.generate_hero_ids_dict()
api.generate_hero_dict()

hero1 = input("Hero please: ")
hero1_id = api.heroes_dict[hero1]
hero1_zeroid = api.hero_ids_dict[hero1_id]
print(hero1_zeroid)
