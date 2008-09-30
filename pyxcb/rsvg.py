import ctypes
from ctypes import *

import pyglet.lib

_lib = CDLL('librsvg-2.so') #pyglet.lib.load_library('rsvg')
gobject = CDLL('libgobject-2.0.so') #pyglet.lib.load_library('gobject')
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

