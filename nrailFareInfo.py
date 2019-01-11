from urllib.request import urlopen

from bs4 import BeautifulSoup


# The dates and times will need to be formatted after being passed in


def getFareInfo(origin, destination, originDepDate, originDepTime, wantsReturn):

    originDepDate = originDepDate.replace('/', '')
    originDepTime = originDepTime.replace(':', '')

# origin = 'Diss'
    origin = origin.replace(' ', '%20')
# destination = 'Norwich'
    destination = destination.replace(' ', '%20')
# # Date is in format ddmmyy
# originDepDate = '120119'
# # Time is in 24 hr format like hhmm
# originDepTime = '1315'
# # If they are looking for a return ticket set boolean to True and fill out other 2 fields
# wantsReturn = True
# returnDepDate = '130119'
# returnDepTime = '2145'


    theURL = 'http://ojp.nationalrail.co.uk/service/timesandfares/' + origin + '/' + destination + '/' \
             + originDepDate + '/' + originDepTime + '/dep'

    # The ticket should be a return ticket
    # if wantsReturn:
    #     theURL += '/' + returnDepDate + '/' + returnDepTime + '/dep'


    page = urlopen(theURL).read()
    soup = BeautifulSoup(page, 'html.parser')


    # Ticket is a single
    if not wantsReturn:
        table = soup.find('table', attrs={'id': 'oft'})
        cheapest = soup.find('td', attrs={'class': 'fare has-cheapest'})
        cheapestData = str(cheapest.find('script'))

        # Information we want is departureStationName, arrivalStationName, departureTime, arrivalTime, durationHours,
        # durationMinutes, changes, ticketPrice

        departureStationName = cheapestData.split('departureStationName":"')[1].split('"')[0]
        # print("Departure Station: " + departureStationName)
        departureDateInfo = soup.find('h3', attrs={'class': 'outward top ctf-h3'})
        departureDayNo = departureDateInfo.findAll(text=True)[6]
        departureDay = departureDateInfo.findAll('abbr')[0].findAll(text=True)[0]
        departureMonth = departureDateInfo.findAll('abbr')[1].findAll(text=True)[0]
        # print("Departure Date: " + departureDay + departureDayNo + departureMonth)
        departureTime = cheapestData.split('departureTime":"')[1].split('"')[0]
        # print("Departure Time: " + departureTime)
        arrivalStationName = cheapestData.split('arrivalStationName":"')[1].split('"')[0]
        # print("Arrival Station: " + arrivalStationName)
        arrivalTime = cheapestData.split('arrivalTime":"')[1].split('"')[0]
        # print("Arrival Time: " + arrivalTime)
        durationHours = cheapestData.split('durationHours":')[1].split(',')[0]
        durationMinutes = cheapestData.split('durationMinutes":')[1].split(',')[0]
        # print("Duration: " + durationHours + "h " + durationMinutes + "m")
        changes = cheapestData.split('changes":')[1].split(',')[0]
        # print("Changes: " + changes)
        ticketPrice = table.find('strong', attrs={'class': 'ctf-pr'}).findAll(text=True)[0]
        # print("Full Ticket Price: " + ticketPrice)

        # print('')
        # print('Click the following link to go and book this ticket: ')
        # print(theURL)

        return theURL

    # This is a return ticket. The cheapest option for a return ticket can be either a normal return ticket. Or two single
    # tickets (one going each way)
    else:
        # table = soup.find('table', attrs={'id': 'oft'})
        cheapest = soup.findAll('td', attrs={'class': 'fare has-cheapest'})

        # Means there is only 1 cheapest ticket, and is therefore a normal return ticket
        if len(cheapest) == 1:
            cheapestData = str(cheapest[0].find('script'))

            # Outbound ticket
            print('######## Outward ########')
            departureStationName = cheapestData.split('departureStationName":"')[1].split('"')[0]
            print("Departure Station: " + departureStationName)
            departureDateInfo = soup.find('h3', attrs={'class': 'outward top ctf-h3'})
            departureDayNo = departureDateInfo.findAll(text=True)[6]
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

            # Return ticket
            table = soup.find('table', attrs={'id': 'ift'})
            selectedRow = table.find('tr', attrs={'class': 'first mtx'})
            selectedReturn = str(selectedRow.find('script'))

            print('######## Return ########')
            departureStationName = selectedReturn.split('departureStationName":"')[1].split('"')[0]
            print("Departure Station: " + departureStationName)
            departureDateInfo = soup.find('h3', attrs={'class': 'ctf-h3 return'})
            departureDayNo = departureDateInfo.findAll(text=True)[6]
            departureDay = departureDateInfo.findAll('abbr')[0].findAll(text=True)[0]
            departureMonth = departureDateInfo.findAll('abbr')[1].findAll(text=True)[0]
            print("Departure Date: " + departureDay + departureDayNo + departureMonth)
            departureTime = selectedReturn.split('departureTime":"')[1].split('"')[0]
            print("Departure Time: " + departureTime)
            arrivalStationName = selectedReturn.split('arrivalStationName":"')[1].split('"')[0]
            print("Arrival Station: " + arrivalStationName)
            arrivalTime = selectedReturn.split('arrivalTime":"')[1].split('"')[0]
            print("Arrival Time: " + arrivalTime)
            durationHours = selectedReturn.split('durationHours":')[1].split(',')[0]
            durationMinutes = selectedReturn.split('durationMinutes":')[1].split(',')[0]
            print("Duration: " + durationHours + "h " + durationMinutes + "m")
            changes = selectedReturn.split('changes":')[1].split(',')[0]
            print("Changes: " + changes)

            print('')
            rightSelected = soup.find('div', attrs={'id': 'fare-switcher'})
            ticketPrice = rightSelected.find('strong', attrs={'class': 'ctf-pr'}).findAll(text=True)[0]
            print('Total Ticket Cost: ' + ticketPrice)
            print('')
            print('Click the following link to go and book this ticket: ')
            print(theURL)

        # Means there is 2 cheapest tickets, and is therefore 2 singles there and back
        else:
            cheapestData = str(cheapest[0].find('script'))

            # Outbound ticket
            print('######## Outward ########')
            departureStationName = cheapestData.split('departureStationName":"')[1].split('"')[0]
            print("Departure Station: " + departureStationName)
            departureDateInfo = soup.find('h3', attrs={'class': 'outward top ctf-h3'})
            departureDayNo = departureDateInfo.findAll(text=True)[6]
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

            cheapestData = str(cheapest[1].find('script'))

            # Return ticket
            print('######## Return ########')
            departureStationName = cheapestData.split('departureStationName":"')[1].split('"')[0]
            print("Departure Station: " + departureStationName)
            departureDateInfo = soup.find('h3', attrs={'class': 'ctf-h3 return'})
            departureDayNo = departureDateInfo.findAll(text=True)[6]
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

            print('')
            rightSelected = soup.find('a', attrs={'id': 'singleFaresPane'})
            ticketPrice = rightSelected.find('strong', attrs={'class': 'ctf-pr'}).findAll(text=True)[0]
            print('Total Ticket Cost: ' + ticketPrice)
            print('')
            print('Click the following link to go and book this ticket: ')
            print(theURL)
