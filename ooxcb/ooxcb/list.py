import ctypes
from ctypes import POINTER

BUILDERS = {'b': POINTER(ctypes.c_byte), 
        'B': POINTER(ctypes.c_ubyte),
        'h': POINTER(ctypes.c_short),
        'H': POINTER(ctypes.c_ushort),
        'i': POINTER(ctypes.c_int),
        'I': POINTER(ctypes.c_uint),
        'L': POINTER(ctypes.c_long), # correct? it's long long in xpyb's list.c
        'K': POINTER(ctypes.c_ulong), # correct?
        'f': POINTER(ctypes.c_float),
        'd': POINTER(ctypes.c_double)
        }

def build_value(s, size, data):
    return ctypes.cast(data, BUILDERS[s[0]]).contents.value

def slice_ptr(ptr, offset):
    return ptr.__class__.from_address(ctypes.addressof(ptr) + offset)

class List(list):
    def __init__(self, conn, stream, offset, length, type, size=-1):
        self.conn = conn
        cur = offset
        for i in xrange(length):
            # TODO: I don't think that call is necessary. If there are problems,
            # try to comment in this call ;-)
            #stream.seek(cur)
            if isinstance(type, str):
                obj = build_value(type, length, stream.read(size))
                cur += size
            elif size > 0:
                obj = type(conn)
                obj.read(stream)
                cur += size
            else:
                obj = type(conn) # ... is a sequence
                obj.read(stream)
                datalen = obj.size
                cur += datalen
            self.append(obj)

        self.size = cur - offset

    def to_string(self):
        """
            my value is a list of ordinal values; return
            the string.
            :todo: use utf-8 (unichr)?
        """
        return ''.join(map(chr, self))
