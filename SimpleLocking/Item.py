# File          : Item.py
# Description   : Item class. Handles locking of the item.
# Author        : Damianus Clairvoyance Diva Putra (13520035)

class Item:
    # constructor
    def __init__(self, name):
        self.name = name
        self.locker = None
    
    # return true if item is locked
    def is_locked(self):
        return self.locker is not None

    # return true if item is locked by locker
    def is_locked_by(self, locker):
        return self.locker == locker
    
    # set item lock by locker
    def set_lock(self, locker):
        self.locker = locker
    
    # free item lock
    def free_lock(self):
        self.locker = None

    # destructor
    # garbage collector