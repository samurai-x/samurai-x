from time import time as timenow
from select import select

import logging
log = logging.getLogger(__name__)


class ScheduledFunc(object):
    def __init__(self, funcs, when, delay=None):
        self.funcs = funcs
        self.when = when
        self.delay = delay

    def __str__(self):
        return "<ScheduledFunc %s %s %s>" % (self.func, self.when, self.delay)


class Timer(object):
    def __init__(self):
        self.scheduled_funcs = []
        self.select_timeout = 0.5

    def schedule(self, func, when):
        sf = ScheduledFunc(func, when)
        self.scheduled_funcs.append(sf)

    def schedule_repeated(self, func, delay):
        # TODO: check for sf's with same delay and attach func to it
        # instead of creating a new item

        sf = ScheduledFunc([func], timenow()+delay, delay)
        self.scheduled_funcs.append(sf)

    def update(self, fd):
        now = timenow()

        to_remove = []
        for sf in self.scheduled_funcs:
            if now > sf.when:
                for func in sf.funcs:
                    func()
                if sf.delay is not None:
                    sf.when += sf.delay
                else:
                    to_remove.append(sf)

        for sf in to_remove:
            self.scheduled_funcs.remove(sf)

        select([fd], [], [fd], self.select_timeout)

