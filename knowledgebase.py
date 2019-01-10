from pyknow import *
from nlpu import *
from nlp_customTagger import *
from nlp_testGround import *

class information(Fact):
    location = Field(str, default="")
    time = Field(str, default="")
    booking = Field(bool, default=False)

class ValidQuestion(Fact):
    question = Field(str, mandatory=True)


class Action(Fact):
    pass

class HumanQuestion(Fact):
    pass

class ComputerChoice(Fact):
    pass

class chatBot(KnowledgeEngine):
    def yes_or_no(self, question):
        return input(question).upper().startswith('Y')

    # @DefFacts()
    # def chat_rules(self):
    #
    #     print("TODO")


    @Rule()
    def startup(self):
        print("Hello, how may I help you today?")
        print("Please enter a quesiton I can help you with today,")
        print("e.g. book a train ticket, get trains times...")
        self.declare(Action('get-human-question'))

    @Rule(NOT(Action()),
        ValidQuestion(question=MATCH.question))
    def store_valid_questions(self, question):
        self.valid_questions[question] = question

    #
    # Get human question
    #
    @Rule(Action('get-human-question'))
    def get_human_question(self):
        question = input()
        res =  tuple(Custom_pos_tag(word_tokenize(question)))
        self.declare(HumanQuestion(res))



        self.declare(information(findLocations(res)))

        self.declare(Action('determine-another-question'))
        print(res)
    #
    # Ask another question
    #
    @Rule(Action('determine-another-question'))
    def another_question(self):
        if not self.yes_or_no("Do you have another question?"):
            print("Thanks for using me, and I hope everything worked sufficiently")
        else:
            self.declare(Action('get-human-question'))

rps = chatBot()
rps.reset()
rps.run()