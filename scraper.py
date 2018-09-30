import requests
import simplejson as json

# parameters = {'mmr_descending': 1}
# response = requests.get('https://api.opendota.com/api/publicMatches', params=parameters)
# data = response.content
# with open('test.json', 'w') as outfile:
#     json.dump(response.content, outfile)

with open('test.json') as infile:
    raw_data = json.load(infile)

print(raw_data)



