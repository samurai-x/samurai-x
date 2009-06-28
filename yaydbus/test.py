from yaydbus.bus import SessionBus
from yaydbus.service import method, Object
from yaydbus.mainloop import Mainloop

class MyObject(Object):
    @method('com.example.SampleInterface', in_signature='s', out_signature='as')
    def HelloWorld(self, hello_message):
        print hello_message
        return ["Hi.", "There."]

bus = SessionBus()
assert bus.request_name('com.example.SampleService')
obj = bus.make_object('/SomeObject', MyObject)

m = Mainloop((bus,))
m.run()
