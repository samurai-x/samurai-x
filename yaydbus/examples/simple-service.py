import sys
sys.path.append('..')

from yaydbus.bus import SessionBus
from yaydbus.service import Object, signal, method
from yaydbus.util import annotate
from yaydbus.mainloop import Mainloop
from yaydbus.dbus_types import UInt32, Variant, Dictionary

class TestObject(Object):
    def __init__(self, bus):
        Object.__init__(self, bus, '/com/example/SimpleService/Test')
        self.items = []

    @method('com.example.SimpleService', in_signature='v')
    def PushItem(self, item):
        self.items.append(item)

    @method('com.example.SimpleService', out_signature='v')
    def PopItem(self):
        return self.items.pop()

    @method('com.example.SimpleService')
    def PrintItems(self):
        print 'My Items'
        print '========'
        for idx, item in enumerate(self.items):
            print ' %d) %r' % (idx, item)
        print

    @method('com.example.SimpleService')
    @annotate(i=UInt32, return_=UInt32)
    def ExpensiveCalculation(self, i):
        while i < 1000:
            i += 1
        return i

    @method('com.example.SimpleService')
    @annotate(something=Variant)
    def PrintSomething(self, something):
        print 'Something:', something

    @method('com.example.SimpleService', in_signature='v', out_signature='s')
    def Repr(self, value):
        return repr(value)

    @method('com.example.SimpleService')
    @annotate(dic=Dictionary(str, str), key=str, return_=str)
    def GetItem(self, dic, key):
        return dic[key]

bus = SessionBus()
bus.request_name('com.example.SimpleService')
obj = bus.add_object(TestObject(bus))

mainloop = Mainloop([bus])
mainloop.run()

