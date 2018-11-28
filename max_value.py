from pyknow import *


# Documentation to read:
#   https://pyknow.readthedocs.io/en/stable/thebasics.html
#
# Other examples:
#   https://github.com/buguroo/pyknow/tree/develop/docs/examples
# This example is from there, but annotated to better explain the
# internal logic
#
# PyKnow is based on CLIPS: http://www.clipsrules.net/
#
# The basics of PROLOG are also helpful to better understand the
# fundamental concepts behind rule based systems:
#   http://www.learnprolognow.org/

# What this example does is set up a database of Facts (numbers)
# and searches through them to find the maximum value while removing
# values that are less than (or equal to) the current maximum.
# The end state is one Fact that contains the largest number
class Maximum(KnowledgeEngine):
    # Step ONE: Rules are processed based on the order they are declared, or
    # based on the salience of them (used for dynamic reordering)
    # AND if the conditions of the rule are satisfied
    #
    # Since in the starting state of the system, Fact(max='anything') is NOT
    # declared, this rule is chosen (versus the others, which require
    # Fact(max='something') to be present) and the method executed - thus
    # setting Fact(max=0) --- the initial maximum value
    @Rule(NOT(Fact(max=W())))
    def init(self):
        self.declare(Fact(max=0))
        print("Initialisation: max val is set to 0")

    # Step TWO: after step 1, rules are put on the agenda ("activated"), and
    # ordered by their priority (order of declaration/salience) and the top
    # rule executed, so compute_max() get called

    # Deactivated rules (e.g. the init() rule) are ones with conditions
    # that can not be satisfied (i.e. Fact(max=?) has been declared so init()
    # no longer should be considered)

    # first, compute_max() gets called based on these valid conditions:
    #   a. Fact(val=12) matching (the first Fact in the database that matches)
    #   b. m=Fact(max=0) matches
    #   c. TEST(12>0) is true
    # so then the m rule is modified, changing Fact(max=0) to Fact(max=12)
    # and then the process starts all over again, with a new agenda and
    # activated/deactivated rules
    @Rule(Fact(val=MATCH.val),
          AS.m << Fact(max=MATCH.max),
          TEST(lambda max, val: val > max))
    def compute_max(self, m, val):
        print("The max value is updated from ", m['max'], "to", val)
        self.modify(m, max=val)

    # Step THREE: after compute_max() is called, based on Fact(12), this rule
    # is still on the current agenda and its preconditions are satisified
    # (matches are found) so it gets executed and Fact(12) gets deleted

    # This rule is invoked whenever, considering the current agenda and Fact(val)
    # under consideration, TEST(val <= max) succeeds -- its purpose is to
    # remove the Fact(val='whatever') from the database as it is no longer
    # useful (i.e. is less than the current maximum)
    # so first Fact(12) gets deleted, then Fact(11) etc
    # <for Fact(11), compute_max() never gets called as its TEST fails>
    @Rule(AS.v << Fact(val=MATCH.val),
          Fact(max=MATCH.max),
          TEST(lambda max, val: val <= max))
    def remove_val(self, v):
        print(v['val'], "is less than, or equal to, the current maximum, " +
              "so this fact (value) removed from database")
        self.retract(v)

    # This rule gets invoked at the very end - the previous two rules are
    # deactivated/not on the current agenda - they can not be invoked as there
    # are no more Fact(val=?) to match against -- so NOT(Fact(val=?)) is true
    # AND v is matched to the Fact(max) fact and thus printed
    @Rule(AS.v << Fact(max=W()),
          NOT(Fact(val=W())))
    def print_max(self, v):
        print("No vals left in database, only the max Fact is left")
        print("Max:", v['max'])


if __name__ == "__main__":
    # instantiation of the rule base, etc
    m = Maximum()
    # the Fact 'InitialFact' is declared and any @DefFact decorated rules
    # executed to initialize the system
    m.reset()

    # initialization of the initial starting state of the 'world'
    # this syntax is a unpacked list comprehension - more compact than
    # doing "m.declare(Fact(val=12))" etc repeatedly
    # Facts are essentially stacked, so Fact(val=12) takes priority
    # over the others

    # IMPORTANT
    # *** change the order of the numbers and see what happens to the output of
    # the program
    m.declare(*[Fact(val=x) for x in (75, 33, 42, 99, 55, 11, 12)])

    # start engine, the purpose of which is to find the maximum value
    # of all the Facts within the initial (or current) state of the world
    m.run()
