import ctypes

import _xcb_keysyms
#from .event import KeyPressEvent, KeyReleaseEvent

class KeySymbols(object):
    """ object that holds keycode and keysyms """
    def __init__(self, connection, _key_symbols=None):
        self.connection = connection
        if _key_symbols is None:
            _key_symbols = _xcb_keysyms.xcb_key_symbols_alloc(self.connection._connection)
        self._key_symbols = _key_symbols

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

