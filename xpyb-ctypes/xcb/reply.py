import ctypes

from .response import Response
from .libxcb import xcb_generic_reply_t

class Reply(Response):
    @property
    def _casted(self):
        return ctypes.cast(self.address, ctypes.POINTER(xcb_generic_reply_t)).contents

    @property
    def length(self):
        return self._casted.length

