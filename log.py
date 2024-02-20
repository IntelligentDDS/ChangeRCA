#encoding = utf-8

import logging


class Logger():
    def __init__(self, logname, loglevel=logging.DEBUG, loggername=None):
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(loglevel)

        fh = logging.FileHandler(logname)
        fh.setLevel(loglevel)
        if not self.logger.handlers:
            ch = logging.StreamHandler()
            ch.setLevel(loglevel)
            formatter = logging.Formatter(
                '[%(levelname)s]%(asctime)s %(filename)s:%(lineno)d: %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

    def getlog(self):
        return self.logger
