from urllib.request import urlopen
from bs4 import BeautifulSoup


def getFareInfo(origin, destination, originDepDate, originDepTime, wantsReturn, returnDepDate, returnDepTime):

    originDepDate = originDepDate.replace('/', '')
    originDepTime = originDepTime.replace(':', '')
    returnDepDate = returnDepDate.replace('/', '')
    returnDepTime = returnDepTime.replace(':', '')

    origin = origin.replace(' ', '%20')
    destination = destination.replace(' ', '%20')


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
        cheapest = soup.find('td', attrs={'class': 'fare has-cheapest'})
        cheapestData = str(cheapest.find('script'))

        # Information we want is departureStationName, arrivalStationName, departureTime, arrivalTime, durationHours,
        # durationMinutes, changes, ticketPrice

        departureStationName = cheapestData.split('departureStationName":"')[1].split('"')[0]

        departureDateInfo = soup.find('h3', attrs={'class': 'outward top ctf-h3'})
        departureDayNo = departureDateInfo.findAll(text=True)[6]
        departureDay = departureDateInfo.findAll('abbr')[0].findAll(text=True)[0]
        departureMonth = departureDateInfo.findAll('abbr')[1].findAll(text=True)[0]

        departureTime = cheapestData.split('departureTime":"')[1].split('"')[0]

        arrivalStationName = cheapestData.split('arrivalStationName":"')[1].split('"')[0]

        arrivalTime = cheapestData.split('arrivalTime":"')[1].split('"')[0]

        durationHours = cheapestData.split('durationHours":')[1].split(',')[0]
        durationMinutes = cheapestData.split('durationMinutes":')[1].split(',')[0]

        changes = cheapestData.split('changes":')[1].split(',')[0]

        ticketPrice = table.find('strong', attrs={'class': 'ctf-pr'}).findAll(text=True)[0]

        return theURL

    # This is a return ticket. The cheapest option for a return ticket can be either a normal return ticket.
    # Or two single tickets (one going each way)
    else:
        # table = soup.find('table', attrs={'id': 'oft'})
        cheapest = soup.findAll('td', attrs={'class': 'fare has-cheapest'})

        # Means there is only 1 cheapest ticket, and is therefore a normal return ticket
        if len(cheapest) == 1:
            cheapestData = str(cheapest[0].find('script'))

            # Outbound ticket
            departureStationName = cheapestData.split('departureStationName":"')[1].split('"')[0]

            departureDateInfo = soup.find('h3', attrs={'class': 'outward top ctf-h3'})
            departureDayNo = departureDateInfo.findAll(text=True)[6]
            departureDay = departureDateInfo.findAll('abbr')[0].findAll(text=True)[0]
            departureMonth = departureDateInfo.findAll('abbr')[1].findAll(text=True)[0]

            departureTime = cheapestData.split('departureTime":"')[1].split('"')[0]

            arrivalStationName = cheapestData.split('arrivalStationName":"')[1].split('"')[0]

            arrivalTime = cheapestData.split('arrivalTime":"')[1].split('"')[0]

            durationHours = cheapestData.split('durationHours":')[1].split(',')[0]
            durationMinutes = cheapestData.split('durationMinutes":')[1].split(',')[0]

            changes = cheapestData.split('changes":')[1].split(',')[0]

            # Return ticket
            table = soup.find('table', attrs={'id': 'ift'})
            selectedRow = table.find('tr', attrs={'class': 'first mtx'})
            selectedReturn = str(selectedRow.find('script'))

            departureStationName = selectedReturn.split('departureStationName":"')[1].split('"')[0]

            departureDateInfo = soup.find('h3', attrs={'class': 'ctf-h3 return'})
            departureDayNo = departureDateInfo.findAll(text=True)[6]
            departureDay = departureDateInfo.findAll('abbr')[0].findAll(text=True)[0]
            departureMonth = departureDateInfo.findAll('abbr')[1].findAll(text=True)[0]

            departureTime = selectedReturn.split('departureTime":"')[1].split('"')[0]

            arrivalStationName = selectedReturn.split('arrivalStationName":"')[1].split('"')[0]

            arrivalTime = selectedReturn.split('arrivalTime":"')[1].split('"')[0]

            durationHours = selectedReturn.split('durationHours":')[1].split(',')[0]
            durationMinutes = selectedReturn.split('durationMinutes":')[1].split(',')[0]

            changes = selectedReturn.split('changes":')[1].split(',')[0]

            rightSelected = soup.find('div', attrs={'id': 'fare-switcher'})
            ticketPrice = rightSelected.find('strong', attrs={'class': 'ctf-pr'}).findAll(text=True)[0]

            return theURL

        # Means there is 2 cheapest tickets, and is therefore 2 singles there and back
        else:
            cheapestData = str(cheapest[0].find('script'))

            # Outbound ticket
            departureStationName = cheapestData.split('departureStationName":"')[1].split('"')[0]

            departureDateInfo = soup.find('h3', attrs={'class': 'outward top ctf-h3'})
            departureDayNo = departureDateInfo.findAll(text=True)[6]
            departureDay = departureDateInfo.findAll('abbr')[0].findAll(text=True)[0]
            departureMonth = departureDateInfo.findAll('abbr')[1].findAll(text=True)[0]

            departureTime = cheapestData.split('departureTime":"')[1].split('"')[0]

            arrivalStationName = cheapestData.split('arrivalStationName":"')[1].split('"')[0]

            arrivalTime = cheapestData.split('arrivalTime":"')[1].split('"')[0]

            durationHours = cheapestData.split('durationHours":')[1].split(',')[0]
            durationMinutes = cheapestData.split('durationMinutes":')[1].split(',')[0]

            changes = cheapestData.split('changes":')[1].split(',')[0]

            cheapestData = str(cheapest[1].find('script'))

            # Return ticket
            departureStationName = cheapestData.split('departureStationName":"')[1].split('"')[0]

            departureDateInfo = soup.find('h3', attrs={'class': 'ctf-h3 return'})
            departureDayNo = departureDateInfo.findAll(text=True)[6]
            departureDay = departureDateInfo.findAll('abbr')[0].findAll(text=True)[0]
            departureMonth = departureDateInfo.findAll('abbr')[1].findAll(text=True)[0]

            departureTime = cheapestData.split('departureTime":"')[1].split('"')[0]

            arrivalStationName = cheapestData.split('arrivalStationName":"')[1].split('"')[0]

            arrivalTime = cheapestData.split('arrivalTime":"')[1].split('"')[0]

            durationHours = cheapestData.split('durationHours":')[1].split(',')[0]
            durationMinutes = cheapestData.split('durationMinutes":')[1].split(',')[0]

            changes = cheapestData.split('changes":')[1].split(',')[0]

            rightSelected = soup.find('a', attrs={'id': 'singleFaresPane'})
            ticketPrice = rightSelected.find('strong', attrs={'class': 'ctf-pr'}).findAll(text=True)[0]

            return theURL
