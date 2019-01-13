import re

import nltk
from nltk import word_tokenize

#This is tagging from a guide

#https://nlpforhackers.io/training-pos-tagger/
#https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html

tagged_sentences = nltk.corpus.treebank.tagged_sents()

def features(sentence, index):
    """ sentence: [w1, w2, ...], index: the index of the word """
    return {
        'word': sentence[index],
        'is_first': index == 0,
        'is_last': index == len(sentence) - 1,
        'is_capitalized': sentence[index][0].upper() == sentence[index][0],
        'is_all_caps': sentence[index].upper() == sentence[index],
        'is_all_lower': sentence[index].lower() == sentence[index],
        'prefix-1': sentence[index][0],
        'prefix-2': sentence[index][:2],
        'prefix-3': sentence[index][:3],
        'suffix-1': sentence[index][-1],
        'suffix-2': sentence[index][-2:],
        'suffix-3': sentence[index][-3:],
        'prev_word': '' if index == 0 else sentence[index - 1],
        'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
        'has_hyphen': '-' in sentence[index],
        'is_numeric': sentence[index].isdigit(),
        'capitals_inside': sentence[index][1:].lower() != sentence[index][1:]
    }

def untag(tagged_sentence):
    return [w for w, t in tagged_sentence]

# Split the dataset for training and testing
cutoff = int(.75 * len(tagged_sentences))
training_sentences = tagged_sentences[:cutoff]
test_sentences = tagged_sentences[cutoff:]

# print(len(training_sentences))  # 2935
# print(len(test_sentences)) # 979

def transform_to_dataset(tagged_sentences):
    X, y = [], []

    for tagged in tagged_sentences:
        for index in range(len(tagged)):
            X.append(features(untag(tagged), index))
            y.append(tagged[index][1])

    return X, y

X, y = transform_to_dataset(training_sentences)

from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline

clf = Pipeline([
    ('vectorizer', DictVectorizer(sparse=False)),
    ('classifier', DecisionTreeClassifier(criterion='entropy'))
])

clf.fit(X[:7000],
        y[:7000])
# Use only the first 10K samples if you're running it multiple times. It takes a fair bit :)

print('Custom tagger training completed')

X_test, y_test = transform_to_dataset(test_sentences)

# print("Accuracy:", clf.score(X_test, y_test))

def Custom_pos_tag(sentence):
    tags = clf.predict([features(sentence, index) for index in range(len(sentence))])
    return zip(sentence, tags)

def findStations(sentence):
    locs = []
    found = []
    # sent = untag(sentence)
    # sent = word_tokenize(sentence)
    with open('allstations.txt', 'r') as allStations:
        data = allStations.readlines()
    for line in data:
        locs = line.split(", ")
    for index, w in enumerate(sentence):
        for l in locs:
            if(w[0].lower() == l.lower()):
                found.append(sentence[index-1])
                found.append(sentence[index])
                break
    return found

def findINandTO(sentence):
    found = []
    for index, w in enumerate(sentence):
        if(w[1] == 'IN') or (w[1] == 'TO'):
            if isRealStation(sentence[index+1][0]):
                found.append(sentence[index])
                found.append(sentence[index+1])
    return found

def isRealStation(station):
    locs = []
    with open('allStattionsAndCodes.txt', 'r') as allStations:
        data = allStations.readlines()
    for line in data:
        locs.append(line.splitlines())
    for l in locs:
        if(station.lower() == l[0].split(",")[0].lower()):
            return True
    return False

def getStationCode(station):
    locs = []
    with open('allStattionsAndCodes.txt', 'r') as allStations:
        data = allStations.readlines()
    for line in data:
        locs.append(line.splitlines())
    for l in locs:
        if(station.lower() == l[0].split(",")[0].lower()):
            return l[0].split(",")[1].upper()


def isTimeFormat(time):
    rex = re.compile("^[0-9]{2}[:][0-9]{2}$")
    if rex.match(time):
        return True
    else:
        return False

def isValidTime(time):
    rex = re.compile("^[0-2][0-9][:][0-5][0-9]$")
    if rex.match(time):
        return True
    else:
        return False

def isDateFormat(date):
    rex = re.compile("^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{2}$")
    if rex.match(date):
        return True
    else:
        return False

def wantsTicket(input):
    key = (('book','VB'),('book', 'NN'),('ticket', 'NN'),('ticket', 'NNP'),
           ('times', 'NNS'), ('reserve', 'VB'))
    for k in key:
        if k in input:
            return True
    if len(findStations(input)) > 0:
        return True
    return False

def removeWantsTicketPart(input):
    final = []
    key = 'book','ticket','reserve', 'by', 'delayed', 'delay'
    for index, i in enumerate(input):
        if len(input)-1 != index:
            if (input[index][0].lower() and input[index+1][0].lower()) not in key:
                if(input[index][0].lower()) not in key:
                    final.append(i)
        else:
            final.append(i)
    return final

def dateInFirstMessage(input):
    input = untag(input)
    rex = re.compile("^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{2}$")
    if 'return' in input:
        for item in input[:input.index('return')]:
            if rex.match(item):
                return item
    else:
        for item in input:
            if rex.match(item):
                return item

def timeInFirstMessage(input):
    input = untag(input)
    rex = re.compile("^[0-2][0-9][:][0-5][0-9]$")
    if 'return' in input:
        for item in input[:input.index('return')]:
            if rex.match(item):
                return item
    else:
        for item in input:
            if rex.match(item):
                return item

def wantsReturn(input):
    input = untag(input)
    if 'return' in input:
        return True
    return False

def retDateInFirstMessage(input):
    input = untag(input)
    rex = re.compile("^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{2}$")
    if 'return' in input:
        for item in input[input.index('return'):]:
            if rex.match(item):
                return item

def retTimeInFirstMessage(input):
    input = untag(input)
    rex = re.compile("^[0-2][0-9][:][0-5][0-9]$")
    if 'return' in input:
        for item in input[input.index('return'):]:
            if rex.match(item):
                return item

def wantsPredicted(input):
    key = (('delay','NN'),('predicted', 'VBD'),('predict', 'NN'),('delayed', 'VBD'),
           ('arrival', 'JJ'), ('predict', 'IN'))
    for k in key:
        if k in input:
            return True
    return False

def isNumber(input):
    rex = re.compile("^\d+$")
    return rex.match(input)
