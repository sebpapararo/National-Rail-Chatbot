from pyknow import *

from nlpu import *

# Global variables
orig = ""
dest = ""


class trainBot(KnowledgeEngine):
    # Facts to initialise at the beginning of the chat
    @DefFacts()
    def _initial_action(self):
        # yield Fact(book='false')
        yield Fact(begin='true')
        # yield Fact(hello='false')
        # yield Fact(originGiven='false')
        # yield Fact(destGiven='false')
        # yield Fact(correct='false')

    # Beginning of the conversation
    @Rule(Fact(begin='true'))
    def hello(self):
        uInput = processInput(input("Hello, what can I help you with?"))
        if 'book' in uInput.returnlist():
            self.declare(Fact(book='true'))
        self.modify(self.facts[1], begin="false")

    # They want to book a ticket, but no destination has been given
    @Rule(Fact(book='true'))
    def whereGo(self):
        global dest
        dest = input("Where would you like to go?")
        self.declare(Fact(destGiven="true"))

    # They want to book a ticket, but no origin has been given
    @Rule(Fact(book='true'))
    def whereFrom(self):
        global orig
        orig = input("Where are you going from?")
        self.declare(Fact(origGiven="true"))

    # They want to book a ticket and both an origin and destination have been given
    @Rule(Fact(origGiven='true'), Fact(destGiven='true'))
    def confirmBookDetails(self):
        uInput = input('You want to book a ticket to go from %s to %s is this correct "yes" or "no"' % (orig, dest))
        uInput = processInput(uInput)
        if 'yes' in uInput.returnlist():
            self.declare(Fact(correct='true'))

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
engine.reset()  # Prepare the engine for the execution.
# engine.declare(states(book='false', begin='true', hello='false', originGiven='false', destGiven='false', correct='false'))
engine.run()  # Run it!
