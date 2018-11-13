import nltk
import nltk, re, pprint
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
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

print(nltk.pos_tag(lemmated))

