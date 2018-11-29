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
    rawMatches = api.get_match_history(game_mode=1, skill=3, matches_requested=matches_requested)["matches"] # Collective list of all matches to be used
    for match in rawMatches:
        match_ids.append(match["match_id"])
    return match_ids

def parse_data(match_ids):
    rawMatches = []
    matches = []
    for match_id in match_ids:
        rawMatches.append(api.get_match_details(match_id=match_id))
    for match in rawMatches:
        newMatch = {}
        radiant_team = []
        dire_team = []
        players = match["players"]
        for player in players:
            if player["player_slot"] in radiant_team_slots:
                radiant_team.append(player["hero_id"])
            elif player["player_slot"] in dire_team_slots:
                dire_team.append(player["hero_id"])

        newMatch["radiant_win"], newMatch["radiant_team"], newMatch["dire_team"] = match["radiant_win"], radiant_team, dire_team
        matches.append(newMatch)
    with open('matches.json', 'a') as outfile:
        json.dump(matches, outfile)
    return matches


initialise()
rawMatches = get_raw_data(matches_requested=1000) # highestMatchID is blank because the current matchids of the current matches could change
print(parse_data(rawMatches))
