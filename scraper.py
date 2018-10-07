import requests
import simplejson as json
#4152438307
def get_raw_data(howManyMatches, highestMatchID):
    rawMatches = []
    while len(rawMatches) < howManyMatches:
        parameters = {'mmr_descending': 1, 'less_than_match_id': highestMatchID} # Sort the matches in decreasing skill order and lower than a specific matchid

        response = requests.get('https://api.opendota.com/api/publicMatches', params=parameters) # GET match data from api.opendota.#
        matchSet = json.loads(response.content)
        rawMatches = rawMatches + matchSet # Concatenate new data with existing data
        highestMatchID = matchSet[0]["match_id"] # Get new highest matchid
        with open('test.json', 'w') as outfile:
            json.dump(rawMatches, outfile)
    return rawMatches

rawMatches = get_raw_data(200, "")

# We need to get these main things: matchid, who wins, and what heroes were in the matchid
# We gather first 100 through standard GET and then get the rest using less than this match id parameter
# We need a list of dictionaries
# We also need to get a list of hero ids and their heroes
# Divide file into two functions: one to get all the data and then another to parse
# We could make the parse function run as the data comes in, adding each match to the matches list
# However that makes it run slower

#matches = []
