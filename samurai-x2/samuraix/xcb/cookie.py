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

from . import _xcb
from .util import cached_property

LONG_LENGTH = 2 ** 32 - 1 # TODO: Wazzup?

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
        return self.connection.pythonize('ATOM', self._value.atom)

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
        # TODO: error handling?
        reply = _xcb.xcb_get_atom_name_reply(self.connection._connection,
                        self._cookie, ctypes.pointer(ctypes.pointer(e))) 
        if not reply:
            # TODO: better exceptions
            raise Exception('Null reply with connection %s atom %s' % 
                (self.connection, self.atom)
            ) 

        value = ctypes.cast(_xcb.xcb_get_atom_name_name(reply), ctypes.c_char_p)
        length = _xcb.xcb_get_atom_name_name_length(reply)

        return value.value[:length]

    def request(self):
        self._cookie = _xcb.xcb_get_atom_name(self.connection._connection, \
                        self.atom.xize())

class PropertyRequest(Cookie):
    def __init__(self, connection, window, atom):
        self.window = window
        self.atom = atom

        super(PropertyRequest, self).__init__(connection)

    def request(self):
        self._cookie = _xcb.xcb_get_property(self.connection._connection,
                0, self.window.xize(),
                self.atom.xize(),_xcb.XCB_GET_PROPERTY_TYPE_ANY,
                0, LONG_LENGTH)

    # NOTE: not cached.
    @property
    def _value(self):
        e = _xcb.xcb_generic_error_t()
        c = _xcb.xcb_get_property_reply(self.connection._connection, self._cookie, \
                ctypes.pointer(ctypes.pointer(e))) # TODO: error handling?
        if c:
            return c.contents
        else:
            return None

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
    def __init__(self, connection, window, atom, obj, format, prop_type):
        self.window = window
        self.atom = atom
        self.obj = obj
        self.format = format
        self.prop_type = prop_type

        super(ChangePropertyRequest, self).__init__(connection)

    def request(self):
        data, type_atom, length = self.connection.xize_property(self.window, self.atom, self.obj, self.prop_type)
        self._cookie = _xcb.xcb_change_property_checked(self.connection._connection,
             _xcb.XCB_PROP_MODE_REPLACE, self.window.xize(),
             self.atom.xize(), type_atom.xize(), self.format, # TODO: 8? oO
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
                0, self.window.xize(),
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
                                             self.drawable.xize())

    @cached_property
    def _value(self):
        return _xcb.xcb_get_geometry_reply(self.connection._connection,
                                          self._cookie,
                                          None).contents

    @cached_property
    def value(self):
        struct = self._value
        attr = {}
        for at in ('x', 'y', 'width', 'height', 'border_width', 'depth',):
            attr[at] = getattr(struct, at)
        attr['root'] = self.connection.pythonize('WINDOW', struct.root)
        return attr

class QueryPointer(object):
    def __init__(self, connection, reply):
        self.same_screen = reply.same_screen
        self.root = connection.pythonize('WINDOW', reply.root)
        self.child = connection.pythonize('WINDOW', reply.child)
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
                                              self.window.xize())

    @cached_property
    def value(self):
        return QueryPointer(self.connection, _xcb.xcb_query_pointer_reply(self.connection._connection,
                                                         self._cookie,
                                                         None).contents) # TODO: error handling

class GetWindowAttributesRequest(Cookie):
    def __init__(self, connection, window):
        self.window = window
        super(GetWindowAttributesRequest, self).__init__(connection)

    def request(self):
        self._cookie = _xcb.xcb_get_window_attributes(self.connection._connection,
                                                      self.window.xize())

    @cached_property
    def _value(self):
        return _xcb.xcb_get_window_attributes_reply(self.connection._connection, self._cookie, None).contents

    @cached_property
    def value(self):
        struct = self._value
        attr = {}
        # first: copy unchanged attributes
        for at in ('visual', # TODO: make `Visual` objects?
                   'bit_gravity', 'win_gravity', 'backing_planes', 'backing_pixel',
                   'save_under', 'map_is_installed', 'map_state', 'override_redirect',
                   'colormap', # TODO: make `Colormap` objects!
                   # TODO: add 'all_even_masks', 'your_event_masks', 'do_not_propagate_mask'
                   ):
            attr[at] = getattr(struct, at)
        # then copy the other attributes
        attr['class'] = struct._class
        return attr
