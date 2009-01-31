import ctypes

from . import libxcb

class Extension(object):
    def __init__(self, conn, key=None):
        self.key = key
        self.conn = conn
        self.major_opcode = 0
        self.first_event = 0
        self.first_error = 0
        
    def send_request(self, request, cookie, reply_cls=None):
        # TODO: remove that...
        if (self.conn.synchronous_check and request.is_void):
            request.is_checked = True

        xcb_req = libxcb.xcb_protocol_request_t()
        xcb_req.count = 2
        xcb_req.ext = ctypes.pointer(self.key.key) if self.key is not None else None # TODO?
        xcb_req.opcode = request.opcode
        xcb_req.isvoid = request.is_void
    
        s = request.buffer
        data = ctypes.cast(ctypes.create_string_buffer(s, len(s)), ctypes.c_void_p)
        
        xcb_parts = (libxcb.iovec * 2)()
        addr = ctypes.cast(xcb_parts, ctypes.c_void_p).value

        xcb_parts[0].iov_base = data
        xcb_parts[0].iov_len = request.size
        xcb_parts[1].iov_base = 0
        xcb_parts[1].iov_len = -xcb_parts[0].iov_len & 3 # ... O_o

        flags = libxcb.XCB_REQUEST_CHECKED if request.is_checked else 0
        seq = libxcb.xcb_send_request(self.conn.conn, flags, 
                xcb_parts,#ctypes.cast(addr + 2, ctypes.POINTER(libxcb.iovec)), 
                ctypes.byref(xcb_req))
        cookie.conn = self.conn
        cookie.request = request
        cookie.reply_cls = reply_cls
        cookie.cookie.sequence = seq
        
        # TODO: remove that...
        if (self.conn.synchronous_check and request.is_void):
            cookie.check()
        return cookie
