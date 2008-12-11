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

from . import _xcb
from .font import Font
from .resource import Resource

# See http://tronche.com/gui/x/xlib/appendix/b/ for values 
XUTIL_CURSOR_FLEUR = 52
XUTIL_CURSOR_LEFT_PTR = 68
XUTIL_CURSOR_SIZING = 120
XUTIL_CURSOR_BOTTOM_LEFT_CORNER = 12
XUTIL_CURSOR_BOTTOM_RIGHT_CORNER = 14
XUTIL_CURSOR_TOP_LEFT_CORNER = 134
XUTIL_CURSOR_TOP_RIGHT_CORNER = 136
XUTIL_CURSOR_DOUBLE_ARROW_HORIZ = 108
XUTIL_CURSOR_DOUBLE_ARROW_VERT = 116

class Cursor(Resource):
    def __init__(self, connection, xid):
        super(Cursor, self).__init__(connection, xid)

    def free(self):
        _xcb.xcb_free_cursor(self.connection._connection, self._xid)

    # TODO: wrap xcb_create_cursor (cool stuff!)

    @classmethod
    def create_glyph(cls, connection, source_font, mask_font, source_char, \
            mask_char, fore_red, fore_green, fore_blue,
            back_red, back_green, back_blue):
            xid = _xcb.xcb_generate_id(connection._connection)
            _xcb.xcb_create_glyph_cursor(connection._connection, xid, 
                    source_font._xid, 
                    mask_font._xid, 
                    source_char, 
                    mask_char, 
                    fore_red, fore_green, fore_blue,
                    back_red, back_green, back_blue)

            return cls(connection, xid)


class Cursors(dict):
    def __init__(self, connection):
        self.connection = connection    
        self.font = None

        cursors = (
            ('Normal',    XUTIL_CURSOR_LEFT_PTR),
            ('Resize',    XUTIL_CURSOR_SIZING),
            ('ResizeH',   XUTIL_CURSOR_DOUBLE_ARROW_HORIZ),
            ('ResizeV',   XUTIL_CURSOR_DOUBLE_ARROW_VERT),
            ('Move',      XUTIL_CURSOR_FLEUR),
            ('TopRight',  XUTIL_CURSOR_TOP_RIGHT_CORNER),
            ('TopLeft',   XUTIL_CURSOR_TOP_LEFT_CORNER),
            ('BotRight',  XUTIL_CURSOR_BOTTOM_RIGHT_CORNER),
            ('BotLeft',   XUTIL_CURSOR_BOTTOM_LEFT_CORNER),
        )

        for name, cursor_font in cursors:
            self._new(name, cursor_font)

    def _new(self, name, cursor_font):
        if self.font is None:
            self.font = Font.open(self.connection, "cursor") 

        cursor = Cursor.create_glyph(self.connection, 
                self.font, self.font,
                cursor_font, cursor_font + 1,
                0, 0, 0,
                65535, 65535, 65535)

        self[name] = cursor


