from nltk import word_tokenize
from nlp_customTagger import Custom_pos_tag

# sentText = 'Hello, I would like to book a train ticket to Norwich from diss'

# def findLocations(sentence):
#     locs = []
#     found = []
#     sent = untag(sentence)
#     # sent = word_tokenize(sentence)
#     with open('GBstations/allstations.txt', 'r') as allStations:
#         data = allStations.readlines()
#     for line in data:
#         locs = line.split(", ")
#     for w in sent:
#         for l in locs:
#             if(w.lower() == l.lower()):
#                 found.append(w)
#                 break
#     return found

# testData = Custom_pos_tag(word_tokenize(sentText))
# copyData = Custom_pos_tag(word_tokenize(sentText))

# customplaces = findLocations(copyData)
#
# print(tuple(testData))
# print("Locations found: ",customplaces)