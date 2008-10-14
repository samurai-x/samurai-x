from samuraix.xcb import _xcb

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

class Cursors(dict):
    def __init__(self, connection):
        self.connection = connection    

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
        font = _xcb.xcb_generate_id(self.connection._connection)
        _xcb.xcb_open_font(self.connection._connection, font, len("cursor")-1, "cursor")

        cursor = _xcb.xcb_generate_id(self.connection._connection)
        _xcb.xcb_create_glyph_cursor(self.connection._connection, cursor, font, font, 
                cursor_font, cursor_font + 1, 
                0, 0, 0,
                65535, 65535, 65535)

        self[name] = cursor


