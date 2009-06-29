import sys
sys.path.append('..')

from yaydbus.bus import SessionBus
from yaydbus.dbus_types import Array

bus = SessionBus()

obj = bus.get_object('/com/example/SimpleService/Test', 'com.example.SimpleService')
proxy = obj.get_bound('com.example.SimpleService')

print 'That should be 1000:', proxy.ExpensiveCalculation(1)
proxy.PrintSomething(33)
print proxy.Repr(Array(str)(['one', 'two', 'three']))

proxy.PushItem('Hello')
proxy.PushItem('World!')
proxy.PushItem(Array(int)([1, 2, 3, 4, 5, 6]))

proxy.PrintItems()
print 'Popped:', proxy.PopItem()
proxy.PrintItems()
