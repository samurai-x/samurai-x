from ctypes import *

c_uchar_p = c_ubyte_p = POINTER(c_ubyte)
c_uchar_p_p = POINTER(c_uchar_p)
c_char_p_p = POINTER(c_char_p)
