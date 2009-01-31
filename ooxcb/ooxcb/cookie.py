import ctypes

from . import (libxcb, util)
from .exception import XcbException
from .error import Error

class Cookie(object):
    def __init__(self):
        self.conn = None
        self.reply_cls = None
        self.request = None
        self.cookie = libxcb.xcb_void_cookie_t()

    def check(self):
        error = ctypes.pointer(libxcb.xcb_generic_error_t())
        if not (self.request.is_void and self.request.is_checked):
            raise XcbException('Request is not void and checked!')
        self.conn.check_conn()
        
        error = libxcb.xcb_request_check(self.conn.conn, self.cookie)
        Error.set(self.conn, error)

    def reply(self):
        if self.request.is_void:
            raise XcbException('Request has no reply.')
        self.conn.check_conn()
        
        err = libxcb.xcb_generic_error_t()
        error = ctypes.pointer(err)
        data = libxcb.xcb_wait_for_reply(self.conn.conn, self.cookie.sequence, ctypes.byref(error))
        Error.set(self.conn, error)
        if not data:
            raise IOError("I/O error on X server connection.")
        return self.reply_cls.create_from_address(self.conn, data)

