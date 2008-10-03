from util import cached_property
import atom

import _xcb

import ctypes

LONG_LENGTH = 512 # TODO: Wazzup?

class Cookie(object):
    def __init__(self, connection):
        self.connection = connection
        self._cookie = None

        self.request()

    @cached_property
    def value(self):
        return None

    def request(self):
        pass

class AtomRequest(Cookie):
    def __init__(self, connection, name, only_if_exists=False):
        self.name = name
        self.only_if_exists = only_if_exists

        super(AtomRequest, self).__init__(connection)

    @cached_property
    def _value(self):
        e = _xcb.xcb_generic_error_t()
        cookie = _xcb.xcb_intern_atom_reply(self.connection._connection, \
                self._cookie, ctypes.pointer(ctypes.pointer(e)))
        # TODO: error handling? - it makes it much slower!
        return cookie.contents

    @cached_property
    def value(self):
        return atom.Atom(self.connection, self._value.atom)

    def request(self):
        self._cookie = _xcb.xcb_intern_atom(self.connection._connection, \
                        self.only_if_exists, len(self.name), self.name)

class AtomNameRequest(Cookie):
    def __init__(self, connection, atom):
        self.atom = atom

        super(AtomNameRequest, self).__init__(connection)

    @cached_property
    def value(self):
        e = _xcb.xcb_generic_error_t()
        reply = _xcb.xcb_get_atom_name_reply(self.connection._connection,
                        self._cookie, ctypes.pointer(ctypes.pointer(e))) # TODO: error handling?
        if not reply:
            raise Exception('Null reply') # TODO: better exceptions

        value = ctypes.cast(_xcb.xcb_get_atom_name_name(reply), ctypes.c_char_p)
        length = _xcb.xcb_get_atom_name_name_length(reply)

        return value.value[:length]

    def request(self):
        self._cookie = _xcb.xcb_get_atom_name(self.connection._connection, \
                        self.atom._atom)

class PropertyRequest(Cookie):
    def __init__(self, connection, window, atom):
        self.window = window
        self.atom = atom

        super(PropertyRequest, self).__init__(connection)

    def request(self):
        self._cookie = _xcb.xcb_get_property(self.connection._connection,
                0, self.window._xid,
                self.atom._atom,_xcb.XCB_GET_PROPERTY_TYPE_ANY,
                0, LONG_LENGTH)

    # NOTE: not cached.
    @property
    def _value(self):
        e = _xcb.xcb_generic_error_t()
        c = _xcb.xcb_get_property_reply(self.connection._connection, self._cookie, \
                ctypes.pointer(ctypes.pointer(e))).contents # TODO: error handling?
        return c

    @property
    def value(self):
        reply = self._value
#        length = _xcb.xcb_get_property_value_length(reply)
#        value = _xcb.xcb_get_property_value(reply)
#        pointer = ctypes.cast(value, ctypes.c_char_p)
        #print reply.type, self.connection.get_atom_by_name('CARDINAL'), self.connection.atoms
        return self.connection.pythonize_property(reply)
#        return pointer.value[:length]

class ChangePropertyRequest(Cookie):
    def __init__(self, connection, window, atom, obj, format):
        self.window = window
        self.atom = atom
        self.obj = obj
        self.format = format

        super(ChangePropertyRequest, self).__init__(connection)

    def request(self):
        data, type_atom, length = self.connection.xize_property(self.window, self.atom, self.obj)
        print type_atom._atom, length, self.window._xid
        self._cookie = _xcb.xcb_change_property_checked(self.connection._connection,
             _xcb.XCB_PROP_MODE_REPLACE,   self.window._xid,
             self.atom._atom, type_atom._atom, self.format, # TODO: 8? oO
            length, data)
        #print _xcb.xcb_request_check(self.connection._connection, self._cookie).contents.error_code

    def execute(self):
        self.connection.flush()

class SendEventRequest(Cookie):
    def __init__(self, connection, window, event):
        self.window = window
        self.event = event

        super(SendEventRequest, self).__init__(connection)

    def request(self):
        self._cookie = _xcb.xcb_send_event_checked(self.connection._connection,
                0, self.window._xid,
                _xcb.XCB_EVENT_MASK_SUBSTRUCTURE_REDIRECT | _xcb.XCB_EVENT_MASK_SUBSTRUCTURE_NOTIFY, # TODO: what's that?
                self.event.char_p)
    
    def execute(self):
        self.connection.flush()

class GetGeometryRequest(Cookie):
    def __init__(self, connection, drawable):
        self.drawable = drawable
        super(GetGeometryRequest, self).__init__(connection)

    def request(self):
        self._cookie = _xcb.xcb_get_geometry(self.connection._connection,
                                             self.drawable._xid)

    # TODO: continue!

class QueryPointer(object):
    def __init__(self, connection, reply):
        self.same_screen = reply.same_screen
        import window
        self.root = window.Window(connection, reply.root)
        self.child = window.Window(connection, reply.child)
        self.root_x = reply.root_x
        self.root_y = reply.root_y
        self.win_x = reply.win_x
        self.win_y = reply.win_y
        self.mask = reply.mask

class QueryPointerRequest(Cookie):
    def __init__(self, connection, window):
        self.window = window
        super(QueryPointerRequest, self).__init__(connection)

    def request(self):
        self._cookie = _xcb.xcb_query_pointer(self.connection._connection,
                                              self.window._xid)

    @cached_property
    def value(self):
        return QueryPointer(self.connection, _xcb.xcb_query_pointer_reply(self.connection._connection,
                                                         self._cookie,
                                                         None).contents) # TODO: error handling
