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
from .iterator import BaseIterator

class VisualType(object):
    def __init__(self, _visualtype):
        self._visualtype = _visualtype
        self.visual_id = _visualtype.visual_id
        self._class = _visualtype._class
        self.bits_per_rgb_value = _visualtype.bits_per_rgb_value
        self.colormap_entries = _visualtype.colormap_entries
        self.red_mask = _visualtype.red_mask
        self.green_mask = _visualtype.green_mask
        self.blue_mask = _visualtype.blue_mask

class VisualTypeIterator(BaseIterator):
    next_func = _xcb.xcb_visualtype_next

    def _transform(self, data):
        return VisualType(data)
        
class Depth(object):
    def __init__(self, _depth):
        self._depth = _depth
        self.depth = _depth.depth
        self.visuals_len = _depth.visuals_len

    @property
    def visualtypes(self):
        return VisualTypeIterator(_xcb.xcb_depth_visuals_iterator(self._depth))
