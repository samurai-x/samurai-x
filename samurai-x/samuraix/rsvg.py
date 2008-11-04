# Copyright (c) 2008, samurai-x.org
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
