import samuraix.xcb
import samuraix.event
import samuraix.screen

class App(object):
    def __init__(self):
        self.screens = []

    def init(self):
        self.connection = samuraix.xcb.connection.Connection()
        self.connection.push_handlers(self)
        self.running = False
        self.screens.append(samuraix.screen.Screen(self, 0))

    def run(self):
        self.running = True
        while self.running:
            self.connection.wait_for_event_dispatch()
