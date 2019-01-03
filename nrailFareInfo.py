from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

origin = 'SPP'
origin = origin.replace(' ', '%20')
destination = 'Manchester'
destination = destination.replace(' ', '%20')
# Date is in format ddmmyy
originDepDate = '150119'
# Time is in 24 hr format like hhmm
originDepTime = '1315'
# If they are looking for a return ticket set boolean to True and fill out other 2 fields
wantsReturn = False
returnDepDate = '160119'
returnDepTime = '1645'


theURL = 'http://ojp.nationalrail.co.uk/service/timesandfares/' + origin + '/' + destination + '/' \
         + originDepDate + '/' + originDepTime + '/dep'

# The ticket should be a return ticket
if wantsReturn:
    theURL += '/' + returnDepDate + '/' + returnDepTime + '/dep'


page = urlopen(theURL).read()
soup = BeautifulSoup(page, 'html.parser')


# Ticket is a single
if not wantsReturn:
    table = soup.find('table', attrs={'id': 'oft'})
    table_body = table.find('tbody')
    rows = table_body.findChildren(['th', 'tr'])
    cheapestRow = ''
    for row in rows:
        cheapest = row.find('td', attrs={'class': 'fare has-cheapest'})
        if cheapest is not None:
            cheapestRow = cheapest
            break

    cheapestData = str(cheapestRow.find('script'))

    # Information we want is departureStationName, arrivalStationName, departureTime, arrivalTime, durationHours,
    # durationMinutes, changes, ticketPrice

    departureStationName = cheapestData.split('departureStationName":"')[1].split('"')[0]
    print("Departure Station: " + departureStationName)
    departureDateInfo = soup.find('h3', attrs={'class': 'outward top ctf-h3'})
    departureDayNo = departureDateInfo.findAll(text=True)[6]
    re.sub(r"[^a-zA-Z0-9]+", '', departureDayNo)
    departureDay = departureDateInfo.findAll('abbr')[0].findAll(text=True)[0]
    departureMonth = departureDateInfo.findAll('abbr')[1].findAll(text=True)[0]
    print("Departure Date: " + departureDay + departureDayNo + departureMonth)
    departureTime = cheapestData.split('departureTime":"')[1].split('"')[0]
    print("Departure Time: " + departureTime)
    arrivalStationName = cheapestData.split('arrivalStationName":"')[1].split('"')[0]
    print("Arrival Station: " + arrivalStationName)
    arrivalTime = cheapestData.split('arrivalTime":"')[1].split('"')[0]
    print("Arrival Time: " + arrivalTime)
    durationHours = cheapestData.split('durationHours":')[1].split(',')[0]
    durationMinutes = cheapestData.split('durationMinutes":')[1].split(',')[0]
    print("Duration: " + durationHours + "h " + durationMinutes + "m")
    changes = cheapestData.split('changes":')[1].split(',')[0]
    print("Changes: " + changes)
    ticketPrice = table.find('strong', attrs={'class': 'ctf-pr'}).findAll(text=True)[0]
    print("Full Ticket Price: " + ticketPrice)
