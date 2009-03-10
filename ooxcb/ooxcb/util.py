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

class MemBuffer(object):
    def __init__(self, address, size=0):
        self.address = address 
        self.size = size #ctypes.sizeof(self.struct_instance)

    def get_slice(self, size, offset=0):
        return ctypes.string_at(self.address + offset, size)

    def get_subobject(self, offset):
        return MemBuffer(self.address + offset)

    def __len__(self):
        return self.size

    def get_string(self):
        return ctypes.string_at(self.address, self.size)

def struct_to_str(struct):
    return ctypes.string_at(ctypes.addressof(struct), ctypes.sizeof(struct))

class cached_property(object):
    """
        A simple cached property descriptor.
        from http://ronny.uberhost.de/simple-cached-for-properties-done-right
    """
    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        
        result = self.func(obj) 
        setattr(obj, self.name, result)
        return result

