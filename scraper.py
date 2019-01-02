import json
import dota2api

radiant_team_slots = [0, 1, 2, 3, 4]
dire_team_slots = [128, 129, 130, 131, 132]
api = None

def initialise():
	with open('apikey', 'r') as apikey_file:
		apikey = str(apikey_file.read())
	global api
	api = dota2api.Initialise(apikey)

def get_raw_data(matches_requested):
	match_ids = []
	rawMatches = api.get_match_history(game_mode=22, matches_requested=matches_requested)["matches"] # Collective list of all matches to be used
	for match in rawMatches:
		match_ids.append(match["match_id"])
	return match_ids
def get_hero_ids():
	rawHeroes = api.get_heroes()
	heroes = {}
	heroes["count"] = rawHeroes["count"]
	for i in range(len(rawHeroes["heroes"])):
		heroes[rawHeroes["heroes"][i]["id"]] = i
	print(heroes)
	return heroes
def parse_data(match_ids, heroes):
	f = open('log', 'a+')
	matchcounter = 0
	count = heroes["count"]
	rawMatches = []
	matches = []
	results = []

	for match_id in match_ids:
		rawMatches.append(api.get_match_details(match_id=match_id))

	for match in rawMatches:
		print("Parsing match {0}".format(matchcounter), file=f)
		newMatch = [0]*(2*count)
		newResult = 0
		radiantTeam = 0
		direTeam = 0
		zeroheroids = False
		players = match["players"]
		for player in players:
			print("Hero ID is {0}".format(player["hero_id"]), file=f)
			if player["hero_id"] == 0:
				print("Continuing", file=f)
				zeroheroids = True
				break
			heroindex = int(heroes[player["hero_id"]])
			print("Hero Index is {0}".format(heroindex), file=f)
			
			if player["player_slot"] in radiant_team_slots:
				print("Putting hero id {0}, with hero index of {1}, at index {1}+{2}".format(player["hero_id"], heroindex, 0), file=f)
				newMatch[heroindex] = 1
				radiantTeam += 1
			elif player["player_slot"] in dire_team_slots:
				print("Putting hero id {0} at index {1}+{2}".format(player["hero_id"], heroindex, count), file=f)
				newMatch[heroindex+count] = 1
				direTeam += 1

		if match["radiant_win"]:
			newResult = 1
		if zeroheroids == True or radiantTeam + direTeam != 10:
			print("Yah yeet, we're moving on", file=f)
			continue
		matches.append(newMatch)
		results.append(newResult)
		matchcounter += 1
		print("----------------", file=f)
	with open('matches.json', 'w') as outfile:
		json.dump(matches, outfile)
	with open('results.json', 'w') as outfile:
		json.dump(results, outfile)
	return matches, results

if __name__ == "__main__":
	initialise()
	data = parse_data(get_raw_data(10), get_hero_ids())
	print(
		data,
		len(data[0]),
		len(data[1])
	)
