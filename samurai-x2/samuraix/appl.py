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

    def run(self):
        self.running = True
        while self.running:
            self.connection.wait_for_event_dispatch()
