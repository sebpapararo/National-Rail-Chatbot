import nltk, re, pprint
import time, datetime
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import wordnet

#This is tagging from a guide

#https://nlpforhackers.io/training-pos-tagger/
#https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html

# print(pos_tag(word_tokenize("I'm learning NLP")))
# # [('I', 'PRP'), ("'m", 'VBP'), ('learning', 'VBG'), ('NLP', 'NNP')]
#

tagged_sentences = nltk.corpus.treebank.tagged_sents()

# print(tagged_sentences[0])
# print("Tagged sentences: ", len(tagged_sentences))
# print("Tagged words:", len(nltk.corpus.treebank.tagged_words()))


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


# import pprint
#
# pprint.pprint(features(['This', 'is', 'a', 'sentence'], 2))

# {'capitals_inside': False,
#  'has_hyphen': False,
#  'is_all_caps': False,
#  'is_all_lower': True,
#  'is_capitalized': False,
#  'is_first': False,
#  'is_last': False,
#  'is_numeric': False,
#  'next_word': 'sentence',
#  'prefix-1': 'a',
#  'prefix-2': 'a',
#  'prefix-3': 'a',
#  'prev_word': 'is',
#  'suffix-1': 'a',
#  'suffix-2': 'a',
#  'suffix-3': 'a',
#  'word': 'a'}


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

clf.fit(X[:10000],
        y[:10000])  # Use only the first 10K samples if you're running it multiple times. It takes a fair bit :)

print('Training completed')

X_test, y_test = transform_to_dataset(test_sentences)

# print("Accuracy:", clf.score(X_test, y_test))


def Custom_pos_tag(sentence):
    tags = clf.predict([features(sentence, index) for index in range(len(sentence))])
    return zip(sentence, tags)


testSet = []

testSet = Custom_pos_tag(word_tokenize('Hello, I would like to book a train ticket please'))

# print(tuple(testSet))
# print(tuple(pos_tag(word_tokenize('I would like to book a train ticket please\n'))))
#
# print(tuple(pos_tag(word_tokenize('Today I read a book\n'))))
#
# print(tuple(pos_tag(word_tokenize('I would like book train please\n'))))
#
# print(tuple(pos_tag(word_tokenize('I would like to book a train ticket to Norwich\n'))))
#
# print(tuple(pos_tag(word_tokenize('I live in Norwich\n'))))
#
# print(tuple(pos_tag(word_tokenize('Norwich is a wonderful city\n'))))
