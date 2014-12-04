# -*- coding: utf-8 -*-
import time


class Log:
    def __init__(self):
        self.i = 2

    def write_to_log(self, message, where=""):
        """
        Function for writing output to the log. Used for debug.

        :rtype : object
        """
        with open('data/log.txt', 'a') as f:
            f.write("%s    ::    %s %s\n" %
                    (time.strftime("%d/%m/%Y  -  %H:%M:%S"), message, where))
