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
    def __init__(self, conn, parent, offset, length, type, size=-1):
        
        # construct it
        #datalen = len(data) 
        
        #assert not (size > 0 and length * size + offset > data), \
        #        "Protocol object buffer too short." # TODO: 'expected ?, got ?' ...
        self.conn = conn
        cur = offset
        for i in xrange(length):
            if isinstance(type, str):
                obj = build_value(type, length, parent.get_slice(size, cur))
                cur += size
            elif size > 0:
                obj = type(conn, parent, cur, size)
                cur += size
            else:
                obj = type(conn, parent, cur) # ... is a sequence
                datalen = len(obj)
                cur += datalen
            self.append(obj)
        
        self._buf = parent.get_subobject(offset)
        self._buf.size = cur - offset
    
    def buf(self):
        return self._buf # c compatibility ...

    def to_string(self):
        """
            my value is a list of ordinal values; return
            the string.
            :todo: use utf-8 (unichr)?
        """
        return ''.join(map(chr, self))
