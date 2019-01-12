import json

import requests

# Documentation can be found at
#   https://wiki.openraildata.com/index.php/HSP

# When registering at https://datafeeds.nationalrail.co.uk/
# you only need the HSP subscription
# The Real time Data feed is too much to deal with
# The On Demand Data Feeds might be useful
#
# In 'Planned usage', mention you are using the HSP data
# for educational purposes, for a project, and for a limited
# time
# The T & Cs should not be an issue, nor the limit on the
# number of requests an hour - but do be polite and do not
# swamp the web service with an excessive number of requests

api_url = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
# api_url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"

headers = { "Content-Type": "application/json" }
auths = ("n.lilly@uea.ac.uk","Qwerty123_")

data = {
  "from_loc": "NRW",
  "to_loc": "DIS",
  "from_time": "0900",
  "to_time": "1100",
  "from_date": "2018-12-23",
  "to_date": "2019-01-11",
  "days": "SUNDAY"
}

r = requests.post(api_url, headers=headers, auth=auths, json=data)

# print(json.dumps(json.loads(r.text), sort_keys=True, indent=2, separators=(',',': ')))

parsedInfo = json.loads(r.text)
# print(parsedInfo, sort_keys=True, indent=2)

allMatchingRIDS = []

for service in parsedInfo['Services']:
  # print(service.get('serviceAttributesMetrics').get('rids'))
  for matchedTrains in service.get('serviceAttributesMetrics').get('rids'):
    allMatchingRIDS.append(matchedTrains)


print(allMatchingRIDS)

api_url = 'https://hsp-prod.rockshore.net/api/v1/serviceDetails'

scheduledArrivalTime = []
scheduledDepartureTime = []
actualArrivalTime = []
actualDepartureTime = []
location = []

for RID in allMatchingRIDS:
  data = {
    "rid": RID
  }
  r = requests.post(api_url, headers=headers, auth=auths, json=data)
  parsedInfo = json.loads(r.text)
  for loc in parsedInfo.get('serviceAttributesDetails').get('locations'):
    scheduledArrivalTime.append(loc.get('gbtt_pta'))
    scheduledDepartureTime.append(loc.get('gbtt_ptd'))
    actualArrivalTime.append(loc.get('actual_ta'))
    actualDepartureTime.append(loc.get('actual_td'))
    location.append(loc.get('location'))




