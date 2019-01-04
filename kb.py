from pyknow import *
from nlpu import *

# f = Fact(a=1, b=2)
#
# print(f['a'])
#
# class Light(Fact):
#     """Info about the traffic light."""
#     pass
#
#
# class RobotCrossStreet(KnowledgeEngine):
#     @Rule(Light(color='green'))
#     def green_light(self):
#         print("Walk")
#
#     @Rule(Light(color='red'))
#     def red_light(self):
#         print("Don't walk")
#
#     @Rule(AS.light << Light(color=L('yellow') | L('blinking-yellow')))
#     def cautious(self, light):
#         print("Be cautious because light is", light["color"])
#
# class Greetings(KnowledgeEngine):
#     @DefFacts()
#     def _initial_action(self):
#         yield Fact(action="greet")
#
#     @Rule(Fact(action='greet'),
#           NOT(Fact(name=W())))
#     def ask_name(self):
#         self.declare(Fact(name=input("What's your name? ")))
#
#     @Rule(Fact(action='greet'),
#           NOT(Fact(location=W())))
#     def ask_location(self):
#         self.declare(Fact(location=input("Where are you? ")))
#
#     @Rule(Fact(action='greet'),
#           Fact(name=MATCH.name),
#           Fact(location=MATCH.location))
#     def greet(self, name, location):
#         print("Hi %s! How is the weather in %s?" % (name, location))

# class Ticket(Fact):
#     pass
# class UserWantsTicket(KnowledgeEngine):
#     @Rule(Ticket(True))
#     def giveTicket(self):
#         print("Here is a Ticket!")
#
#     @Rule(Ticket(False))
#     def noTicket(self):
#         print("How Can I help you today?")
#--------------------------------------------------Chatbot knowledge base doing changing rules on the go
# class Chatbot(KnowledgeEngine):
#     @DefFacts()
#     def _initial_action(self):
#         yield Fact(action="greet")
#
#     @Rule(Fact(action = 'greet'),
#     NOT (Fact(userInput=W())))
#     def ask_action(self):
#         self.declare(Fact(userInput=input("Hello there!\nWhat would you like to do?")))
#
#     @Rule(Fact(action = 'greet'),
#           Fact(userInput=MATCH.userInput),
#           NOT (Fact(bTicket=W())))
#     def process_action(self, userInput):
#         print(userInput)
#         x = MyClass(userInput)
#         self.declare(Fact(bTicket = x.containsBRH()))
#
#     @Rule(Fact(action = 'greet'),
#           Fact(bTicket = True))
#     def wantTicket(self):
#         print("The User wants a ticket! YAY!")
#         self.declare(Fact(userInput = None))
#
#     @Rule(Fact(userInput = None),
#           Fact(bTicket = True))
#     def ask_TODO(self):
#         self.declare(Fact(userInput=input("Where do you want to go?")))


#--------------------------------------------------Chatbot knowledge base doing changing rules in one method
