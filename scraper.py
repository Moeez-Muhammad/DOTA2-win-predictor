import json
import opendota

api = opendota.API()
api.get_heroes()
api.generate_hero_dict()
matches = api.get_more_matches(matches_requested=1000)
parsed_matches = api.parse_matches_for_ml(matches, file_outputs=["matches.json", "results.json"])
print(json.dumps(parsed_matches, indent=4, sort_keys=True))