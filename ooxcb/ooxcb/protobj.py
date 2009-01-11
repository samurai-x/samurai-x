import ctypes
from .util import MemBuffer

class Protobj(MemBuffer):
    def __init__(self, conn, parent, offset=0, size=0):
        self.conn = conn
        if isinstance(parent, basestring):
            self._buf = ctypes.create_string_buffer(parent, len(parent))
            address = ctypes.cast(self._buf, ctypes.c_void_p).value + offset
            size = len(parent) - offset
        elif isinstance(parent, MemBuffer):
            address = parent.address + offset
            size = 0
        else:
            raise Exception("what for an instance?? %s" % repr(parent))

        MemBuffer.__init__(self, address, size)
