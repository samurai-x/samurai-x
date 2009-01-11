import ctypes

from .libxcb import xcb_generic_error_t
from .response import Response
from .util import MemBuffer

class Error(Response):
    @property
    def _casted(self):
        return ctypes.cast(self.getvalue(), ctypes.POINTER(xcb_generic_error_t))

    @property
    def code(self):
        return self._casted.code

    @classmethod
    def set(cls, conn, err):
        if err:
            e = err.contents
            opcode = e.error_code
            type, exception = conn.errors[opcode]
            shim = MemBuffer(ctypes.addressof(e))
        
            raise exception(conn, type(conn, shim))
