import requests
import pandas as pd
from pandas.io.json import json_normalize
from time import sleep
import json

class API:

	OPENDOTA_URL = "https://api.opendota.com/api/"
	REQUEST_TIMEOUT = 0.3

	def __init__(self, apikey=None):
		if not apikey:
			self.wait = 1
		else: wait = 0

	def get_public_matches(self, less_than_match_id=None, mmr_ascending=None, mmr_descending=None):
		url = self.OPENDOTA_URL + 'publicMatches'
		if mmr_ascending == True and mmr_ascending == mmr_descending:
			raise ValueError("mmr_ascending and mmr_descending cannot both be True")
		payload = {less_than_match_id: less_than_match_id, mmr_ascending: mmr_ascending, mmr_descending: mmr_descending}
		if mmr_ascending == True:
			payload[mmr_ascending] = 1
		elif mmr_descending == True:
			payload[mmr_descending] = 1
		r = requests.get(url, payload)
		return json.loads(r.content)

	
	def get_more_matches(self, less_than_match_id=None, min_mmr=4500, matches_requested=100, columns=['match_id', 'radiant_win', 'avg_mmr', 'radiant_team', 'dire_team']):
		matches = pd.DataFrame()
		current_match_id = less_than_match_id
		matches_found = 0

		url = self.OPENDOTA_URL + 'publicMatches?lessthanmatchid='
		if matches_requested % 100 != 0:
			raise ValueError("matches_requested should be a multiple of 100")
		while matches_found < matches_requested:
			jsons = self.get_public_matches(less_than_match_id)
			current_match_id = jsons[-1]['match_id']

			current_dataframe = json_normalize(jsons)
			current_dataframe = current_dataframe[columns] # Get only columns specified
			current_dataframe = current_dataframe.loc[current_dataframe["avg_mmr"] > min_mmr] # Remove low mmr games

			matches_found += len(current_dataframe)
			matches = matches.append(current_dataframe, ignore_index=True)
			sleep(self.wait)
		matches = matches.iloc[0:matches_requested]
		
		return matches





