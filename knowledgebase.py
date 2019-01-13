from pyknow import *

from nlpu import *

# Global Variables
lastBotReply = 0
uInput = ''
orig = ''
dest = ''
origDepDate = ''
origDepTime = ''
retDepDate = ''
retDepTime = ''
wantsRet = False
delayDepDate = ''
delayDepTime = ''
origCode = ''
destCode = ''

class information(Fact):
    booking = Field(bool, default=False)
    wantsPredicted = Field(bool, default=False)

    origin = Field(str)
    destination = Field(str)
    originDepDate = Field(str)
    originDepTime = Field(str)

    askedReturn = Field(bool)
    wantsReturn = Field(bool)
    returnDepDate = Field(str)
    returnDepTime = Field(str)

    isCorrect = Field(bool, default=False)


class Action(Fact):
    pass

class trainBot(KnowledgeEngine):

    def passReply(userInput, engine):
        global uInput
        uInput = userInput.lower()
        def switch_demo(lastbotreply):
            switcher = {
                0: 'get-human-answer',
                1: 'receive-origin',
                2: 'receive-destination',
                3: 'is-correct',
                4: 'receive-origin-dep-date',
                5: 'receive-origin-dep-time',
                6: 'request-data',
                7: 'want-return',
                8: 'receive-return-dep-date',
                9: 'receive-return-dep-time'
            }
            return switcher.get(lastBotReply)

        global lastBotReply
        engine.declare(Action(switch_demo(lastBotReply)))

    def yes_or_no(self, question):
        return input(question).upper().startswith('Y')

    @DefFacts()
    def bot_rules(self):
        yield information(booking=False, wantsPredicted=False, isCorrect=False, origin='', destination='',
                          wantsReturn=False, askedReturn=False, originDepDate='', originDepTime='',
                          returnDepDate='', returnDepTime='')

    @Rule()
    def startup(self):
        from main import botUpdate
        global lastBotReply
        lastBotReply = 0
        botUpdate('Hello, how may I help you today?')
        botUpdate('e.g. Can I book a train ticket, Get my predicted arrival time...')
        botUpdate('Please enter dates in the format: dd/mm/yy, and times in the 24hr format: hh:mm')

    # Do they want to book a ticket
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=False, wantsPredicted=False))
    def receive_human_answer(self, f1, f2):
        self.retract(f1)
        question = uInput
        res = tuple(Custom_pos_tag(word_tokenize(question)))
        print(res)
        if wantsTicket(res):
            res = removeWantsTicketPart(res)
            print(res)
            destin = ''
            origi = ''
            origiDepDate = ''
            origiDepTime = ''
            wanRet = False
            retiDepDate = ''
            retiDepTime = ''
            origiCode = ''
            destinCode = ''
            loc = findINandTO(res)
            print(loc)
            if loc:
                global dest, orig, destCode, origCode
                if loc[0][1] == 'IN':
                    origi = loc[1][0]
                    orig = origi
                    origiCode = getStationCode(loc[1][0])
                    origCode = origiCode
                    if len(loc) > 2:
                        destin = loc[3][0]
                        dest = destin
                        destinCode = getStationCode(loc[3][0])
                        destCode = destinCode
                elif loc[0][1] == 'TO':
                    destin = loc[1][0]
                    dest = destin
                    destinCode = getStationCode(loc[1][0])
                    destCode = destinCode
                    if len(loc) > 2:
                        origi = loc[3][0]
                        orig = origi
                        origiCode = getStationCode(loc[3][0])
                        origCode = origiCode

            if dateInFirstMessage(res):
                global origDepDate
                origDepDate = dateInFirstMessage(res)
                origiDepDate = dateInFirstMessage(res)

            if timeInFirstMessage(res):
                global origDepTime
                origDepTime = timeInFirstMessage(res)
                origiDepTime = timeInFirstMessage(res)

            if wantsReturn(res):
                global wantsRet
                wantsRet = wantsReturn(res)
                wanRet = wantsReturn(res)

            if retDateInFirstMessage(res):
                global retDepDate
                retDepDate = retDateInFirstMessage(res)
                retiDepDate = retDateInFirstMessage(res)

            if retTimeInFirstMessage(res):
                global retDepTime
                retDepTime = retTimeInFirstMessage(res)
                retiDepTime = retTimeInFirstMessage(res)

            self.modify(f2, booking=True, destination=destin, origin=origi, originDepDate=origiDepDate,
                        originDepTime=origiDepTime, wantsReturn=wanRet, returnDepDate=retiDepDate,
                        returnDepTime=retiDepTime)
            self.declare(Action('get-human-answer'))
        elif wantsPredicted(res):
            # print("They want to get train delay information")


            if dateInFirstMessage(res):
                global delayDepDate
                delayDepDate = dateInFirstMessage(res)
                origiDepDate = dateInFirstMessage(res)

            if timeInFirstMessage(res):
                global delayDepTime
                delayDepTime = timeInFirstMessage(res)
                origiDepTime = timeInFirstMessage(res)

            self.modify(f2, wantsPredicted=True)



        else:
            from main import botUpdate
            botUpdate("Sorry I didn't understand what you said. Could you please try again?")


    # Asks the origin
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True, origin=''))
    def get_human_origin(self, f1, f2):
        try:
            self.retract(f1)
            # self.retract(f2)
        except:
            pass
        else:
            from main import botUpdate
            global lastBotReply
            lastBotReply = 1
            botUpdate('Where are you departing from?')

    # Receives the origin
    @Rule(AS.f1 << Action('receive-origin'),
          AS.f2 << information(booking=True, origin=''))
    def receive_origin(self, f1, f2):
        try:
            self.retract(f1)
        except:
            pass
        else:
            answer = uInput
            if isRealStation(answer):
                self.modify(f2, origin=answer)
                global orig, origCode
                orig = uInput
                origCode = getStationCode(uInput)
                self.declare(Action('get-human-answer'))
            else:
                from main import botUpdate
                botUpdate("Sorry I didn't recognise that station. Cloud you please try again?")

    # Gets the destination
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True, destination=''))
    def get_human_destination(self, f1, f2):
        try:
            self.retract(f1)
            # self.retract(f2)
        except:
            pass
        else:
            from main import botUpdate
            global lastBotReply
            lastBotReply = 2
            botUpdate('Where would you like to go?')

    # Receives the destination
    @Rule(AS.f1 << Action('receive-destination'),
          AS.f2 << information(booking=True, destination=''))
    def receive_destination(self, f1, f2):
        try:
            self.retract(f1)
        except:
            pass
        else:
            answer = uInput
            if isRealStation(answer):
                self.modify(f2, destination=answer)
                global dest, destCode
                dest = uInput
                destCode = getStationCode(uInput)
                self.declare(Action('get-human-answer'))
            else:
                from main import botUpdate
                botUpdate("Sorry I didn't recognise that station. Could you please try again?")


    # Gets the origin departure date
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True, originDepDate=''))
    def get_origin_dep_date(self, f1, f2):
        try:
            self.retract(f1)
            # self.retract(f2)
        except:
            pass
        else:
            from main import botUpdate
            global lastBotReply
            lastBotReply = 4
            botUpdate('What date would you like to depart? Please enter in dd/mm/yy format.')

    # Receives the origin departure date
    @Rule(AS.f1 << Action('receive-origin-dep-date'),
          AS.f2 << information(booking=True, originDepDate=''))
    def receive_origin_dep_date(self, f1, f2):
        try:
            self.retract(f1)
        except:
            pass
        else:
            answer = uInput
            if isDateFormat(answer):
                self.modify(f2, originDepDate=answer)
                global origDepDate
                origDepDate = uInput
                self.declare(Action('get-human-answer'))
            else:
                from main import botUpdate
                botUpdate("Sorry that didn't seem to be the correct date format. Could you please try again?")
                botUpdate("i.e (dd/mm/yy) | 31/12/18")

    # Gets the origin departure time
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True, originDepTime=''))
    def get_origin_dep_time(self, f1, f2):
        try:
            self.retract(f1)
            # self.retract(f2)
        except:
            pass
        else:
            from main import botUpdate
            global lastBotReply
            lastBotReply = 5
            botUpdate('What time would you like depart? Please enter in hh:mm 24hr format.')

    # Receives the origin departure time
    @Rule(AS.f1 << Action('receive-origin-dep-time'),
          AS.f2 << information(booking=True, originDepTime=''))
    def receive_origin_dep_time(self, f1, f2):
        try:
            self.retract(f1)
        except:
            pass
        else:
            answer = uInput
            if isTimeFormat(answer) and isValidTime(answer):
                self.modify(f2, originDepTime=answer)
                global origDepTime
                origDepTime = uInput
                self.declare(Action('get-human-answer'))
            elif isValidTime(answer) == False and isTimeFormat(answer) == True:
                from main import botUpdate
                botUpdate("Sorry that didn't seem to be a valid time. Could you please try again?")
            else:
                from main import botUpdate
                botUpdate("Sorry that didn't seem to be the correct format. Could you please try again?")
                botUpdate("i.e (hh:mm) | 14:30")

    # Do they want a return
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True),
          NOT(information(origin='')),
          NOT(information(destination='')),
          NOT(information(originDepDate='')),
          NOT(information(originDepTime='')),
          information(askedReturn=False),
          information(wantsReturn=False)
          )
    def getWantReturn(self, f1, f2):
        self.retract(f1)
        from main import botUpdate
        global lastBotReply
        lastBotReply = 7
        botUpdate('Would you like a return ticket as well, yes or no?')

    # Do they want a return
    @Rule(AS.f1 << Action('want-return'),
          AS.f2 << information(booking=True, askedReturn=False, wantsReturn=False),
          NOT(information(origin='')),
          NOT(information(destination='')),
          NOT(information(originDepDate='')),
          NOT(information(originDepTime='')),
          )
    def receiveWantReturn(self, f1, f2):
        self.retract(f1)
        if uInput == ('yes' or 'y' or 'Y'):
            global wantsRet
            wantsRet = True
            self.modify(f2, wantsReturn=True, askedReturn=True)
        else:
            self.modify(f2, askedReturn=True)
        self.declare(Action('get-human-answer'))

    # Gets the return departure date
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True, wantsReturn=True, returnDepDate=''))
    def get_return_dep_date(self, f1, f2):
        self.retract(f1)
        from main import botUpdate
        global lastBotReply
        lastBotReply = 8
        botUpdate('What date would you like to return on? Please enter in dd/mm/yy format.')

    # Receives the return departure date
    @Rule(AS.f1 << Action('receive-return-dep-date'),
          AS.f2 << information(booking=True, wantsReturn=True, returnDepDate=''))
    def receive_return_dep_date(self, f1, f2):
        self.retract(f1)
        answer = uInput
        self.modify(f2, returnDepDate=answer)
        global retDepDate
        retDepDate = uInput
        self.declare(Action('get-human-answer'))

    # Gets the return departure time
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True, wantsReturn=True, returnDepTime=''))
    def get_return_dep_time(self, f1, f2):
        self.retract(f1)
        from main import botUpdate
        global lastBotReply
        lastBotReply = 9
        botUpdate('What time would you like your return ticket to be? Please enter in hh:mm 24 hr format.')

    # Receives the return departure time
    @Rule(AS.f1 << Action('receive-return-dep-time'),
          AS.f2 << information(booking=True, wantsReturn=True, returnDepTime=''))
    def receive_return_dep_time(self, f1, f2):
        self.retract(f1)
        answer = uInput
        self.modify(f2, returnDepTime=answer)
        global retDepTime
        retDepTime = uInput
        self.declare(Action('get-human-answer'))


    # Has everything
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True),
          NOT(information(origin='')),
          NOT(information(destination='')),
          NOT(information(originDepDate='')),
          NOT(information(originDepTime='')),
          OR(AND(information(wantsReturn=True), NOT(information(retDepDate='')), NOT(information(retDepTime=''))),
             AND(information(wantsReturn=False), information(askedReturn=True)))
          )
    def has_everything(self, f1, f2):
        self.retract(f1)
        # self.retract(f2)
        # print('It has everything')
        self.declare(Action('check-info'))

    @Rule(AS.f1 << Action('check-info'),
          AS.f2 << information(
            booking=MATCH.book,
            origin=MATCH.org,
            destination=MATCH.dest,
            originDepDate=MATCH.orgDepDate,
            originDepTime=MATCH.orgDepTime,
            wantsReturn=MATCH.wantsRet,
            returnDepDate=MATCH.retDepDate,
            returnDepTime=MATCH.retDepTime
            )
          )
    def check_info(self, f1, f2, org, dest, orgDepDate, orgDepTime, wantsRet, retDepDate, retDepTime):
        self.retract(f1)
        from main import botUpdate
        global lastBotReply
        lastBotReply = 3
        botUpdate('You want to book a ticket to go from %s to %s on %s at %s.' % (org.title(), dest.title(), orgDepDate, orgDepTime))
        if wantsRet:
            botUpdate('And you want to return on %s at %s.' % (retDepDate, retDepTime))
        botUpdate('Is this information correct yes or no?')

    @Rule(AS.f1 << Action('is-correct'),
          AS.f2 << information(isCorrect=False))
    def receive_is_correct(self, f1, f2):
        self.retract(f1)
        answer = uInput
        if answer == ('yes' or 'y' or 'Y'):
            self.modify(f2, isCorrect=True)
            # print('Ready to request actual data!')
            from nrailFareInfo import getFareInfo
            from main import botUpdate
            global orig, dest, origDepDate, origDepTime, wantsRet, retDepDate, retDepTime

            theURL = getFareInfo(orig, dest, origDepDate, origDepTime, wantsRet, retDepDate, retDepTime)
            botUpdate(theURL)

    # @Rule(AS.f1 << Action('determine-another-question'))
    # def another_question(self, f1):
    #     self.retract(f1)
    #     if not self.yes_or_no("Do you have another question?"):
    #         print("Thanks for using me, and I hope everything worked sufficiently")
    #     else:
    #         print("How may i help you today?")
    #         self.declare(Action('get-human-answer'))
    #
    # @Rule(AS.f1 << Action('unknown-input'))
    # def unknown_input(self, f1):
    #     self.retract(f1)
    #     from main import botUpdate
    #     botUpdate("I'm sorry, I didn't understand that. Please try again.")
    #     # print("I'm sorry, I didn't understand that. Please try again.")

################################################################################
##########################  Section 2  #########################################














