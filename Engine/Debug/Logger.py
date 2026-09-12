
class Log:
    def __init__(self, logData: str, logType: str = "INFO", priority: int = 1):
        self.logData = logData
        self.logType = logType
        self.priority = priority

    def __str__(self):
        return str(self.logType + ": " + self.logData)

class Logger:
    def __init__(self):
        self.logEntries = []
        self.oldLog = []

    def log(self, message: str, messageType: str = "INFO", priority: int = 1):
        logEntry = Log(message, messageType, priority)
        self.logEntries.append(logEntry)

    def priorityLog(self):
        entries = set([str(entry) for entry in self.logEntries if entry.priority >= 3])
        for entry in entries:
            print(entry.strip("[]'"))
        return True if len(entries) != 0 else False

    def push(self):
        for entry in self.logEntries:
            if entry.priority > 0:
                self.oldLog.append(entry)
        self.logEntries = []

    def clear(self):
        self.oldLog = []

    def isEmpty(self):
        return len(self.logEntries) == 0

    def printLog(self):
        entries = set(self.logEntries)
        for entry in entries:
            print(str(entry).strip("[]'"))

    def saveLog(self):
        out = []
        for entry in self.oldLog:
            out.append({entry.logType: (entry.logData, entry.priority)})
        return out
