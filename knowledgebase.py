from pyknow import *

from nlpu import *

# Global Variables
lastBotReply = 0
uInput = ''
orig = ''
dest = ''
origDepDate = ''
origDepTime = ''


class information(Fact):
    booking = Field(bool, default=False)

    origin = Field(str, mandatory=True)
    destination = Field(str, mandatory=True)
    originDepDate = Field(str, mandatory=True)
    originDepTime = Field(str, mandatory=True)

    wantsReturn = Field(bool, default=False)
    returnDepDate = Field(str)
    returnDepTime = Field(str)

    isCorrect = Field(bool, default=False)


class Action(Fact):
    pass

class trainBot(KnowledgeEngine):

    def passReply(userInput, self):
        global uInput
        uInput = userInput
        def switch_demo(lastbotreply):
            switcher = {
                0: 'get-human-answer',
                1: 'receive-origin',
                2: 'receive-destination',
                3: 'is-correct',
                4: 'receive-origin-dep-date'
            }
            return switcher.get(lastBotReply)

        global lastBotReply
        self.declare(Action(switch_demo(lastBotReply)))


    def yes_or_no(self, question):
        return input(question).upper().startswith('Y')

    @DefFacts()
    def bot_rules(self):
        yield information(booking=False, wantsReturn=False, isCorrect=False, origin='', destination='',
                          originDepDate='', originDepTime='')

    @Rule()
    def startup(self):
        from main import botUpdate
        global lastBotReply
        lastBotReply = 0
        botUpdate('Hello, how may I help you today?')
        botUpdate('e.g. Can I book a train ticket, Get trains times for...')

    # Do they want to book a ticket
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking = False))
    def get_human_answer(self, f1, f2):
        self.retract(f1)
        # print("Would you like to book a ticket?")
        question = uInput
        res = tuple(Custom_pos_tag(word_tokenize(question)))

        if ('book', 'VB') in res:
            print("Booking = True")
            self.modify(f2, booking = True)
            self.declare(Action('get-human-answer'))
            # print(res)
        else:
            self.declare(Action('unknown-input'))

        # print(findLocations(res))

    # Asks the origin
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True, origin=''))
    def get_human_origin(self, f1, f2):
        self.retract(f1)
        from main import botUpdate
        global lastBotReply
        lastBotReply = 1
        botUpdate('Where are you departing from?')

    # Receives the origin
    @Rule(AS.f1 << Action('receive-origin'),
          AS.f2 << information(booking=True, origin=''))
    def receive_origin(self, f2):
        answer = uInput
        self.modify(f2, origin = answer)
        global orig
        orig = uInput
        self.declare(Action('get-human-answer'))

    # Gets the destination
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True, destination=''))
    def get_human_destination(self, f1):
        self.retract(f1)
        from main import botUpdate
        global lastBotReply
        lastBotReply = 2
        botUpdate('Where would you like to go?')

    # Receives the destination
    @Rule(AS.f1 << Action('receive-destination'),
          AS.f2 << information(booking=True, destination=''))
    def receive_destination(self, f2):
        answer = uInput
        self.modify(f2, destination=answer)
        global dest
        dest = uInput
        self.declare(Action('get-human-answer'))

    # Gets the origin departure date
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True, originDepDate=''))
    def get_origin_dep_date(self, f1):
        self.retract(f1)
        from main import botUpdate
        global lastBotReply
        lastBotReply = 4
        botUpdate('What date would you like to go? Please enter in dd/mm/yy format')

    # Receives the origin departure date
    @Rule(AS.f1 << Action('receive-origin-dep-date'),
          AS.f2 << information(booking=True, originDepDate=''))
    def receive_origin_dep_date(self, f2):
        answer = uInput
        self.modify(f2, originDepDate=answer)
        global origDepDate
        origDepDate = uInput
        self.declare(Action('get-human-answer'))

    # Do they want a return
    # @Rule(AS.f1 << Action('get-human-answer'),
    #       AS.f2 << information(booking=True, wants))
    # def wantReturn(self, f1 , f2):

    # Has everything
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True),
          NOT(information(origin='')),
          NOT(information(destination=''))
          )
    def has_everything(self, f1):
        self.retract(f1)
        print('It has everything')
        self.declare(Action('check-info'))

    @Rule(AS.f1 << Action('check-info'), AS.f2 << information(
        booking=MATCH.book,
        origin=MATCH.org,
        destination=MATCH.dest,
        originDepDate=MATCH.orgDepDate,
        # originDepTime=MATCH.orgDepTime,
        # wantsReturn=MATCH.wantsRet,
        # returnDepDate=MATCH.retDepDate,
        # returnDepTime=MATCH.retDepTime
                               ))
    def check_info(self, f1, org, dest, orgDepDate):
        self.retract(f1)
        from main import botUpdate
        global lastBotReply
        lastBotReply = 3
        botUpdate('You want to book a ticket to go from %s to %s on %s.' % (org, dest, orgDepDate))
        botUpdate('Is this correct yes or no?')

    @Rule(AS.f1 << Action('is-correct'),
          AS.f2 << information(isCorrect=False))
    def receive_is_correct(self, f2):
        answer = uInput
        if answer == ('yes' or 'y' or 'Y'):
            self.modify(f2, isCorrect=True)
            print('Ready to request actual data!')

            # self.declare(Action('get-human-answer'))

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
        from main import botUpdate
        botUpdate("I'm sorry, I didn't understand that. Please try again.")
        # print("I'm sorry, I didn't understand that. Please try again.")
