# File          : Input.py
# Description   : Handles input by text file and CLI, then
#                 converts it to list and dictionary.
# Author        : Damianus Clairvoyance Diva Putra (13520035)

import re
from Instruction import *
from Transaction import *
from Item import *

class Input:
    # constructor
    def __init__(self):
        pass

    # read file and return schedule
    def read_file(self, file_name):
        with open(file_name, "r") as file:
            data = file.read().rstrip()
        return data
    
    # read string and return schedule
    def split_string(self, data):
        return data.split()

    # split string into operation, transaction, and instruction,
    # and store into temporary variables
    def split_instructions(self, strings):
        pattern = "([RrWwCc])(\d+)\(*([\w\d])*\)*"
        instructions = [] # list of Instruction
        transactions = {} # dictionary (key-value) of Transaction
        items = {} # dictionary (key-value) of Item

        for string in strings:
            match = re.match(pattern, string)
            if match:
                operation = match.groups()[0]
                transaction = match.groups()[1]
                item = match.groups()[2]

                if (transaction not in transactions):
                    transactions[transaction] = Transaction(transaction)
                
                if (item not in items and item is not None):
                    items[item] = Item(item)

                instruction = Instruction(operation, transaction, item)
                instructions.append(instruction)
        
        return instructions, transactions, items
        
    # destructor
    # garbage collector