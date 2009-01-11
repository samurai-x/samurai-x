import ctypes

from .util import MemBuffer
from .response import Response

class Event(Response):
    @classmethod
    def create(cls, conn, event):
        opcode = event.contents.response_type

        type = cls

        if (opcode < len(conn.events) and conn.events[opcode]):
            type = conn.events[opcode]

        shim = MemBuffer(ctypes.addressof(event.contents)) 
        return type(conn, shim)

    def dispatch(self):
        self.event_target.dispatch_event(self.event_name, self)
