import _xcb
import ctypes

import atom
import cookie
import screen
import window
import event

from util import cached_property

class XcbException(Exception):
    pass

class Connection(object):
    def __init__(self, address=None):
        """
            open a new connection.
            
            :Parameters:
                `address` : str
                    Specify a display address (like ":1") or
                    pass None to use the DISPLAY environment
                    variable.

        """
        if address is None:
            address = ''
        self._connection = _xcb.xcb_connect(address, ctypes.pointer(ctypes.c_long(0))).contents # TODO: set screen
        self._atoms = {}

    def disconnect(self):
        """
            Disconnect from the server. You should really do this.
        """
        if self._connection is None:
            raise XcbException('You can disconnect a display only one time.')

        _xcb.xcb_disconnect(ctypes.pointer(self._connection))
        self._connection = None

    def __del__(self):
        if self._connection is not None:
            self.disconnect()

    @property
    def _setup(self):
        return _xcb.xcb_get_setup(self._connection)

    @cached_property # TODO: really cache it?
    def screens(self):
        """
            return a list of `screen.Screen` instances
            This property is cached.
        """
        setup = self._setup
        iterator = _xcb.xcb_setup_roots_iterator(setup)
        length = _xcb.xcb_setup_roots_length(setup)
        screens = []
        for i in range(length):
            screens.append(screen.Screen(self, iterator.data.contents))
            _xcb.xcb_screen_next(iterator)
        return screens

    def get_atom_by_name(self, name, only_if_exists=False):
        """
            return an `atom.Atom` instance for the atom
            name `name`.
        """
        return cookie.AtomRequest(self, name, only_if_exists).value

    def build_atom_list(self):
        self._atoms = {}
        for name in ('CARDINAL', 'STRING'): # update: http://tronche.com/gui/x/xlib/window-information/properties-and-atoms.html
            self._atoms[name] = self.get_atom_by_name(name, True)
        
    @property
    def atoms(self):
        if not self._atoms:
            self.build_atom_list()
        return self._atoms

    def pythonize_property(self, _reply):
        """
            convert a property reply to a python value and return it.

            STRING, UTF8_STRING : list of str
            CARDINAL : list of int
            ATOM : list of `atom.Atom`
            WINDOW : list of `window.Window`
        """
        def _pythonize_string():
            length = _xcb.xcb_get_property_value_length(_reply)
            value = _xcb.xcb_get_property_value(_reply)
            pointer = ctypes.cast(value, ctypes.POINTER(ctypes.c_ubyte * length))
            elems =  ''.join([chr(x) for x in pointer.contents]).rstrip('\x00').split('\x00') # strip trailing \x00
            return elems

        def _pythonize_cardinal():
            value = _xcb.xcb_get_property_value(_reply)
            p_uint8_t = ctypes.POINTER(ctypes.c_uint * _xcb.xcb_get_property_value_length(_reply))
            return list(ctypes.cast(value, p_uint8_t).contents)

        def _pythonize_atom():
            value = _xcb.xcb_get_property_value(_reply)
            p_uint8_t = ctypes.POINTER(ctypes.c_uint * _xcb.xcb_get_property_value_length(_reply))
            atom_values = ctypes.cast(value, p_uint8_t).contents
            return [atom.Atom(self, atom_value) for atom_value in atom_values]

        def _pythonize_window():
            value = _xcb.xcb_get_property_value(_reply)
            p_uint8_t = ctypes.POINTER(ctypes.c_uint * _xcb.xcb_get_property_value_length(_reply))
            return [window.Window(self, xid) for xid in ctypes.cast(value, p_uint8_t).contents]
           
        PYTHONIZERS = {
                       'CARDINAL': _pythonize_cardinal,
                       'STRING': _pythonize_string,
                       'UTF8_STRING': _pythonize_string,
                       'ATOM': _pythonize_atom,
                       'WINDOW': _pythonize_window
                       }
        return PYTHONIZERS[atom.Atom(self, _reply.type).get_name()]()

    def xize_property(self, window, my_atom, prop, prop_type=None):
        def check():
            assert isinstance(prop, list) # TODO: and iterables?
            cls = prop[0].__class__
            assert all(v.__class__ == cls for v in prop)
            
        def _xize_string():
            return (ctypes.c_char_p * len(prop))(*[ctypes.c_char_p(v) for v in prop])

        def _xize_cardinal():
            return (ctypes.c_uint * len(prop))(*[ctypes.c_uint(v) for v in prop])

        def _xize_window():
            return (ctypes.c_uint * len(prop))(*[ctypes.c_uint(v) for v in prop])

        check()

        if not prop_type:
            prop_type = atom.Atom(self, cookie.PropertyRequest(self, window, my_atom)._value.type).get_name()
        
        XIZERS = {
                 'STRING': _xize_string,
                 'CARDINAL': _xize_cardinal,
                 'WINDOW': _xize_window
                 }
        data = XIZERS[prop_type]()
        print data[0]
        return (ctypes.cast(data, ctypes.c_void_p), self.get_atom_by_name(prop_type), len(data))

    def flush(self):
        _xcb.xcb_flush(self._connection)

    def wait_for_event(self):
        _event = _xcb.xcb_wait_for_event(self._connection)
        return event.pythonize_event(self, _event.contents)
