import json
import requests
from sklearn.naive_bayes import GaussianNB
import numpy as np


def getPredictedDelay(currentLocationCode, destinationCode, delayedBy, travelDate, travelTime):

    from datetime import datetime, timedelta

    # Format the time correctly by removing the colon
    travelTime = travelTime.replace(':', '')

    # Convert the date format
    travelDate = datetime.strptime(travelDate, '%d/%m/%y').strftime('%Y-%m-%d')

    # Set the time period to a 2 hour window  (+- 1 from the users travel time)
    from_time = datetime.strptime(travelTime, '%H%M') - timedelta(hours=1)
    from_time = str(from_time).split(' ')[1][:5].replace(':', '')
    to_time = datetime.strptime(travelTime, '%H%M') + timedelta(hours=1)
    to_time = str(to_time).split(' ')[1][:5].replace(':', '')

    # Set the date period to the previous 30 days
    from_date = datetime.strptime(travelDate, '%Y-%m-%d') - timedelta(days=31)
    from_date = str(from_date).split(' ')[0]
    to_date = datetime.strptime(travelDate, '%Y-%m-%d') - timedelta(days=1)
    to_date = str(to_date).split(' ')[0]

    weekDay = datetime.strptime(travelDate, '%Y-%m-%d').date().weekday()
    if weekDay == 5:
        weekDay = 'SATURDAY'
    elif weekDay == 6:
        weekDay = 'SUNDAY'
    else:
        weekDay = 'WEEKDAY'

    api_url = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"

    headers = {"Content-Type": "application/json"}
    auths = ("n.lilly@uea.ac.uk","Qwerty123_")

    data = {
      "from_loc": currentLocationCode,
      "to_loc": destinationCode,
      "from_time": from_time,
      "to_time": to_time,
      "from_date": from_date,
      "to_date": to_date,
      "days": weekDay
    }

    r = requests.post(api_url, headers=headers, auth=auths, json=data)

    parsedInfo = json.loads(r.text)

    allMatchingRIDS = []

    for service in parsedInfo['Services']:
      for matchedTrains in service.get('serviceAttributesMetrics').get('rids'):
        allMatchingRIDS.append(matchedTrains)

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
        if (loc.get('location') == currentLocationCode) or (loc.get('location') == destinationCode):
          scheduledArrivalTime.append(loc.get('gbtt_pta'))
          scheduledDepartureTime.append(loc.get('gbtt_ptd'))
          actualArrivalTime.append(loc.get('actual_ta'))
          actualDepartureTime.append(loc.get('actual_td'))
          location.append(loc.get('location'))

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
                x = np.append(x, [tdelta], axis=0)

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

    # Create a Gaussian Classifier
    model = GaussianNB()

    # Train the model using the training sets
    model.fit(x, y)

    # Predict Output
    predicted = model.predict([[delayedBy]])

    return str(predicted[0])
