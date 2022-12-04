import sys

# TO DO: AUTOMATE INPUT FROM CMD FOR TEST FILE
class Transaction:
  def __init__(self, trNum, operation):
    self.trNum = trNum
    self.operation = operation
    self.ts = [-1,-1,-1]

  def getStartTS(self):
    return self.ts[0]

  def setStartTS(self, ts):
    self.ts[0] = ts

  def getValidationTS(self):
    return self.ts[1]

  def setValidationTS(self, ts):
    self.ts[1] = ts

  def getFinishTS(self):
    return self.ts[2]

  def setFinishTS(self, ts):
    self.ts[2] = ts

  def getTrNum(self):
    return self.trNum

  def getOperation(self):
    return self.operation

class Schedule:
  def __init__(self):
    self.rawTr = []
    self.tr = []
    self.executedOperation = []

  def setRawTr(self, tr):
    self.rawTr = tr

  def readPhase(self, tr):
    type = 0
    for operation in tr.getOperation():
      if operation[type] == "R":
        self.executedOperation.append(operation)
      elif operation[type] == "W":
        self.executedOperation.append(operation)
    tr.setStartTS(self.rawTr.index(tr.operation[0]))

  def firstConditionCheck(self, trCompare, tr):
    # return true if pass first condition, finishTS(Ti) < startTS(Tj)
    status = True
    if (trCompare.getTrNum() < tr.getTrNum() and not(trCompare.getFinishTS() < tr.getStartTS())):
      status = False
    return status

  def checkIntersect(self, trCompare, tr):
    # return true if tr read item written by trCompare
    status = True
    for operation in tr.getOperation():
      if operation[0] == "R":
        for operationCompare in trCompare.getOperation():
          if operationCompare[0] == "W" and operationCompare[3] == operation[3]:
            if self.executedOperation.index(operationCompare) < self.executedOperation.index(operation):
              status = False
              break
        else:
          continue
    if not status:
      print("Fail intersect constraint, read resource that written by previous transaction.")
    return status

  def secondConditionCheck(self, trCompare, tr):
    # return true if pass second condition
    status = True
    if (trCompare.getTrNum() < tr.getTrNum() and not(tr.getStartTS() < trCompare.getFinishTS() and trCompare.getFinishTS() < tr.getValidationTS())):
      print("Validation phase start after write phase in previous transaction.")
      status = False
    if (not(self.checkIntersect(trCompare, tr))):
      status = False
      
    return status

  def validationPhase(self, tr):
    tr.setValidationTS(self.executedOperation.index(tr.operation[-2]))
    validationTest = False
    while not(validationTest):
      if tr.getTrNum() == 1:
        validationTest = True
        break
      if tr.getTrNum() > 1:
        for trCompare in self.tr:
          if trCompare.getTrNum() < tr.getTrNum():
            if self.firstConditionCheck(trCompare, tr) or self.secondConditionCheck(trCompare, tr):
              validationTest = True
            else:
              sys.exit("Fail validation test, abort.")
    
    if validationTest:
      print("Pass validation test, commit.")
      for operation in tr.getOperation():
        if operation not in self.executedOperation:
          self.executedOperation.append(operation)
      tr.setFinishTS(self.executedOperation.index(tr.operation[-1]))

def main():
  s = Schedule()
  with open('input2.txt','r') as f:
    sentences = list(f)
    temp1 = []
    temp2 = []
    temp3 = []
    allTr = []
    for item in sentences:
      if int(item[1]) == 1:
        temp1.append(item[:-1])
      elif int(item[1]) == 2:
        temp2.append(item[:-1])
      elif int(item[1]) == 3:
        temp3.append(item[:-1])

      allTr.append(item[:-1])

    tr1 = Transaction(1, temp1)
    tr2 = Transaction(2, temp2)
    tr3 = Transaction(3, temp3)

    s.tr.append(tr1)
    s.tr.append(tr2)
    s.tr.append(tr3)
    s.setRawTr(allTr)

  for tr in s.tr:
    print("Transaction",tr.getTrNum(),":")
    s.readPhase(tr)
    s.validationPhase(tr)

if __name__ == "__main__":
  main()
