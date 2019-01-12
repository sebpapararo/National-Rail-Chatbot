import json

import requests
from sklearn.naive_bayes import GaussianNB
import numpy as np

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


currentLocation = 'NRW'
destination = 'IPS'
userTrainRID = '123456789'
# in Minutes
delayedBy = '5'



api_url = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
# api_url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"

headers = { "Content-Type": "application/json" }
auths = ("n.lilly@uea.ac.uk","Qwerty123_")

data = {
  "from_loc": currentLocation,
  "to_loc": destination,
  "from_time": "0900",
  "to_time": "1100",
  "from_date": "2018-12-23",
  "to_date": "2019-01-11",
  "days": "WEEKDAY"
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

# print(allMatchingRIDS)

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
    if (loc.get('location') == currentLocation) or (loc.get('location') == destination):
      scheduledArrivalTime.append(loc.get('gbtt_pta'))
      scheduledDepartureTime.append(loc.get('gbtt_ptd'))
      actualArrivalTime.append(loc.get('actual_ta'))
      actualDepartureTime.append(loc.get('actual_td'))
      location.append(loc.get('location'))

print(scheduledArrivalTime)
print(actualArrivalTime)
print(scheduledDepartureTime)
print(actualDepartureTime)
print(location)

print(len(scheduledArrivalTime))
print(len(scheduledDepartureTime))


import numpy as np
from sklearn.naive_bayes import GaussianNB


from datetime import datetime

depDelay = int(actualDepartureTime[0]) - int(scheduledDepartureTime[0])
FMT = '%H%M'
if depDelay >= 0:
    tdelta = datetime.strptime(actualDepartureTime[0], FMT) - datetime.strptime(scheduledDepartureTime[0], FMT)
    tdelta = str(tdelta).split(':')[1]
    tdelta = int(tdelta)
    tdelta = [tdelta]
    x = np.array([tdelta])
else:
    tdelta = datetime.strptime(scheduledDepartureTime[0], FMT) - datetime.strptime(actualDepartureTime[0], FMT)
    tdelta = str(tdelta).split(':')[1]
    tdelta = '-' + tdelta
    tdelta = int(tdelta)
    tdelta = [tdelta]
    x = np.array([tdelta])

arrDelay = int(actualArrivalTime[1]) - int(scheduledArrivalTime[1])
FMT = '%H%M'
if arrDelay >= 0:
    tdelta = datetime.strptime(actualArrivalTime[1], FMT) - datetime.strptime(scheduledArrivalTime[1], FMT)
    tdelta = str(tdelta).split(':')[1]
    tdelta = int(tdelta)
    y = np.array(tdelta)
else:
    tdelta = datetime.strptime(scheduledArrivalTime[1], FMT) - datetime.strptime(actualArrivalTime[1], FMT)
    tdelta = str(tdelta).split(':')[1]
    tdelta = '-' + tdelta
    tdelta = int(tdelta)
    y = np.array(tdelta)





for i in range(2, len(scheduledDepartureTime), 2):

    if (actualDepartureTime[i] != '') and (actualArrivalTime[i+1] != '') \
            and (scheduledDepartureTime[i] != '') and (scheduledArrivalTime[i+1] != ''):
        depDelay = int(actualDepartureTime[i]) - int(scheduledDepartureTime[i])
        FMT = '%H%M'
        if depDelay >= 0:
            tdelta = datetime.strptime(actualDepartureTime[i], FMT) - datetime.strptime(scheduledDepartureTime[i], FMT)
            tdelta = str(tdelta).split(':')[1]
            tdelta = int(tdelta)
            tdelta = [tdelta]
            x = np.append(x, [tdelta], axis=0)
        else:
            tdelta = datetime.strptime(scheduledDepartureTime[i], FMT) - datetime.strptime(actualDepartureTime[i], FMT)
            tdelta = str(tdelta).split(':')[1]
            tdelta = '-' + tdelta
            tdelta = int(tdelta)
            tdelta = [tdelta]
            x1 = np.append(x, [tdelta], axis=0)

        arrDelay = int(actualArrivalTime[i+1]) - int(scheduledArrivalTime[i+1])
        FMT = '%H%M'
        if arrDelay >= 0:
            tdelta = datetime.strptime(actualArrivalTime[i+1], FMT) - datetime.strptime(scheduledArrivalTime[i+1], FMT)
            tdelta = str(tdelta).split(':')[1]
            tdelta = int(tdelta)
            y = np.append(y, tdelta)
        else:
            tdelta = datetime.strptime(scheduledArrivalTime[i+1], FMT) - datetime.strptime(actualArrivalTime[i+1], FMT)
            tdelta = str(tdelta).split(':')[1]
            tdelta = '-' + tdelta
            tdelta = int(tdelta)
            y = np.append(y, tdelta)

print(x)
print(y)

# Create a Gaussian Classifier
model = GaussianNB()

# Train the model using the training sets
model.fit(x, y)

#Predict Output
predicted= model.predict([[3]])
print('Predicted delay in minutes: ' + predicted)

