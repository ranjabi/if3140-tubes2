# File          : Transaction.py
# Description   : Transaction class. Handles items locking by transaction
#                 and instruction queue of transaction.
# Author        : Damianus Clairvoyance Diva Putra (13520035)

class Transaction:
    # constructor (str, str, str)
    def __init__(self, name):
        self.name = name
        self.item_locked = []
        self.queue = []
        self.done = [] # deadlock prevention

    # remove all item locks
    def release_lock(self):
        self.item_locked.clear()

    # add item lock after last instruction
    def acquire_lock(self, item):
        self.item_locked.append(item)
    
    # remove first instruction
    def do_queue(self):
        self.queue.pop(0)
    
    # add instruction to queue
    def add_queue(self, instruction):
        self.queue.append(instruction)

    # return the first element of queue
    def next_instruction(self):
        return self.queue[0]
    
    # return true if queue is empty
    def is_queue_empty(self):
        return not self.queue
    
    # clear queue
    def empty_queue(self):
        self.queue.clear()
    
    # add instruction to done
    def add_done(self, instruction):
        self.done.append(instruction)
    
    # clear done
    def empty_done(self):
        self.done.clear()
    
    # destructor
    # garbage collector