import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
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


class processInput:
    """Class to take in an input and return what that input means"""
    userInput = []

    def __init__(self, sent):
        global userInput
        token = RegexpTokenizer(r'\w+')
        words = token.tokenize(sent)
        stop_words = set(stopwords.words("english"))
        #-----------------Removes 'a' 'to'  'in' etc...
        filtered_sent = []
        for w in words:
            if w not in stop_words:
                filtered_sent.append(w)
        #-----------------Removes -ing -ed -s
        lem = WordNetLemmatizer()
        lemmated = []
        for q in filtered_sent:
            lemmated.append(lem.lemmatize(q, "v"))

        userInput = lemmated
        # print("Individual Words:", userInput)


        # if (self.containsBRH() == True):
        #     print("The User wants to reserve a ticket.")



        # if (self.containsTime()[0] == True):
        #     print("The time given is: ", self.containsTime()[1])
        # else:
        #     print("No time given")

    def returnlist(self):
        global userInput
        return userInput

    def getVerbs(self):
        global userInput
        test = userInput
        #print(nltk.pos_tag(['He'] + test))

        taggedWords = nltk.pos_tag(userInput)
        print(taggedWords)

        if(self.containsBRH() == True):
            print("Hello World!")
            taggedWordsTrue = nltk.pos_tag(userInput)
            print(taggedWordsTrue)



        # for w in test:
        #     print(w)
        #     print(wordnet.synsets(w))
        #
        # # for w in test:
        # #     tmp = wordnet.synsets(w)[0].pos()
        # #     print (w, ":", tmp)
        #
        # test2 = nltk.pos_tag(test)
        # grammar = "NP: {<DT>?<JJ>*<NN>}"
        # cp = nltk.RegexpParser(grammar)
        # result = cp.parse(test2)
        # print("Result: ", result)
        # result.draw()

        #print(nltk.pos_tag(test))

        #https://www.nltk.org/book/ch05.html

    def containsBRH(self):
        global userInput

        bookingSynonyms = []
        for s in wordnet.synsets('reserve'):
            bookingSynonyms = s.lemma_names()
            #print(s.name(), s.lemma_names())

        #print(bookingSynonyms)

        for w in userInput:
            for b in bookingSynonyms:
                if(w == b):
                    #print("True")
                    return True
        #print("False")
        return False

    def containsTime(self):
        global userInput
        time = ""
        for w in userInput:
            if(w.isdigit()):
                time+=w

        if(time != ""):
            return True, time
        return False


        # for w in rawWords:
        #     if(time.strptime(w, '%H:%M')):
        #         return True, w
        # return False

            # try:
            #     time.strptime(w, '%H:%M')
            #     return True, w
            # except ValueError:
            #     return False


    def containsLoc(self):


        return True


    # def query(self):
    #     locs = [('Omnicom', 'IN', 'New York'),
    #             ('DDB Needham', 'IN', 'New York'),
    #             ('Kaplan Thaler Group', 'IN', 'New York'),
    #             ('BBDO South', 'IN', 'Atlanta'),
    #             ('Georgia-Pacific', 'IN', 'Atlanta')]
    #     query = [e1 for (e1, rel, e2) in locs if e2 == 'Atlanta']
    #     print(query)