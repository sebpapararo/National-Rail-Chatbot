import json
import pprint
from urllib.request import urlopen

# Option 1 - brfares
# - static information on tickets available for a trip from station A to station B
# - easier to use, but only provides generic information on ticketing options
# - does not indicate if a ticket actually available or options like reserved seating
# - does not provide time of train information
# - have to use Network Rail documentation to understand the data

originString = 'diss'
originJson = urlopen('http://api.brfares.com/ac_loc?term=%s' % originString).read()
parsedOrigin = json.loads(originJson)
# print(json.dumps(parsedOrigin, sort_keys=True))
originCode = parsedOrigin[0]['code']
# print(originCode)


destinationString = 'norwich'
destinationJson = urlopen('http://api.brfares.com/ac_loc?term=%s' % destinationString).read()
parsedDestination = json.loads(destinationJson)
# print(json.dumps(parsedDestination, sort_keys=True))
destinationCode = parsedDestination[0]['code']
# print(destinationCode)


faresQuery = urlopen('http://api.brfares.com/querysimple?orig=%s&dest=%s' % (originCode, destinationCode)).read()
parsedQuery = json.loads(faresQuery)
print(json.dumps(parsedQuery, indent=4, sort_keys=True))

usefulInfo = []
print('===================================')
# From this we want: adult(status(name), fare), child(status(name), fare), fare_setter(name),
# route(longname), ticket(longname)
for ticket in parsedQuery['fares']:
    ticketInfo = {}
    for key, value in ticket.items():
        if key == 'ticket':
            ticketInfo['ticketName'] = value['longname']
            ticketInfo['ticketType'] = value['type']['desc']
            ticketInfo['ticketClass'] = value['tclass']['desc']
        if key == 'route':
            ticketInfo['ticketRestrictions'] = value['longname']
        if key == 'fare_setter':
            ticketInfo['ticketFareSetter'] = value['name']
        if key == 'adult':
            # check if the ticket is child only
            if 'fare' in value.keys():
                ticketInfo['adultTicketFare'] = value['fare']
        if key == 'child':
            if 'fare' in value.keys():
                ticketInfo['childTicketFare'] = value['fare']
    usefulInfo.append(ticketInfo)

for ticket in usefulInfo:
    pprint.pprint(ticket)
