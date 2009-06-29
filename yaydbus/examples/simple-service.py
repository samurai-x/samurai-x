import sys
sys.path.append('..')

from yaydbus.bus import SessionBus
from yaydbus.service import Object, signal, method
from yaydbus.util import annotate
from yaydbus.mainloop import Mainloop
from yaydbus.dbus_types import UInt32, Variant

class TestObject(Object):
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

bus = SessionBus()
bus.request_name('com.example.SimpleService')
obj = bus.make_object('/com/example/SimpleService/Test', TestObject)

mainloop = Mainloop([bus])
mainloop.run()

