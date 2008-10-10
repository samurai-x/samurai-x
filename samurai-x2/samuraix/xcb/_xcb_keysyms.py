'''Wrapper for xcb-keysyms

Generated with:
wrap.py -o _xcb_keysyms.py -l xcb-keysyms /usr/local/include/xcb/xcb_keysyms.h

Done some modifications to make it use _xcb structs
'''

__docformat__ =  'restructuredtext'
__version__ = '$Id: wrap.py 1694 2008-01-30 23:12:00Z Alex.Holkner $'

import _xcb

import ctypes
from ctypes import *

import pyglet.lib

_lib = pyglet.lib.load_library('xcb-keysyms')

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (ctypes.c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]



class struct__XCBKeySymbols(Structure):
    __slots__ = [
    ]
struct__XCBKeySymbols._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__XCBKeySymbols(Structure):
    __slots__ = [
    ]
struct__XCBKeySymbols._fields_ = [
    ('_opaque_struct', c_int)
]

xcb_key_symbols_t = struct__XCBKeySymbols 	# /usr/local/include/xcb/xcb_keysyms.h:12

xcb_connection_t = _xcb.xcb_connection_t
# /usr/local/include/xcb/xcb_keysyms.h:22
xcb_key_symbols_alloc = _lib.xcb_key_symbols_alloc
xcb_key_symbols_alloc.restype = POINTER(xcb_key_symbols_t)
xcb_key_symbols_alloc.argtypes = [POINTER(xcb_connection_t)]

# /usr/local/include/xcb/xcb_keysyms.h:24
xcb_key_symbols_free = _lib.xcb_key_symbols_free
xcb_key_symbols_free.restype = None
xcb_key_symbols_free.argtypes = [POINTER(xcb_key_symbols_t)]

xcb_keysym_t = c_uint32 	# /usr/include/xcb/xproto.h:155
xcb_keycode_t = c_uint8 	# /usr/include/xcb/xproto.h:166
# /usr/local/include/xcb/xcb_keysyms.h:26
xcb_key_symbols_get_keysym = _lib.xcb_key_symbols_get_keysym
xcb_key_symbols_get_keysym.restype = xcb_keysym_t
xcb_key_symbols_get_keysym.argtypes = [POINTER(xcb_key_symbols_t), xcb_keycode_t, c_int]

# /usr/local/include/xcb/xcb_keysyms.h:30
xcb_key_symbols_get_keycode = _lib.xcb_key_symbols_get_keycode
xcb_key_symbols_get_keycode.restype = xcb_keycode_t
xcb_key_symbols_get_keycode.argtypes = [POINTER(xcb_key_symbols_t), xcb_keysym_t]


xcb_timestamp_t = c_uint32 	# /usr/include/xcb/xproto.h:144
xcb_window_t = c_uint32 	# /usr/include/xcb/xproto.h:34
struct_xcb_key_press_event_t = _xcb.struct_xcb_key_press_event_t

xcb_key_press_event_t = struct_xcb_key_press_event_t 	# /usr/include/xcb/xproto.h:476
# /usr/local/include/xcb/xcb_keysyms.h:33
xcb_key_press_lookup_keysym = _lib.xcb_key_press_lookup_keysym
xcb_key_press_lookup_keysym.restype = xcb_keysym_t
xcb_key_press_lookup_keysym.argtypes = [POINTER(xcb_key_symbols_t), POINTER(xcb_key_press_event_t), c_int]

xcb_key_release_event_t = xcb_key_press_event_t 	# /usr/include/xcb/xproto.h:481
# /usr/local/include/xcb/xcb_keysyms.h:37
xcb_key_release_lookup_keysym = _lib.xcb_key_release_lookup_keysym
xcb_key_release_lookup_keysym.restype = xcb_keysym_t
xcb_key_release_lookup_keysym.argtypes = [POINTER(xcb_key_symbols_t), POINTER(xcb_key_release_event_t), c_int]

struct_xcb_mapping_notify_event_t = _xcb.struct_xcb_mapping_notify_event_t

xcb_mapping_notify_event_t = struct_xcb_mapping_notify_event_t 	# /usr/include/xcb/xproto.h:1034
# /usr/local/include/xcb/xcb_keysyms.h:41
xcb_refresh_keyboard_mapping = _lib.xcb_refresh_keyboard_mapping
xcb_refresh_keyboard_mapping.restype = c_int
xcb_refresh_keyboard_mapping.argtypes = [POINTER(xcb_key_symbols_t), POINTER(xcb_mapping_notify_event_t)]

# /usr/local/include/xcb/xcb_keysyms.h:48
xcb_is_keypad_key = _lib.xcb_is_keypad_key
xcb_is_keypad_key.restype = c_int
xcb_is_keypad_key.argtypes = [xcb_keysym_t]

# /usr/local/include/xcb/xcb_keysyms.h:50
xcb_is_private_keypad_key = _lib.xcb_is_private_keypad_key
xcb_is_private_keypad_key.restype = c_int
xcb_is_private_keypad_key.argtypes = [xcb_keysym_t]

# /usr/local/include/xcb/xcb_keysyms.h:52
xcb_is_cursor_key = _lib.xcb_is_cursor_key
xcb_is_cursor_key.restype = c_int
xcb_is_cursor_key.argtypes = [xcb_keysym_t]

# /usr/local/include/xcb/xcb_keysyms.h:54
xcb_is_pf_key = _lib.xcb_is_pf_key
xcb_is_pf_key.restype = c_int
xcb_is_pf_key.argtypes = [xcb_keysym_t]

# /usr/local/include/xcb/xcb_keysyms.h:56
xcb_is_function_key = _lib.xcb_is_function_key
xcb_is_function_key.restype = c_int
xcb_is_function_key.argtypes = [xcb_keysym_t]

# /usr/local/include/xcb/xcb_keysyms.h:58
xcb_is_misc_function_key = _lib.xcb_is_misc_function_key
xcb_is_misc_function_key.restype = c_int
xcb_is_misc_function_key.argtypes = [xcb_keysym_t]

# /usr/local/include/xcb/xcb_keysyms.h:60
xcb_is_modifier_key = _lib.xcb_is_modifier_key
xcb_is_modifier_key.restype = c_int
xcb_is_modifier_key.argtypes = [xcb_keysym_t]


__all__ = ['xcb_key_symbols_t', 'xcb_key_symbols_alloc',
'xcb_key_symbols_free', 'xcb_key_symbols_get_keysym',
'xcb_key_symbols_get_keycode', 'xcb_key_press_lookup_keysym',
'xcb_key_release_lookup_keysym', 'xcb_refresh_keyboard_mapping',
'xcb_is_keypad_key', 'xcb_is_private_keypad_key', 'xcb_is_cursor_key',
'xcb_is_pf_key', 'xcb_is_function_key', 'xcb_is_misc_function_key',
'xcb_is_modifier_key']
