# Option 1 - brfares
# - static information on tickets available for a trip from station A to station B
# - easier to use, but only provides generic information on ticketing options
# - does not indicate if a ticket actually available or options like reserved seating
# - does not provide time of train information
# - have to use Network Rail documentation to understand the data

# originString = 'diss'
# originJson = urlopen('http://api.brfares.com/ac_loc?term=%s' % originString).read()
# parsedOrigin = json.loads(originJson)
# print(json.dumps(parsedOrigin, sort_keys=True))
# originCode = parsedOrigin[0]['code']
# print(originCode)
#
#
# destinationString = 'norwich'
# destinationJson = urlopen('http://api.brfares.com/ac_loc?term=%s' % destinationString).read()
# parsedDestination = json.loads(destinationJson)
# print(json.dumps(parsedDestination, sort_keys=True))
# destinationCode = parsedDestination[0]['code']
# print(destinationCode)
#
#
# faresQuery = urlopen('http://api.brfares.com/querysimple?orig=%s&dest=%s' % (originCode, destinationCode)).read()
# parsedQuery = json.loads(faresQuery)
# print(json.dumps(parsedQuery, indent=4, sort_keys=True))
