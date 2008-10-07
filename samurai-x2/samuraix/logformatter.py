import logging

class FDFormatter(logging.Formatter):
    error_colors = {
        logging.DEBUG: '\033[0;36m',
        logging.INFO: '\033[0;32m',
        logging.WARN: '\033[1;33m',
        logging.ERROR: '\033[1;31m',
    }

    def format(self, record):
        if "%(asctime)" in self._fmt:
            record.asctime = self.formatTime(record, self.datefmt)
        record.message = record.getMessage()
        ret = "%s%s\033[0m" % (self.error_colors.get(record.levelno, ''), self._fmt)
        ret = ret % record.__dict__
        return ret

    def formatException(self, ei):
        sio = cStringIO.StringIO()
        traceback.print_exception(ei[0], ei[1], ei[2], None, sio)
        s = sio.getvalue()
        sio.close()
        if s[-1:] == "\n":
            s = s[:-1]
        return self.error_colors[logging.ERROR] + s



