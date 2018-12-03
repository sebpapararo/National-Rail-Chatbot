from nlpu import *
from kb import *
from random import choice

#from flask import Flask, render_template

#app = Flask(__name__)



#@app.route('/', methods=['GET', 'POST'])
#def index():

   #return render_template('index.html')





if __name__ == '__main__':
    #app.run(host='127.0.0.1', debug=True)

    #y = testingGround()
    #y.testing()

    #x = MyClass("I would like to book a train please at 13:00")
    #x.getVerbs()
    #x.query()
    #x.containsBRH()

    # engine = RobotCrossStreet()
    # engine.reset()
    # engine.declare(Light(color=choice(['green', 'yellow', 'blinking-yellow', 'red'])))
    # engine.run()

    # kb = UserWantsTicket()
    # kb.reset()
    # kb.declare(Ticket(x.containsBRH()))
    # kb.run()

    # en = Greetings()
    # en.reset()  # Prepare the engine for the execution.
    # en.run()  # Run it!

    engine = chatBotMain()
    engine.reset()
    engine.run()
    engine.declare(Fact(greet = True, book = False, time = False, location = False))
    print(engine.facts)
    x = MyClass(input())
    engine.modify(engine.facts[1], book = x.containsBRH(), time = x.containsTime() , location = x.containsLoc(), greet = False)
    print(engine.facts)
    print(engine.agenda)

#https://www.nltk.org/book/ch05.html

#https://www.nltk.org/book/ch07.html

#https://stackoverflow.com/questions/33318975/how-to-get-common-tag-pattern-for-sentences-list-in-python-with-nltk

#https://towardsdatascience.com/a-practitioners-guide-to-natural-language-processing-part-i-processing-understanding-text-9f4abfd13e72