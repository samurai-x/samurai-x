import warnings

import cookie
import _xcb
import ctypes
import util

def _xize_event_mask(events):
    mask = 0
    for cls in events:
        mask |= cls.event_mask
    if not _xcb.XCB_EVENT_MASK_EXPOSURE & mask:
        warnings.warn('You did not add the exposure event to your event mask.\n'
                      'Do you really want that?')
    return mask

CLASS_INPUT_OUTPUT = _xcb.XCB_WINDOW_CLASS_INPUT_OUTPUT

ATTRIBUTE_ORDER = [
            ('back_pixmap', _xcb.XCB_CW_BACK_PIXMAP), # TODO: xizer
            ('back_pixel', _xcb.XCB_CW_BACK_PIXEL),# TODO: xizer
            ('border_pixmap', _xcb.XCB_CW_BORDER_PIXMAP),# TODO: xizer
            ('border_pixel', _xcb.XCB_CW_BORDER_PIXEL),# TODO: xizer
            ('bit_gravity', _xcb.XCB_CW_BIT_GRAVITY),
            ('win_gravity', _xcb.XCB_CW_WIN_GRAVITY),
            ('backing_store', _xcb.XCB_CW_BACKING_STORE),
            ('backing_planes', _xcb.XCB_CW_BACKING_PLANES),
            ('backing_pixel', _xcb.XCB_CW_BACKING_PIXEL),
            ('override_redirect', _xcb.XCB_CW_OVERRIDE_REDIRECT),
            ('save_under', _xcb.XCB_CW_SAVE_UNDER),
            ('event_mask', _xcb.XCB_CW_EVENT_MASK, _xize_event_mask),
            ('dont_propagate', _xcb.XCB_CW_DONT_PROPAGATE),
            ('colormap', _xcb.XCB_CW_COLORMAP), # TODO: xizer
            ('cursor', _xcb.XCB_CW_CURSOR) # TODO: xizer
           ]

class Window(object):
    def __init__(self, connection, xid):
        self.connection = connection
        self._xid = xid

    def request_get_property(self, name):
        return cookie.PropertyRequest(self.connection, self, \
                                      self.connection.get_atom_by_name(name))

    def get_property(self, name):
        return self.request_get_property(name).value

    def request_set_property(self, name, content, format):
        return cookie.ChangePropertyRequest(self.connection, self, \
                                      self.connection.get_atom_by_name(name),
                                      content, format)

    def set_property(self, name, content, format):
        return self.request_set_property(name, content, format).value

    def request_send_event(self, event):
        return cookie.SendEventRequest(self.connection, self, event)

    def send_event(self, event):
        self.request_send_event(event).execute()

    @classmethod
    def create(cls, connection, screen, x, y, width, height, border_width=0, parent=None, class_=None, visual=None, attributes=None):
        if not class_:
            class_ = CLASS_INPUT_OUTPUT
        if not visual:
            visual = screen.root_visual
        if not attributes:
            attributes = {}
        if not parent:
            parent = screen.root

        parent = parent._xid

        xid = _xcb.xcb_generate_id(connection._connection) # TODO
        attr, mask = util.xize_attributes(attributes, ATTRIBUTE_ORDER)

        _xcb.xcb_create_window(connection._connection, # connection
                               _xcb.XCB_COPY_FROM_PARENT, # depth
                               xid, # xid
                               parent, # parent xid
                               x, y,
                               width, height,
                               border_width,
                               class_,
                               visual,
                               mask,
                               attr)

        if not 'event_mask' in attributes:
            warnings.warn('You did not an event mask to your window.\n'
                          'Do you really want that?')
        connection.flush()

        return cls(connection, xid)

    def map(self):
        _xcb.xcb_map_window(self.connection._connection, self._xid)
        self.connection.flush()
