# Copyright (c) 2008-2009, samurai-x.org
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

from . import libxcb
from .event import Event
from .eventsys import EventDispatcher
from .error import Error
from .atoms import AtomDict
from .keysyms import Keysyms

class Connection(EventDispatcher):
    def __init__(self, core):
        EventDispatcher.__init__(self)

        self.core = core(self)
        setattr(self, core.header, self.core)

        self.conn = None
        self.events = {}
        self.errors = {}
        self.extcache = {}
        self._setup = None
        # The following option is only for debugging,
        # and it should be removed in a release.
        # If synchronous_check is True, all events
        # will be sended as checked (regardless if
        # x() or x_checked() is called) and each requests
        # will be checked automatically.
        # ... AND THAT'S SLOW!
        self.synchronous_check = False

        self.keysyms = Keysyms(self)

        self._cache = {}
        self.atoms = AtomDict(self)
        
    def setup(self):
        import ooxcb
        # load core ...
        ext = self.core
        events = ooxcb.CORE_EVENTS
        errors = ooxcb.CORE_ERRORS
        self.setup_helper(ext, events, errors)
       
        for key, events in ooxcb.EXT_EVENTS.iteritems():
            errors = ooxcb.EXT_ERRORS[key]
            ext = self.load_ext(key)

            if ext.present:
                self.setup_helper(ext, events, errors)

    def setup_helper(self, ext, events, errors):
        for num, type in events.iteritems():
            opcode = ext.first_event + num
            self.events[opcode] = type
            # register all events to their target!
            type.event_target_class.register_event_type(type.event_name)

        for num, type in errors.iteritems():
            opcode = ext.first_error + num
            self.errors[opcode] = type

    def load_ext(self, key):
        import ooxcb
        if key in self.extcache:
            return self.extcache[key]
        else:
            cls = ooxcb.EXTDICT[key]
            ext = cls(self, key)
            reply = libxcb.xcb_get_extension_data(self.conn, key.key).contents
            ext.present = reply.present
            ext.major_opcode = reply.major_opcode
            ext.first_event = reply.first_event
            ext.first_error = reply.first_error
            
            self.extcache[key] = ext
            setattr(self, cls.header, ext)

            return ext
    
    def __call__(self, key):
        self.check_conn()
        ext = self.load_ext(key)
        return ext 

    def check_conn(self):
        assert self.conn is not None, "Invalid Connection"

    def has_error(self):
        self.check_conn()
        return bool(libxcb.xcb_connection_has_error(self.conn))

    def get_file_descriptor(self):
        self.check_conn()
        return libxcb.xcb_get_file_descriptor(self.conn)
    
    def get_maximum_request_length(self):
        self.check_conn()
        return libxcb.xcb_connection_get_maximum_request_length(self.conn)

    def prefetch_maximum_request_length(self):
        self.check_conn()
        libxcb.xcb_prefetch_maximum_request_length(self.conn)
    
    def get_setup(self):
        self.check_conn()
        if self._setup is None:
            s = libxcb.xcb_get_setup(self.conn)
            addr = ctypes.addressof(s.contents)
            from . import SETUP
            self._setup = SETUP.create_from_address(self, addr)

        return self._setup

    def generate_id(self):
        self.check_conn()
        xid = libxcb.xcb_generate_id(self.conn)
        # TODO: error checking ...
        return xid

    def wait_for_event(self):
        data = libxcb.xcb_wait_for_event(self.conn)
        if not data:
            raise IOError("I/O error on X server connection.")
        if data.contents.response_type == 0:
            Error.set(self, ctypes.cast(data, ctypes.POINTER(libxcb.xcb_generic_error_t)))
            return
        return Event.create(self, data)

    def poll_for_event(self):
        data = libxcb.xcb_poll_for_event(self.conn)
        if not data:
            return None 

        if data.contents.response_type == 0:
            Error.set(self, ctypes.cast(data, ctypes.POINTER(libxcb.xcb_generic_error_t)))
            return
        return Event.create(self, data)
       
    def flush(self):
        self.check_conn()
        libxcb.xcb_flush(self.conn)

    def disconnect(self):
        if self.conn:
            libxcb.xcb_disconnect(self.conn)
            self.conn = None

    def add_to_cache(self, xid, obj):
        self._cache[xid] = obj

    def get_from_cache_fallback(self, xid, cls):
        """
            If there is a resource using the xid `xid` in the cache,
            return it. If not, instantiate `cls`, add to cache
            and return the newly created object.
        """
        if xid in self._cache:
            return self._cache[xid]
        else:
            self._cache[xid] = ret = cls(self, xid)
            return ret
