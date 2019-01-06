from pyknow import *
from nlpu import *

# Global variables
orig = ""
dest = ""
uInput = ""
lastBotReply = ""

# After a user response is supplied the engine carries out all functions where teh rules are met

class trainBot(KnowledgeEngine):

    def passReply(userInput):
        global uInput
        uInput = userInput

    # Facts to initialise at the beginning of the chat
    @DefFacts()
    def _initial_action(self):
        yield Fact(begin='true')
        yield Fact(receivedInput='false')


    # Beginning of the conversation
    @Rule(Fact(begin='true'))
    def hello(self):
        from main import botUpdate
        botUpdate("Hello, what can I help you with?")
        global lastBotReply
        lastBotReply = "Hello, what can I help you with?"
        self.modify(self.facts[1], begin="false")

    # Just received user input
    @Rule(Fact(receivedInput='true'))
    def waiting(self):
        # print('it did something')
        # print(uInput)

        global orig, dest, lastBotReply

        processedInput = processInput(uInput)

        if 'book' in processedInput.returnlist():
            self.declare(Fact(book='true'))

        if lastBotReply == "Where would you like to go?":
            dest = uInput
            self.declare(Fact(destGiven="true"))

        if lastBotReply == "Where are you going from?":
            orig = uInput
            self.declare(Fact(origGiven="true"))

        if lastBotReply == 'You want to book a ticket to go from %s to %s is this correct yes or no?':
            if 'yes' in processedInput.returnlist():
                self.declare(Fact(correct='true'))

        engine.run()

    # They want to book a ticket, but no destination has been given
    @Rule(Fact(book='true'))
    def whereGo(self):
        from main import botUpdate
        botUpdate("Where would you like to go?")
        global lastBotReply
        lastBotReply = "Where would you like to go?"

    # They want to book a ticket, but no origin has been given
    @Rule(Fact(book='true'), Fact(destGiven="true"))
    def whereFrom(self):
        from main import botUpdate
        botUpdate("Where are you going from?")
        global lastBotReply
        lastBotReply = "Where are you going from?"

    # They want to book a ticket and both an origin and destination have been given
    @Rule(AND(Fact(origGiven='true'), Fact(destGiven='true')))
    def confirmBookDetails(self):

        from main import botUpdate
        botUpdate('You want to book a ticket to go from %s to %s is this correct yes or no?' % (orig, dest))
        global lastBotReply
        lastBotReply = 'You want to book a ticket to go from %s to %s is this correct yes or no?'

    # Default response if it doesnt understand you
    # @Rule()
    # def unknown(self):
    #     uInput = processInput(input("Sorry, I didn't understand that. Try again: "))
    #     print(Fact)
    #     if 'book' in uInput.returnlist():
    #         self.declare(Fact(book='true'))
    #     else:
    #         self.unknown()


engine = trainBot()
# engine.reset()  # Prepare the engine for the execution.
# engine.declare(states(book='false', begin='true', hello='false', originGiven='false', destGiven='false', correct='false'))
# engine.run()  # Run it!
