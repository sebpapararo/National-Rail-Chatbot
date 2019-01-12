import requests
import json

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
  "from_date": "2018-12-20",
  "to_date": "2019-01-11",
  "days": "WEEKDAY"
}

r = requests.post(api_url, headers=headers, auth=auths, json=data)

# print(json.dumps(json.loads(r.text), sort_keys=True, indent=2, separators=(',',': ')))

parsedInfo = json.loads(r.text)
# print(parsedInfo, sort_keys=True, indent=2)

usefulInfo = []

for service in parsedInfo['Services']:
  print(service.get('serviceAttributesMetrics'))
  # service = service.item
  # for key, value in service.items:
  #   if key == 'origin_location':
  #     print(value)
  # for attrMetrics in service:
  #   if attrMetrics == 'serviceAttributesMetrics':
  #     print(attrMetrics)
