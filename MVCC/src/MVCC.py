class Transaction:
    def __init__(self, id, timestamp):
        self.id = id
        self.ts = timestamp
        self.process = []
    def __str__(self) -> str:
        return f'Transaction {self.id} with timestamp {self.ts}'
    

class Data:
    def __init__(self, name, version=0, RTS=0, WTS=0):
        self.name = name
        self.version = version
        self.RTS = RTS
        self.WTS = WTS
    def __str__(self) -> str:
        return f'{self.name}{self.version} (R-TS: {self.RTS},W-TS: {self.WTS})'

class DataVersion:
    def __init__(self, arrData):
        self.version = {}
        for i in range(len(arrData)):
            self.version.update({arrData[i].name: [arrData[i]]})

class Process:
    def __init__(self, transID, process, data=None):
        self.transID = transID
        self.dataID = data
        self.process = process

    def __str__(self) -> str:
        if (self.process == 'C'):
            return f'{self.process}{self.transID}'
        else:
            return f'{self.process}{self.transID}{self.dataID}'


class MVCC:
    def __init__(self, schedule, transaction, data):
        self.schedule = schedule
        self.transaction = transaction
        self.data = data

    def exec(self, schedule):
        if (schedule.process == 'C'):
            print(f'{schedule}: Commit {schedule.transID}')
            return True
        elif (schedule.process == 'R'):
            return self.read(schedule)
        else:
            return self.write(schedule)
        
    def read(self, schedule):
        listVersion = self.data.version[schedule.dataID]
        for idx, t in enumerate(self.transaction):
            if (t.ts == schedule.transID):
                transaction = t
        for version in listVersion[::-1]:
            if (version.WTS <= transaction.ts):
                if (version.RTS < transaction.ts):
                    version.RTS = transaction.ts
                print(f'{schedule}: Read {version}')
                break
        return True
    
    def write(self, schedule):
        listVersion = self.data.version[schedule.dataID]
        for idx, t in enumerate(self.transaction):
            if (t.id == schedule.transID):
                transaction = t
        for version in listVersion[::-1]:
            if (version.WTS <= transaction.ts):
                if (version.RTS > transaction.ts):
                    return False
                elif (version.WTS == transaction.ts):
                    print(f'{schedule}: Overwrite {version}')
                    return True
                else:
                    newVersion = Data(schedule.dataID, version.version + 1, transaction.ts, transaction.ts)
                    print(f'{schedule}: Write {newVersion}')
                    listVersion.append(newVersion)
                    return True
        return False

    
    def start(self):
        print("Starting MVCC")
        aborted = []
        for i in range(len(self.schedule)):
            if (self.schedule[i].transID not in aborted and self.exec(self.schedule[i]) == False):
                print(f'{self.schedule[i]}: Abort {self.schedule[i].transID}')
                aborted.append(self.schedule[i].transID)
        
        while (aborted):
            processAborted = []
            for i in range(len(aborted)):
                for idx, t in enumerate(self.transaction):
                    if (t.id == aborted[i]):
                        t.ts = len(self.transaction) + 1 + i
                        processAborted = processAborted + t.process
                        break
            aborted = []
            for i in range(len(processAborted)):
                if (processAborted[i].transID not in aborted and self.exec(processAborted[i]) == False):
                    print(f'{processAborted[i]}: Abort {processAborted[i].transID}')
                    aborted.append(processAborted[i].transID)
        print("MVCC Finished")