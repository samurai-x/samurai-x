from select import select

class Mainloop(object):
    def __init__(self, busses=()):
        self.busses = set(busses)
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            read, blah, blubb = select(self.busses, (), ())
            for bus in read:
                bus.receive_one()

    def add_bus(self, bus):
        self.busses.add(bus)

    def quit(self):
        self.running = False

