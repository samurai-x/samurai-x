import samuraix.xcb
import samuraix.xcb.screen
import samuraix.event
import samuraix.screen

class App(object):
    def __init__(self):
        self.screens = []

    def init(self):
        self.connection = samuraix.xcb.connection.Connection()
        self.connection.push_handlers(self)
        self.running = False

        if False:
            print "found %d screens" % samuraix.xcb.screen.Screen.get_screen_count(self.connection)
            for i in range(samuraix.xcb.Screen.get_screen_count(self.connection)):
                self.screens.append(samuraix.screen.Screen(self, i))
        else:
            self.screens.append(samuraix.screen.Screen(self, 0))
            

    def run(self):
        self.running = True
        while self.running:
            self.connection.wait_for_event_dispatch()
