import signal
import sys
from select import select

import samuraix.xcb
import samuraix.xcb.screen
import samuraix.event
import samuraix.screen

import logging
log = logging.getLogger(__name__)

class App(object):
    def __init__(self):
        self.screens = []

    def init(self):
        self.connection = samuraix.xcb.connection.Connection()
        self.connection.push_handlers(self)
        self.running = False

        log.debug("found %d screens" % samuraix.xcb.screen.Screen.get_screen_count(self.connection))

        for i in range(samuraix.xcb.screen.Screen.get_screen_count(self.connection)):
            scr = samuraix.screen.Screen(self, i)
            scr.scan()
            self.screens.append(scr)

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGHUP, self.stop)

    def stop(self, *args):
        log.info('stopping')
        self.running = False

    def run(self):
        self.running = True

        if True:
            # process any events that are waiting first 
            while True:
                try:
                    ev = self.connection.poll_for_event()
                except Exception, e:
                    log.error(e)
                else:
                    if ev is None:
                        break
                    ev.dispatch()

            while self.running:
                log.debug('selecting...')
                try:
                    select([self.connection._fd], [], [self.connection._fd], 1.0)
                except Exception, e:
                    # error 4 is when a signal has been caught
                    if e.args[0] == 4:
                        pass
                    else:
                        log.error(str((e, type(e), dir(e), e.args)))
                        raise 

                # might as well process all events in the queue...
                while True:
                    try:
                        ev = self.connection.poll_for_event()
                    except Exception, e:
                        log.error(e)
                    else:
                        if ev is None:
                            break
                        ev.dispatch()
        else:
            while self.running:
                self.connection.wait_for_event_dispatch()


