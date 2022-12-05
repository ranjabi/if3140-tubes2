import os
from Transaction import Transaction

def countTransaction(transaction):
  num = 0
  trNum = 1
  for operation in transaction:
    if int(operation[trNum]) > num:
      num = int(operation[trNum])
  return num

def readFile(filename, schedule):
  # parse input to a schedule
  mainPath = os.path.dirname(__file__)
  testPath = os.path.join(mainPath, 'test\\', filename)
  
  with open(testPath,'r') as f:
    transaction = list(f)
    nTr = countTransaction(transaction)
    trNum = 1
    allTr = []

    for i in range(nTr):
      singleTransaction = []

      for operation in transaction:
        if int(operation[trNum]) == i+1:
          singleTransaction.append(operation[:-1])
        if operation not in allTr:
          allTr.append(operation[:-1])

      trTemp = Transaction(i+1, singleTransaction)
      schedule.tr.append(trTemp)
    schedule.setRawTr(allTr)