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
            return f'T{self.transID} commit'
        elif(self.process == 'R'):
            return f'T{self.transID} read {self.dataID}'
        else:
            return f'T{self.transID} write {self.dataID}'


class MVCC:
    def __init__(self, schedule, transaction, data):
        self.schedule = schedule
        self.transaction = transaction
        self.data = data

    def exec(self, schedule):
        if (schedule.process == 'C'):
            print(f'{schedule}: Commit success')
            print("--------------------------------------------------")
            self.schedule.remove(schedule)
            return True
        elif (schedule.process == 'R'):
            return self.read(schedule)
        else:
            return self.write(schedule)
        
    def read(self, schedule):
        listVersion = self.data.version[schedule.dataID]
        for idx, t in enumerate(self.transaction):
            if (t.id == schedule.transID):
                transaction = t
        for version in listVersion[::-1]:
            if (version.WTS <= transaction.ts):
                if (version.RTS < transaction.ts):
                    print(f'Updating R-TS of {version.name + str(version.version)} from {version.RTS} to {transaction.ts}')
                    version.RTS = transaction.ts
                print(f'{schedule}: Read {version}')
                print("--------------------------------------------------")
                break
        self.schedule.remove(schedule)
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
                    print("--------------------------------------------------")
                    self.schedule.remove(schedule)
                    return True
                else:
                    newVersion = Data(schedule.dataID, len(listVersion), transaction.ts, transaction.ts)
                    print(f'Creating new version {newVersion}')
                    print(f'{schedule}: Write {newVersion}')
                    print("--------------------------------------------------")
                    listVersion.append(newVersion)
                    listVersion.sort(key=lambda x: x.WTS)
                    self.schedule.remove(schedule)
                    return True
        return False

    
    def start(self):
        maxTS = 0
        for t in self.transaction:
            maxTS = max(maxTS, t.ts)
        print("Starting MVCC...")
        print("--------------------------------------------------")
        while (len(self.schedule) > 0):
            scheduleNow = self.schedule[0]
            if (self.exec(scheduleNow) == False):
                print(f'{scheduleNow}: Write failed. Aborting T{scheduleNow.transID}')
                print(f'Trying to start T{scheduleNow.transID} again with new timestamp {maxTS + 1}')
                print("--------------------------------------------------")
                for idx, t in enumerate(self.transaction):
                    if (t.id == scheduleNow.transID):
                        t.ts = maxTS + 1
                        maxTS += 1
                        processNow = t.process.index(scheduleNow)
                        t.process = t.process[:processNow]
                        self.schedule = t.process + self.schedule
                        break
        print("MVCC Finished")