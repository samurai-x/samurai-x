import sys
sys.path.append('..')

from yaydbus.bus import SessionBus
from yaydbus.dbus_types import Variant, Array

bus = SessionBus()

obj = bus.get_object('/com/example/SimpleService/Test', 'com.example.SimpleService')
proxy = obj.get_bound('com.example.SimpleService')

print 'That should be 1000:', proxy.ExpensiveCalculation(1)
proxy.PrintSomething(Variant(33))
print proxy.Repr(Array(str)(['one', 'two', 'three']))
