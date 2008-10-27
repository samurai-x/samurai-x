import ctypes
import ctypes.util
from ctypes import *

def load_lib(name):
    libname = ctypes.util.find_library(name)
    if not libname:
        raise OSError("Could not find library '%s'" % name)
    else:
        return ctypes.CDLL(libname)

_lib = load_lib('rsvg-2') #pyglet.lib.load_library('rsvg')
gobject = load_lib('gobject-2.0') #pyglet.lib.load_library('gobject')
gobject.g_type_init()

class RsvgDimensionData(Structure):
    _fields_ = [("width", c_int),
                ("height", c_int),
                ("em",c_double),
                ("ex",c_double)]

rsvg_handle_new_from_file = _lib.rsvg_handle_new_from_file
rsvg_handle_get_dimensions = _lib.rsvg_handle_get_dimensions
rsvg_handle_render_cairo = _lib.rsvg_handle_render_cairo

__all__ = [
    'rsvg_handle_new_from_file', 
    'rsvg_handle_get_dimensions', 
    'rsvg_handle_render_cairo',
    'RsvgDimensionData',
]

