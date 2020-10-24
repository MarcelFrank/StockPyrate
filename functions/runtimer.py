from datetime import datetime

class TimeKeeper():
        
    def __init__(self):
        self.begin = 0
        self.end = 0
        self.runtime = 0

    def start(self):
        self.begin = datetime.now()

    def show(self):
        self.end = datetime.now()
        self.runtime = self.end - self.begin
        return (print(self.runtime))