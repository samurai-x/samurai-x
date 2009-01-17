import ctypes

from .util import MemBuffer
from .response import Response

class Event(Response):
    event_name = 'on_event'
    def __init__(self, conn, parent, offset=0, size=0):
        Response.__init__(self, conn, parent, offset, size)
        self.event_target = conn

    @classmethod
    def create(cls, conn, event):
        opcode = event.contents.response_type

        type = cls

        if (opcode in conn.events and conn.events[opcode]):
            type = conn.events[opcode]

        shim = MemBuffer(ctypes.addressof(event.contents)) 
        return type(conn, shim)

    def dispatch(self):
        print 'Dispatching %s to %s ...' % (self.event_name, self.event_target)
        self.event_target.dispatch_event(self.event_name, self)
