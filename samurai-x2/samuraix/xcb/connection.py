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

import samuraix.event

from . import (_xcb, keysymbols, atom, cookie, screen, cursor)

from .containers import SizeHints
from .util import cached_property
from .pythonize import Pythonizer

class XcbException(Exception):
    pass

class Connection(samuraix.event.EventDispatcher):
    """
        The central connection, similar to Xlib's Display.
        You have to create a connection before you can use
        xcb, and you should really call `Connection.disconnect`
        after being done.

        All objects have a reference to the connection they belong to.
        The connection object holds a cache of resource objects
        (subclasses of `resource.Resource`, e.g. `window.Window` or
        `pixmap.Pixmap`), so it should be guaranteed that there is
        only *one* resource representation for an xid using *one*
        connection.
    """
    def __init__(self, address=None):
        """
            open a new connection.
            
            :Parameters:
                `address` : str
                    Specify a display address (like ":1") or
                    pass None to use the DISPLAY environment
                    variable.

        """
        super(Connection, self).__init__()
        
        if address is None:
            address = ''
        self._connection = _xcb.xcb_connect(address, ctypes.pointer(ctypes.c_long(0))).contents # TODO: set screen
        self._fd = _xcb.xcb_get_file_descriptor(self._connection)
        self.atoms = atom.AtomDict(self)
        self._resource_cache = {} # Resource xid: Resource object
        self._keysymbols = None # a KeySymbols object, if needed
        self.pythonizer = Pythonizer(self)
        self.cursors = cursor.Cursors(self)
       
    @property
    def keysymbols(self):
        """
            get (one!) `keysymbols.KeySymbols` instance if needed
            This instance will be killed when you call `self.disconnect`.
        """
        if self._keysymbols is None:
            self._keysymbols = keysymbols.KeySymbols(self)
        return self._keysymbols

    def pythonize(self, identifier, data):
        """
            just a convenience method, a shortcut for
            `connection.pythonizer.pythonize(identifier, data)`.
        """
        return self.pythonizer.pythonize(identifier, data)

    def get_from_cache(self, xid):
        """ 
            return the resource object with the associated xid `xid` if
            it is in cache or None if it isn't.
        """
        return self._resource_cache.get(xid, None)

    def add_to_cache(self, obj):
        """
            add the resource object `obj` to the cache

            :note: will raise an AssertionError if it's already in cache.
        """
        assert obj._xid not in self._resource_cache # already in cache!
        self._resource_cache[obj._xid] = obj # TODO: make a weak reference?

    def remove_from_cache(self, obj):
        """
            delete the resource object `obj` entry in the cache

            :note: it has to be sure that the object is in the cache.
        """
        del self._resource_cache[obj._xid]

    def disconnect(self):
        """
            Disconnect from the server. You should really do this.
        """
        if self._connection is None:
            raise XcbException('You can disconnect a display only one time.')
        if self._keysymbols is not None:
            self._keysymbols.die()
            self._keysymbols = None
        _xcb.xcb_disconnect(ctypes.pointer(self._connection))
        self._connection = None

    def __del__(self):
        if self._connection is not None:
            self.disconnect()

    @property
    def _setup(self):
        """
            get the (internal) xcb setup struct
        """
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

    def pythonize_property(self, _reply):
        """
            convert a property reply to a list of python values and return it.

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

        def _pythonize_integer():
            value = _xcb.xcb_get_property_value(_reply)
            p_int8_t = ctypes.POINTER(ctypes.c_int * _xcb.xcb_get_property_value_length(_reply))
            return list(ctypes.cast(value, p_int8_t).contents)

        def _pythonize_atom():
            return [self.pythonize('ATOM', xid) for xid in _pythonize_cardinal()]

        def _pythonize_window():
            return [self.pythonize('WINDOW', xid) for xid in _pythonize_cardinal()]

        def _pythonize_wm_size_hints():
            value = _xcb.xcb_get_property_value(_reply)

            length = _xcb.xcb_get_property_value_length(_reply)
            p_int_t = ctypes.POINTER(ctypes.c_int * length) 
            p_uint_t = ctypes.POINTER(ctypes.c_uint * length)

            values = list(ctypes.cast(value, p_int_t).contents)[1:-1]
            uints = list(ctypes.cast(value, p_uint_t).contents)
            flags = uints[0]
            win_gravity = uints[-1]

            kwargs = dict(zip(SizeHints.properties, values))
            kwargs['flags'] = flags
            kwargs['win_gravity'] = win_gravity

            hints = SizeHints(**kwargs)

            return hints

        PYTHONIZERS = {
                       'CARDINAL': _pythonize_cardinal,
                       'INTEGER': _pythonize_integer,
                       'STRING': _pythonize_string,
                       'UTF8_STRING': _pythonize_string,
                       'WM_SIZE_HINTS': _pythonize_wm_size_hints,
                       'ATOM': _pythonize_atom,
                       'WINDOW': _pythonize_window
                       }
        if not (_reply and _reply.type): # return if reply's atom is 0 -> invalid
            return []
        try:
            return PYTHONIZERS[atom.Atom(self, _reply.type).get_name()]()
        except KeyError, e:
            return None # TODO: raise?

    def xize_property(self, window, my_atom, prop, prop_type=None):
        """
            convert a window property object to a XCB value

            :Parameters:
                `window`: window.Window
                    The window object the property does belong to
                `my_atom`: atom.Atom
                    The window property atom object
                `prop`: list
                    The property contents as list
                `prop_type`: atom.Atom or None
                    The property type atom object, e.g. the STRING atom
                    If this is None, the property type atom will be 
                    requested: this will cause a more or less slow
                    atom request.
                    If the atom is created newly, you *have to*
                    specify `prop_type` obligatorily.
            :returns: The data as ctypes void pointer, the property type atom 
                and the data length.
            :rtype: a tuple: (pointer to data, atom.Atom, data length)
        """
        def check():
            assert isinstance(prop, list) # TODO: and iterables?
            if prop:
                cls = prop[0].__class__
                assert all(v.__class__ == cls for v in prop)
            
        def _xize_string():
            return ctypes.create_string_buffer('\x00'.join(prop)+'\x00')

        def _xize_cardinal():
            return (ctypes.c_uint * len(prop))(*[v for v in prop])

        def _xize_integer():
            return (ctypes.c_int * len(prop))(*[v for v in prop])

        def _xize_window():
            return (ctypes.c_uint * len(prop))(*[v.xize() for v in prop])

        def _xize_atom():
            return (ctypes.c_uint * len(prop))(*[v.xize() for v in prop])

        check()

        if not prop_type:
            prop_type = atom.Atom(self, cookie.PropertyRequest(self, window, my_atom)._value.type).get_name()
        
        XIZERS = {
                 'STRING': _xize_string,
                 'UTF8_STRING': _xize_string,
                 'CARDINAL': _xize_cardinal,
                 'INTEGER': _xize_integer,
                 'WINDOW': _xize_window,
                 'ATOM': _xize_atom,
                 }
        data = XIZERS[prop_type]()
        
        return (ctypes.cast(data, ctypes.c_void_p), self.get_atom_by_name(prop_type), len(data))

    def flush(self):
        """
            perform a connection flush. That is necessary after any operation
            which does not require a separate response request.

            You normally should not have to call this yourself.
        """
        _xcb.xcb_flush(self._connection)

    def wait_for_event(self):
        """
            wait for a xcb event and return the pythonized
            `event.Event` subclass instance.
        """
        _event = _xcb.xcb_wait_for_event(self._connection)
        return event.pythonize_event(self, _event.contents)

    #def wait_for_event_fd(self, rlist=None, wlist=None, xlist=None, timeout=None):
    #    select((rlist or []) + [self._fd], 
    #           (wlist or [])
    #           (xlist or []) + [self._fd], 
    #           timeout
    #    )
        

    def wait_for_event_dispatch(self):
        """
            wait for a xcb event and dispatch it using the
            pyglet event dispatcher coming with samurai-x
            as `samuraix.event`.
        """
        _event = _xcb.xcb_wait_for_event(self._connection)
        pyevent = event.pythonize_event(self, _event.contents)
        if pyevent:
            pyevent.dispatch()

    def poll_for_event(self):
        """
            poll for a xcb event; return None if there is no
            event in the queue, return the pythonized
            `event.Event` subclass instance if there is one.
        """
        _event = _xcb.xcb_poll_for_event(self._connection)
        if _event:
            return event.pythonize_event(self, _event.contents)
        else:
            return None

from samuraix.xcb import event
