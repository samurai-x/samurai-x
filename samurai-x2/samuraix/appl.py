import signal
import sys

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

        # TODO these wont work until we fix the event loop
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGHUP, self.stop)

    def stop(self, *args):
        # TODO this wont work until we fix the event loop 
        self.running = False

    def run(self):
        self.running = True

        # TODO i think we want to change this to using either a select based method 
        # or using libevent (like awesome3 :)) 
        # this will allow properly setting up signal callbacks and timers 

        while self.running:
            try:
                self.connection.wait_for_event_dispatch()
            except Exception, e:
                log.error(e)


