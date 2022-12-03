from MVCC import *

class Reader:
    def setup(self, filename):
        arrSchedule = self.readFile(filename)
        self.setTrans(arrSchedule)
        self.setData(arrSchedule)
        self.setSchedule(arrSchedule)

    def readFile(self, fileName):
        file = open("../test/" + fileName, "r")
        arrSchedule = file.read().splitlines()
        file.close()
        return arrSchedule

    def setTrans(self, arrSchedule):
        self.transaction = []
        for i in range(len(arrSchedule)):
            transID = int(arrSchedule[i][1:2])
            if transID not in self.transaction:
                self.transaction.append(transID)
        self.transaction.sort()
        for i in range(len(self.transaction)):
            self.transaction[i] = Transaction(self.transaction[i], self.transaction[i])

    def setData(self, arrSchedule):
        data = []
        for i in range(len(arrSchedule)):
            if arrSchedule[i][3:4] not in data and arrSchedule[i][:1] != "C":
                data.append(arrSchedule[i][3:4])
        data.sort()
        for i in range(len(data)):
            data[i] = Data(data[i])
        self.data = DataVersion(data)
    
    def setSchedule(self, arrSchedule):
        self.schedule = []
        for i in range(len(arrSchedule)):
            if arrSchedule[i][:1] == "C":
                self.schedule.append(Process(int(arrSchedule[i][1:2]), arrSchedule[i][:1]))
            else:
                self.schedule.append(Process(int(arrSchedule[i][1:2]), arrSchedule[i][:1], arrSchedule[i][3:4]))
        for i in range(len(self.schedule)):
            for idx, trans in enumerate(self.transaction):
                if trans.ts == self.schedule[i].transID:
                    self.transaction[idx].process.append(self.schedule[i])
                    break