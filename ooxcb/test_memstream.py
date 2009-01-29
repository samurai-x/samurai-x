from ctypes import *
from construct import *

from ooxcb.memstream import MemoryInputStream

class MyStructure(Structure):
    _fields_ = [
            ('a', c_int),
            ('b', c_float)
            ]


c_struct = MyStructure()
c_struct.a = 123
c_struct.b = 666.666 

struct = Struct('struct',
        UNInt32('a'),
        NFloat32('b'))

address = addressof(c_struct)
stream = MemoryInputStream(address)

print struct.parse_stream(stream)
