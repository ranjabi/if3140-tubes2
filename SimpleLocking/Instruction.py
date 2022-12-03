# File          : Instruction.py
# Description   : Instruction class. In case of R1(A),
#                 R is operator, 1 is transaction, and A is item.
# Author        : Damianus Clairvoyance Diva Putra (13520035)

class Instruction:
    # constructor
    def __init__(self, operation, transaction, item):
        self.operation = operation
        self.transaction = transaction
        self.item = item
    
    # print to CLI
    def print_cli(self):
        if (self.item is not None):
            print("%s%s(%s)" % (self.operation, self.transaction, self.item), end="; ")
        else:
            print("%s%s" % (self.operation, self.transaction), end="; ")
    
    # destructor
    # garbage collector