import ctypes

from .libxcb import xcb_generic_reply_t
from .response import Response
from .util import cached_property

class Reply(Response):
    @cached_property
    def _struct(self):
        return xcb_generic_reply_t.from_address(self._address)

    @property
    def length(self):
        return self._struct.length

