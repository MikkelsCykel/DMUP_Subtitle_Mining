import time


class Log:
    def __init__(self):
        self.i = 2

    def writeToLog(self, message, where=""):
        with open('../data/log.txt', 'a') as f:
            f.write("%s    ::    %s %s\n" %
                    (time.strftime("%d/%m/%Y  -  %H:%M:%S"), message, where))
