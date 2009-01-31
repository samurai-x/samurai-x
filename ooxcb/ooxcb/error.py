import ctypes

from .libxcb import xcb_generic_error_t
from .response import Response
from .util import MemBuffer

class Error(Response):
    @classmethod
    def set(cls, conn, err):
        if err:
            e = err.contents
            opcode = e.error_code
            type, exception = conn.errors[opcode]
            address = ctypes.addressof(e)
        
            inst = type.create_from_address(conn, address)
            raise exception(conn, inst)

