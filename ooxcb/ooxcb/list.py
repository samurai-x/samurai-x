# Copyright (c) 2008-2009, samurai-x.org
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the samurai-x.org nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SAMURAI-X.ORG ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL SAMURAI-X.ORG  BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
                # If the type has a `pythonize_lazy` method defined, call it.
                if type.pythonize_lazy:
                    obj = obj.pythonize_lazy()

            self.append(obj)

        self.size = cur - offset

    def to_string(self):
        """
            my value is a list of ordinal values; return
            the string.
        """
        return ''.join(map(chr, self))

    def to_utf8(self):
        """
            interpret the string as utf-8 and return a Python
            unicode object.
        """
        return self.to_string().decode('utf-8')

