from pyknow import *
from nlpu import *
from nlp_customTagger import *
from nlp_testGround import *


class information(Fact):
    origin = Field(str, mandatory=True, default='')

    destination = Field(str, mandatory=True, default='')
    originDepDate = Field(str, default="")
    originDepTime = Field(str,default="")

    wantsReturn = Field(bool, default=False)
    booking = Field(bool, default=False)

    returnDepDate = Field(str,default="")
    returnDepTime = Field(str,default="")

    userInput = Field(str, default="")
    botReply = Field(str, default="")

class Action(Fact):
    pass

class userAnswer(Fact):
    pass

class ComputerQuestion(Fact):
    pass

class trainBot(KnowledgeEngine):
    def yes_or_no(self, question):
        return input(question).upper().startswith('Y')

    @DefFacts()
    def bot_rules(self):
        yield information(booking = False, origin = '', destination ='')

    @Rule()
    def startup(self):
        print("Hello, how may I help you today?")
        # print("Please enter a quesiton I can help you with today,")
        print("e.g. Can I book a train ticket, Get trains times for...")

        self.declare(Action('get-human-answer'))

#Do they want to book a ticket
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking = False))
    def get_human_answer(self, f1, f2):
        self.retract(f1)
        print("Would you like to book a ticket?")
        question = input()
        res =  tuple(Custom_pos_tag(word_tokenize(question)))
        self.declare(userAnswer(res))

        #self.declare(information(findLocations(res)))

        if ('book', 'VB') in res:
            print("Booking = True")
            self.modify(f2, booking = True)
            self.declare(Action('get-human-answer'))
            print(res)
        else:
            self.declare(Action('unknown-input'))

        # print(findLocations(res))


#Gets the origin
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True, origin=''))
    def get_human_origin(self, f1, f2):
        self.retract(f1)
        print("where are you departing from?")
        answer = input()
        self.modify(f2, origin = answer)
        self.declare(Action('get-human-answer'))

#Gets the destination
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True, destination=''))
    def get_human_destination(self, f1, f2):
        self.retract(f1)
        print("Where would you like to go?")
        answer = input()
        self.modify(f2, destination=answer)
        self.declare(Action('get-human-answer'))

#Do they want a return
    # @Rule(AS.f1 << Action('get-human-answer'),
    #       AS.f2 << information(booking=True, wants))
    # def wantReturn(self, f1 , f2):

#Has everything
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True))
    def has_everything(self, f1):
        self.retract(f1)

        self.declare(Action('check-information'))


    @Rule(AS.f1 << Action('check-information'),
          AS.f2 << information(
                               booking = MATCH.book,
                               origin = MATCH.org,
                               destination = MATCH.dest,
                               originDepDate = MATCH.orgDepDate,
                               originDepTime = MATCH.orgDepTime,
                               wantsReturn = MATCH.wantsRet,
                               returnDepDate = MATCH.retDepDate,
                               returnDepTime = MATCH.retDepTime
                               ))
    def check_information(self, f1, f2, book, org, dest, orgDepDate, orgDepTime,
                          wantsRet,retDepDate, retDepTime):
        self.retract(f1)
        print("The Origin is: " + org)
        print("The destination is: " + dest)

        print("Is this correct?")

        self.declare(Action('determine-another-question'))


    @Rule(AS.f1 << Action('determine-another-question'))
    def another_question(self, f1):
        self.retract(f1)
        if not self.yes_or_no("Do you have another question?"):
            print("Thanks for using me, and I hope everything worked sufficiently")
        else:
            print("How may i help you today?")
            self.declare(Action('get-human-answer'))


    @Rule(AS.f1 << Action('unknown-input'))
    def unknown_input(self, f1):
        self.retract(f1)
        print("I'm sorry, I didn't understand that. Please try again.")

engine = trainBot()
engine.reset()
engine.run()