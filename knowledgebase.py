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
delayByTime = ''


class information(Fact):
    booking = Field(bool, default=False)

    origin = Field(str)
    destination = Field(str)
    originDepDate = Field(str)
    originDepTime = Field(str)

    askedReturn = Field(bool)
    wantsReturn = Field(bool)
    returnDepDate = Field(str)
    returnDepTime = Field(str)

    isCorrect = Field(bool, default=False)

    wantsPredicted = Field(bool, default=False)
    delayDepDate = Field(str)
    delayDepTime = Field(str)
    delayDestCode = Field(str)
    delayCurrCode = Field(str)
    delayedBy = Field(str)


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
                9: 'receive-return-dep-time',
                10: 'receive-current',
                11: 'receive-delay-destination',
                12: 'receive-delayed-by',
                13: 'is-delay-correct'
            }
            return switcher.get(lastBotReply)

        global lastBotReply
        engine.declare(Action(switch_demo(lastBotReply)))

    @DefFacts()
    def bot_rules(self):
        yield information(booking=False, wantsPredicted=False, isCorrect=False, origin='', destination='',
                          wantsReturn=False, askedReturn=False, originDepDate='', originDepTime='',
                          returnDepDate='', returnDepTime='', delayDepDate='', delayDepTime='', delayDestCode='',
                          delayCurrCode='', delayedBy='')

    @Rule()
    def startup(self):
        from main import botUpdate
        global lastBotReply
        lastBotReply = 0
        botUpdate('Hello, how may I help you today?')
        botUpdate('e.g. Can I book a train ticket, Get my predicted arrival time...')
        botUpdate('Please enter in the format: dd/mm/yy, today, tomorrow, and time in the 24hr format: hh:mm')

    # Do they want to book a ticket
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=False, wantsPredicted=False))
    def receive_human_answer(self, f1, f2):
        self.retract(f1)
        global dest, orig, destCode, origCode
        question = uInput
        res = tuple(Custom_pos_tag(word_tokenize(question)))
        # print(res)
        destin = ''
        origi = ''
        origiDepDate = ''
        origiDepTime = ''
        wanRet = False
        retiDepDate = ''
        retiDepTime = ''
        origiCode = ''
        destinCode = ''
        if wantsTicket(res):
            if wantsReturn(res):
                global wantsRet
                wantsRet = wantsReturn(res)
                wanRet = wantsReturn(res)
            res = removeWantsTicketPart(res)
            loc = findINandTO(res)
            if loc:
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

            if retDateInFirstMessage(res) != '':
                global retDepDate
                retDepDate = retDateInFirstMessage(res)
                retiDepDate = retDateInFirstMessage(res)

            if retTimeInFirstMessage(res) != '':
                global retDepTime
                retDepTime = retTimeInFirstMessage(res)
                retiDepTime = retTimeInFirstMessage(res)

            self.modify(f2, booking=True, destination=destin, origin=origi, originDepDate=origiDepDate,
                        originDepTime=origiDepTime, wantsReturn=wanRet, returnDepDate=retiDepDate,
                        returnDepTime=retiDepTime)
            self.declare(Action('get-human-answer'))

        elif wantsPredicted(res):
            res = removeWantsTicketPart(res)
            delDepDate = ''
            delDepTime = ''

            loc = findINandTO(res)
            if loc:
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
                global delayDepDate
                delayDepDate = dateInFirstMessage(res)
                delDepDate = dateInFirstMessage(res)

            if timeInFirstMessage(res):
                global delayDepTime
                delayDepTime = timeInFirstMessage(res)
                delDepTime = timeInFirstMessage(res)

            self.modify(f2, wantsPredicted=True, delayCurrCode=origiCode, delayDestCode=destinCode,
                        delayDepDate=delDepDate, delayDepTime=delDepTime)

            self.declare(Action('get-human-answer'))

        else:
            from main import botUpdate
            botUpdate("Sorry I didn't understand what you said. Could you please try again?")

    # Asks the origin
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True, origin=''))
    def get_human_origin(self, f1):
        try:
            self.retract(f1)
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
            if isRealStation(uInput):
                self.modify(f2, origin=uInput)
                global orig, origCode
                orig = uInput
                origCode = getStationCode(uInput)
                self.declare(Action('get-human-answer'))
            elif len(hasMultipule(uInput)) > 1:
                from main import botUpdate
                locations = hasMultipule(uInput)
                botUpdate("Did you mean? " + str(locations))
            else:
                from main import botUpdate
                botUpdate("Sorry I didn't recognise that station. Could you please try again?")

    # Gets the destination
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True, destination=''))
    def get_human_destination(self, f1):
        try:
            self.retract(f1)
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
            if isRealStation(uInput):
                self.modify(f2, destination=uInput)
                global dest, destCode
                dest = uInput
                destCode = getStationCode(uInput)
                self.declare(Action('get-human-answer'))
            elif len(hasMultipule(uInput)) > 1:
                from main import botUpdate
                locations = hasMultipule(uInput)
                botUpdate("Did you mean? " + str(locations))
            else:
                from main import botUpdate
                botUpdate("Sorry I didn't recognise that station. Could you please try again?")

    # Gets the origin departure date
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True, originDepDate=''))
    def get_origin_dep_date(self, f1):
        try:
            self.retract(f1)
        except:
            pass
        else:
            from main import botUpdate
            global lastBotReply
            lastBotReply = 4
            botUpdate('What date would you like to depart?')
            botUpdate('Please enter in dd/mm/yy format or common words like today and tomorrow.')

    # Receives the origin departure date
    @Rule(AS.f1 << Action('receive-origin-dep-date'),
          AS.f2 << information(booking=True, originDepDate=''))
    def receive_origin_dep_date(self, f1, f2):
        try:
            self.retract(f1)
        except:
            pass
        else:
            if isDateFormat(isDateWord(uInput)):
                self.modify(f2, originDepDate=isDateWord(uInput))
                global origDepDate
                origDepDate = isDateWord(uInput)
                self.declare(Action('get-human-answer'))
            else:
                from main import botUpdate
                botUpdate("Sorry that didn't seem to be the correct date format. Could you please try again?")
                botUpdate("i.e (dd/mm/yy) | 31/12/18 | today | tomorrow")

    # Gets the origin departure time
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True, originDepTime=''))
    def get_origin_dep_time(self, f1):
        try:
            self.retract(f1)
        except:
            pass
        else:
            from main import botUpdate
            global lastBotReply
            lastBotReply = 5
            botUpdate('What time would you like depart?')
            botUpdate('Please enter in hh:mm 24hr format.')

    # Receives the origin departure time
    @Rule(AS.f1 << Action('receive-origin-dep-time'),
          AS.f2 << information(booking=True, originDepTime=''))
    def receive_origin_dep_time(self, f1, f2):
        try:
            self.retract(f1)
        except:
            pass
        else:
            if isTimeFormat(uInput) and isValidTime(uInput):
                self.modify(f2, originDepTime=uInput)
                global origDepTime
                origDepTime = uInput
                self.declare(Action('get-human-answer'))
            elif isValidTime(uInput) == False and isTimeFormat(uInput) == True:
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
    def getWantReturn(self, f1):
        try:
            self.retract(f1)
        except:
            pass
        else:
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
        try:
            self.retract(f1)
        except:
            pass
        else:
            if uInput == ('yes' or 'y' or 'Y'):
                global wantsRet
                wantsRet = True
                self.modify(f2, wantsReturn=True, askedReturn=True)
            elif uInput == ('no' or 'n' or 'N'):
                self.modify(f2, askedReturn=True)
            else:
                from main import botUpdate
                botUpdate("Sorry, I didn't understand that. Enter yes or no.")
            self.declare(Action('get-human-answer'))

    # Gets the return departure date
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True, wantsReturn=True, returnDepDate=''))
    def get_return_dep_date(self, f1):
        try:
            self.retract(f1)
        except:
            pass
        else:
            from main import botUpdate
            global lastBotReply
            lastBotReply = 8
            botUpdate('What date would you like to return on?')
            botUpdate('Please enter in dd/mm/yy format or common words like today and tomorrow.')

    # Receives the return departure date
    @Rule(AS.f1 << Action('receive-return-dep-date'),
          AS.f2 << information(booking=True, wantsReturn=True, returnDepDate=''))
    def receive_return_dep_date(self, f1, f2):
        try:
            self.retract(f1)
        except:
            pass
        else:
            if isDateFormat(isDateWord(uInput)):
                self.modify(f2, returnDepDate=isDateWord(uInput))
                global retDepDate
                retDepDate = isDateWord(uInput)
                self.declare(Action('get-human-answer'))
            else:
                from main import botUpdate
                botUpdate("Sorry that didn't seem to be the correct date format. Could you please try again?")
                botUpdate("i.e (dd/mm/yy) | 31/12/18 | today | tomorrow")

    # Gets the return departure time
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(booking=True, wantsReturn=True, returnDepTime=''))
    def get_return_dep_time(self, f1):
        try:
            self.retract(f1)
        except:
            pass
        else:
            from main import botUpdate
            global lastBotReply
            lastBotReply = 9
            botUpdate('What time would you like your return ticket to be?')
            botUpdate('Please enter in hh:mm 24hr format.')

    # Receives the return departure time
    @Rule(AS.f1 << Action('receive-return-dep-time'),
          AS.f2 << information(booking=True, wantsReturn=True, returnDepTime=''))
    def receive_return_dep_time(self, f1, f2):
        try:
            self.retract(f1)
        except:
            pass
        else:
            if isTimeFormat(uInput) and isValidTime(uInput):
                self.modify(f2, returnDepTime=uInput)
                global retDepTime
                retDepTime = uInput
                self.declare(Action('get-human-answer'))
            elif isValidTime(uInput) is False and isTimeFormat(uInput) is True:
                from main import botUpdate
                botUpdate("Sorry that didn't seem to be a valid time. Could you please try again?")
            else:
                from main import botUpdate
                botUpdate("Sorry that didn't seem to be the correct format. Could you please try again?")
                botUpdate("i.e (hh:mm) | 14:30")

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
    def has_everything(self, f1):
        try:
            self.retract(f1)
        except:
            pass
        else:
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
    def check_info(self, f1, org, dest, orgDepDate, orgDepTime, wantsRet, retDepDate, retDepTime):
        try:
            self.retract(f1)
        except:
            pass
        else:
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
        try:
            self.retract(f1)
        except:
            pass
        else:
            from main import botUpdate
            if uInput == ('yes' or 'y' or 'Y'):
                self.modify(f2, isCorrect=True)
                from nrailFareInfo import getFareInfo
                global orig, dest, origDepDate, origDepTime, wantsRet, retDepDate, retDepTime
                try:
                    theURL = getFareInfo(orig, dest, origDepDate, origDepTime, wantsRet, retDepDate, retDepTime)
                    botUpdate(theURL)
                except:
                    botUpdate("Sorry, something went wrong could you please try again.")
            elif uInput == ('no' or 'n' or 'N'):
                from main import restartChat
                restartChat()
            else:
                botUpdate("Sorry, I didn't understand that. Enter yes or no.")

################################################################################
##########################  Section 2  #########################################
################################################################################

    # Gets the destination
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(wantsPredicted=True, delayDestCode=''))
    def get_delay_destination(self, f1):
        try:
            self.retract(f1)
        except:
            pass
        else:
            from main import botUpdate
            global lastBotReply
            lastBotReply = 11
            botUpdate('What station is your destination?')

    # Receives the destination
    @Rule(AS.f1 << Action('receive-delay-destination'),
          AS.f2 << information(wantsPredicted=True, delayDestCode=''))
    def receive__delay_destination(self, f1, f2):
        try:
            self.retract(f1)
        except:
            pass
        else:
            if isRealStation(uInput):
                global dest, destCode
                dest = uInput
                destCode = getStationCode(uInput)
                self.modify(f2, delayDestCode=destCode)
                self.declare(Action('get-human-answer'))
            elif len(hasMultipule(uInput)) > 1:
                from main import botUpdate
                locations = hasMultipule(uInput)
                botUpdate("Did you mean? " + str(locations))
            else:
                from main import botUpdate
                botUpdate("Sorry I didn't recognise that station. Could you please try again?")

    # Asks the origin/current location
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(wantsPredicted=True, delayCurrCode=''))
    def get_delay_origin(self, f1):
        try:
            self.retract(f1)
        except:
            pass
        else:
            from main import botUpdate
            global lastBotReply
            lastBotReply = 10
            botUpdate('What station are you currently at?')

    # Receives the origin/current location
    @Rule(AS.f1 << Action('receive-current'),
          AS.f2 << information(wantsPredicted=True, delayCurrCode=''))
    def receive_delay_origin(self, f1, f2):
        try:
            self.retract(f1)
        except:
            pass
        else:
            if isRealStation(uInput):
                global orig, origCode
                orig = uInput
                origCode = getStationCode(uInput)
                self.modify(f2, delayCurrCode=origCode)
                self.declare(Action('get-human-answer'))
            elif len(hasMultipule(uInput)) > 1:
                from main import botUpdate
                locations = hasMultipule(uInput)
                botUpdate("Did you mean? " + str(locations))
            else:
                from main import botUpdate
                botUpdate("Sorry I didn't recognise that station. Could you please try again?")

    # Gets the travel date
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(wantsPredicted=True, delayDepDate=''))
    def get_origin_del_dep_date(self, f1):
        try:
            self.retract(f1)
        except:
            pass
        else:
            from main import botUpdate
            global lastBotReply
            lastBotReply = 4
            botUpdate('What date are you traveling?')

    # Receives the travel date
    @Rule(AS.f1 << Action('receive-origin-dep-date'),
          AS.f2 << information(wantsPredicted=True, delayDepDate=''))
    def receive_origin_del_dep_date(self, f1, f2):
        try:
            self.retract(f1)
        except:
            pass
        else:
            if isDateFormat(isDateWord(uInput)):
                global delayDepDate
                delayDepDate = isDateWord(uInput)
                self.modify(f2, delayDepDate=isDateWord(uInput))
                self.declare(Action('get-human-answer'))
            else:
                from main import botUpdate
                botUpdate("Sorry that didn't seem to be the correct date format. Could you please try again?")
                botUpdate("i.e (dd/mm/yy) | 31/12/18")

    # Gets the origin departure time
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(wantsPredicted=True, delayDepTime=''))
    def get_origin_del_dep_time(self, f1):
        try:
            self.retract(f1)
        except:
            pass
        else:
            from main import botUpdate
            global lastBotReply
            lastBotReply = 5
            botUpdate('What time are you travelling?')

    # Receives the origin departure time
    @Rule(AS.f1 << Action('receive-origin-dep-time'),
          AS.f2 << information(wantsPredicted=True, delayDepTime=''))
    def receive_origin_del_dep_time(self, f1, f2):
        try:
            self.retract(f1)
        except:
            pass
        else:
            if isTimeFormat(uInput) and isValidTime(uInput):
                global delayDepTime
                delayDepTime = uInput
                self.modify(f2, delayDepTime=delayDepTime)
                self.declare(Action('get-human-answer'))
            elif isValidTime(uInput) is False and isTimeFormat(uInput) is True:
                from main import botUpdate
                botUpdate("Sorry that didn't seem to be a valid time. Could you please try again?")
            else:
                from main import botUpdate
                botUpdate("Sorry that didn't seem to be the correct format. Could you please try again?")
                botUpdate("i.e (hh:mm) | 14:30")

    # Asks how much they are delayed by
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(wantsPredicted=True, delayedBy=''))
    def get_delayed_by(self, f1):
        try:
            self.retract(f1)
        except:
            pass
        else:
            from main import botUpdate
            global lastBotReply
            lastBotReply = 12
            botUpdate('How many minutes are you delayed by?')

    # Receives how much they are delayed by
    @Rule(AS.f1 << Action('receive-delayed-by'),
          AS.f2 << information(wantsPredicted=True, delayedBy=''))
    def receive_delayed_by(self, f1, f2):
        try:
            self.retract(f1)
        except:
            pass
        else:
            if isNumber(uInput):
                global delayByTime
                delayByTime = uInput
                self.modify(f2, delayedBy=delayByTime)
                self.declare(Action('get-human-answer'))
            else:
                from main import botUpdate
                botUpdate("Sorry that doesn't seem to be valid. Could you please try again?")

    # Has everything
    @Rule(AS.f1 << Action('get-human-answer'),
          AS.f2 << information(wantsPredicted=True),
          NOT(information(delayDepDate='')),
          NOT(information(delayDepTime='')),
          NOT(information(delayDestCode='')),
          NOT(information(delayCurrCode='')),
          NOT(information(delayedBy=''))
          )
    def has_everything_delay(self, f1):
        try:
            self.retract(f1)
        except:
            pass
        else:
            self.declare(Action('check-delay-info'))

    @Rule(AS.f1 << Action('check-delay-info'),
          AS.f2 << information(
              wantsPredicted=MATCH.wantPredic,
              delayDepDate=MATCH.delDepD,
              delayDepTime=MATCH.delDepT,
              delayDestCode=MATCH.delDest,
              delayCurrCode=MATCH.delCurr,
              delayedBy=MATCH.delBy)
          )
    def check_info_delay(self, f1, wantPredic, delDepD, delDepT, delDest, delCurr, delBy):
        try:
            self.retract(f1)
        except:
            pass
        else:
            from main import botUpdate
            global lastBotReply, orig, dest
            lastBotReply = 13
            botUpdate('You want to check the predicted train delay from %s to %s on %s at %s' % \
                (orig.title(), dest.title(), delDepD, delDepT))
            botUpdate('Is this information correct yes or no?')

    @Rule(AS.f1 << Action('is-delay-correct'),
          AS.f2 << information(isCorrect=False))
    def receive_is_correct_delay(self, f1, f2):
        try:
            self.retract(f1)
        except:
            pass
        else:
            from main import botUpdate
            if uInput == ('yes' or 'y' or 'Y'):
                self.modify(f2, isCorrect=True)
                from hspTrainInfo import getPredictedDelay
                global origCode, destCode, delayByTime, delayDepDate, delayDepTime
                try:
                    predictedDelay = getPredictedDelay(origCode, destCode, int(delayByTime), delayDepDate, delayDepTime)
                except:
                    botUpdate("Sorry, something went wrong.")
                else:
                    if int(predictedDelay) > 0:
                        botUpdate('We expect a delay of %s minute(s)' % predictedDelay)
                    elif int(predictedDelay) < 0:
                        predictedDelay = int(predictedDelay) * -1
                        botUpdate('We expect it will be %s minute(s) early' % predictedDelay)
                    else:
                        botUpdate('We expect your train to be on time!')
            elif uInput == ('no' or 'n' or 'N'):
                from main import restartChat
                restartChat()
            else:
                botUpdate("Sorry, I didn't understand that. Enter yes or no.")
