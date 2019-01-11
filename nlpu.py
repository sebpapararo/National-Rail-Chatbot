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

def findLocations(sentence):
    locs = []
    found = []
    sent = untag(sentence)
    # sent = word_tokenize(sentence)
    with open('GBstations/allstations.txt', 'r') as allStations:
        data = allStations.readlines()
    for line in data:
        locs = line.split(", ")
    for w in sent:
        for l in locs:
            if(w.lower() == l.lower()):
                found.append(w)
                break
    return found