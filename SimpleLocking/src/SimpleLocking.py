# File          : SimpleLocking.py
# Description   : Main Program
# Author        : Damianus Clairvoyance Diva Putra (13520035)

from Input import *

# coloring (adapted from geeksforgeeks.org)
def print_red(string):
    print("\033[91m{}\033[00m".format(string))

def print_green(string):
    print("\033[92m{}\033[00m".format(string))

# check deadlock
def check_deadlock(waiting):
    found = False
    transaction1 = None
    transaction2 = None
    for transaction1 in waiting:
        for transaction2 in waiting[transaction1]:
            if (transaction1 in waiting[transaction2]):
                found = True
                break
        if found:
            break
    return found, transaction1, transaction2

# return younger transaction of transaction1 and transaction2
def check_younger(transaction_order, transaction1, transaction2):
    for transaction in transaction_order:
        if (transaction == transaction1):
            return transaction2
        elif (transaction == transaction2):
            return transaction1
    return 0

# remove instruction from queue
def remove_from_queue(queue, transaction):
    for instruction in queue:
        if (instruction.transaction == transaction):
            queue.remove(instruction)

# Simple Locking Algorithm
def SimpleLocking():
    # handle input and store into variables
    input_handler = Input()
    input_method = int(input("Input via CLI (1) or .txt file (2): "))

    # input validation
    while (not(input_method == 1 or input_method == 2)):
        input_method = input("Input via CLI (1) or .txt file (2): ")
    if (input_method == 1):
        print()
        input_string = input("Schedule: ")
    else:
        file_name = input("File name: ")
        print()
        input_string = input_handler.read_file("test/" + file_name)
        print("Schedule:", input_string)
    strings = input_handler.split_string(input_string)
    instructions, transactions, items = input_handler.split_instructions(strings)

    # initialize temporary variables
    queue = []
    schedule = []
    transaction_order = []
    waiting = {}
    for transaction in transactions:
        waiting[transaction] = [] # add when wait, delete when commit
    print()

    # while instructions not empty
    while (instructions or queue):
        # if deadlock
        is_deadlock, transaction1, transaction2 = check_deadlock(waiting)
        if (is_deadlock):
            # rollback old transaction
            transaction_rb = check_younger(transaction_order, transaction1, transaction2)
            transactions[transaction_rb].empty_queue() #
            remove_from_queue(queue, transaction_rb)
            instructions = queue + transactions[transaction_rb].done + instructions
            queue.clear()
            transactions[transaction_rb].empty_done()
            for transaction in transactions:
                if (transaction_rb in waiting[transaction]):
                    waiting[transaction].remove(transaction_rb)
                transactions[transaction].empty_queue()
            rollback_instruction = Instruction('RB', transaction_rb, None)
            schedule.append(rollback_instruction)
            print("RB%s;        " % transaction_rb, end="")
            for item_locked in transactions[transaction_rb].item_locked:
                item_locked.free_lock()
                unlock_instruction = Instruction('UL', transaction_rb, item_locked.name)
                schedule.append(unlock_instruction)
                print("UL%s(%s)" % (transaction_rb, item_locked.name), end="; ")
            print()

        # take the first instruction
        instruction = instructions.pop(0)

        # store transaction order (deadlock prevention)
        if (instruction.transaction not in transaction_order):
            transaction_order.append(instruction.transaction)

        # print to CLI
        instruction.print_cli()
        if (instruction.operation == 'C'):
            print("        ", end="")
        else:
            print("     ", end="")
        
        # if instruction is commit and transaction queue empty
        if (instruction.operation == 'C' and transactions[instruction.transaction].is_queue_empty()):
            # release lock from transaction and free lock from item
            for item_locked in transactions[instruction.transaction].item_locked:
                item_locked.free_lock()
                unlock_instruction = Instruction('UL', instruction.transaction, item_locked.name)
                schedule.append(unlock_instruction)
                print("UL%s(%s)" % (instruction.transaction, item_locked.name), end="; ")
            transactions[instruction.transaction].release_lock()
            # restart queues of all transactions
            for transaction in transactions:
                transactions[transaction].empty_queue()
            # remove from waiting queue
            for transaction in transactions:
                if (instruction.transaction in waiting[transaction]):
                    waiting[transaction].remove(instruction.transaction)
            # verdict: do instruction
            instructions = queue + instructions
            queue.clear()
            schedule.append(instruction)
            print("C%s; " % (instruction.transaction))
        
        # else if transaction has predecessor in transaction queue
        elif (not (transactions[instruction.transaction].is_queue_empty())):
            # verdict: wait instruction
            queue.append(instruction)
            transactions[instruction.transaction].add_done(instruction)
            print("wait for", end=" ")
            for instruction_queue in transactions[instruction.transaction].queue:
                instruction_queue.print_cli()    
            print()
            # if instruction is not commit
            if (instruction.operation != 'C'):
                # add to transaction queue
                transactions[instruction.transaction].add_queue(instruction)
            
        # else if item is locked by other transaction
        elif (not items[instruction.item].is_locked_by(instruction.transaction) \
            and items[instruction.item].is_locked()):
            # add to transaction queue and waiting queue
            transactions[instruction.transaction].add_queue(instruction)
            waiting[instruction.transaction].append(items[instruction.item].locker)
            transactions[instruction.transaction].add_done(instruction)
            # verdict: wait instruction
            queue.append(instruction)
            print("wait for XL%s(%s); " % (items[instruction.item].locker, instruction.item))
        
        # everything else
        else:
            # if item is not locked by this transaction
            if (not items[instruction.item].is_locked()):
                # acquire lock from transaction and set lock from item
                items[instruction.item].set_lock(instruction.transaction)
                transactions[instruction.transaction].acquire_lock(items[instruction.item])
                lock_instruction = Instruction('XL', instruction.transaction, instruction.item)
                schedule.append(lock_instruction)
                print("XL%s(%s)" % (instruction.transaction, instruction.item), end ="; ")
            # if instruction is in transaction queue
            if (not transactions[instruction.transaction].is_queue_empty() \
                and transactions[instruction.transaction].next_instruction() == instruction):
                # remove from transaction queue
                transactions[instruction.transaction].do_queue()
            transactions[instruction.transaction].add_done(instruction)
            # verdict: read/write
            schedule.append(instruction)
            instruction.print_cli()
            print()
    
    # print final schedule
    print()
    print("Final Schedule: ", end="")
    for instruction in schedule:
        instruction.print_cli()
        print("", end="")
    print()

# main
if __name__ == "__main__":
    SimpleLocking()