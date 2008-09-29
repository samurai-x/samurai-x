import cookie
import _xcb
import ctypes

CLASS_INPUT_OUTPUT = _xcb.XCB_WINDOW_CLASS_INPUT_OUTPUT

ATTR_MAP = {
            'back_pixel': _xcb.XCB_CW_BACK_PIXEL
           }

def xize_attributes(attributes):
    mask = 0
    values = []
    for key, value in attributes.iteritems():
        mask |= ATTR_MAP[key]
        values.append(value)
    # TODO
#    mask |= _xcb.XCB_CW_EVENT_MASK
#    values.append(_xcb.XCB_EVENT_MASK_EXPOSURE)
    return (ctypes.c_uint * len(values))(*values)

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
        attr = xize_attributes(attributes)

        _xcb.xcb_create_window(connection._connection, # connection
                               _xcb.XCB_COPY_FROM_PARENT, # depth
                               xid, # xid
                               parent, # parent xid
                               x, y,
                               width, height,
                               border_width,
                               class_,
                               visual,
                               len(attr),
                               attr)
        connection.flush()

        return cls(connection, xid)

    def map(self):
        _xcb.xcb_map_window(self.connection._connection, self._xid)
        self.connection.flush()
