import requests
import simplejson as json
#4152438307
def get_raw_data(howManyMatches, highestMatchID):
    '''
    ///MUST READ TO UNDERSTAND CODE AND COMMENTS///

    Opendota's API works like this:
        * /publicmatches?mmr_descending=1 gets a random sample of public matches with a high skill rating, sorting ascending by matchid
        * Example list of matchids: {100..200}
        * /publicmatches?mmr_descending=1&less_than_match_id=100 gets a random sample of public matches with a high skill rating, sorting descending by matchid, where all matchid < less_than_match_id
        * So, if we set less_than_match_id to blank, we get a random sample sorted matchid ascending from a to b
        * Then, we take a, and get a random sample of matchids less than a from a to c where c < a
        * We then take c and keep recursively doing that, going lower and lower in matchids until the required number of matches has been met
    '''
    rawMatches = [] # Collective list of all matches to be used
    while len(rawMatches) < howManyMatches: # Check if we have the required number of matches
        parameters = {'mmr_descending': 1, 'less_than_match_id': highestMatchID} # Sort the matches in decreasing skill order and lower than a specific matchid
        response = requests.get('https://api.opendota.com/api/publicMatches', params=parameters) # GET matches data from api.opendota.com
        matchSet = json.loads(response.content) # Get the json of the response data
        rawMatches = rawMatches + matchSet # Concatenate new data with existing data
        highestMatchID = matchSet[0]["match_id"] # Get new highest matchid from the first match
        with open('test.json', 'w') as outfile:
            json.dump(rawMatches, outfile)
    return rawMatches


rawMatches = get_raw_data(200, "") # highestMatchID is blank because the current matchids of the current matches could change

# We need to get these main things: matchid, who wins, and what heroes were in the matchid
# We gather first 100 through standard GET and then get the rest using less than this match id parameter
# We need a list of dictionaries where one dictionary is one match
# We also need to get a list of hero ids and their corresponding hero names
# Divide file into two functions: one to get all the data and then another to parse
# One function could be made to get hero data but that won't be ran in the final code as we can store the results
# Code can be in the final file however, for documentation purposes
# We could make the parse function run as the data comes in, adding each match to the matches list
# However that makes it run slower

#matches = []
