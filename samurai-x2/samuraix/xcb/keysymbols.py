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

from samuraix.xcb import _xcb_keysyms
#from .event import KeyPressEvent, KeyReleaseEvent

class KeySymbols(object):
    """ object that holds keycode and keysyms """
    def __init__(self, connection, _key_symbols=None):
        self.connection = connection
        if _key_symbols is None:
            _key_symbols = _xcb_keysyms.xcb_key_symbols_alloc(self.connection._connection)
        self._key_symbols = _key_symbols

    # FIXME: use __del__ instead?
    def die(self):
        """
            it would be nice to call that.
        """
        _xcb_keysyms.xcb_key_symbols_free(self._key_symbols)

    def get_keysym(self, keycode, column=0):
        return _xcb_keysyms.xcb_key_symbols_get_keysym(self._key_symbols, keycode, column)

    def get_keycode(self, keysym):
        return _xcb_keysyms.xcb_key_symbols_get_keycode(self._key_symbols, keysym)

    def lookup_keysym(self, event, column=0):
        """
            There is no runtime check.
            As xcb_key_release_event_t is typedef'ed to
            xcb_key_press_event_t, there should be no difference,
            so we use xcb_key_press_lookup_keysym here.
            Could be a bug. Maybe a feature. Or both.
            TODO?
        """
#        func = None
        func = _xcb_keysyms.xcb_key_press_lookup_keysym
#        if isinstance(event, KeyPressEvent):
#            func = _xcb_keysyms.xcb_key_press_lookup_keysym
#        elif isinstance(event, KeyReleaseEvent):
#            func = _xcb_keysyms.xcb_key_release_lookup_keysym
#        else:
#            raise Exception('event is neither a key press nor a key release event!')
        return func(self._key_symbols, event._event, column)
    
    def is_keypad_key(self, keysym):
        return _xcb_keysyms.is_keypad_key(keysym)

    def is_private_keypad_key(self, keysym):
        return _xcb_keysyms.is_private_keypad_key(keysym)

    def is_cursor_key(self, keysym):
        return _xcb_keysyms.is_cursor_key(keysym)

    def is_pf_key(self, keysym):
        return _xcb_keysyms.is_pf_key(keysym)

    def is_function_key(self, keysym):
        return _xcb_keysyms.is_function_key(keysym)

    def is_misc_function_key(self, keysym):
        return _xcb_keysyms.is_misc_function_key(keysym)

    def is_modifier_key(self, keysym):
        return _xcb_keysyms.is_modifier_key(keysym)

