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

class testingGround:

    def testing(self):
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
        print("\n\nSynsets: ")
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


        print("Comparing Words: 'book.v.02' and 'reserve.v.04'")
        w1 = wordnet.synset('book.v.02') # v here denotes the tag verb
        w2 = wordnet.synset('reserve.v.04')
        print(w1.wup_similarity(w2))

        #This is very useful as it will help us define words, i.e. book means to book and not an actual book
        wordnet.synset('book.v.02').frame_ids()

        print("------------------------------------------------------------------------------------------------I am here cunt")
        for lemma in wordnet.synset('book.v.02').lemmas():
            print(lemma, lemma.frame_ids())
            print(" | ".join(lemma.frame_strings()))

        verb = wordnet.synset('book.v.02')

        print(verb.name())

        print(verb.definition())

        print(verb.examples())

        print("\n\n\n")
        #synsets

        # class WordReplacer(object):
        #   def __init__(self, word_map):
        #     self.word_map = word_map
        #
        #   def replace(self, word):
        #     return self.word_map.get(word, word)


class MyClass:
    """Class to take in an input and return what that input means"""
    userInput = []

    def __init__(self, sent):
        global userInput
        token = RegexpTokenizer(r'\w+')
        words = token.tokenize(sent)
        stop_words = set(stopwords.words("english"))

        filtered_sent = []  #############Removes 'a' 'to'  'in' etc...
        for w in words:
            if w not in stop_words:
                filtered_sent.append(w)

        lem = WordNetLemmatizer()  ########Removes -ing -ed -s
        lemmated = []
        for q in filtered_sent:
            lemmated.append(lem.lemmatize(q, "v"))

        userInput = lemmated
        print("Individual Words:", userInput)

    def getVerbs(self):
        global userInput
        test = userInput
        print(nltk.pos_tag(['He'] + test))

        verbs = {}

        verbs['book'] = 'V'

        print(verbs)

        for w in test:
            print(w)
            print(wordnet.synsets(w))

        for w in test:
            tmp = wordnet.synsets(w)[0].pos()
            print (w, ":", tmp)

        #print(nltk.pos_tag(test))

        #https://www.nltk.org/book/ch05.html
            # Just to make it a bit more readable
            WN_NOUN = 'n'
            WN_VERB = 'v'
            WN_ADJECTIVE = 'a'
            WN_ADJECTIVE_SATELLITE = 's'
            WN_ADVERB = 'r'

        def convert(word, from_pos, to_pos):
            """ Transform words given from/to POS tags """

            synsets = wordnet.synsets(word, pos=from_pos)

            # Word not found
            if not synsets:
                return []

            # Get all lemmas of the word (consider 'a'and 's' equivalent)
            lemmas = [l for s in synsets
                      for l in s.lemmas
                      if s.name.split('.')[1] == from_pos
                            or from_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)
                                and s.name.split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)]
            # Get related forms
            derivationally_related_forms = [(l, l.derivationally_related_forms()) for l in lemmas]

            # filter only the desired pos (consider 'a' and 's' equivalent)
            related_noun_lemmas = [l for drf in derivationally_related_forms
                                        for l in drf[1]
                                        if l.synset.name.split('.')[1] == to_pos
                                            or to_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)
                                                and l.synset.name.split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)]


            # Extract the words from the lemmas
            words = [l.name for l in related_noun_lemmas]
            len_words = len(words)

            # Build the result in the form of a list containing tuples (word, probability)
            result = [(w, float(words.count(w)) / len_words) for w in set(words)]
            result.sort(key=lambda w: -w[1])

            # return all the possibilities sorted by probability
            return result