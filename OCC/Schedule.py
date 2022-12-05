import sys
from FileReader import readFile

class Schedule:
  # store the transactions of a schedule
  # interface to run OCC protocol

  def __init__(self):
    self.rawTr = []
    self.tr = []
    self.executedOperation = []

  def setRawTr(self, tr):
    self.rawTr = tr

  def readPhase(self, tr):
    # start read phase
    type = 0
    for operation in tr.getOperation():
      if operation[type] == "R":
        self.executedOperation.append(operation)
      elif operation[type] == "W":
        self.executedOperation.append(operation)
    tr.setStartTS(self.rawTr.index(tr.operation[0]))

  def firstConditionCheck(self, trCompare, tr):
    # return true if pass first condition, finishTS(Ti) < startTS(Tj) where Ti<Tj
    status = True
    if (trCompare.getTrNum() < tr.getTrNum() and not(trCompare.getFinishTS() < tr.getStartTS())):
      status = False
    return status

  def checkIntersect(self, trCompare, tr):
    # return true if tr read item written by trCompare where TS(trCompare) < TS(tr)
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
    # return true if pass second condition checking
    status = True
    if (trCompare.getTrNum() < tr.getTrNum() and not(tr.getStartTS() < trCompare.getFinishTS() and trCompare.getFinishTS() < tr.getValidationTS())):
      print("Validation phase start after write phase in previous transaction.")
      status = False
    if (not(self.checkIntersect(trCompare, tr))):
      status = False
      
    return status

  def validationPhase(self, tr):
    # start validation phase
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

  def runOCC(self):
    # start OCC protocol
    for tr in self.tr:
      print("Transaction",tr.getTrNum(),":")
      self.readPhase(tr)
      self.validationPhase(tr)

if __name__ == "__main__":
  print("args", sys.argv)

  if (len(sys.argv) != 2):
    print("Please enter the correct format. Example:\npython Schedule.py <filename.txt>")
  else:
    schedule = Schedule()

    try:
      readFile(sys.argv[1],schedule)
    except FileNotFoundError as e:
      print(e.filename,"\nis not found. Please enter the correct filename.")
      sys.exit()

    schedule.runOCC()
