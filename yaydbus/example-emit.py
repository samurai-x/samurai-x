from yaydbus.mainloop import Mainloop
from yaydbus.bus import SessionBus
from yaydbus.service import Object, signal, method
from yaydbus.util import annotate

class TestObject(Object):
    @signal('com.example.TestService')
    @annotate(message='s')
    def HelloSignal(self, message):
        # The signal is emitted when this method exits
        # You can have code here if you wish
        pass

    @method('com.example.TestService')
    @annotate(return_='s')
    def emitHelloSignal(self):
        #you emit signals by calling the signal's skeleton method
        self.HelloSignal('Hello')
        return 'Signal emitted'

    @method("com.example.TestService",
            out_signature='')
    def Exit(self):
        loop.quit()

if __name__ == '__main__':
    bus = SessionBus()
    bus.request_name('com.example.TestService')
    object = bus.make_object('/com/example/TestService/object', TestObject)

    loop = Mainloop([bus])
    loop.run()
