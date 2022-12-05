class Transaction:
  # store the operations for a single transaction
  
  def __init__(self, trNum, operation):
    self.trNum = trNum
    self.operation = operation
    self.ts = [0,0,0]

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