from pyknow import *

# Global variables
orig = ""
dest = ""
uInput = ""
lastBotReply = ""

# After a user response is supplied the engine carries out all functions where the rules are met


class trainBot(KnowledgeEngine):

    # Default response if it doesnt understand you
    def unknown(self):
        from main import botUpdate
        botUpdate("I'm sorry, I didn't understand that. Please try again.")

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
        global lastBotReply
        lastBotReply = "Hello, what can I help you with?"
        botUpdate(lastBotReply)
        self.modify(self.facts[1], begin="false")

    # Just received user input
    @Rule(Fact(receivedInput='true'))
    def waiting(self):
        global orig, dest, lastBotReply
        processedInput = processInput(uInput)

        # Each if/case should have an else where the users response is unknown so it allows them to try again

        if lastBotReply in "Hello, what can I help you with?":
            if 'book' in processedInput.returnlist():
                self.declare(Fact(book='true'))
            else:
                self.unknown()

        # Maybe add a check against a list of train stations to make sure its real
        if lastBotReply == "Sure thing! Where would you like to go?":
            dest = uInput
            self.declare(Fact(destGiven="true"))

        # Maybe add a check against a list of train stations to make sure its real
        if lastBotReply == "Excellent! Where are you departing from?":
            orig = uInput
            self.declare(Fact(origGiven="true"))

        if lastBotReply == 'You want to book a ticket to go from %s to %s is this correct yes or no?' % (orig, dest):
            if 'yes' in processedInput.returnlist():
                self.declare(Fact(correct='true'))
            elif 'no' in processedInput.returnlist():
                self.declare(Fact(correct='false'))
            else:
                self.unknown()

        engine.run()

    # They want to book a ticket, but no destination has been given
    @Rule(Fact(book='true'))
    def whereGo(self):
        from main import botUpdate
        global lastBotReply
        lastBotReply = "Sure thing! Where would you like to go?"
        botUpdate(lastBotReply)

    # They want to book a ticket, but no origin has been given
    @Rule(Fact(book='true'), Fact(destGiven="true"))
    def whereFrom(self):
        from main import botUpdate
        global lastBotReply
        lastBotReply = "Excellent! Where are you departing from?"
        botUpdate(lastBotReply)

    # They want to book a ticket and both an origin and destination have been given
    @Rule(AND(Fact(origGiven='true'), Fact(destGiven='true')))
    def confirmBookDetails(self):
        from main import botUpdate
        global lastBotReply
        lastBotReply = 'You want to book a ticket to go from %s to %s is this correct yes or no?' % (orig, dest)
        botUpdate(lastBotReply)

engine = trainBot()
