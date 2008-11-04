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

import _xcb
import window
from .iterator import BaseIterator
from util import cached_property
from . import depth

class DepthIterator(BaseIterator):
    next_func = _xcb.xcb_depth_next

    def _transform(self, data):
        return depth.Depth(data)

class Screen(object):
    @classmethod
    def get_screen_count(cls, connection):
        return _xcb.xcb_setup_roots_length(connection._setup)

    def __init__(self, connection, _screen):
        self.connection = connection
        self._screen = _screen

    # TODO - surely this should be cached?!
    @cached_property
    def root(self):
        """
            return the root window instance
        """
        return window.Window(self.connection, self._screen.root)

    @property
    def root_visual(self):
        return self._screen.root_visual

    @property
    def white_pixel(self):
        return self._screen.white_pixel

    @property
    def black_pixel(self):
        return self._screen.black_pixel

    @property
    def allowed_depths(self):
        return DepthIterator(_xcb.xcb_screen_allowed_depths_iterator(self._screen))

    @cached_property # TODO: really cache it?
    def root_visual_type(self):
        """
            returns either a root visual type or None.
            TODO: implement pythinonic iterators
            TODO: add a `Visual` object?
        """
        for d in self.allowed_depths:
            for vt in d.visualtypes:
                if self._screen.root_visual == vt.visual_id:
                    return vt
        return None

    @property
    def root_depth(self):
        return self._screen.root_depth

    @property
    def width_in_pixels(self):
        return self._screen.width_in_pixels

    @property
    def height_in_pixels(self):
        return self._screen.height_in_pixels

    @property
    def size_in_pixels(self):
        return (self.width_in_pixels, self.height_in_pixels)

