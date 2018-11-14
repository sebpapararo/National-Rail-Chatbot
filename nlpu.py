import nltk
import nltk, re, pprint
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import wordnet
##############Book examle and practice#############
#nltk.download()
# from nltk.book import *
#
# def lexical_diversity(text):
#     return len(set(text)) / len(text)
#
#
# sent1 = ['Can','I','book','a','ticket','.']
#
# print(len(sent1))
#
# print(lexical_diversity(sent1))
#
# test1 = ["I'd like to book a ticket please."]
#
# print(sorted(set(text1)))
###################################################

stop_words=set(stopwords.words("english"))

sent = "Hello, I would like to books a ticket please."

tokens=nltk.word_tokenize(sent) #####Tokenize and keep punctuation
print("Sent sentance:\t\t",tokens)

RMPunctuation = RegexpTokenizer(r'\w+')
PunctuationRMd = RMPunctuation.tokenize(sent)###### Tokenize and remove punctuation
print("Punctuation removed:", PunctuationRMd)

filtered_sent=[] #############Removes 'a' 'to'  'in' etc...
for w in PunctuationRMd:
    if w not in stop_words:
        filtered_sent.append(w)
#print("Tokenized Sentence:\t",PunctuationRMd)
print("Filterd Sentence:\t",filtered_sent)

lem = WordNetLemmatizer()########Removes -ing -ed -s
lemmated=[]
for q in filtered_sent:
    lemmated.append(lem.lemmatize(q,"v"))
print("Lemmated:\t\t\t",lemmated)

#########Prints all the words and the tags that each word comes under
print(nltk.pos_tag(lemmated))

#https://www.geeksforgeeks.org/get-synonymsantonyms-nltk-wordnet-python/


# Then, we're going to use the term "program" to find synsets like so:
syns = wordnet.synsets("book")# use .v to make it a verb (which is what we want)

# An example of a synset:
print(syns[0].name())

# Just the word:
print(syns[0].lemmas()[0].name())

# Definition of that first synset:
print(syns[0].definition())

# Examples of the word in use in sentences:
print(syns[0].examples())


synonyms = []
antonyms = []

for syn in wordnet.synsets('book.v.01'):
    for l in syn.lemmas():
        synonyms.append(l.name())
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())

print(set(synonyms))
print(set(antonyms))


# Let's compare the noun of "ship" and "boat:"

w1 = wordnet.synset('book.v.01') # v here denotes the tag verb
w2 = wordnet.synset('reserve.v.01')
print(w1.wup_similarity(w2))

#This is very useful as it will help us define words, i.e. book means to book and not an actual book
wordnet.synset('book.v.01').frame_ids()

for lemma in wordnet.synset('book.v.01').lemmas():
    print(lemma, lemma.frame_ids())
    print(" | ".join(lemma.frame_strings()))




#synsets

# class WordReplacer(object):
#   def __init__(self, word_map):
#     self.word_map = word_map
#
#   def replace(self, word):
#     return self.word_map.get(word, word)

