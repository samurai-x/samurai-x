import ctypes

from .libxcb import xcb_generic_event_t
from .protobj import Protobj

class Response(Protobj):
    @property
    def _casted(self):
        return ctypes.cast(self.getvalue(), ctypes.POINTER(xcb_generic_event_t))

    @property
    def _type(self): # to avoid name clash
        return self._casted.response_type

    @property
    def sequence(self):
        return self._casted.sequence

