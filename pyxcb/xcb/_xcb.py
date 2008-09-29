'''Wrapper for /usr/include/xcb/bigreq

Generated with:
wrap.py -o ../pyxcb/_xcb.py /usr/include/xcb/bigreq.h /usr/include/xcb/xcbext.h /usr/include/xcb/xcb.h /usr/include/xcb/xcbxlib.h /usr/include/xcb/xc_misc.h /usr/include/xcb/xproto.h

Do not modify this file.
'''

__docformat__ =  'restructuredtext'
__version__ = '$Id: wrap.py 1694 2008-01-30 23:12:00Z Alex.Holkner $'

import ctypes
from ctypes import *

import pyglet.lib

_lib = pyglet.lib.load_library('xcb')

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



X_PROTOCOL = 11 	# /usr/include/xcb/xcb.h:60
X_PROTOCOL_REVISION = 0 	# /usr/include/xcb/xcb.h:63
X_TCP_PORT = 6000 	# /usr/include/xcb/xcb.h:66
class struct_xcb_connection_t(Structure):
    __slots__ = [
    ]
struct_xcb_connection_t._fields_ = [
    ('_opaque_struct', c_int)
]

class struct_xcb_connection_t(Structure):
    __slots__ = [
    ]
struct_xcb_connection_t._fields_ = [
    ('_opaque_struct', c_int)
]

xcb_connection_t = struct_xcb_connection_t 	# /usr/include/xcb/xcb.h:77
class struct_anon_25(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_anon_25._fields_ = [
    ('data', POINTER(None)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_generic_iterator_t = struct_anon_25 	# /usr/include/xcb/xcb.h:91
class struct_anon_26(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
    ]
struct_anon_26._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
]

xcb_generic_reply_t = struct_anon_26 	# /usr/include/xcb/xcb.h:103
class struct_anon_27(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'pad',
        'full_sequence',
    ]
struct_anon_27._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('pad', c_uint32 * 7),
    ('full_sequence', c_uint32),
]

xcb_generic_event_t = struct_anon_27 	# /usr/include/xcb/xcb.h:116
class struct_anon_28(Structure):
    __slots__ = [
        'response_type',
        'error_code',
        'sequence',
        'pad',
        'full_sequence',
    ]
struct_anon_28._fields_ = [
    ('response_type', c_uint8),
    ('error_code', c_uint8),
    ('sequence', c_uint16),
    ('pad', c_uint32 * 7),
    ('full_sequence', c_uint32),
]

xcb_generic_error_t = struct_anon_28 	# /usr/include/xcb/xcb.h:129
class struct_anon_29(Structure):
    __slots__ = [
        'sequence',
    ]
struct_anon_29._fields_ = [
    ('sequence', c_uint),
]

xcb_void_cookie_t = struct_anon_29 	# /usr/include/xcb/xcb.h:138
class struct_xcb_char2b_t(Structure):
    __slots__ = [
        'byte1',
        'byte2',
    ]
struct_xcb_char2b_t._fields_ = [
    ('byte1', c_uint8),
    ('byte2', c_uint8),
]

xcb_char2b_t = struct_xcb_char2b_t 	# /usr/include/xcb/xproto.h:23
class struct_xcb_char2b_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_char2b_iterator_t._fields_ = [
    ('data', POINTER(xcb_char2b_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_char2b_iterator_t = struct_xcb_char2b_iterator_t 	# /usr/include/xcb/xproto.h:32
xcb_window_t = c_uint32 	# /usr/include/xcb/xproto.h:34
class struct_xcb_window_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_window_iterator_t._fields_ = [
    ('data', POINTER(xcb_window_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_window_iterator_t = struct_xcb_window_iterator_t 	# /usr/include/xcb/xproto.h:43
xcb_pixmap_t = c_uint32 	# /usr/include/xcb/xproto.h:45
class struct_xcb_pixmap_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_pixmap_iterator_t._fields_ = [
    ('data', POINTER(xcb_pixmap_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_pixmap_iterator_t = struct_xcb_pixmap_iterator_t 	# /usr/include/xcb/xproto.h:54
xcb_cursor_t = c_uint32 	# /usr/include/xcb/xproto.h:56
class struct_xcb_cursor_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_cursor_iterator_t._fields_ = [
    ('data', POINTER(xcb_cursor_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_cursor_iterator_t = struct_xcb_cursor_iterator_t 	# /usr/include/xcb/xproto.h:65
xcb_font_t = c_uint32 	# /usr/include/xcb/xproto.h:67
class struct_xcb_font_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_font_iterator_t._fields_ = [
    ('data', POINTER(xcb_font_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_font_iterator_t = struct_xcb_font_iterator_t 	# /usr/include/xcb/xproto.h:76
xcb_gcontext_t = c_uint32 	# /usr/include/xcb/xproto.h:78
class struct_xcb_gcontext_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_gcontext_iterator_t._fields_ = [
    ('data', POINTER(xcb_gcontext_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_gcontext_iterator_t = struct_xcb_gcontext_iterator_t 	# /usr/include/xcb/xproto.h:87
xcb_colormap_t = c_uint32 	# /usr/include/xcb/xproto.h:89
class struct_xcb_colormap_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_colormap_iterator_t._fields_ = [
    ('data', POINTER(xcb_colormap_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_colormap_iterator_t = struct_xcb_colormap_iterator_t 	# /usr/include/xcb/xproto.h:98
xcb_atom_t = c_uint32 	# /usr/include/xcb/xproto.h:100
class struct_xcb_atom_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_atom_iterator_t._fields_ = [
    ('data', POINTER(xcb_atom_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_atom_iterator_t = struct_xcb_atom_iterator_t 	# /usr/include/xcb/xproto.h:109
xcb_drawable_t = c_uint32 	# /usr/include/xcb/xproto.h:111
class struct_xcb_drawable_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_drawable_iterator_t._fields_ = [
    ('data', POINTER(xcb_drawable_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_drawable_iterator_t = struct_xcb_drawable_iterator_t 	# /usr/include/xcb/xproto.h:120
xcb_fontable_t = c_uint32 	# /usr/include/xcb/xproto.h:122
class struct_xcb_fontable_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_fontable_iterator_t._fields_ = [
    ('data', POINTER(xcb_fontable_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_fontable_iterator_t = struct_xcb_fontable_iterator_t 	# /usr/include/xcb/xproto.h:131
xcb_visualid_t = c_uint32 	# /usr/include/xcb/xproto.h:133
class struct_xcb_visualid_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_visualid_iterator_t._fields_ = [
    ('data', POINTER(xcb_visualid_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_visualid_iterator_t = struct_xcb_visualid_iterator_t 	# /usr/include/xcb/xproto.h:142
xcb_timestamp_t = c_uint32 	# /usr/include/xcb/xproto.h:144
class struct_xcb_timestamp_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_timestamp_iterator_t._fields_ = [
    ('data', POINTER(xcb_timestamp_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_timestamp_iterator_t = struct_xcb_timestamp_iterator_t 	# /usr/include/xcb/xproto.h:153
xcb_keysym_t = c_uint32 	# /usr/include/xcb/xproto.h:155
class struct_xcb_keysym_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_keysym_iterator_t._fields_ = [
    ('data', POINTER(xcb_keysym_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_keysym_iterator_t = struct_xcb_keysym_iterator_t 	# /usr/include/xcb/xproto.h:164
xcb_keycode_t = c_uint8 	# /usr/include/xcb/xproto.h:166
class struct_xcb_keycode_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_keycode_iterator_t._fields_ = [
    ('data', POINTER(xcb_keycode_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_keycode_iterator_t = struct_xcb_keycode_iterator_t 	# /usr/include/xcb/xproto.h:175
xcb_button_t = c_uint8 	# /usr/include/xcb/xproto.h:177
class struct_xcb_button_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_button_iterator_t._fields_ = [
    ('data', POINTER(xcb_button_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_button_iterator_t = struct_xcb_button_iterator_t 	# /usr/include/xcb/xproto.h:186
class struct_xcb_point_t(Structure):
    __slots__ = [
        'x',
        'y',
    ]
struct_xcb_point_t._fields_ = [
    ('x', c_int16),
    ('y', c_int16),
]

xcb_point_t = struct_xcb_point_t 	# /usr/include/xcb/xproto.h:194
class struct_xcb_point_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_point_iterator_t._fields_ = [
    ('data', POINTER(xcb_point_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_point_iterator_t = struct_xcb_point_iterator_t 	# /usr/include/xcb/xproto.h:203
class struct_xcb_rectangle_t(Structure):
    __slots__ = [
        'x',
        'y',
        'width',
        'height',
    ]
struct_xcb_rectangle_t._fields_ = [
    ('x', c_int16),
    ('y', c_int16),
    ('width', c_uint16),
    ('height', c_uint16),
]

xcb_rectangle_t = struct_xcb_rectangle_t 	# /usr/include/xcb/xproto.h:213
class struct_xcb_rectangle_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_rectangle_iterator_t._fields_ = [
    ('data', POINTER(xcb_rectangle_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_rectangle_iterator_t = struct_xcb_rectangle_iterator_t 	# /usr/include/xcb/xproto.h:222
class struct_xcb_arc_t(Structure):
    __slots__ = [
        'x',
        'y',
        'width',
        'height',
        'angle1',
        'angle2',
    ]
struct_xcb_arc_t._fields_ = [
    ('x', c_int16),
    ('y', c_int16),
    ('width', c_uint16),
    ('height', c_uint16),
    ('angle1', c_int16),
    ('angle2', c_int16),
]

xcb_arc_t = struct_xcb_arc_t 	# /usr/include/xcb/xproto.h:234
class struct_xcb_arc_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_arc_iterator_t._fields_ = [
    ('data', POINTER(xcb_arc_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_arc_iterator_t = struct_xcb_arc_iterator_t 	# /usr/include/xcb/xproto.h:243
class struct_xcb_format_t(Structure):
    __slots__ = [
        'depth',
        'bits_per_pixel',
        'scanline_pad',
        'pad0',
    ]
struct_xcb_format_t._fields_ = [
    ('depth', c_uint8),
    ('bits_per_pixel', c_uint8),
    ('scanline_pad', c_uint8),
    ('pad0', c_uint8 * 5),
]

xcb_format_t = struct_xcb_format_t 	# /usr/include/xcb/xproto.h:253
class struct_xcb_format_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_format_iterator_t._fields_ = [
    ('data', POINTER(xcb_format_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_format_iterator_t = struct_xcb_format_iterator_t 	# /usr/include/xcb/xproto.h:262
enum_xcb_visual_class_t = c_int
XCB_VISUAL_CLASS_STATIC_GRAY = 0
XCB_VISUAL_CLASS_GRAY_SCALE = 1
XCB_VISUAL_CLASS_STATIC_COLOR = 2
XCB_VISUAL_CLASS_PSEUDO_COLOR = 3
XCB_VISUAL_CLASS_TRUE_COLOR = 4
XCB_VISUAL_CLASS_DIRECT_COLOR = 5
xcb_visual_class_t = enum_xcb_visual_class_t 	# /usr/include/xcb/xproto.h:271
class struct_xcb_visualtype_t(Structure):
    __slots__ = [
        'visual_id',
        '_class',
        'bits_per_rgb_value',
        'colormap_entries',
        'red_mask',
        'green_mask',
        'blue_mask',
        'pad0',
    ]
struct_xcb_visualtype_t._fields_ = [
    ('visual_id', xcb_visualid_t),
    ('_class', c_uint8),
    ('bits_per_rgb_value', c_uint8),
    ('colormap_entries', c_uint16),
    ('red_mask', c_uint32),
    ('green_mask', c_uint32),
    ('blue_mask', c_uint32),
    ('pad0', c_uint8 * 4),
]

xcb_visualtype_t = struct_xcb_visualtype_t 	# /usr/include/xcb/xproto.h:285
class struct_xcb_visualtype_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_visualtype_iterator_t._fields_ = [
    ('data', POINTER(xcb_visualtype_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_visualtype_iterator_t = struct_xcb_visualtype_iterator_t 	# /usr/include/xcb/xproto.h:294
class struct_xcb_depth_t(Structure):
    __slots__ = [
        'depth',
        'pad0',
        'visuals_len',
        'pad1',
    ]
struct_xcb_depth_t._fields_ = [
    ('depth', c_uint8),
    ('pad0', c_uint8),
    ('visuals_len', c_uint16),
    ('pad1', c_uint8 * 4),
]

xcb_depth_t = struct_xcb_depth_t 	# /usr/include/xcb/xproto.h:304
class struct_xcb_depth_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_depth_iterator_t._fields_ = [
    ('data', POINTER(xcb_depth_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_depth_iterator_t = struct_xcb_depth_iterator_t 	# /usr/include/xcb/xproto.h:313
class struct_xcb_screen_t(Structure):
    __slots__ = [
        'root',
        'default_colormap',
        'white_pixel',
        'black_pixel',
        'current_input_masks',
        'width_in_pixels',
        'height_in_pixels',
        'width_in_millimeters',
        'height_in_millimeters',
        'min_installed_maps',
        'max_installed_maps',
        'root_visual',
        'backing_stores',
        'save_unders',
        'root_depth',
        'allowed_depths_len',
    ]
struct_xcb_screen_t._fields_ = [
    ('root', xcb_window_t),
    ('default_colormap', xcb_colormap_t),
    ('white_pixel', c_uint32),
    ('black_pixel', c_uint32),
    ('current_input_masks', c_uint32),
    ('width_in_pixels', c_uint16),
    ('height_in_pixels', c_uint16),
    ('width_in_millimeters', c_uint16),
    ('height_in_millimeters', c_uint16),
    ('min_installed_maps', c_uint16),
    ('max_installed_maps', c_uint16),
    ('root_visual', xcb_visualid_t),
    ('backing_stores', c_uint8),
    ('save_unders', c_uint8),
    ('root_depth', c_uint8),
    ('allowed_depths_len', c_uint8),
]

xcb_screen_t = struct_xcb_screen_t 	# /usr/include/xcb/xproto.h:335
class struct_xcb_screen_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_screen_iterator_t._fields_ = [
    ('data', POINTER(xcb_screen_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_screen_iterator_t = struct_xcb_screen_iterator_t 	# /usr/include/xcb/xproto.h:344
class struct_xcb_setup_request_t(Structure):
    __slots__ = [
        'byte_order',
        'pad0',
        'protocol_major_version',
        'protocol_minor_version',
        'authorization_protocol_name_len',
        'authorization_protocol_data_len',
    ]
struct_xcb_setup_request_t._fields_ = [
    ('byte_order', c_uint8),
    ('pad0', c_uint8),
    ('protocol_major_version', c_uint16),
    ('protocol_minor_version', c_uint16),
    ('authorization_protocol_name_len', c_uint16),
    ('authorization_protocol_data_len', c_uint16),
]

xcb_setup_request_t = struct_xcb_setup_request_t 	# /usr/include/xcb/xproto.h:356
class struct_xcb_setup_request_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_setup_request_iterator_t._fields_ = [
    ('data', POINTER(xcb_setup_request_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_setup_request_iterator_t = struct_xcb_setup_request_iterator_t 	# /usr/include/xcb/xproto.h:365
class struct_xcb_setup_failed_t(Structure):
    __slots__ = [
        'status',
        'reason_len',
        'protocol_major_version',
        'protocol_minor_version',
        'length',
    ]
struct_xcb_setup_failed_t._fields_ = [
    ('status', c_uint8),
    ('reason_len', c_uint8),
    ('protocol_major_version', c_uint16),
    ('protocol_minor_version', c_uint16),
    ('length', c_uint16),
]

xcb_setup_failed_t = struct_xcb_setup_failed_t 	# /usr/include/xcb/xproto.h:376
class struct_xcb_setup_failed_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_setup_failed_iterator_t._fields_ = [
    ('data', POINTER(xcb_setup_failed_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_setup_failed_iterator_t = struct_xcb_setup_failed_iterator_t 	# /usr/include/xcb/xproto.h:385
class struct_xcb_setup_authenticate_t(Structure):
    __slots__ = [
        'status',
        'pad0',
        'length',
    ]
struct_xcb_setup_authenticate_t._fields_ = [
    ('status', c_uint8),
    ('pad0', c_uint8 * 5),
    ('length', c_uint16),
]

xcb_setup_authenticate_t = struct_xcb_setup_authenticate_t 	# /usr/include/xcb/xproto.h:394
class struct_xcb_setup_authenticate_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_setup_authenticate_iterator_t._fields_ = [
    ('data', POINTER(xcb_setup_authenticate_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_setup_authenticate_iterator_t = struct_xcb_setup_authenticate_iterator_t 	# /usr/include/xcb/xproto.h:403
enum_xcb_image_order_t = c_int
XCB_IMAGE_ORDER_LSB_FIRST = 0
XCB_IMAGE_ORDER_MSB_FIRST = 1
xcb_image_order_t = enum_xcb_image_order_t 	# /usr/include/xcb/xproto.h:408
class struct_xcb_setup_t(Structure):
    __slots__ = [
        'status',
        'pad0',
        'protocol_major_version',
        'protocol_minor_version',
        'length',
        'release_number',
        'resource_id_base',
        'resource_id_mask',
        'motion_buffer_size',
        'vendor_len',
        'maximum_request_length',
        'roots_len',
        'pixmap_formats_len',
        'image_byte_order',
        'bitmap_format_bit_order',
        'bitmap_format_scanline_unit',
        'bitmap_format_scanline_pad',
        'min_keycode',
        'max_keycode',
        'pad1',
    ]
struct_xcb_setup_t._fields_ = [
    ('status', c_uint8),
    ('pad0', c_uint8),
    ('protocol_major_version', c_uint16),
    ('protocol_minor_version', c_uint16),
    ('length', c_uint16),
    ('release_number', c_uint32),
    ('resource_id_base', c_uint32),
    ('resource_id_mask', c_uint32),
    ('motion_buffer_size', c_uint32),
    ('vendor_len', c_uint16),
    ('maximum_request_length', c_uint16),
    ('roots_len', c_uint8),
    ('pixmap_formats_len', c_uint8),
    ('image_byte_order', c_uint8),
    ('bitmap_format_bit_order', c_uint8),
    ('bitmap_format_scanline_unit', c_uint8),
    ('bitmap_format_scanline_pad', c_uint8),
    ('min_keycode', xcb_keycode_t),
    ('max_keycode', xcb_keycode_t),
    ('pad1', c_uint8 * 4),
]

xcb_setup_t = struct_xcb_setup_t 	# /usr/include/xcb/xproto.h:434
class struct_xcb_setup_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_setup_iterator_t._fields_ = [
    ('data', POINTER(xcb_setup_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_setup_iterator_t = struct_xcb_setup_iterator_t 	# /usr/include/xcb/xproto.h:443
enum_xcb_mod_mask_t = c_int
XCB_MOD_MASK_SHIFT = 0
XCB_MOD_MASK_LOCK = 1
XCB_MOD_MASK_CONTROL = 2
XCB_MOD_MASK_1 = 3
XCB_MOD_MASK_2 = 4
XCB_MOD_MASK_3 = 5
XCB_MOD_MASK_4 = 6
XCB_MOD_MASK_5 = 7
xcb_mod_mask_t = enum_xcb_mod_mask_t 	# /usr/include/xcb/xproto.h:454
XCB_KEY_PRESS = 2 	# /usr/include/xcb/xproto.h:457
class struct_xcb_key_press_event_t(Structure):
    __slots__ = [
        'response_type',
        'detail',
        'sequence',
        'time',
        'root',
        'event',
        'child',
        'root_x',
        'root_y',
        'event_x',
        'event_y',
        'state',
        'same_screen',
    ]
struct_xcb_key_press_event_t._fields_ = [
    ('response_type', c_uint8),
    ('detail', xcb_keycode_t),
    ('sequence', c_uint16),
    ('time', xcb_timestamp_t),
    ('root', xcb_window_t),
    ('event', xcb_window_t),
    ('child', xcb_window_t),
    ('root_x', c_int16),
    ('root_y', c_int16),
    ('event_x', c_int16),
    ('event_y', c_int16),
    ('state', c_uint16),
    ('same_screen', c_uint8),
]

xcb_key_press_event_t = struct_xcb_key_press_event_t 	# /usr/include/xcb/xproto.h:476
XCB_KEY_RELEASE = 3 	# /usr/include/xcb/xproto.h:479
xcb_key_release_event_t = xcb_key_press_event_t 	# /usr/include/xcb/xproto.h:481
enum_xcb_button_mask_t = c_int
XCB_BUTTON_MASK_1 = 0
XCB_BUTTON_MASK_2 = 1
XCB_BUTTON_MASK_3 = 2
XCB_BUTTON_MASK_4 = 3
XCB_BUTTON_MASK_5 = 4
XCB_BUTTON_MASK_ANY = 5
xcb_button_mask_t = enum_xcb_button_mask_t 	# /usr/include/xcb/xproto.h:490
XCB_BUTTON_PRESS = 4 	# /usr/include/xcb/xproto.h:493
class struct_xcb_button_press_event_t(Structure):
    __slots__ = [
        'response_type',
        'detail',
        'sequence',
        'time',
        'root',
        'event',
        'child',
        'root_x',
        'root_y',
        'event_x',
        'event_y',
        'state',
        'same_screen',
    ]
struct_xcb_button_press_event_t._fields_ = [
    ('response_type', c_uint8),
    ('detail', xcb_button_t),
    ('sequence', c_uint16),
    ('time', xcb_timestamp_t),
    ('root', xcb_window_t),
    ('event', xcb_window_t),
    ('child', xcb_window_t),
    ('root_x', c_int16),
    ('root_y', c_int16),
    ('event_x', c_int16),
    ('event_y', c_int16),
    ('state', c_uint16),
    ('same_screen', c_uint8),
]

xcb_button_press_event_t = struct_xcb_button_press_event_t 	# /usr/include/xcb/xproto.h:512
XCB_BUTTON_RELEASE = 5 	# /usr/include/xcb/xproto.h:515
xcb_button_release_event_t = xcb_button_press_event_t 	# /usr/include/xcb/xproto.h:517
enum_xcb_motion_t = c_int
XCB_MOTION_NORMAL = 0
XCB_MOTION_HINT = 1
xcb_motion_t = enum_xcb_motion_t 	# /usr/include/xcb/xproto.h:522
XCB_MOTION_NOTIFY = 6 	# /usr/include/xcb/xproto.h:525
class struct_xcb_motion_notify_event_t(Structure):
    __slots__ = [
        'response_type',
        'detail',
        'sequence',
        'time',
        'root',
        'event',
        'child',
        'root_x',
        'root_y',
        'event_x',
        'event_y',
        'state',
        'same_screen',
    ]
struct_xcb_motion_notify_event_t._fields_ = [
    ('response_type', c_uint8),
    ('detail', c_uint8),
    ('sequence', c_uint16),
    ('time', xcb_timestamp_t),
    ('root', xcb_window_t),
    ('event', xcb_window_t),
    ('child', xcb_window_t),
    ('root_x', c_int16),
    ('root_y', c_int16),
    ('event_x', c_int16),
    ('event_y', c_int16),
    ('state', c_uint16),
    ('same_screen', c_uint8),
]

xcb_motion_notify_event_t = struct_xcb_motion_notify_event_t 	# /usr/include/xcb/xproto.h:544
enum_xcb_notify_detail_t = c_int
XCB_NOTIFY_DETAIL_ANCESTOR = 0
XCB_NOTIFY_DETAIL_VIRTUAL = 1
XCB_NOTIFY_DETAIL_INFERIOR = 2
XCB_NOTIFY_DETAIL_NONLINEAR = 3
XCB_NOTIFY_DETAIL_NONLINEAR_VIRTUAL = 4
XCB_NOTIFY_DETAIL_POINTER = 5
XCB_NOTIFY_DETAIL_POINTER_ROOT = 6
XCB_NOTIFY_DETAIL_NONE = 7
xcb_notify_detail_t = enum_xcb_notify_detail_t 	# /usr/include/xcb/xproto.h:555
enum_xcb_notify_mode_t = c_int
XCB_NOTIFY_MODE_NORMAL = 0
XCB_NOTIFY_MODE_GRAB = 1
XCB_NOTIFY_MODE_UNGRAB = 2
XCB_NOTIFY_MODE_WHILE_GRABBED = 3
xcb_notify_mode_t = enum_xcb_notify_mode_t 	# /usr/include/xcb/xproto.h:562
XCB_ENTER_NOTIFY = 7 	# /usr/include/xcb/xproto.h:565
class struct_xcb_enter_notify_event_t(Structure):
    __slots__ = [
        'response_type',
        'detail',
        'sequence',
        'time',
        'root',
        'event',
        'child',
        'root_x',
        'root_y',
        'event_x',
        'event_y',
        'state',
        'mode',
        'same_screen_focus',
    ]
struct_xcb_enter_notify_event_t._fields_ = [
    ('response_type', c_uint8),
    ('detail', c_uint8),
    ('sequence', c_uint16),
    ('time', xcb_timestamp_t),
    ('root', xcb_window_t),
    ('event', xcb_window_t),
    ('child', xcb_window_t),
    ('root_x', c_int16),
    ('root_y', c_int16),
    ('event_x', c_int16),
    ('event_y', c_int16),
    ('state', c_uint16),
    ('mode', c_uint8),
    ('same_screen_focus', c_uint8),
]

xcb_enter_notify_event_t = struct_xcb_enter_notify_event_t 	# /usr/include/xcb/xproto.h:585
XCB_LEAVE_NOTIFY = 8 	# /usr/include/xcb/xproto.h:588
xcb_leave_notify_event_t = xcb_enter_notify_event_t 	# /usr/include/xcb/xproto.h:590
XCB_FOCUS_IN = 9 	# /usr/include/xcb/xproto.h:593
class struct_xcb_focus_in_event_t(Structure):
    __slots__ = [
        'response_type',
        'detail',
        'sequence',
        'event',
        'mode',
    ]
struct_xcb_focus_in_event_t._fields_ = [
    ('response_type', c_uint8),
    ('detail', c_uint8),
    ('sequence', c_uint16),
    ('event', xcb_window_t),
    ('mode', c_uint8),
]

xcb_focus_in_event_t = struct_xcb_focus_in_event_t 	# /usr/include/xcb/xproto.h:604
XCB_FOCUS_OUT = 10 	# /usr/include/xcb/xproto.h:607
xcb_focus_out_event_t = xcb_focus_in_event_t 	# /usr/include/xcb/xproto.h:609
XCB_KEYMAP_NOTIFY = 11 	# /usr/include/xcb/xproto.h:612
class struct_xcb_keymap_notify_event_t(Structure):
    __slots__ = [
        'response_type',
        'keys',
    ]
struct_xcb_keymap_notify_event_t._fields_ = [
    ('response_type', c_uint8),
    ('keys', c_uint8 * 31),
]

xcb_keymap_notify_event_t = struct_xcb_keymap_notify_event_t 	# /usr/include/xcb/xproto.h:620
XCB_EXPOSE = 12 	# /usr/include/xcb/xproto.h:623
class struct_xcb_expose_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'window',
        'x',
        'y',
        'width',
        'height',
        'count',
    ]
struct_xcb_expose_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('window', xcb_window_t),
    ('x', c_uint16),
    ('y', c_uint16),
    ('width', c_uint16),
    ('height', c_uint16),
    ('count', c_uint16),
]

xcb_expose_event_t = struct_xcb_expose_event_t 	# /usr/include/xcb/xproto.h:638
XCB_GRAPHICS_EXPOSURE = 13 	# /usr/include/xcb/xproto.h:641
class struct_xcb_graphics_exposure_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'drawable',
        'x',
        'y',
        'width',
        'height',
        'minor_opcode',
        'count',
        'major_opcode',
    ]
struct_xcb_graphics_exposure_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('drawable', xcb_drawable_t),
    ('x', c_uint16),
    ('y', c_uint16),
    ('width', c_uint16),
    ('height', c_uint16),
    ('minor_opcode', c_uint16),
    ('count', c_uint16),
    ('major_opcode', c_uint8),
]

xcb_graphics_exposure_event_t = struct_xcb_graphics_exposure_event_t 	# /usr/include/xcb/xproto.h:658
XCB_NO_EXPOSURE = 14 	# /usr/include/xcb/xproto.h:661
class struct_xcb_no_exposure_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'drawable',
        'minor_opcode',
        'major_opcode',
    ]
struct_xcb_no_exposure_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('drawable', xcb_drawable_t),
    ('minor_opcode', c_uint16),
    ('major_opcode', c_uint8),
]

xcb_no_exposure_event_t = struct_xcb_no_exposure_event_t 	# /usr/include/xcb/xproto.h:673
enum_xcb_visibility_t = c_int
XCB_VISIBILITY_UNOBSCURED = 0
XCB_VISIBILITY_PARTIALLY_OBSCURED = 1
XCB_VISIBILITY_FULLY_OBSCURED = 2
xcb_visibility_t = enum_xcb_visibility_t 	# /usr/include/xcb/xproto.h:679
XCB_VISIBILITY_NOTIFY = 15 	# /usr/include/xcb/xproto.h:682
class struct_xcb_visibility_notify_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'window',
        'state',
    ]
struct_xcb_visibility_notify_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('window', xcb_window_t),
    ('state', c_uint8),
]

xcb_visibility_notify_event_t = struct_xcb_visibility_notify_event_t 	# /usr/include/xcb/xproto.h:693
XCB_CREATE_NOTIFY = 16 	# /usr/include/xcb/xproto.h:696
class struct_xcb_create_notify_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'parent',
        'window',
        'x',
        'y',
        'width',
        'height',
        'border_width',
        'override_redirect',
    ]
struct_xcb_create_notify_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('parent', xcb_window_t),
    ('window', xcb_window_t),
    ('x', c_int16),
    ('y', c_int16),
    ('width', c_uint16),
    ('height', c_uint16),
    ('border_width', c_uint16),
    ('override_redirect', c_uint8),
]

xcb_create_notify_event_t = struct_xcb_create_notify_event_t 	# /usr/include/xcb/xproto.h:713
XCB_DESTROY_NOTIFY = 17 	# /usr/include/xcb/xproto.h:716
class struct_xcb_destroy_notify_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'event',
        'window',
    ]
struct_xcb_destroy_notify_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('event', xcb_window_t),
    ('window', xcb_window_t),
]

xcb_destroy_notify_event_t = struct_xcb_destroy_notify_event_t 	# /usr/include/xcb/xproto.h:727
XCB_UNMAP_NOTIFY = 18 	# /usr/include/xcb/xproto.h:730
class struct_xcb_unmap_notify_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'event',
        'window',
        'from_configure',
    ]
struct_xcb_unmap_notify_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('event', xcb_window_t),
    ('window', xcb_window_t),
    ('from_configure', c_uint8),
]

xcb_unmap_notify_event_t = struct_xcb_unmap_notify_event_t 	# /usr/include/xcb/xproto.h:742
XCB_MAP_NOTIFY = 19 	# /usr/include/xcb/xproto.h:745
class struct_xcb_map_notify_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'event',
        'window',
        'override_redirect',
    ]
struct_xcb_map_notify_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('event', xcb_window_t),
    ('window', xcb_window_t),
    ('override_redirect', c_uint8),
]

xcb_map_notify_event_t = struct_xcb_map_notify_event_t 	# /usr/include/xcb/xproto.h:757
XCB_MAP_REQUEST = 20 	# /usr/include/xcb/xproto.h:760
class struct_xcb_map_request_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'parent',
        'window',
    ]
struct_xcb_map_request_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('parent', xcb_window_t),
    ('window', xcb_window_t),
]

xcb_map_request_event_t = struct_xcb_map_request_event_t 	# /usr/include/xcb/xproto.h:771
XCB_REPARENT_NOTIFY = 21 	# /usr/include/xcb/xproto.h:774
class struct_xcb_reparent_notify_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'event',
        'window',
        'parent',
        'x',
        'y',
        'override_redirect',
    ]
struct_xcb_reparent_notify_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('event', xcb_window_t),
    ('window', xcb_window_t),
    ('parent', xcb_window_t),
    ('x', c_int16),
    ('y', c_int16),
    ('override_redirect', c_uint8),
]

xcb_reparent_notify_event_t = struct_xcb_reparent_notify_event_t 	# /usr/include/xcb/xproto.h:789
XCB_CONFIGURE_NOTIFY = 22 	# /usr/include/xcb/xproto.h:792
class struct_xcb_configure_notify_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'event',
        'window',
        'above_sibling',
        'x',
        'y',
        'width',
        'height',
        'border_width',
        'override_redirect',
    ]
struct_xcb_configure_notify_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('event', xcb_window_t),
    ('window', xcb_window_t),
    ('above_sibling', xcb_window_t),
    ('x', c_int16),
    ('y', c_int16),
    ('width', c_uint16),
    ('height', c_uint16),
    ('border_width', c_uint16),
    ('override_redirect', c_uint8),
]

xcb_configure_notify_event_t = struct_xcb_configure_notify_event_t 	# /usr/include/xcb/xproto.h:810
XCB_CONFIGURE_REQUEST = 23 	# /usr/include/xcb/xproto.h:813
class struct_xcb_configure_request_event_t(Structure):
    __slots__ = [
        'response_type',
        'stack_mode',
        'sequence',
        'parent',
        'window',
        'sibling',
        'x',
        'y',
        'width',
        'height',
        'border_width',
        'value_mask',
    ]
struct_xcb_configure_request_event_t._fields_ = [
    ('response_type', c_uint8),
    ('stack_mode', c_uint8),
    ('sequence', c_uint16),
    ('parent', xcb_window_t),
    ('window', xcb_window_t),
    ('sibling', xcb_window_t),
    ('x', c_int16),
    ('y', c_int16),
    ('width', c_uint16),
    ('height', c_uint16),
    ('border_width', c_uint16),
    ('value_mask', c_uint16),
]

xcb_configure_request_event_t = struct_xcb_configure_request_event_t 	# /usr/include/xcb/xproto.h:831
XCB_GRAVITY_NOTIFY = 24 	# /usr/include/xcb/xproto.h:834
class struct_xcb_gravity_notify_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'event',
        'window',
        'x',
        'y',
    ]
struct_xcb_gravity_notify_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('event', xcb_window_t),
    ('window', xcb_window_t),
    ('x', c_int16),
    ('y', c_int16),
]

xcb_gravity_notify_event_t = struct_xcb_gravity_notify_event_t 	# /usr/include/xcb/xproto.h:847
XCB_RESIZE_REQUEST = 25 	# /usr/include/xcb/xproto.h:850
class struct_xcb_resize_request_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'window',
        'width',
        'height',
    ]
struct_xcb_resize_request_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('window', xcb_window_t),
    ('width', c_uint16),
    ('height', c_uint16),
]

xcb_resize_request_event_t = struct_xcb_resize_request_event_t 	# /usr/include/xcb/xproto.h:862
enum_xcb_place_t = c_int
XCB_PLACE_ON_TOP = 0
XCB_PLACE_ON_BOTTOM = 1
xcb_place_t = enum_xcb_place_t 	# /usr/include/xcb/xproto.h:867
XCB_CIRCULATE_NOTIFY = 26 	# /usr/include/xcb/xproto.h:870
class struct_xcb_circulate_notify_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'event',
        'window',
        'pad1',
        'place',
    ]
struct_xcb_circulate_notify_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('event', xcb_window_t),
    ('window', xcb_window_t),
    ('pad1', c_uint8 * 4),
    ('place', c_uint8),
]

xcb_circulate_notify_event_t = struct_xcb_circulate_notify_event_t 	# /usr/include/xcb/xproto.h:883
XCB_CIRCULATE_REQUEST = 27 	# /usr/include/xcb/xproto.h:886
xcb_circulate_request_event_t = xcb_circulate_notify_event_t 	# /usr/include/xcb/xproto.h:888
enum_xcb_property_t = c_int
XCB_PROPERTY_NEW_VALUE = 0
XCB_PROPERTY_DELETE = 1
xcb_property_t = enum_xcb_property_t 	# /usr/include/xcb/xproto.h:893
XCB_PROPERTY_NOTIFY = 28 	# /usr/include/xcb/xproto.h:896
class struct_xcb_property_notify_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'window',
        'atom',
        'time',
        'state',
    ]
struct_xcb_property_notify_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('window', xcb_window_t),
    ('atom', xcb_atom_t),
    ('time', xcb_timestamp_t),
    ('state', c_uint8),
]

xcb_property_notify_event_t = struct_xcb_property_notify_event_t 	# /usr/include/xcb/xproto.h:909
XCB_SELECTION_CLEAR = 29 	# /usr/include/xcb/xproto.h:912
class struct_xcb_selection_clear_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'time',
        'owner',
        'selection',
    ]
struct_xcb_selection_clear_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('time', xcb_timestamp_t),
    ('owner', xcb_window_t),
    ('selection', xcb_atom_t),
]

xcb_selection_clear_event_t = struct_xcb_selection_clear_event_t 	# /usr/include/xcb/xproto.h:924
XCB_SELECTION_REQUEST = 30 	# /usr/include/xcb/xproto.h:927
class struct_xcb_selection_request_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'time',
        'owner',
        'requestor',
        'selection',
        'target',
        'property',
    ]
struct_xcb_selection_request_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('time', xcb_timestamp_t),
    ('owner', xcb_window_t),
    ('requestor', xcb_window_t),
    ('selection', xcb_atom_t),
    ('target', xcb_atom_t),
    ('property', xcb_atom_t),
]

xcb_selection_request_event_t = struct_xcb_selection_request_event_t 	# /usr/include/xcb/xproto.h:942
XCB_SELECTION_NOTIFY = 31 	# /usr/include/xcb/xproto.h:945
class struct_xcb_selection_notify_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'time',
        'requestor',
        'selection',
        'target',
        'property',
    ]
struct_xcb_selection_notify_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('time', xcb_timestamp_t),
    ('requestor', xcb_window_t),
    ('selection', xcb_atom_t),
    ('target', xcb_atom_t),
    ('property', xcb_atom_t),
]

xcb_selection_notify_event_t = struct_xcb_selection_notify_event_t 	# /usr/include/xcb/xproto.h:959
enum_xcb_colormap_state_t = c_int
XCB_COLORMAP_STATE_UNINSTALLED = 0
XCB_COLORMAP_STATE_INSTALLED = 1
xcb_colormap_state_t = enum_xcb_colormap_state_t 	# /usr/include/xcb/xproto.h:964
XCB_COLORMAP_NOTIFY = 32 	# /usr/include/xcb/xproto.h:967
class struct_xcb_colormap_notify_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'window',
        'colormap',
        '_new',
        'state',
    ]
struct_xcb_colormap_notify_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('window', xcb_window_t),
    ('colormap', xcb_colormap_t),
    ('_new', c_uint8),
    ('state', c_uint8),
]

xcb_colormap_notify_event_t = struct_xcb_colormap_notify_event_t 	# /usr/include/xcb/xproto.h:980
class struct_xcb_client_message_data_t(Union):
    __slots__ = [
        'data8',
        'data16',
        'data32',
    ]
struct_xcb_client_message_data_t._fields_ = [
    ('data8', c_uint8 * 20),
    ('data16', c_uint16 * 10),
    ('data32', c_uint32 * 5),
]

xcb_client_message_data_t = struct_xcb_client_message_data_t 	# /usr/include/xcb/xproto.h:989
class struct_xcb_client_message_data_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_client_message_data_iterator_t._fields_ = [
    ('data', POINTER(xcb_client_message_data_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_client_message_data_iterator_t = struct_xcb_client_message_data_iterator_t 	# /usr/include/xcb/xproto.h:998
XCB_CLIENT_MESSAGE = 33 	# /usr/include/xcb/xproto.h:1001
class struct_xcb_client_message_event_t(Structure):
    __slots__ = [
        'response_type',
        'format',
        'sequence',
        'window',
        'type',
        'data',
    ]
struct_xcb_client_message_event_t._fields_ = [
    ('response_type', c_uint8),
    ('format', c_uint8),
    ('sequence', c_uint16),
    ('window', xcb_window_t),
    ('type', xcb_atom_t),
    ('data', xcb_client_message_data_t),
]

xcb_client_message_event_t = struct_xcb_client_message_event_t 	# /usr/include/xcb/xproto.h:1013
enum_xcb_mapping_t = c_int
XCB_MAPPING_MODIFIER = 0
XCB_MAPPING_KEYBOARD = 1
XCB_MAPPING_POINTER = 2
xcb_mapping_t = enum_xcb_mapping_t 	# /usr/include/xcb/xproto.h:1019
XCB_MAPPING_NOTIFY = 34 	# /usr/include/xcb/xproto.h:1022
class struct_xcb_mapping_notify_event_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'request',
        'first_keycode',
        'count',
    ]
struct_xcb_mapping_notify_event_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('request', c_uint8),
    ('first_keycode', xcb_keycode_t),
    ('count', c_uint8),
]

xcb_mapping_notify_event_t = struct_xcb_mapping_notify_event_t 	# /usr/include/xcb/xproto.h:1034
XCB_REQUEST = 1 	# /usr/include/xcb/xproto.h:1037
class struct_xcb_request_error_t(Structure):
    __slots__ = [
        'response_type',
        'error_code',
        'sequence',
        'bad_value',
        'minor_opcode',
        'major_opcode',
    ]
struct_xcb_request_error_t._fields_ = [
    ('response_type', c_uint8),
    ('error_code', c_uint8),
    ('sequence', c_uint16),
    ('bad_value', c_uint32),
    ('minor_opcode', c_uint16),
    ('major_opcode', c_uint8),
]

xcb_request_error_t = struct_xcb_request_error_t 	# /usr/include/xcb/xproto.h:1049
XCB_VALUE = 2 	# /usr/include/xcb/xproto.h:1052
class struct_xcb_value_error_t(Structure):
    __slots__ = [
        'response_type',
        'error_code',
        'sequence',
        'bad_value',
        'minor_opcode',
        'major_opcode',
    ]
struct_xcb_value_error_t._fields_ = [
    ('response_type', c_uint8),
    ('error_code', c_uint8),
    ('sequence', c_uint16),
    ('bad_value', c_uint32),
    ('minor_opcode', c_uint16),
    ('major_opcode', c_uint8),
]

xcb_value_error_t = struct_xcb_value_error_t 	# /usr/include/xcb/xproto.h:1064
XCB_WINDOW = 3 	# /usr/include/xcb/xproto.h:1067
xcb_window_error_t = xcb_value_error_t 	# /usr/include/xcb/xproto.h:1069
XCB_PIXMAP = 4 	# /usr/include/xcb/xproto.h:1072
xcb_pixmap_error_t = xcb_value_error_t 	# /usr/include/xcb/xproto.h:1074
XCB_ATOM = 5 	# /usr/include/xcb/xproto.h:1077
xcb_atom_error_t = xcb_value_error_t 	# /usr/include/xcb/xproto.h:1079
XCB_CURSOR = 6 	# /usr/include/xcb/xproto.h:1082
xcb_cursor_error_t = xcb_value_error_t 	# /usr/include/xcb/xproto.h:1084
XCB_FONT = 7 	# /usr/include/xcb/xproto.h:1087
xcb_font_error_t = xcb_value_error_t 	# /usr/include/xcb/xproto.h:1089
XCB_MATCH = 8 	# /usr/include/xcb/xproto.h:1092
xcb_match_error_t = xcb_request_error_t 	# /usr/include/xcb/xproto.h:1094
XCB_DRAWABLE = 9 	# /usr/include/xcb/xproto.h:1097
xcb_drawable_error_t = xcb_value_error_t 	# /usr/include/xcb/xproto.h:1099
XCB_ACCESS = 10 	# /usr/include/xcb/xproto.h:1102
xcb_access_error_t = xcb_request_error_t 	# /usr/include/xcb/xproto.h:1104
XCB_ALLOC = 11 	# /usr/include/xcb/xproto.h:1107
xcb_alloc_error_t = xcb_request_error_t 	# /usr/include/xcb/xproto.h:1109
XCB_COLORMAP = 12 	# /usr/include/xcb/xproto.h:1112
xcb_colormap_error_t = xcb_value_error_t 	# /usr/include/xcb/xproto.h:1114
XCB_G_CONTEXT = 13 	# /usr/include/xcb/xproto.h:1117
xcb_g_context_error_t = xcb_value_error_t 	# /usr/include/xcb/xproto.h:1119
XCB_ID_CHOICE = 14 	# /usr/include/xcb/xproto.h:1122
xcb_id_choice_error_t = xcb_value_error_t 	# /usr/include/xcb/xproto.h:1124
XCB_NAME = 15 	# /usr/include/xcb/xproto.h:1127
xcb_name_error_t = xcb_request_error_t 	# /usr/include/xcb/xproto.h:1129
XCB_LENGTH = 16 	# /usr/include/xcb/xproto.h:1132
xcb_length_error_t = xcb_request_error_t 	# /usr/include/xcb/xproto.h:1134
XCB_IMPLEMENTATION = 17 	# /usr/include/xcb/xproto.h:1137
xcb_implementation_error_t = xcb_request_error_t 	# /usr/include/xcb/xproto.h:1139
enum_xcb_window_class_t = c_int
XCB_WINDOW_CLASS_COPY_FROM_PARENT = 0
XCB_WINDOW_CLASS_INPUT_OUTPUT = 1
XCB_WINDOW_CLASS_INPUT_ONLY = 2
xcb_window_class_t = enum_xcb_window_class_t 	# /usr/include/xcb/xproto.h:1145
enum_xcb_cw_t = c_int
XCB_CW_BACK_PIXMAP = 0
XCB_CW_BACK_PIXEL = 1
XCB_CW_BORDER_PIXMAP = 2
XCB_CW_BORDER_PIXEL = 3
XCB_CW_BIT_GRAVITY = 4
XCB_CW_WIN_GRAVITY = 5
XCB_CW_BACKING_STORE = 6
XCB_CW_BACKING_PLANES = 7
XCB_CW_BACKING_PIXEL = 8
XCB_CW_OVERRIDE_REDIRECT = 9
XCB_CW_SAVE_UNDER = 10
XCB_CW_EVENT_MASK = 11
XCB_CW_DONT_PROPAGATE = 12
XCB_CW_COLORMAP = 13
XCB_CW_CURSOR = 14
xcb_cw_t = enum_xcb_cw_t 	# /usr/include/xcb/xproto.h:1163
enum_xcb_back_pixmap_t = c_int
XCB_BACK_PIXMAP_NONE = 0
XCB_BACK_PIXMAP_PARENT_RELATIVE = 1
xcb_back_pixmap_t = enum_xcb_back_pixmap_t 	# /usr/include/xcb/xproto.h:1168
enum_xcb_gravity_t = c_int
XCB_GRAVITY_BIT_FORGET = 0
XCB_GRAVITY_WIN_UNMAP = 0
XCB_GRAVITY_NORTH_WEST = 1
XCB_GRAVITY_NORTH = 2
XCB_GRAVITY_NORTH_EAST = 3
XCB_GRAVITY_WEST = 4
XCB_GRAVITY_CENTER = 5
XCB_GRAVITY_EAST = 6
XCB_GRAVITY_SOUTH_WEST = 7
XCB_GRAVITY_SOUTH = 8
XCB_GRAVITY_SOUTH_EAST = 9
XCB_GRAVITY_STATIC = 10
xcb_gravity_t = enum_xcb_gravity_t 	# /usr/include/xcb/xproto.h:1183
enum_xcb_backing_store_t = c_int
XCB_BACKING_STORE_NOT_USEFUL = 0
XCB_BACKING_STORE_WHEN_MAPPED = 1
XCB_BACKING_STORE_ALWAYS = 2
xcb_backing_store_t = enum_xcb_backing_store_t 	# /usr/include/xcb/xproto.h:1189
enum_xcb_event_mask_t = c_int
XCB_EVENT_MASK_NO_EVENT = 0
XCB_EVENT_MASK_KEY_PRESS = 1
XCB_EVENT_MASK_KEY_RELEASE = 2
XCB_EVENT_MASK_BUTTON_PRESS = 3
XCB_EVENT_MASK_BUTTON_RELEASE = 4
XCB_EVENT_MASK_ENTER_WINDOW = 5
XCB_EVENT_MASK_LEAVE_WINDOW = 6
XCB_EVENT_MASK_POINTER_MOTION = 7
XCB_EVENT_MASK_POINTER_MOTION_HINT = 8
XCB_EVENT_MASK_BUTTON_1_MOTION = 9
XCB_EVENT_MASK_BUTTON_2_MOTION = 10
XCB_EVENT_MASK_BUTTON_3_MOTION = 11
XCB_EVENT_MASK_BUTTON_4_MOTION = 12
XCB_EVENT_MASK_BUTTON_5_MOTION = 13
XCB_EVENT_MASK_BUTTON_MOTION = 14
XCB_EVENT_MASK_KEYMAP_STATE = 15
XCB_EVENT_MASK_EXPOSURE = 16
XCB_EVENT_MASK_VISIBILITY_CHANGE = 17
XCB_EVENT_MASK_STRUCTURE_NOTIFY = 18
XCB_EVENT_MASK_RESIZE_REDIRECT = 19
XCB_EVENT_MASK_SUBSTRUCTURE_NOTIFY = 20
XCB_EVENT_MASK_SUBSTRUCTURE_REDIRECT = 21
XCB_EVENT_MASK_FOCUS_CHANGE = 22
XCB_EVENT_MASK_PROPERTY_CHANGE = 23
XCB_EVENT_MASK_COLOR_MAP_CHANGE = 24
XCB_EVENT_MASK_OWNER_GRAB_BUTTON = 25
xcb_event_mask_t = enum_xcb_event_mask_t 	# /usr/include/xcb/xproto.h:1218
XCB_CREATE_WINDOW = 1 	# /usr/include/xcb/xproto.h:1221
class struct_xcb_create_window_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'depth',
        'length',
        'wid',
        'parent',
        'x',
        'y',
        'width',
        'height',
        'border_width',
        '_class',
        'visual',
        'value_mask',
    ]
struct_xcb_create_window_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('depth', c_uint8),
    ('length', c_uint16),
    ('wid', xcb_window_t),
    ('parent', xcb_window_t),
    ('x', c_int16),
    ('y', c_int16),
    ('width', c_uint16),
    ('height', c_uint16),
    ('border_width', c_uint16),
    ('_class', c_uint16),
    ('visual', xcb_visualid_t),
    ('value_mask', c_uint32),
]

xcb_create_window_request_t = struct_xcb_create_window_request_t 	# /usr/include/xcb/xproto.h:1240
XCB_CHANGE_WINDOW_ATTRIBUTES = 2 	# /usr/include/xcb/xproto.h:1243
class struct_xcb_change_window_attributes_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'window',
        'value_mask',
    ]
struct_xcb_change_window_attributes_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
    ('value_mask', c_uint32),
]

xcb_change_window_attributes_request_t = struct_xcb_change_window_attributes_request_t 	# /usr/include/xcb/xproto.h:1254
enum_xcb_map_state_t = c_int
XCB_MAP_STATE_UNMAPPED = 0
XCB_MAP_STATE_UNVIEWABLE = 1
XCB_MAP_STATE_VIEWABLE = 2
xcb_map_state_t = enum_xcb_map_state_t 	# /usr/include/xcb/xproto.h:1260
class struct_xcb_get_window_attributes_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_get_window_attributes_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_get_window_attributes_cookie_t = struct_xcb_get_window_attributes_cookie_t 	# /usr/include/xcb/xproto.h:1267
XCB_GET_WINDOW_ATTRIBUTES = 3 	# /usr/include/xcb/xproto.h:1270
class struct_xcb_get_window_attributes_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'window',
    ]
struct_xcb_get_window_attributes_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
]

xcb_get_window_attributes_request_t = struct_xcb_get_window_attributes_request_t 	# /usr/include/xcb/xproto.h:1280
class struct_xcb_get_window_attributes_reply_t(Structure):
    __slots__ = [
        'response_type',
        'backing_store',
        'sequence',
        'length',
        'visual',
        '_class',
        'bit_gravity',
        'win_gravity',
        'backing_planes',
        'backing_pixel',
        'save_under',
        'map_is_installed',
        'map_state',
        'override_redirect',
        'colormap',
        'all_event_masks',
        'your_event_mask',
        'do_not_propagate_mask',
    ]
struct_xcb_get_window_attributes_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('backing_store', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('visual', xcb_visualid_t),
    ('_class', c_uint16),
    ('bit_gravity', c_uint8),
    ('win_gravity', c_uint8),
    ('backing_planes', c_uint32),
    ('backing_pixel', c_uint32),
    ('save_under', c_uint8),
    ('map_is_installed', c_uint8),
    ('map_state', c_uint8),
    ('override_redirect', c_uint8),
    ('colormap', xcb_colormap_t),
    ('all_event_masks', c_uint32),
    ('your_event_mask', c_uint32),
    ('do_not_propagate_mask', c_uint16),
]

xcb_get_window_attributes_reply_t = struct_xcb_get_window_attributes_reply_t 	# /usr/include/xcb/xproto.h:1304
XCB_DESTROY_WINDOW = 4 	# /usr/include/xcb/xproto.h:1307
class struct_xcb_destroy_window_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'window',
    ]
struct_xcb_destroy_window_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
]

xcb_destroy_window_request_t = struct_xcb_destroy_window_request_t 	# /usr/include/xcb/xproto.h:1317
XCB_DESTROY_SUBWINDOWS = 5 	# /usr/include/xcb/xproto.h:1320
class struct_xcb_destroy_subwindows_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'window',
    ]
struct_xcb_destroy_subwindows_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
]

xcb_destroy_subwindows_request_t = struct_xcb_destroy_subwindows_request_t 	# /usr/include/xcb/xproto.h:1330
enum_xcb_set_mode_t = c_int
XCB_SET_MODE_INSERT = 0
XCB_SET_MODE_DELETE = 1
xcb_set_mode_t = enum_xcb_set_mode_t 	# /usr/include/xcb/xproto.h:1335
XCB_CHANGE_SAVE_SET = 6 	# /usr/include/xcb/xproto.h:1338
class struct_xcb_change_save_set_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'mode',
        'length',
        'window',
    ]
struct_xcb_change_save_set_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('mode', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
]

xcb_change_save_set_request_t = struct_xcb_change_save_set_request_t 	# /usr/include/xcb/xproto.h:1348
XCB_REPARENT_WINDOW = 7 	# /usr/include/xcb/xproto.h:1351
class struct_xcb_reparent_window_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'window',
        'parent',
        'x',
        'y',
    ]
struct_xcb_reparent_window_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
    ('parent', xcb_window_t),
    ('x', c_int16),
    ('y', c_int16),
]

xcb_reparent_window_request_t = struct_xcb_reparent_window_request_t 	# /usr/include/xcb/xproto.h:1364
XCB_MAP_WINDOW = 8 	# /usr/include/xcb/xproto.h:1367
class struct_xcb_map_window_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'window',
    ]
struct_xcb_map_window_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
]

xcb_map_window_request_t = struct_xcb_map_window_request_t 	# /usr/include/xcb/xproto.h:1377
XCB_MAP_SUBWINDOWS = 9 	# /usr/include/xcb/xproto.h:1380
class struct_xcb_map_subwindows_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'window',
    ]
struct_xcb_map_subwindows_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
]

xcb_map_subwindows_request_t = struct_xcb_map_subwindows_request_t 	# /usr/include/xcb/xproto.h:1390
XCB_UNMAP_WINDOW = 10 	# /usr/include/xcb/xproto.h:1393
class struct_xcb_unmap_window_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'window',
    ]
struct_xcb_unmap_window_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
]

xcb_unmap_window_request_t = struct_xcb_unmap_window_request_t 	# /usr/include/xcb/xproto.h:1403
XCB_UNMAP_SUBWINDOWS = 11 	# /usr/include/xcb/xproto.h:1406
class struct_xcb_unmap_subwindows_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'window',
    ]
struct_xcb_unmap_subwindows_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
]

xcb_unmap_subwindows_request_t = struct_xcb_unmap_subwindows_request_t 	# /usr/include/xcb/xproto.h:1416
enum_xcb_config_window_t = c_int
XCB_CONFIG_WINDOW_X = 0
XCB_CONFIG_WINDOW_Y = 1
XCB_CONFIG_WINDOW_WIDTH = 2
XCB_CONFIG_WINDOW_HEIGHT = 3
XCB_CONFIG_WINDOW_BORDER_WIDTH = 4
XCB_CONFIG_WINDOW_SIBLING = 5
XCB_CONFIG_WINDOW_STACK_MODE = 6
xcb_config_window_t = enum_xcb_config_window_t 	# /usr/include/xcb/xproto.h:1426
enum_xcb_stack_mode_t = c_int
XCB_STACK_MODE_ABOVE = 0
XCB_STACK_MODE_BELOW = 1
XCB_STACK_MODE_TOP_IF = 2
XCB_STACK_MODE_BOTTOM_IF = 3
XCB_STACK_MODE_OPPOSITE = 4
xcb_stack_mode_t = enum_xcb_stack_mode_t 	# /usr/include/xcb/xproto.h:1434
XCB_CONFIGURE_WINDOW = 12 	# /usr/include/xcb/xproto.h:1437
class struct_xcb_configure_window_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'window',
        'value_mask',
    ]
struct_xcb_configure_window_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
    ('value_mask', c_uint16),
]

xcb_configure_window_request_t = struct_xcb_configure_window_request_t 	# /usr/include/xcb/xproto.h:1448
enum_xcb_circulate_t = c_int
XCB_CIRCULATE_RAISE_LOWEST = 0
XCB_CIRCULATE_LOWER_HIGHEST = 1
xcb_circulate_t = enum_xcb_circulate_t 	# /usr/include/xcb/xproto.h:1453
XCB_CIRCULATE_WINDOW = 13 	# /usr/include/xcb/xproto.h:1456
class struct_xcb_circulate_window_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'direction',
        'length',
        'window',
    ]
struct_xcb_circulate_window_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('direction', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
]

xcb_circulate_window_request_t = struct_xcb_circulate_window_request_t 	# /usr/include/xcb/xproto.h:1466
class struct_xcb_get_geometry_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_get_geometry_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_get_geometry_cookie_t = struct_xcb_get_geometry_cookie_t 	# /usr/include/xcb/xproto.h:1473
XCB_GET_GEOMETRY = 14 	# /usr/include/xcb/xproto.h:1476
class struct_xcb_get_geometry_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'drawable',
    ]
struct_xcb_get_geometry_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('drawable', xcb_drawable_t),
]

xcb_get_geometry_request_t = struct_xcb_get_geometry_request_t 	# /usr/include/xcb/xproto.h:1486
class struct_xcb_get_geometry_reply_t(Structure):
    __slots__ = [
        'response_type',
        'depth',
        'sequence',
        'length',
        'root',
        'x',
        'y',
        'width',
        'height',
        'border_width',
    ]
struct_xcb_get_geometry_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('depth', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('root', xcb_window_t),
    ('x', c_int16),
    ('y', c_int16),
    ('width', c_uint16),
    ('height', c_uint16),
    ('border_width', c_uint16),
]

xcb_get_geometry_reply_t = struct_xcb_get_geometry_reply_t 	# /usr/include/xcb/xproto.h:1502
class struct_xcb_query_tree_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_query_tree_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_query_tree_cookie_t = struct_xcb_query_tree_cookie_t 	# /usr/include/xcb/xproto.h:1509
XCB_QUERY_TREE = 15 	# /usr/include/xcb/xproto.h:1512
class struct_xcb_query_tree_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'window',
    ]
struct_xcb_query_tree_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
]

xcb_query_tree_request_t = struct_xcb_query_tree_request_t 	# /usr/include/xcb/xproto.h:1522
class struct_xcb_query_tree_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'root',
        'parent',
        'children_len',
        'pad1',
    ]
struct_xcb_query_tree_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('root', xcb_window_t),
    ('parent', xcb_window_t),
    ('children_len', c_uint16),
    ('pad1', c_uint8 * 14),
]

xcb_query_tree_reply_t = struct_xcb_query_tree_reply_t 	# /usr/include/xcb/xproto.h:1536
class struct_xcb_intern_atom_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_intern_atom_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_intern_atom_cookie_t = struct_xcb_intern_atom_cookie_t 	# /usr/include/xcb/xproto.h:1543
XCB_INTERN_ATOM = 16 	# /usr/include/xcb/xproto.h:1546
class struct_xcb_intern_atom_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'only_if_exists',
        'length',
        'name_len',
        'pad0',
    ]
struct_xcb_intern_atom_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('only_if_exists', c_uint8),
    ('length', c_uint16),
    ('name_len', c_uint16),
    ('pad0', c_uint8 * 2),
]

xcb_intern_atom_request_t = struct_xcb_intern_atom_request_t 	# /usr/include/xcb/xproto.h:1557
class struct_xcb_intern_atom_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'atom',
    ]
struct_xcb_intern_atom_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('atom', xcb_atom_t),
]

xcb_intern_atom_reply_t = struct_xcb_intern_atom_reply_t 	# /usr/include/xcb/xproto.h:1568
class struct_xcb_get_atom_name_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_get_atom_name_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_get_atom_name_cookie_t = struct_xcb_get_atom_name_cookie_t 	# /usr/include/xcb/xproto.h:1575
XCB_GET_ATOM_NAME = 17 	# /usr/include/xcb/xproto.h:1578
class struct_xcb_get_atom_name_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'atom',
    ]
struct_xcb_get_atom_name_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('atom', xcb_atom_t),
]

xcb_get_atom_name_request_t = struct_xcb_get_atom_name_request_t 	# /usr/include/xcb/xproto.h:1588
class struct_xcb_get_atom_name_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'name_len',
        'pad1',
    ]
struct_xcb_get_atom_name_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('name_len', c_uint16),
    ('pad1', c_uint8 * 22),
]

xcb_get_atom_name_reply_t = struct_xcb_get_atom_name_reply_t 	# /usr/include/xcb/xproto.h:1600
enum_xcb_prop_mode_t = c_int
XCB_PROP_MODE_REPLACE = 0
XCB_PROP_MODE_PREPEND = 1
XCB_PROP_MODE_APPEND = 2
xcb_prop_mode_t = enum_xcb_prop_mode_t 	# /usr/include/xcb/xproto.h:1606
XCB_CHANGE_PROPERTY = 18 	# /usr/include/xcb/xproto.h:1609
class struct_xcb_change_property_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'mode',
        'length',
        'window',
        'property',
        'type',
        'format',
        'pad0',
        'data_len',
    ]
struct_xcb_change_property_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('mode', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
    ('property', xcb_atom_t),
    ('type', xcb_atom_t),
    ('format', c_uint8),
    ('pad0', c_uint8 * 3),
    ('data_len', c_uint32),
]

xcb_change_property_request_t = struct_xcb_change_property_request_t 	# /usr/include/xcb/xproto.h:1624
XCB_DELETE_PROPERTY = 19 	# /usr/include/xcb/xproto.h:1627
class struct_xcb_delete_property_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'window',
        'property',
    ]
struct_xcb_delete_property_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
    ('property', xcb_atom_t),
]

xcb_delete_property_request_t = struct_xcb_delete_property_request_t 	# /usr/include/xcb/xproto.h:1638
enum_xcb_get_property_type_t = c_int
XCB_GET_PROPERTY_TYPE_ANY = 0
xcb_get_property_type_t = enum_xcb_get_property_type_t 	# /usr/include/xcb/xproto.h:1642
class struct_xcb_get_property_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_get_property_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_get_property_cookie_t = struct_xcb_get_property_cookie_t 	# /usr/include/xcb/xproto.h:1649
XCB_GET_PROPERTY = 20 	# /usr/include/xcb/xproto.h:1652
class struct_xcb_get_property_request_t(Structure):
    __slots__ = [
        'major_opcode',
        '_delete',
        'length',
        'window',
        'property',
        'type',
        'long_offset',
        'long_length',
    ]
struct_xcb_get_property_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('_delete', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
    ('property', xcb_atom_t),
    ('type', xcb_atom_t),
    ('long_offset', c_uint32),
    ('long_length', c_uint32),
]

xcb_get_property_request_t = struct_xcb_get_property_request_t 	# /usr/include/xcb/xproto.h:1666
class struct_xcb_get_property_reply_t(Structure):
    __slots__ = [
        'response_type',
        'format',
        'sequence',
        'length',
        'type',
        'bytes_after',
        'value_len',
        'pad0',
    ]
struct_xcb_get_property_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('format', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('type', xcb_atom_t),
    ('bytes_after', c_uint32),
    ('value_len', c_uint32),
    ('pad0', c_uint8 * 12),
]

xcb_get_property_reply_t = struct_xcb_get_property_reply_t 	# /usr/include/xcb/xproto.h:1680
class struct_xcb_list_properties_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_list_properties_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_list_properties_cookie_t = struct_xcb_list_properties_cookie_t 	# /usr/include/xcb/xproto.h:1687
XCB_LIST_PROPERTIES = 21 	# /usr/include/xcb/xproto.h:1690
class struct_xcb_list_properties_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'window',
    ]
struct_xcb_list_properties_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
]

xcb_list_properties_request_t = struct_xcb_list_properties_request_t 	# /usr/include/xcb/xproto.h:1700
class struct_xcb_list_properties_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'atoms_len',
        'pad1',
    ]
struct_xcb_list_properties_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('atoms_len', c_uint16),
    ('pad1', c_uint8 * 22),
]

xcb_list_properties_reply_t = struct_xcb_list_properties_reply_t 	# /usr/include/xcb/xproto.h:1712
XCB_SET_SELECTION_OWNER = 22 	# /usr/include/xcb/xproto.h:1715
class struct_xcb_set_selection_owner_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'owner',
        'selection',
        'time',
    ]
struct_xcb_set_selection_owner_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('owner', xcb_window_t),
    ('selection', xcb_atom_t),
    ('time', xcb_timestamp_t),
]

xcb_set_selection_owner_request_t = struct_xcb_set_selection_owner_request_t 	# /usr/include/xcb/xproto.h:1727
class struct_xcb_get_selection_owner_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_get_selection_owner_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_get_selection_owner_cookie_t = struct_xcb_get_selection_owner_cookie_t 	# /usr/include/xcb/xproto.h:1734
XCB_GET_SELECTION_OWNER = 23 	# /usr/include/xcb/xproto.h:1737
class struct_xcb_get_selection_owner_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'selection',
    ]
struct_xcb_get_selection_owner_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('selection', xcb_atom_t),
]

xcb_get_selection_owner_request_t = struct_xcb_get_selection_owner_request_t 	# /usr/include/xcb/xproto.h:1747
class struct_xcb_get_selection_owner_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'owner',
    ]
struct_xcb_get_selection_owner_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('owner', xcb_window_t),
]

xcb_get_selection_owner_reply_t = struct_xcb_get_selection_owner_reply_t 	# /usr/include/xcb/xproto.h:1758
XCB_CONVERT_SELECTION = 24 	# /usr/include/xcb/xproto.h:1761
class struct_xcb_convert_selection_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'requestor',
        'selection',
        'target',
        'property',
        'time',
    ]
struct_xcb_convert_selection_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('requestor', xcb_window_t),
    ('selection', xcb_atom_t),
    ('target', xcb_atom_t),
    ('property', xcb_atom_t),
    ('time', xcb_timestamp_t),
]

xcb_convert_selection_request_t = struct_xcb_convert_selection_request_t 	# /usr/include/xcb/xproto.h:1775
enum_xcb_send_event_dest_t = c_int
XCB_SEND_EVENT_DEST_POINTER_WINDOW = 0
XCB_SEND_EVENT_DEST_ITEM_FOCUS = 1
xcb_send_event_dest_t = enum_xcb_send_event_dest_t 	# /usr/include/xcb/xproto.h:1780
XCB_SEND_EVENT = 25 	# /usr/include/xcb/xproto.h:1783
class struct_xcb_send_event_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'propagate',
        'length',
        'destination',
        'event_mask',
    ]
struct_xcb_send_event_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('propagate', c_uint8),
    ('length', c_uint16),
    ('destination', xcb_window_t),
    ('event_mask', c_uint32),
]

xcb_send_event_request_t = struct_xcb_send_event_request_t 	# /usr/include/xcb/xproto.h:1794
enum_xcb_grab_mode_t = c_int
XCB_GRAB_MODE_SYNC = 0
XCB_GRAB_MODE_ASYNC = 1
xcb_grab_mode_t = enum_xcb_grab_mode_t 	# /usr/include/xcb/xproto.h:1799
enum_xcb_grab_status_t = c_int
XCB_GRAB_STATUS_SUCCESS = 0
XCB_GRAB_STATUS_ALREADY_GRABBED = 1
XCB_GRAB_STATUS_INVALID_TIME = 2
XCB_GRAB_STATUS_NOT_VIEWABLE = 3
XCB_GRAB_STATUS_FROZEN = 4
xcb_grab_status_t = enum_xcb_grab_status_t 	# /usr/include/xcb/xproto.h:1807
class struct_xcb_grab_pointer_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_grab_pointer_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_grab_pointer_cookie_t = struct_xcb_grab_pointer_cookie_t 	# /usr/include/xcb/xproto.h:1814
XCB_GRAB_POINTER = 26 	# /usr/include/xcb/xproto.h:1817
class struct_xcb_grab_pointer_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'owner_events',
        'length',
        'grab_window',
        'event_mask',
        'pointer_mode',
        'keyboard_mode',
        'confine_to',
        'cursor',
        'time',
    ]
struct_xcb_grab_pointer_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('owner_events', c_uint8),
    ('length', c_uint16),
    ('grab_window', xcb_window_t),
    ('event_mask', c_uint16),
    ('pointer_mode', c_uint8),
    ('keyboard_mode', c_uint8),
    ('confine_to', xcb_window_t),
    ('cursor', xcb_cursor_t),
    ('time', xcb_timestamp_t),
]

xcb_grab_pointer_request_t = struct_xcb_grab_pointer_request_t 	# /usr/include/xcb/xproto.h:1833
class struct_xcb_grab_pointer_reply_t(Structure):
    __slots__ = [
        'response_type',
        'status',
        'sequence',
        'length',
    ]
struct_xcb_grab_pointer_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('status', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
]

xcb_grab_pointer_reply_t = struct_xcb_grab_pointer_reply_t 	# /usr/include/xcb/xproto.h:1843
XCB_UNGRAB_POINTER = 27 	# /usr/include/xcb/xproto.h:1846
class struct_xcb_ungrab_pointer_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'time',
    ]
struct_xcb_ungrab_pointer_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('time', xcb_timestamp_t),
]

xcb_ungrab_pointer_request_t = struct_xcb_ungrab_pointer_request_t 	# /usr/include/xcb/xproto.h:1856
enum_xcb_button_index_t = c_int
XCB_BUTTON_INDEX_ANY = 0
XCB_BUTTON_INDEX_1 = 1
XCB_BUTTON_INDEX_2 = 2
XCB_BUTTON_INDEX_3 = 3
XCB_BUTTON_INDEX_4 = 4
XCB_BUTTON_INDEX_5 = 5
xcb_button_index_t = enum_xcb_button_index_t 	# /usr/include/xcb/xproto.h:1865
XCB_GRAB_BUTTON = 28 	# /usr/include/xcb/xproto.h:1868
class struct_xcb_grab_button_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'owner_events',
        'length',
        'grab_window',
        'event_mask',
        'pointer_mode',
        'keyboard_mode',
        'confine_to',
        'cursor',
        'button',
        'pad0',
        'modifiers',
    ]
struct_xcb_grab_button_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('owner_events', c_uint8),
    ('length', c_uint16),
    ('grab_window', xcb_window_t),
    ('event_mask', c_uint16),
    ('pointer_mode', c_uint8),
    ('keyboard_mode', c_uint8),
    ('confine_to', xcb_window_t),
    ('cursor', xcb_cursor_t),
    ('button', c_uint8),
    ('pad0', c_uint8),
    ('modifiers', c_uint16),
]

xcb_grab_button_request_t = struct_xcb_grab_button_request_t 	# /usr/include/xcb/xproto.h:1886
XCB_UNGRAB_BUTTON = 29 	# /usr/include/xcb/xproto.h:1889
class struct_xcb_ungrab_button_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'button',
        'length',
        'grab_window',
        'modifiers',
        'pad0',
    ]
struct_xcb_ungrab_button_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('button', c_uint8),
    ('length', c_uint16),
    ('grab_window', xcb_window_t),
    ('modifiers', c_uint16),
    ('pad0', c_uint8 * 2),
]

xcb_ungrab_button_request_t = struct_xcb_ungrab_button_request_t 	# /usr/include/xcb/xproto.h:1901
XCB_CHANGE_ACTIVE_POINTER_GRAB = 30 	# /usr/include/xcb/xproto.h:1904
class struct_xcb_change_active_pointer_grab_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'cursor',
        'time',
        'event_mask',
    ]
struct_xcb_change_active_pointer_grab_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('cursor', xcb_cursor_t),
    ('time', xcb_timestamp_t),
    ('event_mask', c_uint16),
]

xcb_change_active_pointer_grab_request_t = struct_xcb_change_active_pointer_grab_request_t 	# /usr/include/xcb/xproto.h:1916
class struct_xcb_grab_keyboard_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_grab_keyboard_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_grab_keyboard_cookie_t = struct_xcb_grab_keyboard_cookie_t 	# /usr/include/xcb/xproto.h:1923
XCB_GRAB_KEYBOARD = 31 	# /usr/include/xcb/xproto.h:1926
class struct_xcb_grab_keyboard_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'owner_events',
        'length',
        'grab_window',
        'time',
        'pointer_mode',
        'keyboard_mode',
    ]
struct_xcb_grab_keyboard_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('owner_events', c_uint8),
    ('length', c_uint16),
    ('grab_window', xcb_window_t),
    ('time', xcb_timestamp_t),
    ('pointer_mode', c_uint8),
    ('keyboard_mode', c_uint8),
]

xcb_grab_keyboard_request_t = struct_xcb_grab_keyboard_request_t 	# /usr/include/xcb/xproto.h:1939
class struct_xcb_grab_keyboard_reply_t(Structure):
    __slots__ = [
        'response_type',
        'status',
        'sequence',
        'length',
    ]
struct_xcb_grab_keyboard_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('status', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
]

xcb_grab_keyboard_reply_t = struct_xcb_grab_keyboard_reply_t 	# /usr/include/xcb/xproto.h:1949
XCB_UNGRAB_KEYBOARD = 32 	# /usr/include/xcb/xproto.h:1952
class struct_xcb_ungrab_keyboard_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'time',
    ]
struct_xcb_ungrab_keyboard_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('time', xcb_timestamp_t),
]

xcb_ungrab_keyboard_request_t = struct_xcb_ungrab_keyboard_request_t 	# /usr/include/xcb/xproto.h:1962
enum_xcb_grab_t = c_int
XCB_GRAB_ANY = 0
xcb_grab_t = enum_xcb_grab_t 	# /usr/include/xcb/xproto.h:1966
XCB_GRAB_KEY = 33 	# /usr/include/xcb/xproto.h:1969
class struct_xcb_grab_key_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'owner_events',
        'length',
        'grab_window',
        'modifiers',
        'key',
        'pointer_mode',
        'keyboard_mode',
    ]
struct_xcb_grab_key_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('owner_events', c_uint8),
    ('length', c_uint16),
    ('grab_window', xcb_window_t),
    ('modifiers', c_uint16),
    ('key', xcb_keycode_t),
    ('pointer_mode', c_uint8),
    ('keyboard_mode', c_uint8),
]

xcb_grab_key_request_t = struct_xcb_grab_key_request_t 	# /usr/include/xcb/xproto.h:1983
XCB_UNGRAB_KEY = 34 	# /usr/include/xcb/xproto.h:1986
class struct_xcb_ungrab_key_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'key',
        'length',
        'grab_window',
        'modifiers',
    ]
struct_xcb_ungrab_key_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('key', xcb_keycode_t),
    ('length', c_uint16),
    ('grab_window', xcb_window_t),
    ('modifiers', c_uint16),
]

xcb_ungrab_key_request_t = struct_xcb_ungrab_key_request_t 	# /usr/include/xcb/xproto.h:1997
enum_xcb_allow_t = c_int
XCB_ALLOW_ASYNC_POINTER = 0
XCB_ALLOW_SYNC_POINTER = 1
XCB_ALLOW_REPLAY_POINTER = 2
XCB_ALLOW_ASYNC_KEYBOARD = 3
XCB_ALLOW_SYNC_KEYBOARD = 4
XCB_ALLOW_REPLAY_KEYBOARD = 5
XCB_ALLOW_ASYNC_BOTH = 6
XCB_ALLOW_SYNC_BOTH = 7
xcb_allow_t = enum_xcb_allow_t 	# /usr/include/xcb/xproto.h:2008
XCB_ALLOW_EVENTS = 35 	# /usr/include/xcb/xproto.h:2011
class struct_xcb_allow_events_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'mode',
        'length',
        'time',
    ]
struct_xcb_allow_events_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('mode', c_uint8),
    ('length', c_uint16),
    ('time', xcb_timestamp_t),
]

xcb_allow_events_request_t = struct_xcb_allow_events_request_t 	# /usr/include/xcb/xproto.h:2021
XCB_GRAB_SERVER = 36 	# /usr/include/xcb/xproto.h:2024
class struct_xcb_grab_server_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
    ]
struct_xcb_grab_server_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
]

xcb_grab_server_request_t = struct_xcb_grab_server_request_t 	# /usr/include/xcb/xproto.h:2033
XCB_UNGRAB_SERVER = 37 	# /usr/include/xcb/xproto.h:2036
class struct_xcb_ungrab_server_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
    ]
struct_xcb_ungrab_server_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
]

xcb_ungrab_server_request_t = struct_xcb_ungrab_server_request_t 	# /usr/include/xcb/xproto.h:2045
class struct_xcb_query_pointer_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_query_pointer_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_query_pointer_cookie_t = struct_xcb_query_pointer_cookie_t 	# /usr/include/xcb/xproto.h:2052
XCB_QUERY_POINTER = 38 	# /usr/include/xcb/xproto.h:2055
class struct_xcb_query_pointer_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'window',
    ]
struct_xcb_query_pointer_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
]

xcb_query_pointer_request_t = struct_xcb_query_pointer_request_t 	# /usr/include/xcb/xproto.h:2065
class struct_xcb_query_pointer_reply_t(Structure):
    __slots__ = [
        'response_type',
        'same_screen',
        'sequence',
        'length',
        'root',
        'child',
        'root_x',
        'root_y',
        'win_x',
        'win_y',
        'mask',
    ]
struct_xcb_query_pointer_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('same_screen', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('root', xcb_window_t),
    ('child', xcb_window_t),
    ('root_x', c_int16),
    ('root_y', c_int16),
    ('win_x', c_int16),
    ('win_y', c_int16),
    ('mask', c_uint16),
]

xcb_query_pointer_reply_t = struct_xcb_query_pointer_reply_t 	# /usr/include/xcb/xproto.h:2082
class struct_xcb_timecoord_t(Structure):
    __slots__ = [
        'time',
        'x',
        'y',
    ]
struct_xcb_timecoord_t._fields_ = [
    ('time', xcb_timestamp_t),
    ('x', c_int16),
    ('y', c_int16),
]

xcb_timecoord_t = struct_xcb_timecoord_t 	# /usr/include/xcb/xproto.h:2091
class struct_xcb_timecoord_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_timecoord_iterator_t._fields_ = [
    ('data', POINTER(xcb_timecoord_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_timecoord_iterator_t = struct_xcb_timecoord_iterator_t 	# /usr/include/xcb/xproto.h:2100
class struct_xcb_get_motion_events_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_get_motion_events_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_get_motion_events_cookie_t = struct_xcb_get_motion_events_cookie_t 	# /usr/include/xcb/xproto.h:2107
XCB_GET_MOTION_EVENTS = 39 	# /usr/include/xcb/xproto.h:2110
class struct_xcb_get_motion_events_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'window',
        'start',
        'stop',
    ]
struct_xcb_get_motion_events_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
    ('start', xcb_timestamp_t),
    ('stop', xcb_timestamp_t),
]

xcb_get_motion_events_request_t = struct_xcb_get_motion_events_request_t 	# /usr/include/xcb/xproto.h:2122
class struct_xcb_get_motion_events_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'events_len',
        'pad1',
    ]
struct_xcb_get_motion_events_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('events_len', c_uint32),
    ('pad1', c_uint8 * 20),
]

xcb_get_motion_events_reply_t = struct_xcb_get_motion_events_reply_t 	# /usr/include/xcb/xproto.h:2134
class struct_xcb_translate_coordinates_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_translate_coordinates_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_translate_coordinates_cookie_t = struct_xcb_translate_coordinates_cookie_t 	# /usr/include/xcb/xproto.h:2141
XCB_TRANSLATE_COORDINATES = 40 	# /usr/include/xcb/xproto.h:2144
class struct_xcb_translate_coordinates_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'src_window',
        'dst_window',
        'src_x',
        'src_y',
    ]
struct_xcb_translate_coordinates_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('src_window', xcb_window_t),
    ('dst_window', xcb_window_t),
    ('src_x', c_int16),
    ('src_y', c_int16),
]

xcb_translate_coordinates_request_t = struct_xcb_translate_coordinates_request_t 	# /usr/include/xcb/xproto.h:2157
class struct_xcb_translate_coordinates_reply_t(Structure):
    __slots__ = [
        'response_type',
        'same_screen',
        'sequence',
        'length',
        'child',
        'dst_x',
        'dst_y',
    ]
struct_xcb_translate_coordinates_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('same_screen', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('child', xcb_window_t),
    ('dst_x', c_uint16),
    ('dst_y', c_uint16),
]

xcb_translate_coordinates_reply_t = struct_xcb_translate_coordinates_reply_t 	# /usr/include/xcb/xproto.h:2170
XCB_WARP_POINTER = 41 	# /usr/include/xcb/xproto.h:2173
class struct_xcb_warp_pointer_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'src_window',
        'dst_window',
        'src_x',
        'src_y',
        'src_width',
        'src_height',
        'dst_x',
        'dst_y',
    ]
struct_xcb_warp_pointer_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('src_window', xcb_window_t),
    ('dst_window', xcb_window_t),
    ('src_x', c_int16),
    ('src_y', c_int16),
    ('src_width', c_uint16),
    ('src_height', c_uint16),
    ('dst_x', c_int16),
    ('dst_y', c_int16),
]

xcb_warp_pointer_request_t = struct_xcb_warp_pointer_request_t 	# /usr/include/xcb/xproto.h:2190
enum_xcb_input_focus_t = c_int
XCB_INPUT_FOCUS_NONE = 0
XCB_INPUT_FOCUS_POINTER_ROOT = 1
XCB_INPUT_FOCUS_PARENT = 2
xcb_input_focus_t = enum_xcb_input_focus_t 	# /usr/include/xcb/xproto.h:2196
XCB_SET_INPUT_FOCUS = 42 	# /usr/include/xcb/xproto.h:2199
class struct_xcb_set_input_focus_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'revert_to',
        'length',
        'focus',
        'time',
    ]
struct_xcb_set_input_focus_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('revert_to', c_uint8),
    ('length', c_uint16),
    ('focus', xcb_window_t),
    ('time', xcb_timestamp_t),
]

xcb_set_input_focus_request_t = struct_xcb_set_input_focus_request_t 	# /usr/include/xcb/xproto.h:2210
class struct_xcb_get_input_focus_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_get_input_focus_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_get_input_focus_cookie_t = struct_xcb_get_input_focus_cookie_t 	# /usr/include/xcb/xproto.h:2217
XCB_GET_INPUT_FOCUS = 43 	# /usr/include/xcb/xproto.h:2220
class struct_xcb_get_input_focus_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
    ]
struct_xcb_get_input_focus_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
]

xcb_get_input_focus_request_t = struct_xcb_get_input_focus_request_t 	# /usr/include/xcb/xproto.h:2229
class struct_xcb_get_input_focus_reply_t(Structure):
    __slots__ = [
        'response_type',
        'revert_to',
        'sequence',
        'length',
        'focus',
    ]
struct_xcb_get_input_focus_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('revert_to', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('focus', xcb_window_t),
]

xcb_get_input_focus_reply_t = struct_xcb_get_input_focus_reply_t 	# /usr/include/xcb/xproto.h:2240
class struct_xcb_query_keymap_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_query_keymap_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_query_keymap_cookie_t = struct_xcb_query_keymap_cookie_t 	# /usr/include/xcb/xproto.h:2247
XCB_QUERY_KEYMAP = 44 	# /usr/include/xcb/xproto.h:2250
class struct_xcb_query_keymap_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
    ]
struct_xcb_query_keymap_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
]

xcb_query_keymap_request_t = struct_xcb_query_keymap_request_t 	# /usr/include/xcb/xproto.h:2259
class struct_xcb_query_keymap_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'keys',
    ]
struct_xcb_query_keymap_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('keys', c_uint8 * 32),
]

xcb_query_keymap_reply_t = struct_xcb_query_keymap_reply_t 	# /usr/include/xcb/xproto.h:2270
XCB_OPEN_FONT = 45 	# /usr/include/xcb/xproto.h:2273
class struct_xcb_open_font_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'fid',
        'name_len',
    ]
struct_xcb_open_font_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('fid', xcb_font_t),
    ('name_len', c_uint16),
]

xcb_open_font_request_t = struct_xcb_open_font_request_t 	# /usr/include/xcb/xproto.h:2284
XCB_CLOSE_FONT = 46 	# /usr/include/xcb/xproto.h:2287
class struct_xcb_close_font_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'font',
    ]
struct_xcb_close_font_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('font', xcb_font_t),
]

xcb_close_font_request_t = struct_xcb_close_font_request_t 	# /usr/include/xcb/xproto.h:2297
enum_xcb_font_draw_t = c_int
XCB_FONT_DRAW_LEFT_TO_RIGHT = 0
XCB_FONT_DRAW_RIGHT_TO_LEFT = 1
xcb_font_draw_t = enum_xcb_font_draw_t 	# /usr/include/xcb/xproto.h:2302
class struct_xcb_fontprop_t(Structure):
    __slots__ = [
        'name',
        'value',
    ]
struct_xcb_fontprop_t._fields_ = [
    ('name', xcb_atom_t),
    ('value', c_uint32),
]

xcb_fontprop_t = struct_xcb_fontprop_t 	# /usr/include/xcb/xproto.h:2310
class struct_xcb_fontprop_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_fontprop_iterator_t._fields_ = [
    ('data', POINTER(xcb_fontprop_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_fontprop_iterator_t = struct_xcb_fontprop_iterator_t 	# /usr/include/xcb/xproto.h:2319
class struct_xcb_charinfo_t(Structure):
    __slots__ = [
        'left_side_bearing',
        'right_side_bearing',
        'character_width',
        'ascent',
        'descent',
        'attributes',
    ]
struct_xcb_charinfo_t._fields_ = [
    ('left_side_bearing', c_int16),
    ('right_side_bearing', c_int16),
    ('character_width', c_int16),
    ('ascent', c_int16),
    ('descent', c_int16),
    ('attributes', c_uint16),
]

xcb_charinfo_t = struct_xcb_charinfo_t 	# /usr/include/xcb/xproto.h:2331
class struct_xcb_charinfo_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_charinfo_iterator_t._fields_ = [
    ('data', POINTER(xcb_charinfo_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_charinfo_iterator_t = struct_xcb_charinfo_iterator_t 	# /usr/include/xcb/xproto.h:2340
class struct_xcb_query_font_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_query_font_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_query_font_cookie_t = struct_xcb_query_font_cookie_t 	# /usr/include/xcb/xproto.h:2347
XCB_QUERY_FONT = 47 	# /usr/include/xcb/xproto.h:2350
class struct_xcb_query_font_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'font',
    ]
struct_xcb_query_font_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('font', xcb_fontable_t),
]

xcb_query_font_request_t = struct_xcb_query_font_request_t 	# /usr/include/xcb/xproto.h:2360
class struct_xcb_query_font_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'min_bounds',
        'pad1',
        'max_bounds',
        'pad2',
        'min_char_or_byte2',
        'max_char_or_byte2',
        'default_char',
        'properties_len',
        'draw_direction',
        'min_byte1',
        'max_byte1',
        'all_chars_exist',
        'font_ascent',
        'font_descent',
        'char_infos_len',
    ]
struct_xcb_query_font_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('min_bounds', xcb_charinfo_t),
    ('pad1', c_uint8 * 4),
    ('max_bounds', xcb_charinfo_t),
    ('pad2', c_uint8 * 4),
    ('min_char_or_byte2', c_uint16),
    ('max_char_or_byte2', c_uint16),
    ('default_char', c_uint16),
    ('properties_len', c_uint16),
    ('draw_direction', c_uint8),
    ('min_byte1', c_uint8),
    ('max_byte1', c_uint8),
    ('all_chars_exist', c_uint8),
    ('font_ascent', c_int16),
    ('font_descent', c_int16),
    ('char_infos_len', c_uint32),
]

xcb_query_font_reply_t = struct_xcb_query_font_reply_t 	# /usr/include/xcb/xproto.h:2385
class struct_xcb_query_text_extents_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_query_text_extents_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_query_text_extents_cookie_t = struct_xcb_query_text_extents_cookie_t 	# /usr/include/xcb/xproto.h:2392
XCB_QUERY_TEXT_EXTENTS = 48 	# /usr/include/xcb/xproto.h:2395
class struct_xcb_query_text_extents_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'odd_length',
        'length',
        'font',
    ]
struct_xcb_query_text_extents_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('odd_length', c_uint8),
    ('length', c_uint16),
    ('font', xcb_fontable_t),
]

xcb_query_text_extents_request_t = struct_xcb_query_text_extents_request_t 	# /usr/include/xcb/xproto.h:2405
class struct_xcb_query_text_extents_reply_t(Structure):
    __slots__ = [
        'response_type',
        'draw_direction',
        'sequence',
        'length',
        'font_ascent',
        'font_descent',
        'overall_ascent',
        'overall_descent',
        'overall_width',
        'overall_left',
        'overall_right',
    ]
struct_xcb_query_text_extents_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('draw_direction', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('font_ascent', c_int16),
    ('font_descent', c_int16),
    ('overall_ascent', c_int16),
    ('overall_descent', c_int16),
    ('overall_width', c_int32),
    ('overall_left', c_int32),
    ('overall_right', c_int32),
]

xcb_query_text_extents_reply_t = struct_xcb_query_text_extents_reply_t 	# /usr/include/xcb/xproto.h:2422
class struct_xcb_str_t(Structure):
    __slots__ = [
        'name_len',
    ]
struct_xcb_str_t._fields_ = [
    ('name_len', c_uint8),
]

xcb_str_t = struct_xcb_str_t 	# /usr/include/xcb/xproto.h:2429
class struct_xcb_str_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_str_iterator_t._fields_ = [
    ('data', POINTER(xcb_str_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_str_iterator_t = struct_xcb_str_iterator_t 	# /usr/include/xcb/xproto.h:2438
class struct_xcb_list_fonts_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_list_fonts_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_list_fonts_cookie_t = struct_xcb_list_fonts_cookie_t 	# /usr/include/xcb/xproto.h:2445
XCB_LIST_FONTS = 49 	# /usr/include/xcb/xproto.h:2448
class struct_xcb_list_fonts_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'max_names',
        'pattern_len',
    ]
struct_xcb_list_fonts_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('max_names', c_uint16),
    ('pattern_len', c_uint16),
]

xcb_list_fonts_request_t = struct_xcb_list_fonts_request_t 	# /usr/include/xcb/xproto.h:2459
class struct_xcb_list_fonts_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'names_len',
        'pad1',
    ]
struct_xcb_list_fonts_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('names_len', c_uint16),
    ('pad1', c_uint8 * 22),
]

xcb_list_fonts_reply_t = struct_xcb_list_fonts_reply_t 	# /usr/include/xcb/xproto.h:2471
class struct_xcb_list_fonts_with_info_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_list_fonts_with_info_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_list_fonts_with_info_cookie_t = struct_xcb_list_fonts_with_info_cookie_t 	# /usr/include/xcb/xproto.h:2478
XCB_LIST_FONTS_WITH_INFO = 50 	# /usr/include/xcb/xproto.h:2481
class struct_xcb_list_fonts_with_info_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'max_names',
        'pattern_len',
    ]
struct_xcb_list_fonts_with_info_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('max_names', c_uint16),
    ('pattern_len', c_uint16),
]

xcb_list_fonts_with_info_request_t = struct_xcb_list_fonts_with_info_request_t 	# /usr/include/xcb/xproto.h:2492
class struct_xcb_list_fonts_with_info_reply_t(Structure):
    __slots__ = [
        'response_type',
        'name_len',
        'sequence',
        'length',
        'min_bounds',
        'pad0',
        'max_bounds',
        'pad1',
        'min_char_or_byte2',
        'max_char_or_byte2',
        'default_char',
        'properties_len',
        'draw_direction',
        'min_byte1',
        'max_byte1',
        'all_chars_exist',
        'font_ascent',
        'font_descent',
        'replies_hint',
    ]
struct_xcb_list_fonts_with_info_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('name_len', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('min_bounds', xcb_charinfo_t),
    ('pad0', c_uint8 * 4),
    ('max_bounds', xcb_charinfo_t),
    ('pad1', c_uint8 * 4),
    ('min_char_or_byte2', c_uint16),
    ('max_char_or_byte2', c_uint16),
    ('default_char', c_uint16),
    ('properties_len', c_uint16),
    ('draw_direction', c_uint8),
    ('min_byte1', c_uint8),
    ('max_byte1', c_uint8),
    ('all_chars_exist', c_uint8),
    ('font_ascent', c_int16),
    ('font_descent', c_int16),
    ('replies_hint', c_uint32),
]

xcb_list_fonts_with_info_reply_t = struct_xcb_list_fonts_with_info_reply_t 	# /usr/include/xcb/xproto.h:2517
XCB_SET_FONT_PATH = 51 	# /usr/include/xcb/xproto.h:2520
class struct_xcb_set_font_path_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'font_qty',
    ]
struct_xcb_set_font_path_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('font_qty', c_uint16),
]

xcb_set_font_path_request_t = struct_xcb_set_font_path_request_t 	# /usr/include/xcb/xproto.h:2530
class struct_xcb_get_font_path_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_get_font_path_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_get_font_path_cookie_t = struct_xcb_get_font_path_cookie_t 	# /usr/include/xcb/xproto.h:2537
XCB_GET_FONT_PATH = 52 	# /usr/include/xcb/xproto.h:2540
class struct_xcb_get_font_path_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
    ]
struct_xcb_get_font_path_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
]

xcb_get_font_path_request_t = struct_xcb_get_font_path_request_t 	# /usr/include/xcb/xproto.h:2549
class struct_xcb_get_font_path_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'path_len',
        'pad1',
    ]
struct_xcb_get_font_path_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('path_len', c_uint16),
    ('pad1', c_uint8 * 22),
]

xcb_get_font_path_reply_t = struct_xcb_get_font_path_reply_t 	# /usr/include/xcb/xproto.h:2561
XCB_CREATE_PIXMAP = 53 	# /usr/include/xcb/xproto.h:2564
class struct_xcb_create_pixmap_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'depth',
        'length',
        'pid',
        'drawable',
        'width',
        'height',
    ]
struct_xcb_create_pixmap_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('depth', c_uint8),
    ('length', c_uint16),
    ('pid', xcb_pixmap_t),
    ('drawable', xcb_drawable_t),
    ('width', c_uint16),
    ('height', c_uint16),
]

xcb_create_pixmap_request_t = struct_xcb_create_pixmap_request_t 	# /usr/include/xcb/xproto.h:2577
XCB_FREE_PIXMAP = 54 	# /usr/include/xcb/xproto.h:2580
class struct_xcb_free_pixmap_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'pixmap',
    ]
struct_xcb_free_pixmap_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('pixmap', xcb_pixmap_t),
]

xcb_free_pixmap_request_t = struct_xcb_free_pixmap_request_t 	# /usr/include/xcb/xproto.h:2590
enum_xcb_gc_t = c_int
XCB_GC_FUNCTION = 0
XCB_GC_PLANE_MASK = 1
XCB_GC_FOREGROUND = 2
XCB_GC_BACKGROUND = 3
XCB_GC_LINE_WIDTH = 4
XCB_GC_LINE_STYLE = 5
XCB_GC_CAP_STYLE = 6
XCB_GC_JOIN_STYLE = 7
XCB_GC_FILL_STYLE = 8
XCB_GC_FILL_RULE = 9
XCB_GC_TILE = 10
XCB_GC_STIPPLE = 11
XCB_GC_TILE_STIPPLE_ORIGIN_X = 12
XCB_GC_TILE_STIPPLE_ORIGIN_Y = 13
XCB_GC_FONT = 14
XCB_GC_SUBWINDOW_MODE = 15
XCB_GC_GRAPHICS_EXPOSURES = 16
XCB_GC_CLIP_ORIGIN_X = 17
XCB_GC_CLIP_ORIGIN_Y = 18
XCB_GC_CLIP_MASK = 19
XCB_GC_DASH_OFFSET = 20
XCB_GC_DASH_LIST = 21
XCB_GC_ARC_MODE = 22
xcb_gc_t = enum_xcb_gc_t 	# /usr/include/xcb/xproto.h:2616
enum_xcb_gx_t = c_int
XCB_GX_CLEAR = 0
XCB_GX_AND = 1
XCB_GX_AND_REVERSE = 2
XCB_GX_COPY = 3
XCB_GX_AND_INVERTED = 4
XCB_GX_NOOP = 5
XCB_GX_XOR = 6
XCB_GX_OR = 7
XCB_GX_NOR = 8
XCB_GX_EQUIV = 9
XCB_GX_INVERT = 10
XCB_GX_OR_REVERSE = 11
XCB_GX_COPY_INVERTED = 12
XCB_GX_OR_INVERTED = 13
XCB_GX_NAND = 14
XCB_GX_SET = 15
xcb_gx_t = enum_xcb_gx_t 	# /usr/include/xcb/xproto.h:2635
enum_xcb_line_style_t = c_int
XCB_LINE_STYLE_SOLID = 0
XCB_LINE_STYLE_ON_OFF_DASH = 1
XCB_LINE_STYLE_DOUBLE_DASH = 2
xcb_line_style_t = enum_xcb_line_style_t 	# /usr/include/xcb/xproto.h:2641
enum_xcb_cap_style_t = c_int
XCB_CAP_STYLE_NOT_LAST = 0
XCB_CAP_STYLE_BUTT = 1
XCB_CAP_STYLE_ROUND = 2
XCB_CAP_STYLE_PROJECTING = 3
xcb_cap_style_t = enum_xcb_cap_style_t 	# /usr/include/xcb/xproto.h:2648
enum_xcb_join_style_t = c_int
XCB_JOIN_STYLE_MITRE = 0
XCB_JOIN_STYLE_ROUND = 1
XCB_JOIN_STYLE_BEVEL = 2
xcb_join_style_t = enum_xcb_join_style_t 	# /usr/include/xcb/xproto.h:2654
enum_xcb_fill_style_t = c_int
XCB_FILL_STYLE_SOLID = 0
XCB_FILL_STYLE_TILED = 1
XCB_FILL_STYLE_STIPPLED = 2
XCB_FILL_STYLE_OPAQUE_STIPPLED = 3
xcb_fill_style_t = enum_xcb_fill_style_t 	# /usr/include/xcb/xproto.h:2661
enum_xcb_fill_rule_t = c_int
XCB_FILL_RULE_EVEN_ODD = 0
XCB_FILL_RULE_WINDING = 1
xcb_fill_rule_t = enum_xcb_fill_rule_t 	# /usr/include/xcb/xproto.h:2666
enum_xcb_subwindow_mode_t = c_int
XCB_SUBWINDOW_MODE_CLIP_BY_CHILDREN = 0
XCB_SUBWINDOW_MODE_INCLUDE_INFERIORS = 1
xcb_subwindow_mode_t = enum_xcb_subwindow_mode_t 	# /usr/include/xcb/xproto.h:2671
enum_xcb_arc_mode_t = c_int
XCB_ARC_MODE_CHORD = 0
XCB_ARC_MODE_PIE_SLICE = 1
xcb_arc_mode_t = enum_xcb_arc_mode_t 	# /usr/include/xcb/xproto.h:2676
XCB_CREATE_GC = 55 	# /usr/include/xcb/xproto.h:2679
class struct_xcb_create_gc_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'cid',
        'drawable',
        'value_mask',
    ]
struct_xcb_create_gc_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('cid', xcb_gcontext_t),
    ('drawable', xcb_drawable_t),
    ('value_mask', c_uint32),
]

xcb_create_gc_request_t = struct_xcb_create_gc_request_t 	# /usr/include/xcb/xproto.h:2691
XCB_CHANGE_GC = 56 	# /usr/include/xcb/xproto.h:2694
class struct_xcb_change_gc_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'gc',
        'value_mask',
    ]
struct_xcb_change_gc_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('gc', xcb_gcontext_t),
    ('value_mask', c_uint32),
]

xcb_change_gc_request_t = struct_xcb_change_gc_request_t 	# /usr/include/xcb/xproto.h:2705
XCB_COPY_GC = 57 	# /usr/include/xcb/xproto.h:2708
class struct_xcb_copy_gc_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'src_gc',
        'dst_gc',
        'value_mask',
    ]
struct_xcb_copy_gc_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('src_gc', xcb_gcontext_t),
    ('dst_gc', xcb_gcontext_t),
    ('value_mask', c_uint32),
]

xcb_copy_gc_request_t = struct_xcb_copy_gc_request_t 	# /usr/include/xcb/xproto.h:2720
XCB_SET_DASHES = 58 	# /usr/include/xcb/xproto.h:2723
class struct_xcb_set_dashes_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'gc',
        'dash_offset',
        'dashes_len',
    ]
struct_xcb_set_dashes_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('gc', xcb_gcontext_t),
    ('dash_offset', c_uint16),
    ('dashes_len', c_uint16),
]

xcb_set_dashes_request_t = struct_xcb_set_dashes_request_t 	# /usr/include/xcb/xproto.h:2735
enum_xcb_clip_ordering_t = c_int
XCB_CLIP_ORDERING_UNSORTED = 0
XCB_CLIP_ORDERING_Y_SORTED = 1
XCB_CLIP_ORDERING_YX_SORTED = 2
XCB_CLIP_ORDERING_YX_BANDED = 3
xcb_clip_ordering_t = enum_xcb_clip_ordering_t 	# /usr/include/xcb/xproto.h:2742
XCB_SET_CLIP_RECTANGLES = 59 	# /usr/include/xcb/xproto.h:2745
class struct_xcb_set_clip_rectangles_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'ordering',
        'length',
        'gc',
        'clip_x_origin',
        'clip_y_origin',
    ]
struct_xcb_set_clip_rectangles_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('ordering', c_uint8),
    ('length', c_uint16),
    ('gc', xcb_gcontext_t),
    ('clip_x_origin', c_int16),
    ('clip_y_origin', c_int16),
]

xcb_set_clip_rectangles_request_t = struct_xcb_set_clip_rectangles_request_t 	# /usr/include/xcb/xproto.h:2757
XCB_FREE_GC = 60 	# /usr/include/xcb/xproto.h:2760
class struct_xcb_free_gc_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'gc',
    ]
struct_xcb_free_gc_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('gc', xcb_gcontext_t),
]

xcb_free_gc_request_t = struct_xcb_free_gc_request_t 	# /usr/include/xcb/xproto.h:2770
XCB_CLEAR_AREA = 61 	# /usr/include/xcb/xproto.h:2773
class struct_xcb_clear_area_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'exposures',
        'length',
        'window',
        'x',
        'y',
        'width',
        'height',
    ]
struct_xcb_clear_area_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('exposures', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
    ('x', c_int16),
    ('y', c_int16),
    ('width', c_uint16),
    ('height', c_uint16),
]

xcb_clear_area_request_t = struct_xcb_clear_area_request_t 	# /usr/include/xcb/xproto.h:2787
XCB_COPY_AREA = 62 	# /usr/include/xcb/xproto.h:2790
class struct_xcb_copy_area_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'src_drawable',
        'dst_drawable',
        'gc',
        'src_x',
        'src_y',
        'dst_x',
        'dst_y',
        'width',
        'height',
    ]
struct_xcb_copy_area_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('src_drawable', xcb_drawable_t),
    ('dst_drawable', xcb_drawable_t),
    ('gc', xcb_gcontext_t),
    ('src_x', c_int16),
    ('src_y', c_int16),
    ('dst_x', c_int16),
    ('dst_y', c_int16),
    ('width', c_uint16),
    ('height', c_uint16),
]

xcb_copy_area_request_t = struct_xcb_copy_area_request_t 	# /usr/include/xcb/xproto.h:2808
XCB_COPY_PLANE = 63 	# /usr/include/xcb/xproto.h:2811
class struct_xcb_copy_plane_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'src_drawable',
        'dst_drawable',
        'gc',
        'src_x',
        'src_y',
        'dst_x',
        'dst_y',
        'width',
        'height',
        'bit_plane',
    ]
struct_xcb_copy_plane_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('src_drawable', xcb_drawable_t),
    ('dst_drawable', xcb_drawable_t),
    ('gc', xcb_gcontext_t),
    ('src_x', c_int16),
    ('src_y', c_int16),
    ('dst_x', c_int16),
    ('dst_y', c_int16),
    ('width', c_uint16),
    ('height', c_uint16),
    ('bit_plane', c_uint32),
]

xcb_copy_plane_request_t = struct_xcb_copy_plane_request_t 	# /usr/include/xcb/xproto.h:2830
enum_xcb_coord_mode_t = c_int
XCB_COORD_MODE_ORIGIN = 0
XCB_COORD_MODE_PREVIOUS = 1
xcb_coord_mode_t = enum_xcb_coord_mode_t 	# /usr/include/xcb/xproto.h:2835
XCB_POLY_POINT = 64 	# /usr/include/xcb/xproto.h:2838
class struct_xcb_poly_point_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'coordinate_mode',
        'length',
        'drawable',
        'gc',
    ]
struct_xcb_poly_point_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('coordinate_mode', c_uint8),
    ('length', c_uint16),
    ('drawable', xcb_drawable_t),
    ('gc', xcb_gcontext_t),
]

xcb_poly_point_request_t = struct_xcb_poly_point_request_t 	# /usr/include/xcb/xproto.h:2849
XCB_POLY_LINE = 65 	# /usr/include/xcb/xproto.h:2852
class struct_xcb_poly_line_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'coordinate_mode',
        'length',
        'drawable',
        'gc',
    ]
struct_xcb_poly_line_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('coordinate_mode', c_uint8),
    ('length', c_uint16),
    ('drawable', xcb_drawable_t),
    ('gc', xcb_gcontext_t),
]

xcb_poly_line_request_t = struct_xcb_poly_line_request_t 	# /usr/include/xcb/xproto.h:2863
class struct_xcb_segment_t(Structure):
    __slots__ = [
        'x1',
        'y1',
        'x2',
        'y2',
    ]
struct_xcb_segment_t._fields_ = [
    ('x1', c_int16),
    ('y1', c_int16),
    ('x2', c_int16),
    ('y2', c_int16),
]

xcb_segment_t = struct_xcb_segment_t 	# /usr/include/xcb/xproto.h:2873
class struct_xcb_segment_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_segment_iterator_t._fields_ = [
    ('data', POINTER(xcb_segment_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_segment_iterator_t = struct_xcb_segment_iterator_t 	# /usr/include/xcb/xproto.h:2882
XCB_POLY_SEGMENT = 66 	# /usr/include/xcb/xproto.h:2885
class struct_xcb_poly_segment_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'drawable',
        'gc',
    ]
struct_xcb_poly_segment_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('drawable', xcb_drawable_t),
    ('gc', xcb_gcontext_t),
]

xcb_poly_segment_request_t = struct_xcb_poly_segment_request_t 	# /usr/include/xcb/xproto.h:2896
XCB_POLY_RECTANGLE = 67 	# /usr/include/xcb/xproto.h:2899
class struct_xcb_poly_rectangle_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'drawable',
        'gc',
    ]
struct_xcb_poly_rectangle_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('drawable', xcb_drawable_t),
    ('gc', xcb_gcontext_t),
]

xcb_poly_rectangle_request_t = struct_xcb_poly_rectangle_request_t 	# /usr/include/xcb/xproto.h:2910
XCB_POLY_ARC = 68 	# /usr/include/xcb/xproto.h:2913
class struct_xcb_poly_arc_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'drawable',
        'gc',
    ]
struct_xcb_poly_arc_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('drawable', xcb_drawable_t),
    ('gc', xcb_gcontext_t),
]

xcb_poly_arc_request_t = struct_xcb_poly_arc_request_t 	# /usr/include/xcb/xproto.h:2924
enum_xcb_poly_shape_t = c_int
XCB_POLY_SHAPE_COMPLEX = 0
XCB_POLY_SHAPE_NONCONVEX = 1
XCB_POLY_SHAPE_CONVEX = 2
xcb_poly_shape_t = enum_xcb_poly_shape_t 	# /usr/include/xcb/xproto.h:2930
XCB_FILL_POLY = 69 	# /usr/include/xcb/xproto.h:2933
class struct_xcb_fill_poly_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'drawable',
        'gc',
        'shape',
        'coordinate_mode',
    ]
struct_xcb_fill_poly_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('drawable', xcb_drawable_t),
    ('gc', xcb_gcontext_t),
    ('shape', c_uint8),
    ('coordinate_mode', c_uint8),
]

xcb_fill_poly_request_t = struct_xcb_fill_poly_request_t 	# /usr/include/xcb/xproto.h:2946
XCB_POLY_FILL_RECTANGLE = 70 	# /usr/include/xcb/xproto.h:2949
class struct_xcb_poly_fill_rectangle_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'drawable',
        'gc',
    ]
struct_xcb_poly_fill_rectangle_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('drawable', xcb_drawable_t),
    ('gc', xcb_gcontext_t),
]

xcb_poly_fill_rectangle_request_t = struct_xcb_poly_fill_rectangle_request_t 	# /usr/include/xcb/xproto.h:2960
XCB_POLY_FILL_ARC = 71 	# /usr/include/xcb/xproto.h:2963
class struct_xcb_poly_fill_arc_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'drawable',
        'gc',
    ]
struct_xcb_poly_fill_arc_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('drawable', xcb_drawable_t),
    ('gc', xcb_gcontext_t),
]

xcb_poly_fill_arc_request_t = struct_xcb_poly_fill_arc_request_t 	# /usr/include/xcb/xproto.h:2974
enum_xcb_image_format_t = c_int
XCB_IMAGE_FORMAT_XY_BITMAP = 0
XCB_IMAGE_FORMAT_XY_PIXMAP = 1
XCB_IMAGE_FORMAT_Z_PIXMAP = 2
xcb_image_format_t = enum_xcb_image_format_t 	# /usr/include/xcb/xproto.h:2980
XCB_PUT_IMAGE = 72 	# /usr/include/xcb/xproto.h:2983
class struct_xcb_put_image_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'format',
        'length',
        'drawable',
        'gc',
        'width',
        'height',
        'dst_x',
        'dst_y',
        'left_pad',
        'depth',
    ]
struct_xcb_put_image_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('format', c_uint8),
    ('length', c_uint16),
    ('drawable', xcb_drawable_t),
    ('gc', xcb_gcontext_t),
    ('width', c_uint16),
    ('height', c_uint16),
    ('dst_x', c_int16),
    ('dst_y', c_int16),
    ('left_pad', c_uint8),
    ('depth', c_uint8),
]

xcb_put_image_request_t = struct_xcb_put_image_request_t 	# /usr/include/xcb/xproto.h:3000
class struct_xcb_get_image_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_get_image_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_get_image_cookie_t = struct_xcb_get_image_cookie_t 	# /usr/include/xcb/xproto.h:3007
XCB_GET_IMAGE = 73 	# /usr/include/xcb/xproto.h:3010
class struct_xcb_get_image_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'format',
        'length',
        'drawable',
        'x',
        'y',
        'width',
        'height',
        'plane_mask',
    ]
struct_xcb_get_image_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('format', c_uint8),
    ('length', c_uint16),
    ('drawable', xcb_drawable_t),
    ('x', c_int16),
    ('y', c_int16),
    ('width', c_uint16),
    ('height', c_uint16),
    ('plane_mask', c_uint32),
]

xcb_get_image_request_t = struct_xcb_get_image_request_t 	# /usr/include/xcb/xproto.h:3025
class struct_xcb_get_image_reply_t(Structure):
    __slots__ = [
        'response_type',
        'depth',
        'sequence',
        'length',
        'visual',
        'pad0',
    ]
struct_xcb_get_image_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('depth', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('visual', xcb_visualid_t),
    ('pad0', c_uint8 * 20),
]

xcb_get_image_reply_t = struct_xcb_get_image_reply_t 	# /usr/include/xcb/xproto.h:3037
XCB_POLY_TEXT_8 = 74 	# /usr/include/xcb/xproto.h:3040
class struct_xcb_poly_text_8_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'drawable',
        'gc',
        'x',
        'y',
    ]
struct_xcb_poly_text_8_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('drawable', xcb_drawable_t),
    ('gc', xcb_gcontext_t),
    ('x', c_int16),
    ('y', c_int16),
]

xcb_poly_text_8_request_t = struct_xcb_poly_text_8_request_t 	# /usr/include/xcb/xproto.h:3053
XCB_POLY_TEXT_16 = 75 	# /usr/include/xcb/xproto.h:3056
class struct_xcb_poly_text_16_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'drawable',
        'gc',
        'x',
        'y',
    ]
struct_xcb_poly_text_16_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('drawable', xcb_drawable_t),
    ('gc', xcb_gcontext_t),
    ('x', c_int16),
    ('y', c_int16),
]

xcb_poly_text_16_request_t = struct_xcb_poly_text_16_request_t 	# /usr/include/xcb/xproto.h:3069
XCB_IMAGE_TEXT_8 = 76 	# /usr/include/xcb/xproto.h:3072
class struct_xcb_image_text_8_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'string_len',
        'length',
        'drawable',
        'gc',
        'x',
        'y',
    ]
struct_xcb_image_text_8_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('string_len', c_uint8),
    ('length', c_uint16),
    ('drawable', xcb_drawable_t),
    ('gc', xcb_gcontext_t),
    ('x', c_int16),
    ('y', c_int16),
]

xcb_image_text_8_request_t = struct_xcb_image_text_8_request_t 	# /usr/include/xcb/xproto.h:3085
XCB_IMAGE_TEXT_16 = 77 	# /usr/include/xcb/xproto.h:3088
class struct_xcb_image_text_16_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'string_len',
        'length',
        'drawable',
        'gc',
        'x',
        'y',
    ]
struct_xcb_image_text_16_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('string_len', c_uint8),
    ('length', c_uint16),
    ('drawable', xcb_drawable_t),
    ('gc', xcb_gcontext_t),
    ('x', c_int16),
    ('y', c_int16),
]

xcb_image_text_16_request_t = struct_xcb_image_text_16_request_t 	# /usr/include/xcb/xproto.h:3101
enum_xcb_colormap_alloc_t = c_int
XCB_COLORMAP_ALLOC_NONE = 0
XCB_COLORMAP_ALLOC_ALL = 1
xcb_colormap_alloc_t = enum_xcb_colormap_alloc_t 	# /usr/include/xcb/xproto.h:3106
XCB_CREATE_COLORMAP = 78 	# /usr/include/xcb/xproto.h:3109
class struct_xcb_create_colormap_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'alloc',
        'length',
        'mid',
        'window',
        'visual',
    ]
struct_xcb_create_colormap_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('alloc', c_uint8),
    ('length', c_uint16),
    ('mid', xcb_colormap_t),
    ('window', xcb_window_t),
    ('visual', xcb_visualid_t),
]

xcb_create_colormap_request_t = struct_xcb_create_colormap_request_t 	# /usr/include/xcb/xproto.h:3121
XCB_FREE_COLORMAP = 79 	# /usr/include/xcb/xproto.h:3124
class struct_xcb_free_colormap_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'cmap',
    ]
struct_xcb_free_colormap_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('cmap', xcb_colormap_t),
]

xcb_free_colormap_request_t = struct_xcb_free_colormap_request_t 	# /usr/include/xcb/xproto.h:3134
XCB_COPY_COLORMAP_AND_FREE = 80 	# /usr/include/xcb/xproto.h:3137
class struct_xcb_copy_colormap_and_free_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'mid',
        'src_cmap',
    ]
struct_xcb_copy_colormap_and_free_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('mid', xcb_colormap_t),
    ('src_cmap', xcb_colormap_t),
]

xcb_copy_colormap_and_free_request_t = struct_xcb_copy_colormap_and_free_request_t 	# /usr/include/xcb/xproto.h:3148
XCB_INSTALL_COLORMAP = 81 	# /usr/include/xcb/xproto.h:3151
class struct_xcb_install_colormap_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'cmap',
    ]
struct_xcb_install_colormap_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('cmap', xcb_colormap_t),
]

xcb_install_colormap_request_t = struct_xcb_install_colormap_request_t 	# /usr/include/xcb/xproto.h:3161
XCB_UNINSTALL_COLORMAP = 82 	# /usr/include/xcb/xproto.h:3164
class struct_xcb_uninstall_colormap_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'cmap',
    ]
struct_xcb_uninstall_colormap_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('cmap', xcb_colormap_t),
]

xcb_uninstall_colormap_request_t = struct_xcb_uninstall_colormap_request_t 	# /usr/include/xcb/xproto.h:3174
class struct_xcb_list_installed_colormaps_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_list_installed_colormaps_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_list_installed_colormaps_cookie_t = struct_xcb_list_installed_colormaps_cookie_t 	# /usr/include/xcb/xproto.h:3181
XCB_LIST_INSTALLED_COLORMAPS = 83 	# /usr/include/xcb/xproto.h:3184
class struct_xcb_list_installed_colormaps_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'window',
    ]
struct_xcb_list_installed_colormaps_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('window', xcb_window_t),
]

xcb_list_installed_colormaps_request_t = struct_xcb_list_installed_colormaps_request_t 	# /usr/include/xcb/xproto.h:3194
class struct_xcb_list_installed_colormaps_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'cmaps_len',
        'pad1',
    ]
struct_xcb_list_installed_colormaps_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('cmaps_len', c_uint16),
    ('pad1', c_uint8 * 22),
]

xcb_list_installed_colormaps_reply_t = struct_xcb_list_installed_colormaps_reply_t 	# /usr/include/xcb/xproto.h:3206
class struct_xcb_alloc_color_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_alloc_color_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_alloc_color_cookie_t = struct_xcb_alloc_color_cookie_t 	# /usr/include/xcb/xproto.h:3213
XCB_ALLOC_COLOR = 84 	# /usr/include/xcb/xproto.h:3216
class struct_xcb_alloc_color_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'cmap',
        'red',
        'green',
        'blue',
    ]
struct_xcb_alloc_color_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('cmap', xcb_colormap_t),
    ('red', c_uint16),
    ('green', c_uint16),
    ('blue', c_uint16),
]

xcb_alloc_color_request_t = struct_xcb_alloc_color_request_t 	# /usr/include/xcb/xproto.h:3229
class struct_xcb_alloc_color_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'red',
        'green',
        'blue',
        'pad1',
        'pixel',
    ]
struct_xcb_alloc_color_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('red', c_uint16),
    ('green', c_uint16),
    ('blue', c_uint16),
    ('pad1', c_uint8 * 2),
    ('pixel', c_uint32),
]

xcb_alloc_color_reply_t = struct_xcb_alloc_color_reply_t 	# /usr/include/xcb/xproto.h:3244
class struct_xcb_alloc_named_color_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_alloc_named_color_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_alloc_named_color_cookie_t = struct_xcb_alloc_named_color_cookie_t 	# /usr/include/xcb/xproto.h:3251
XCB_ALLOC_NAMED_COLOR = 85 	# /usr/include/xcb/xproto.h:3254
class struct_xcb_alloc_named_color_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'cmap',
        'name_len',
    ]
struct_xcb_alloc_named_color_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('cmap', xcb_colormap_t),
    ('name_len', c_uint16),
]

xcb_alloc_named_color_request_t = struct_xcb_alloc_named_color_request_t 	# /usr/include/xcb/xproto.h:3265
class struct_xcb_alloc_named_color_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'pixel',
        'exact_red',
        'exact_green',
        'exact_blue',
        'visual_red',
        'visual_green',
        'visual_blue',
    ]
struct_xcb_alloc_named_color_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('pixel', c_uint32),
    ('exact_red', c_uint16),
    ('exact_green', c_uint16),
    ('exact_blue', c_uint16),
    ('visual_red', c_uint16),
    ('visual_green', c_uint16),
    ('visual_blue', c_uint16),
]

xcb_alloc_named_color_reply_t = struct_xcb_alloc_named_color_reply_t 	# /usr/include/xcb/xproto.h:3282
class struct_xcb_alloc_color_cells_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_alloc_color_cells_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_alloc_color_cells_cookie_t = struct_xcb_alloc_color_cells_cookie_t 	# /usr/include/xcb/xproto.h:3289
XCB_ALLOC_COLOR_CELLS = 86 	# /usr/include/xcb/xproto.h:3292
class struct_xcb_alloc_color_cells_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'contiguous',
        'length',
        'cmap',
        'colors',
        'planes',
    ]
struct_xcb_alloc_color_cells_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('contiguous', c_uint8),
    ('length', c_uint16),
    ('cmap', xcb_colormap_t),
    ('colors', c_uint16),
    ('planes', c_uint16),
]

xcb_alloc_color_cells_request_t = struct_xcb_alloc_color_cells_request_t 	# /usr/include/xcb/xproto.h:3304
class struct_xcb_alloc_color_cells_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'pixels_len',
        'masks_len',
        'pad1',
    ]
struct_xcb_alloc_color_cells_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('pixels_len', c_uint16),
    ('masks_len', c_uint16),
    ('pad1', c_uint8 * 20),
]

xcb_alloc_color_cells_reply_t = struct_xcb_alloc_color_cells_reply_t 	# /usr/include/xcb/xproto.h:3317
class struct_xcb_alloc_color_planes_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_alloc_color_planes_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_alloc_color_planes_cookie_t = struct_xcb_alloc_color_planes_cookie_t 	# /usr/include/xcb/xproto.h:3324
XCB_ALLOC_COLOR_PLANES = 87 	# /usr/include/xcb/xproto.h:3327
class struct_xcb_alloc_color_planes_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'contiguous',
        'length',
        'cmap',
        'colors',
        'reds',
        'greens',
        'blues',
    ]
struct_xcb_alloc_color_planes_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('contiguous', c_uint8),
    ('length', c_uint16),
    ('cmap', xcb_colormap_t),
    ('colors', c_uint16),
    ('reds', c_uint16),
    ('greens', c_uint16),
    ('blues', c_uint16),
]

xcb_alloc_color_planes_request_t = struct_xcb_alloc_color_planes_request_t 	# /usr/include/xcb/xproto.h:3341
class struct_xcb_alloc_color_planes_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'pixels_len',
        'pad1',
        'red_mask',
        'green_mask',
        'blue_mask',
        'pad2',
    ]
struct_xcb_alloc_color_planes_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('pixels_len', c_uint16),
    ('pad1', c_uint8 * 2),
    ('red_mask', c_uint32),
    ('green_mask', c_uint32),
    ('blue_mask', c_uint32),
    ('pad2', c_uint8 * 8),
]

xcb_alloc_color_planes_reply_t = struct_xcb_alloc_color_planes_reply_t 	# /usr/include/xcb/xproto.h:3357
XCB_FREE_COLORS = 88 	# /usr/include/xcb/xproto.h:3360
class struct_xcb_free_colors_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'cmap',
        'plane_mask',
    ]
struct_xcb_free_colors_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('cmap', xcb_colormap_t),
    ('plane_mask', c_uint32),
]

xcb_free_colors_request_t = struct_xcb_free_colors_request_t 	# /usr/include/xcb/xproto.h:3371
enum_xcb_color_flag_t = c_int
XCB_COLOR_FLAG_RED = 0
XCB_COLOR_FLAG_GREEN = 1
XCB_COLOR_FLAG_BLUE = 2
xcb_color_flag_t = enum_xcb_color_flag_t 	# /usr/include/xcb/xproto.h:3377
class struct_xcb_coloritem_t(Structure):
    __slots__ = [
        'pixel',
        'red',
        'green',
        'blue',
        'flags',
        'pad0',
    ]
struct_xcb_coloritem_t._fields_ = [
    ('pixel', c_uint32),
    ('red', c_uint16),
    ('green', c_uint16),
    ('blue', c_uint16),
    ('flags', c_uint8),
    ('pad0', c_uint8),
]

xcb_coloritem_t = struct_xcb_coloritem_t 	# /usr/include/xcb/xproto.h:3389
class struct_xcb_coloritem_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_coloritem_iterator_t._fields_ = [
    ('data', POINTER(xcb_coloritem_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_coloritem_iterator_t = struct_xcb_coloritem_iterator_t 	# /usr/include/xcb/xproto.h:3398
XCB_STORE_COLORS = 89 	# /usr/include/xcb/xproto.h:3401
class struct_xcb_store_colors_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'cmap',
    ]
struct_xcb_store_colors_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('cmap', xcb_colormap_t),
]

xcb_store_colors_request_t = struct_xcb_store_colors_request_t 	# /usr/include/xcb/xproto.h:3411
XCB_STORE_NAMED_COLOR = 90 	# /usr/include/xcb/xproto.h:3414
class struct_xcb_store_named_color_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'flags',
        'length',
        'cmap',
        'pixel',
        'name_len',
    ]
struct_xcb_store_named_color_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('flags', c_uint8),
    ('length', c_uint16),
    ('cmap', xcb_colormap_t),
    ('pixel', c_uint32),
    ('name_len', c_uint16),
]

xcb_store_named_color_request_t = struct_xcb_store_named_color_request_t 	# /usr/include/xcb/xproto.h:3426
class struct_xcb_rgb_t(Structure):
    __slots__ = [
        'red',
        'green',
        'blue',
        'pad0',
    ]
struct_xcb_rgb_t._fields_ = [
    ('red', c_uint16),
    ('green', c_uint16),
    ('blue', c_uint16),
    ('pad0', c_uint8 * 2),
]

xcb_rgb_t = struct_xcb_rgb_t 	# /usr/include/xcb/xproto.h:3436
class struct_xcb_rgb_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_rgb_iterator_t._fields_ = [
    ('data', POINTER(xcb_rgb_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_rgb_iterator_t = struct_xcb_rgb_iterator_t 	# /usr/include/xcb/xproto.h:3445
class struct_xcb_query_colors_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_query_colors_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_query_colors_cookie_t = struct_xcb_query_colors_cookie_t 	# /usr/include/xcb/xproto.h:3452
XCB_QUERY_COLORS = 91 	# /usr/include/xcb/xproto.h:3455
class struct_xcb_query_colors_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'cmap',
    ]
struct_xcb_query_colors_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('cmap', xcb_colormap_t),
]

xcb_query_colors_request_t = struct_xcb_query_colors_request_t 	# /usr/include/xcb/xproto.h:3465
class struct_xcb_query_colors_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'colors_len',
        'pad1',
    ]
struct_xcb_query_colors_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('colors_len', c_uint16),
    ('pad1', c_uint8 * 22),
]

xcb_query_colors_reply_t = struct_xcb_query_colors_reply_t 	# /usr/include/xcb/xproto.h:3477
class struct_xcb_lookup_color_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_lookup_color_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_lookup_color_cookie_t = struct_xcb_lookup_color_cookie_t 	# /usr/include/xcb/xproto.h:3484
XCB_LOOKUP_COLOR = 92 	# /usr/include/xcb/xproto.h:3487
class struct_xcb_lookup_color_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'cmap',
        'name_len',
    ]
struct_xcb_lookup_color_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('cmap', xcb_colormap_t),
    ('name_len', c_uint16),
]

xcb_lookup_color_request_t = struct_xcb_lookup_color_request_t 	# /usr/include/xcb/xproto.h:3498
class struct_xcb_lookup_color_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'exact_red',
        'exact_green',
        'exact_blue',
        'visual_red',
        'visual_green',
        'visual_blue',
    ]
struct_xcb_lookup_color_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('exact_red', c_uint16),
    ('exact_green', c_uint16),
    ('exact_blue', c_uint16),
    ('visual_red', c_uint16),
    ('visual_green', c_uint16),
    ('visual_blue', c_uint16),
]

xcb_lookup_color_reply_t = struct_xcb_lookup_color_reply_t 	# /usr/include/xcb/xproto.h:3514
XCB_CREATE_CURSOR = 93 	# /usr/include/xcb/xproto.h:3517
class struct_xcb_create_cursor_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'cid',
        'source',
        'mask',
        'fore_red',
        'fore_green',
        'fore_blue',
        'back_red',
        'back_green',
        'back_blue',
        'x',
        'y',
    ]
struct_xcb_create_cursor_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('cid', xcb_cursor_t),
    ('source', xcb_pixmap_t),
    ('mask', xcb_pixmap_t),
    ('fore_red', c_uint16),
    ('fore_green', c_uint16),
    ('fore_blue', c_uint16),
    ('back_red', c_uint16),
    ('back_green', c_uint16),
    ('back_blue', c_uint16),
    ('x', c_uint16),
    ('y', c_uint16),
]

xcb_create_cursor_request_t = struct_xcb_create_cursor_request_t 	# /usr/include/xcb/xproto.h:3537
XCB_CREATE_GLYPH_CURSOR = 94 	# /usr/include/xcb/xproto.h:3540
class struct_xcb_create_glyph_cursor_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'cid',
        'source_font',
        'mask_font',
        'source_char',
        'mask_char',
        'fore_red',
        'fore_green',
        'fore_blue',
        'back_red',
        'back_green',
        'back_blue',
    ]
struct_xcb_create_glyph_cursor_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('cid', xcb_cursor_t),
    ('source_font', xcb_font_t),
    ('mask_font', xcb_font_t),
    ('source_char', c_uint16),
    ('mask_char', c_uint16),
    ('fore_red', c_uint16),
    ('fore_green', c_uint16),
    ('fore_blue', c_uint16),
    ('back_red', c_uint16),
    ('back_green', c_uint16),
    ('back_blue', c_uint16),
]

xcb_create_glyph_cursor_request_t = struct_xcb_create_glyph_cursor_request_t 	# /usr/include/xcb/xproto.h:3560
XCB_FREE_CURSOR = 95 	# /usr/include/xcb/xproto.h:3563
class struct_xcb_free_cursor_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'cursor',
    ]
struct_xcb_free_cursor_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('cursor', xcb_cursor_t),
]

xcb_free_cursor_request_t = struct_xcb_free_cursor_request_t 	# /usr/include/xcb/xproto.h:3573
XCB_RECOLOR_CURSOR = 96 	# /usr/include/xcb/xproto.h:3576
class struct_xcb_recolor_cursor_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'cursor',
        'fore_red',
        'fore_green',
        'fore_blue',
        'back_red',
        'back_green',
        'back_blue',
    ]
struct_xcb_recolor_cursor_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('cursor', xcb_cursor_t),
    ('fore_red', c_uint16),
    ('fore_green', c_uint16),
    ('fore_blue', c_uint16),
    ('back_red', c_uint16),
    ('back_green', c_uint16),
    ('back_blue', c_uint16),
]

xcb_recolor_cursor_request_t = struct_xcb_recolor_cursor_request_t 	# /usr/include/xcb/xproto.h:3592
enum_xcb_query_shape_of_t = c_int
XCB_QUERY_SHAPE_OF_LARGEST_CURSOR = 0
XCB_QUERY_SHAPE_OF_FASTEST_TILE = 1
XCB_QUERY_SHAPE_OF_FASTEST_STIPPLE = 2
xcb_query_shape_of_t = enum_xcb_query_shape_of_t 	# /usr/include/xcb/xproto.h:3598
class struct_xcb_query_best_size_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_query_best_size_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_query_best_size_cookie_t = struct_xcb_query_best_size_cookie_t 	# /usr/include/xcb/xproto.h:3605
XCB_QUERY_BEST_SIZE = 97 	# /usr/include/xcb/xproto.h:3608
class struct_xcb_query_best_size_request_t(Structure):
    __slots__ = [
        'major_opcode',
        '_class',
        'length',
        'drawable',
        'width',
        'height',
    ]
struct_xcb_query_best_size_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('_class', c_uint8),
    ('length', c_uint16),
    ('drawable', xcb_drawable_t),
    ('width', c_uint16),
    ('height', c_uint16),
]

xcb_query_best_size_request_t = struct_xcb_query_best_size_request_t 	# /usr/include/xcb/xproto.h:3620
class struct_xcb_query_best_size_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'width',
        'height',
    ]
struct_xcb_query_best_size_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('width', c_uint16),
    ('height', c_uint16),
]

xcb_query_best_size_reply_t = struct_xcb_query_best_size_reply_t 	# /usr/include/xcb/xproto.h:3632
class struct_xcb_query_extension_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_query_extension_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_query_extension_cookie_t = struct_xcb_query_extension_cookie_t 	# /usr/include/xcb/xproto.h:3639
XCB_QUERY_EXTENSION = 98 	# /usr/include/xcb/xproto.h:3642
class struct_xcb_query_extension_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'name_len',
    ]
struct_xcb_query_extension_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('name_len', c_uint16),
]

xcb_query_extension_request_t = struct_xcb_query_extension_request_t 	# /usr/include/xcb/xproto.h:3652
class struct_xcb_query_extension_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'present',
        'major_opcode',
        'first_event',
        'first_error',
    ]
struct_xcb_query_extension_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('present', c_uint8),
    ('major_opcode', c_uint8),
    ('first_event', c_uint8),
    ('first_error', c_uint8),
]

xcb_query_extension_reply_t = struct_xcb_query_extension_reply_t 	# /usr/include/xcb/xproto.h:3666
class struct_xcb_list_extensions_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_list_extensions_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_list_extensions_cookie_t = struct_xcb_list_extensions_cookie_t 	# /usr/include/xcb/xproto.h:3673
XCB_LIST_EXTENSIONS = 99 	# /usr/include/xcb/xproto.h:3676
class struct_xcb_list_extensions_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
    ]
struct_xcb_list_extensions_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
]

xcb_list_extensions_request_t = struct_xcb_list_extensions_request_t 	# /usr/include/xcb/xproto.h:3685
class struct_xcb_list_extensions_reply_t(Structure):
    __slots__ = [
        'response_type',
        'names_len',
        'sequence',
        'length',
        'pad0',
    ]
struct_xcb_list_extensions_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('names_len', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('pad0', c_uint8 * 24),
]

xcb_list_extensions_reply_t = struct_xcb_list_extensions_reply_t 	# /usr/include/xcb/xproto.h:3696
XCB_CHANGE_KEYBOARD_MAPPING = 100 	# /usr/include/xcb/xproto.h:3699
class struct_xcb_change_keyboard_mapping_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'keycode_count',
        'length',
        'first_keycode',
        'keysyms_per_keycode',
    ]
struct_xcb_change_keyboard_mapping_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('keycode_count', c_uint8),
    ('length', c_uint16),
    ('first_keycode', xcb_keycode_t),
    ('keysyms_per_keycode', c_uint8),
]

xcb_change_keyboard_mapping_request_t = struct_xcb_change_keyboard_mapping_request_t 	# /usr/include/xcb/xproto.h:3710
class struct_xcb_get_keyboard_mapping_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_get_keyboard_mapping_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_get_keyboard_mapping_cookie_t = struct_xcb_get_keyboard_mapping_cookie_t 	# /usr/include/xcb/xproto.h:3717
XCB_GET_KEYBOARD_MAPPING = 101 	# /usr/include/xcb/xproto.h:3720
class struct_xcb_get_keyboard_mapping_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'first_keycode',
        'count',
    ]
struct_xcb_get_keyboard_mapping_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('first_keycode', xcb_keycode_t),
    ('count', c_uint8),
]

xcb_get_keyboard_mapping_request_t = struct_xcb_get_keyboard_mapping_request_t 	# /usr/include/xcb/xproto.h:3731
class struct_xcb_get_keyboard_mapping_reply_t(Structure):
    __slots__ = [
        'response_type',
        'keysyms_per_keycode',
        'sequence',
        'length',
        'pad0',
    ]
struct_xcb_get_keyboard_mapping_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('keysyms_per_keycode', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('pad0', c_uint8 * 24),
]

xcb_get_keyboard_mapping_reply_t = struct_xcb_get_keyboard_mapping_reply_t 	# /usr/include/xcb/xproto.h:3742
enum_xcb_kb_t = c_int
XCB_KB_KEY_CLICK_PERCENT = 0
XCB_KB_BELL_PERCENT = 1
XCB_KB_BELL_PITCH = 2
XCB_KB_BELL_DURATION = 3
XCB_KB_LED = 4
XCB_KB_LED_MODE = 5
XCB_KB_KEY = 6
XCB_KB_AUTO_REPEAT_MODE = 7
xcb_kb_t = enum_xcb_kb_t 	# /usr/include/xcb/xproto.h:3753
enum_xcb_led_mode_t = c_int
XCB_LED_MODE_OFF = 0
XCB_LED_MODE_ON = 1
xcb_led_mode_t = enum_xcb_led_mode_t 	# /usr/include/xcb/xproto.h:3758
enum_xcb_auto_repeat_mode_t = c_int
XCB_AUTO_REPEAT_MODE_OFF = 0
XCB_AUTO_REPEAT_MODE_ON = 1
XCB_AUTO_REPEAT_MODE_DEFAULT = 2
xcb_auto_repeat_mode_t = enum_xcb_auto_repeat_mode_t 	# /usr/include/xcb/xproto.h:3764
XCB_CHANGE_KEYBOARD_CONTROL = 102 	# /usr/include/xcb/xproto.h:3767
class struct_xcb_change_keyboard_control_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'value_mask',
    ]
struct_xcb_change_keyboard_control_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('value_mask', c_uint32),
]

xcb_change_keyboard_control_request_t = struct_xcb_change_keyboard_control_request_t 	# /usr/include/xcb/xproto.h:3777
class struct_xcb_get_keyboard_control_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_get_keyboard_control_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_get_keyboard_control_cookie_t = struct_xcb_get_keyboard_control_cookie_t 	# /usr/include/xcb/xproto.h:3784
XCB_GET_KEYBOARD_CONTROL = 103 	# /usr/include/xcb/xproto.h:3787
class struct_xcb_get_keyboard_control_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
    ]
struct_xcb_get_keyboard_control_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
]

xcb_get_keyboard_control_request_t = struct_xcb_get_keyboard_control_request_t 	# /usr/include/xcb/xproto.h:3796
class struct_xcb_get_keyboard_control_reply_t(Structure):
    __slots__ = [
        'response_type',
        'global_auto_repeat',
        'sequence',
        'length',
        'led_mask',
        'key_click_percent',
        'bell_percent',
        'bell_pitch',
        'bell_duration',
        'pad0',
        'auto_repeats',
    ]
struct_xcb_get_keyboard_control_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('global_auto_repeat', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('led_mask', c_uint32),
    ('key_click_percent', c_uint8),
    ('bell_percent', c_uint8),
    ('bell_pitch', c_uint16),
    ('bell_duration', c_uint16),
    ('pad0', c_uint8 * 2),
    ('auto_repeats', c_uint8 * 32),
]

xcb_get_keyboard_control_reply_t = struct_xcb_get_keyboard_control_reply_t 	# /usr/include/xcb/xproto.h:3813
XCB_BELL = 104 	# /usr/include/xcb/xproto.h:3816
class struct_xcb_bell_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'percent',
        'length',
    ]
struct_xcb_bell_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('percent', c_int8),
    ('length', c_uint16),
]

xcb_bell_request_t = struct_xcb_bell_request_t 	# /usr/include/xcb/xproto.h:3825
XCB_CHANGE_POINTER_CONTROL = 105 	# /usr/include/xcb/xproto.h:3828
class struct_xcb_change_pointer_control_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'acceleration_numerator',
        'acceleration_denominator',
        'threshold',
        'do_acceleration',
        'do_threshold',
    ]
struct_xcb_change_pointer_control_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('acceleration_numerator', c_int16),
    ('acceleration_denominator', c_int16),
    ('threshold', c_int16),
    ('do_acceleration', c_uint8),
    ('do_threshold', c_uint8),
]

xcb_change_pointer_control_request_t = struct_xcb_change_pointer_control_request_t 	# /usr/include/xcb/xproto.h:3842
class struct_xcb_get_pointer_control_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_get_pointer_control_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_get_pointer_control_cookie_t = struct_xcb_get_pointer_control_cookie_t 	# /usr/include/xcb/xproto.h:3849
XCB_GET_POINTER_CONTROL = 106 	# /usr/include/xcb/xproto.h:3852
class struct_xcb_get_pointer_control_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
    ]
struct_xcb_get_pointer_control_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
]

xcb_get_pointer_control_request_t = struct_xcb_get_pointer_control_request_t 	# /usr/include/xcb/xproto.h:3861
class struct_xcb_get_pointer_control_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'acceleration_numerator',
        'acceleration_denominator',
        'threshold',
    ]
struct_xcb_get_pointer_control_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('acceleration_numerator', c_uint16),
    ('acceleration_denominator', c_uint16),
    ('threshold', c_uint16),
]

xcb_get_pointer_control_reply_t = struct_xcb_get_pointer_control_reply_t 	# /usr/include/xcb/xproto.h:3874
enum_xcb_blanking_t = c_int
XCB_BLANKING_NOT_PREFERRED = 0
XCB_BLANKING_PREFERRED = 1
XCB_BLANKING_DEFAULT = 2
xcb_blanking_t = enum_xcb_blanking_t 	# /usr/include/xcb/xproto.h:3880
enum_xcb_exposures_t = c_int
XCB_EXPOSURES_NOT_ALLOWED = 0
XCB_EXPOSURES_ALLOWED = 1
XCB_EXPOSURES_DEFAULT = 2
xcb_exposures_t = enum_xcb_exposures_t 	# /usr/include/xcb/xproto.h:3886
XCB_SET_SCREEN_SAVER = 107 	# /usr/include/xcb/xproto.h:3889
class struct_xcb_set_screen_saver_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'timeout',
        'interval',
        'prefer_blanking',
        'allow_exposures',
    ]
struct_xcb_set_screen_saver_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('timeout', c_int16),
    ('interval', c_int16),
    ('prefer_blanking', c_uint8),
    ('allow_exposures', c_uint8),
]

xcb_set_screen_saver_request_t = struct_xcb_set_screen_saver_request_t 	# /usr/include/xcb/xproto.h:3902
class struct_xcb_get_screen_saver_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_get_screen_saver_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_get_screen_saver_cookie_t = struct_xcb_get_screen_saver_cookie_t 	# /usr/include/xcb/xproto.h:3909
XCB_GET_SCREEN_SAVER = 108 	# /usr/include/xcb/xproto.h:3912
class struct_xcb_get_screen_saver_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
    ]
struct_xcb_get_screen_saver_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
]

xcb_get_screen_saver_request_t = struct_xcb_get_screen_saver_request_t 	# /usr/include/xcb/xproto.h:3921
class struct_xcb_get_screen_saver_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'timeout',
        'interval',
        'prefer_blanking',
        'allow_exposures',
    ]
struct_xcb_get_screen_saver_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('timeout', c_uint16),
    ('interval', c_uint16),
    ('prefer_blanking', c_uint8),
    ('allow_exposures', c_uint8),
]

xcb_get_screen_saver_reply_t = struct_xcb_get_screen_saver_reply_t 	# /usr/include/xcb/xproto.h:3935
enum_xcb_host_mode_t = c_int
XCB_HOST_MODE_INSERT = 0
XCB_HOST_MODE_DELETE = 1
xcb_host_mode_t = enum_xcb_host_mode_t 	# /usr/include/xcb/xproto.h:3940
enum_xcb_family_t = c_int
XCB_FAMILY_INTERNET = 0
XCB_FAMILY_DECNET = 1
XCB_FAMILY_CHAOS = 2
XCB_FAMILY_SERVER_INTERPRETED = 5
XCB_FAMILY_INTERNET_6 = 6
xcb_family_t = enum_xcb_family_t 	# /usr/include/xcb/xproto.h:3948
XCB_CHANGE_HOSTS = 109 	# /usr/include/xcb/xproto.h:3951
class struct_xcb_change_hosts_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'mode',
        'length',
        'family',
        'pad0',
        'address_len',
    ]
struct_xcb_change_hosts_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('mode', c_uint8),
    ('length', c_uint16),
    ('family', c_uint8),
    ('pad0', c_uint8),
    ('address_len', c_uint16),
]

xcb_change_hosts_request_t = struct_xcb_change_hosts_request_t 	# /usr/include/xcb/xproto.h:3963
class struct_xcb_host_t(Structure):
    __slots__ = [
        'family',
        'pad0',
        'address_len',
    ]
struct_xcb_host_t._fields_ = [
    ('family', c_uint8),
    ('pad0', c_uint8),
    ('address_len', c_uint16),
]

xcb_host_t = struct_xcb_host_t 	# /usr/include/xcb/xproto.h:3972
class struct_xcb_host_iterator_t(Structure):
    __slots__ = [
        'data',
        'rem',
        'index',
    ]
struct_xcb_host_iterator_t._fields_ = [
    ('data', POINTER(xcb_host_t)),
    ('rem', c_int),
    ('index', c_int),
]

xcb_host_iterator_t = struct_xcb_host_iterator_t 	# /usr/include/xcb/xproto.h:3981
class struct_xcb_list_hosts_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_list_hosts_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_list_hosts_cookie_t = struct_xcb_list_hosts_cookie_t 	# /usr/include/xcb/xproto.h:3988
XCB_LIST_HOSTS = 110 	# /usr/include/xcb/xproto.h:3991
class struct_xcb_list_hosts_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
    ]
struct_xcb_list_hosts_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
]

xcb_list_hosts_request_t = struct_xcb_list_hosts_request_t 	# /usr/include/xcb/xproto.h:4000
class struct_xcb_list_hosts_reply_t(Structure):
    __slots__ = [
        'response_type',
        'mode',
        'sequence',
        'length',
        'hosts_len',
        'pad0',
    ]
struct_xcb_list_hosts_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('mode', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('hosts_len', c_uint16),
    ('pad0', c_uint8 * 22),
]

xcb_list_hosts_reply_t = struct_xcb_list_hosts_reply_t 	# /usr/include/xcb/xproto.h:4012
enum_xcb_access_control_t = c_int
XCB_ACCESS_CONTROL_DISABLE = 0
XCB_ACCESS_CONTROL_ENABLE = 1
xcb_access_control_t = enum_xcb_access_control_t 	# /usr/include/xcb/xproto.h:4017
XCB_SET_ACCESS_CONTROL = 111 	# /usr/include/xcb/xproto.h:4020
class struct_xcb_set_access_control_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'mode',
        'length',
    ]
struct_xcb_set_access_control_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('mode', c_uint8),
    ('length', c_uint16),
]

xcb_set_access_control_request_t = struct_xcb_set_access_control_request_t 	# /usr/include/xcb/xproto.h:4029
enum_xcb_close_down_t = c_int
XCB_CLOSE_DOWN_DESTROY_ALL = 0
XCB_CLOSE_DOWN_RETAIN_PERMANENT = 1
XCB_CLOSE_DOWN_RETAIN_TEMPORARY = 2
xcb_close_down_t = enum_xcb_close_down_t 	# /usr/include/xcb/xproto.h:4035
XCB_SET_CLOSE_DOWN_MODE = 112 	# /usr/include/xcb/xproto.h:4038
class struct_xcb_set_close_down_mode_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'mode',
        'length',
    ]
struct_xcb_set_close_down_mode_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('mode', c_uint8),
    ('length', c_uint16),
]

xcb_set_close_down_mode_request_t = struct_xcb_set_close_down_mode_request_t 	# /usr/include/xcb/xproto.h:4047
enum_xcb_kill_t = c_int
XCB_KILL_ALL_TEMPORARY = 0
xcb_kill_t = enum_xcb_kill_t 	# /usr/include/xcb/xproto.h:4051
XCB_KILL_CLIENT = 113 	# /usr/include/xcb/xproto.h:4054
class struct_xcb_kill_client_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
        'resource',
    ]
struct_xcb_kill_client_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
    ('resource', c_uint32),
]

xcb_kill_client_request_t = struct_xcb_kill_client_request_t 	# /usr/include/xcb/xproto.h:4064
XCB_ROTATE_PROPERTIES = 114 	# /usr/include/xcb/xproto.h:4067
class struct_xcb_rotate_properties_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'window',
        'length',
        'atoms_len',
        'delta',
    ]
struct_xcb_rotate_properties_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('window', xcb_window_t),
    ('length', c_uint16),
    ('atoms_len', c_uint16),
    ('delta', c_int16),
]

xcb_rotate_properties_request_t = struct_xcb_rotate_properties_request_t 	# /usr/include/xcb/xproto.h:4078
enum_xcb_screen_saver_t = c_int
XCB_SCREEN_SAVER_RESET = 0
XCB_SCREEN_SAVER_ACTIVE = 1
xcb_screen_saver_t = enum_xcb_screen_saver_t 	# /usr/include/xcb/xproto.h:4083
XCB_FORCE_SCREEN_SAVER = 115 	# /usr/include/xcb/xproto.h:4086
class struct_xcb_force_screen_saver_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'mode',
        'length',
    ]
struct_xcb_force_screen_saver_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('mode', c_uint8),
    ('length', c_uint16),
]

xcb_force_screen_saver_request_t = struct_xcb_force_screen_saver_request_t 	# /usr/include/xcb/xproto.h:4095
enum_xcb_mapping_status_t = c_int
XCB_MAPPING_STATUS_SUCCESS = 0
XCB_MAPPING_STATUS_BUSY = 1
XCB_MAPPING_STATUS_FAILURE = 2
xcb_mapping_status_t = enum_xcb_mapping_status_t 	# /usr/include/xcb/xproto.h:4101
class struct_xcb_set_pointer_mapping_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_set_pointer_mapping_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_set_pointer_mapping_cookie_t = struct_xcb_set_pointer_mapping_cookie_t 	# /usr/include/xcb/xproto.h:4108
XCB_SET_POINTER_MAPPING = 116 	# /usr/include/xcb/xproto.h:4111
class struct_xcb_set_pointer_mapping_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'map_len',
        'length',
    ]
struct_xcb_set_pointer_mapping_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('map_len', c_uint8),
    ('length', c_uint16),
]

xcb_set_pointer_mapping_request_t = struct_xcb_set_pointer_mapping_request_t 	# /usr/include/xcb/xproto.h:4120
class struct_xcb_set_pointer_mapping_reply_t(Structure):
    __slots__ = [
        'response_type',
        'status',
        'sequence',
        'length',
    ]
struct_xcb_set_pointer_mapping_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('status', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
]

xcb_set_pointer_mapping_reply_t = struct_xcb_set_pointer_mapping_reply_t 	# /usr/include/xcb/xproto.h:4130
class struct_xcb_get_pointer_mapping_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_get_pointer_mapping_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_get_pointer_mapping_cookie_t = struct_xcb_get_pointer_mapping_cookie_t 	# /usr/include/xcb/xproto.h:4137
XCB_GET_POINTER_MAPPING = 117 	# /usr/include/xcb/xproto.h:4140
class struct_xcb_get_pointer_mapping_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
    ]
struct_xcb_get_pointer_mapping_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
]

xcb_get_pointer_mapping_request_t = struct_xcb_get_pointer_mapping_request_t 	# /usr/include/xcb/xproto.h:4149
class struct_xcb_get_pointer_mapping_reply_t(Structure):
    __slots__ = [
        'response_type',
        'map_len',
        'sequence',
        'length',
        'pad0',
    ]
struct_xcb_get_pointer_mapping_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('map_len', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('pad0', c_uint8 * 24),
]

xcb_get_pointer_mapping_reply_t = struct_xcb_get_pointer_mapping_reply_t 	# /usr/include/xcb/xproto.h:4160
enum_xcb_map_index_t = c_int
XCB_MAP_INDEX_SHIFT = 0
XCB_MAP_INDEX_LOCK = 1
XCB_MAP_INDEX_CONTROL = 2
XCB_MAP_INDEX_1 = 3
XCB_MAP_INDEX_2 = 4
XCB_MAP_INDEX_3 = 5
XCB_MAP_INDEX_4 = 6
XCB_MAP_INDEX_5 = 7
xcb_map_index_t = enum_xcb_map_index_t 	# /usr/include/xcb/xproto.h:4171
class struct_xcb_set_modifier_mapping_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_set_modifier_mapping_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_set_modifier_mapping_cookie_t = struct_xcb_set_modifier_mapping_cookie_t 	# /usr/include/xcb/xproto.h:4178
XCB_SET_MODIFIER_MAPPING = 118 	# /usr/include/xcb/xproto.h:4181
class struct_xcb_set_modifier_mapping_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'keycodes_per_modifier',
        'length',
    ]
struct_xcb_set_modifier_mapping_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('keycodes_per_modifier', c_uint8),
    ('length', c_uint16),
]

xcb_set_modifier_mapping_request_t = struct_xcb_set_modifier_mapping_request_t 	# /usr/include/xcb/xproto.h:4190
class struct_xcb_set_modifier_mapping_reply_t(Structure):
    __slots__ = [
        'response_type',
        'status',
        'sequence',
        'length',
    ]
struct_xcb_set_modifier_mapping_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('status', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
]

xcb_set_modifier_mapping_reply_t = struct_xcb_set_modifier_mapping_reply_t 	# /usr/include/xcb/xproto.h:4200
class struct_xcb_get_modifier_mapping_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_get_modifier_mapping_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_get_modifier_mapping_cookie_t = struct_xcb_get_modifier_mapping_cookie_t 	# /usr/include/xcb/xproto.h:4207
XCB_GET_MODIFIER_MAPPING = 119 	# /usr/include/xcb/xproto.h:4210
class struct_xcb_get_modifier_mapping_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
    ]
struct_xcb_get_modifier_mapping_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
]

xcb_get_modifier_mapping_request_t = struct_xcb_get_modifier_mapping_request_t 	# /usr/include/xcb/xproto.h:4219
class struct_xcb_get_modifier_mapping_reply_t(Structure):
    __slots__ = [
        'response_type',
        'keycodes_per_modifier',
        'sequence',
        'length',
        'pad0',
    ]
struct_xcb_get_modifier_mapping_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('keycodes_per_modifier', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('pad0', c_uint8 * 24),
]

xcb_get_modifier_mapping_reply_t = struct_xcb_get_modifier_mapping_reply_t 	# /usr/include/xcb/xproto.h:4230
XCB_NO_OPERATION = 127 	# /usr/include/xcb/xproto.h:4233
class struct_xcb_no_operation_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'pad0',
        'length',
    ]
struct_xcb_no_operation_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('pad0', c_uint8),
    ('length', c_uint16),
]

xcb_no_operation_request_t = struct_xcb_no_operation_request_t 	# /usr/include/xcb/xproto.h:4242
# /usr/include/xcb/xproto.h:4263
xcb_char2b_next = _lib.xcb_char2b_next
xcb_char2b_next.restype = None
xcb_char2b_next.argtypes = [POINTER(xcb_char2b_iterator_t)]

# /usr/include/xcb/xproto.h:4285
xcb_char2b_end = _lib.xcb_char2b_end
xcb_char2b_end.restype = xcb_generic_iterator_t
xcb_char2b_end.argtypes = [xcb_char2b_iterator_t]

# /usr/include/xcb/xproto.h:4306
xcb_window_next = _lib.xcb_window_next
xcb_window_next.restype = None
xcb_window_next.argtypes = [POINTER(xcb_window_iterator_t)]

# /usr/include/xcb/xproto.h:4328
xcb_window_end = _lib.xcb_window_end
xcb_window_end.restype = xcb_generic_iterator_t
xcb_window_end.argtypes = [xcb_window_iterator_t]

# /usr/include/xcb/xproto.h:4349
xcb_pixmap_next = _lib.xcb_pixmap_next
xcb_pixmap_next.restype = None
xcb_pixmap_next.argtypes = [POINTER(xcb_pixmap_iterator_t)]

# /usr/include/xcb/xproto.h:4371
xcb_pixmap_end = _lib.xcb_pixmap_end
xcb_pixmap_end.restype = xcb_generic_iterator_t
xcb_pixmap_end.argtypes = [xcb_pixmap_iterator_t]

# /usr/include/xcb/xproto.h:4392
xcb_cursor_next = _lib.xcb_cursor_next
xcb_cursor_next.restype = None
xcb_cursor_next.argtypes = [POINTER(xcb_cursor_iterator_t)]

# /usr/include/xcb/xproto.h:4414
xcb_cursor_end = _lib.xcb_cursor_end
xcb_cursor_end.restype = xcb_generic_iterator_t
xcb_cursor_end.argtypes = [xcb_cursor_iterator_t]

# /usr/include/xcb/xproto.h:4435
xcb_font_next = _lib.xcb_font_next
xcb_font_next.restype = None
xcb_font_next.argtypes = [POINTER(xcb_font_iterator_t)]

# /usr/include/xcb/xproto.h:4457
xcb_font_end = _lib.xcb_font_end
xcb_font_end.restype = xcb_generic_iterator_t
xcb_font_end.argtypes = [xcb_font_iterator_t]

# /usr/include/xcb/xproto.h:4478
xcb_gcontext_next = _lib.xcb_gcontext_next
xcb_gcontext_next.restype = None
xcb_gcontext_next.argtypes = [POINTER(xcb_gcontext_iterator_t)]

# /usr/include/xcb/xproto.h:4500
xcb_gcontext_end = _lib.xcb_gcontext_end
xcb_gcontext_end.restype = xcb_generic_iterator_t
xcb_gcontext_end.argtypes = [xcb_gcontext_iterator_t]

# /usr/include/xcb/xproto.h:4521
xcb_colormap_next = _lib.xcb_colormap_next
xcb_colormap_next.restype = None
xcb_colormap_next.argtypes = [POINTER(xcb_colormap_iterator_t)]

# /usr/include/xcb/xproto.h:4543
xcb_colormap_end = _lib.xcb_colormap_end
xcb_colormap_end.restype = xcb_generic_iterator_t
xcb_colormap_end.argtypes = [xcb_colormap_iterator_t]

# /usr/include/xcb/xproto.h:4564
xcb_atom_next = _lib.xcb_atom_next
xcb_atom_next.restype = None
xcb_atom_next.argtypes = [POINTER(xcb_atom_iterator_t)]

# /usr/include/xcb/xproto.h:4586
xcb_atom_end = _lib.xcb_atom_end
xcb_atom_end.restype = xcb_generic_iterator_t
xcb_atom_end.argtypes = [xcb_atom_iterator_t]

# /usr/include/xcb/xproto.h:4607
xcb_drawable_next = _lib.xcb_drawable_next
xcb_drawable_next.restype = None
xcb_drawable_next.argtypes = [POINTER(xcb_drawable_iterator_t)]

# /usr/include/xcb/xproto.h:4629
xcb_drawable_end = _lib.xcb_drawable_end
xcb_drawable_end.restype = xcb_generic_iterator_t
xcb_drawable_end.argtypes = [xcb_drawable_iterator_t]

# /usr/include/xcb/xproto.h:4650
xcb_fontable_next = _lib.xcb_fontable_next
xcb_fontable_next.restype = None
xcb_fontable_next.argtypes = [POINTER(xcb_fontable_iterator_t)]

# /usr/include/xcb/xproto.h:4672
xcb_fontable_end = _lib.xcb_fontable_end
xcb_fontable_end.restype = xcb_generic_iterator_t
xcb_fontable_end.argtypes = [xcb_fontable_iterator_t]

# /usr/include/xcb/xproto.h:4693
xcb_visualid_next = _lib.xcb_visualid_next
xcb_visualid_next.restype = None
xcb_visualid_next.argtypes = [POINTER(xcb_visualid_iterator_t)]

# /usr/include/xcb/xproto.h:4715
xcb_visualid_end = _lib.xcb_visualid_end
xcb_visualid_end.restype = xcb_generic_iterator_t
xcb_visualid_end.argtypes = [xcb_visualid_iterator_t]

# /usr/include/xcb/xproto.h:4736
xcb_timestamp_next = _lib.xcb_timestamp_next
xcb_timestamp_next.restype = None
xcb_timestamp_next.argtypes = [POINTER(xcb_timestamp_iterator_t)]

# /usr/include/xcb/xproto.h:4758
xcb_timestamp_end = _lib.xcb_timestamp_end
xcb_timestamp_end.restype = xcb_generic_iterator_t
xcb_timestamp_end.argtypes = [xcb_timestamp_iterator_t]

# /usr/include/xcb/xproto.h:4779
xcb_keysym_next = _lib.xcb_keysym_next
xcb_keysym_next.restype = None
xcb_keysym_next.argtypes = [POINTER(xcb_keysym_iterator_t)]

# /usr/include/xcb/xproto.h:4801
xcb_keysym_end = _lib.xcb_keysym_end
xcb_keysym_end.restype = xcb_generic_iterator_t
xcb_keysym_end.argtypes = [xcb_keysym_iterator_t]

# /usr/include/xcb/xproto.h:4822
xcb_keycode_next = _lib.xcb_keycode_next
xcb_keycode_next.restype = None
xcb_keycode_next.argtypes = [POINTER(xcb_keycode_iterator_t)]

# /usr/include/xcb/xproto.h:4844
xcb_keycode_end = _lib.xcb_keycode_end
xcb_keycode_end.restype = xcb_generic_iterator_t
xcb_keycode_end.argtypes = [xcb_keycode_iterator_t]

# /usr/include/xcb/xproto.h:4865
xcb_button_next = _lib.xcb_button_next
xcb_button_next.restype = None
xcb_button_next.argtypes = [POINTER(xcb_button_iterator_t)]

# /usr/include/xcb/xproto.h:4887
xcb_button_end = _lib.xcb_button_end
xcb_button_end.restype = xcb_generic_iterator_t
xcb_button_end.argtypes = [xcb_button_iterator_t]

# /usr/include/xcb/xproto.h:4908
xcb_point_next = _lib.xcb_point_next
xcb_point_next.restype = None
xcb_point_next.argtypes = [POINTER(xcb_point_iterator_t)]

# /usr/include/xcb/xproto.h:4930
xcb_point_end = _lib.xcb_point_end
xcb_point_end.restype = xcb_generic_iterator_t
xcb_point_end.argtypes = [xcb_point_iterator_t]

# /usr/include/xcb/xproto.h:4951
xcb_rectangle_next = _lib.xcb_rectangle_next
xcb_rectangle_next.restype = None
xcb_rectangle_next.argtypes = [POINTER(xcb_rectangle_iterator_t)]

# /usr/include/xcb/xproto.h:4973
xcb_rectangle_end = _lib.xcb_rectangle_end
xcb_rectangle_end.restype = xcb_generic_iterator_t
xcb_rectangle_end.argtypes = [xcb_rectangle_iterator_t]

# /usr/include/xcb/xproto.h:4994
xcb_arc_next = _lib.xcb_arc_next
xcb_arc_next.restype = None
xcb_arc_next.argtypes = [POINTER(xcb_arc_iterator_t)]

# /usr/include/xcb/xproto.h:5016
xcb_arc_end = _lib.xcb_arc_end
xcb_arc_end.restype = xcb_generic_iterator_t
xcb_arc_end.argtypes = [xcb_arc_iterator_t]

# /usr/include/xcb/xproto.h:5037
xcb_format_next = _lib.xcb_format_next
xcb_format_next.restype = None
xcb_format_next.argtypes = [POINTER(xcb_format_iterator_t)]

# /usr/include/xcb/xproto.h:5059
xcb_format_end = _lib.xcb_format_end
xcb_format_end.restype = xcb_generic_iterator_t
xcb_format_end.argtypes = [xcb_format_iterator_t]

# /usr/include/xcb/xproto.h:5080
xcb_visualtype_next = _lib.xcb_visualtype_next
xcb_visualtype_next.restype = None
xcb_visualtype_next.argtypes = [POINTER(xcb_visualtype_iterator_t)]

# /usr/include/xcb/xproto.h:5102
xcb_visualtype_end = _lib.xcb_visualtype_end
xcb_visualtype_end.restype = xcb_generic_iterator_t
xcb_visualtype_end.argtypes = [xcb_visualtype_iterator_t]

# /usr/include/xcb/xproto.h:5114
xcb_depth_visuals = _lib.xcb_depth_visuals
xcb_depth_visuals.restype = POINTER(xcb_visualtype_t)
xcb_depth_visuals.argtypes = [POINTER(xcb_depth_t)]

# /usr/include/xcb/xproto.h:5128
xcb_depth_visuals_length = _lib.xcb_depth_visuals_length
xcb_depth_visuals_length.restype = c_int
xcb_depth_visuals_length.argtypes = [POINTER(xcb_depth_t)]

# /usr/include/xcb/xproto.h:5141
xcb_depth_visuals_iterator = _lib.xcb_depth_visuals_iterator
xcb_depth_visuals_iterator.restype = xcb_visualtype_iterator_t
xcb_depth_visuals_iterator.argtypes = [POINTER(xcb_depth_t)]

# /usr/include/xcb/xproto.h:5162
xcb_depth_next = _lib.xcb_depth_next
xcb_depth_next.restype = None
xcb_depth_next.argtypes = [POINTER(xcb_depth_iterator_t)]

# /usr/include/xcb/xproto.h:5184
xcb_depth_end = _lib.xcb_depth_end
xcb_depth_end.restype = xcb_generic_iterator_t
xcb_depth_end.argtypes = [xcb_depth_iterator_t]

# /usr/include/xcb/xproto.h:5197
xcb_screen_allowed_depths_length = _lib.xcb_screen_allowed_depths_length
xcb_screen_allowed_depths_length.restype = c_int
xcb_screen_allowed_depths_length.argtypes = [POINTER(xcb_screen_t)]

# /usr/include/xcb/xproto.h:5210
xcb_screen_allowed_depths_iterator = _lib.xcb_screen_allowed_depths_iterator
xcb_screen_allowed_depths_iterator.restype = xcb_depth_iterator_t
xcb_screen_allowed_depths_iterator.argtypes = [POINTER(xcb_screen_t)]

# /usr/include/xcb/xproto.h:5231
xcb_screen_next = _lib.xcb_screen_next
xcb_screen_next.restype = None
xcb_screen_next.argtypes = [POINTER(xcb_screen_iterator_t)]

# /usr/include/xcb/xproto.h:5253
xcb_screen_end = _lib.xcb_screen_end
xcb_screen_end.restype = xcb_generic_iterator_t
xcb_screen_end.argtypes = [xcb_screen_iterator_t]

# /usr/include/xcb/xproto.h:5265
xcb_setup_request_authorization_protocol_name = _lib.xcb_setup_request_authorization_protocol_name
xcb_setup_request_authorization_protocol_name.restype = c_char_p
xcb_setup_request_authorization_protocol_name.argtypes = [POINTER(xcb_setup_request_t)]

# /usr/include/xcb/xproto.h:5279
xcb_setup_request_authorization_protocol_name_length = _lib.xcb_setup_request_authorization_protocol_name_length
xcb_setup_request_authorization_protocol_name_length.restype = c_int
xcb_setup_request_authorization_protocol_name_length.argtypes = [POINTER(xcb_setup_request_t)]

# /usr/include/xcb/xproto.h:5292
xcb_setup_request_authorization_protocol_name_end = _lib.xcb_setup_request_authorization_protocol_name_end
xcb_setup_request_authorization_protocol_name_end.restype = xcb_generic_iterator_t
xcb_setup_request_authorization_protocol_name_end.argtypes = [POINTER(xcb_setup_request_t)]

# /usr/include/xcb/xproto.h:5304
xcb_setup_request_authorization_protocol_data = _lib.xcb_setup_request_authorization_protocol_data
xcb_setup_request_authorization_protocol_data.restype = c_char_p
xcb_setup_request_authorization_protocol_data.argtypes = [POINTER(xcb_setup_request_t)]

# /usr/include/xcb/xproto.h:5318
xcb_setup_request_authorization_protocol_data_length = _lib.xcb_setup_request_authorization_protocol_data_length
xcb_setup_request_authorization_protocol_data_length.restype = c_int
xcb_setup_request_authorization_protocol_data_length.argtypes = [POINTER(xcb_setup_request_t)]

# /usr/include/xcb/xproto.h:5331
xcb_setup_request_authorization_protocol_data_end = _lib.xcb_setup_request_authorization_protocol_data_end
xcb_setup_request_authorization_protocol_data_end.restype = xcb_generic_iterator_t
xcb_setup_request_authorization_protocol_data_end.argtypes = [POINTER(xcb_setup_request_t)]

# /usr/include/xcb/xproto.h:5352
xcb_setup_request_next = _lib.xcb_setup_request_next
xcb_setup_request_next.restype = None
xcb_setup_request_next.argtypes = [POINTER(xcb_setup_request_iterator_t)]

# /usr/include/xcb/xproto.h:5374
xcb_setup_request_end = _lib.xcb_setup_request_end
xcb_setup_request_end.restype = xcb_generic_iterator_t
xcb_setup_request_end.argtypes = [xcb_setup_request_iterator_t]

# /usr/include/xcb/xproto.h:5386
xcb_setup_failed_reason = _lib.xcb_setup_failed_reason
xcb_setup_failed_reason.restype = c_char_p
xcb_setup_failed_reason.argtypes = [POINTER(xcb_setup_failed_t)]

# /usr/include/xcb/xproto.h:5400
xcb_setup_failed_reason_length = _lib.xcb_setup_failed_reason_length
xcb_setup_failed_reason_length.restype = c_int
xcb_setup_failed_reason_length.argtypes = [POINTER(xcb_setup_failed_t)]

# /usr/include/xcb/xproto.h:5413
xcb_setup_failed_reason_end = _lib.xcb_setup_failed_reason_end
xcb_setup_failed_reason_end.restype = xcb_generic_iterator_t
xcb_setup_failed_reason_end.argtypes = [POINTER(xcb_setup_failed_t)]

# /usr/include/xcb/xproto.h:5434
xcb_setup_failed_next = _lib.xcb_setup_failed_next
xcb_setup_failed_next.restype = None
xcb_setup_failed_next.argtypes = [POINTER(xcb_setup_failed_iterator_t)]

# /usr/include/xcb/xproto.h:5456
xcb_setup_failed_end = _lib.xcb_setup_failed_end
xcb_setup_failed_end.restype = xcb_generic_iterator_t
xcb_setup_failed_end.argtypes = [xcb_setup_failed_iterator_t]

# /usr/include/xcb/xproto.h:5468
xcb_setup_authenticate_reason = _lib.xcb_setup_authenticate_reason
xcb_setup_authenticate_reason.restype = c_char_p
xcb_setup_authenticate_reason.argtypes = [POINTER(xcb_setup_authenticate_t)]

# /usr/include/xcb/xproto.h:5482
xcb_setup_authenticate_reason_length = _lib.xcb_setup_authenticate_reason_length
xcb_setup_authenticate_reason_length.restype = c_int
xcb_setup_authenticate_reason_length.argtypes = [POINTER(xcb_setup_authenticate_t)]

# /usr/include/xcb/xproto.h:5495
xcb_setup_authenticate_reason_end = _lib.xcb_setup_authenticate_reason_end
xcb_setup_authenticate_reason_end.restype = xcb_generic_iterator_t
xcb_setup_authenticate_reason_end.argtypes = [POINTER(xcb_setup_authenticate_t)]

# /usr/include/xcb/xproto.h:5516
xcb_setup_authenticate_next = _lib.xcb_setup_authenticate_next
xcb_setup_authenticate_next.restype = None
xcb_setup_authenticate_next.argtypes = [POINTER(xcb_setup_authenticate_iterator_t)]

# /usr/include/xcb/xproto.h:5538
xcb_setup_authenticate_end = _lib.xcb_setup_authenticate_end
xcb_setup_authenticate_end.restype = xcb_generic_iterator_t
xcb_setup_authenticate_end.argtypes = [xcb_setup_authenticate_iterator_t]

# /usr/include/xcb/xproto.h:5550
xcb_setup_vendor = _lib.xcb_setup_vendor
xcb_setup_vendor.restype = c_char_p
xcb_setup_vendor.argtypes = [POINTER(xcb_setup_t)]

# /usr/include/xcb/xproto.h:5564
xcb_setup_vendor_length = _lib.xcb_setup_vendor_length
xcb_setup_vendor_length.restype = c_int
xcb_setup_vendor_length.argtypes = [POINTER(xcb_setup_t)]

# /usr/include/xcb/xproto.h:5577
xcb_setup_vendor_end = _lib.xcb_setup_vendor_end
xcb_setup_vendor_end.restype = xcb_generic_iterator_t
xcb_setup_vendor_end.argtypes = [POINTER(xcb_setup_t)]

# /usr/include/xcb/xproto.h:5589
xcb_setup_pixmap_formats = _lib.xcb_setup_pixmap_formats
xcb_setup_pixmap_formats.restype = POINTER(xcb_format_t)
xcb_setup_pixmap_formats.argtypes = [POINTER(xcb_setup_t)]

# /usr/include/xcb/xproto.h:5603
xcb_setup_pixmap_formats_length = _lib.xcb_setup_pixmap_formats_length
xcb_setup_pixmap_formats_length.restype = c_int
xcb_setup_pixmap_formats_length.argtypes = [POINTER(xcb_setup_t)]

# /usr/include/xcb/xproto.h:5616
xcb_setup_pixmap_formats_iterator = _lib.xcb_setup_pixmap_formats_iterator
xcb_setup_pixmap_formats_iterator.restype = xcb_format_iterator_t
xcb_setup_pixmap_formats_iterator.argtypes = [POINTER(xcb_setup_t)]

# /usr/include/xcb/xproto.h:5629
xcb_setup_roots_length = _lib.xcb_setup_roots_length
xcb_setup_roots_length.restype = c_int
xcb_setup_roots_length.argtypes = [POINTER(xcb_setup_t)]

# /usr/include/xcb/xproto.h:5642
xcb_setup_roots_iterator = _lib.xcb_setup_roots_iterator
xcb_setup_roots_iterator.restype = xcb_screen_iterator_t
xcb_setup_roots_iterator.argtypes = [POINTER(xcb_setup_t)]

# /usr/include/xcb/xproto.h:5663
xcb_setup_next = _lib.xcb_setup_next
xcb_setup_next.restype = None
xcb_setup_next.argtypes = [POINTER(xcb_setup_iterator_t)]

# /usr/include/xcb/xproto.h:5685
xcb_setup_end = _lib.xcb_setup_end
xcb_setup_end.restype = xcb_generic_iterator_t
xcb_setup_end.argtypes = [xcb_setup_iterator_t]

# /usr/include/xcb/xproto.h:5706
xcb_client_message_data_next = _lib.xcb_client_message_data_next
xcb_client_message_data_next.restype = None
xcb_client_message_data_next.argtypes = [POINTER(xcb_client_message_data_iterator_t)]

# /usr/include/xcb/xproto.h:5728
xcb_client_message_data_end = _lib.xcb_client_message_data_end
xcb_client_message_data_end.restype = xcb_generic_iterator_t
xcb_client_message_data_end.argtypes = [xcb_client_message_data_iterator_t]

# /usr/include/xcb/xproto.h:5764
xcb_create_window_checked = _lib.xcb_create_window_checked
xcb_create_window_checked.restype = xcb_void_cookie_t
xcb_create_window_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, xcb_window_t, c_int16, c_int16, c_uint16, c_uint16, c_uint16, c_uint16, xcb_visualid_t, c_uint32, POINTER(c_uint32)]

# /usr/include/xcb/xproto.h:5809
xcb_create_window = _lib.xcb_create_window
xcb_create_window.restype = xcb_void_cookie_t
xcb_create_window.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, xcb_window_t, c_int16, c_int16, c_uint16, c_uint16, c_uint16, c_uint16, xcb_visualid_t, c_uint32, POINTER(c_uint32)]

# /usr/include/xcb/xproto.h:5848
xcb_change_window_attributes_checked = _lib.xcb_change_window_attributes_checked
xcb_change_window_attributes_checked.restype = xcb_void_cookie_t
xcb_change_window_attributes_checked.argtypes = [POINTER(xcb_connection_t), xcb_window_t, c_uint32, POINTER(c_uint32)]

# /usr/include/xcb/xproto.h:5875
xcb_change_window_attributes = _lib.xcb_change_window_attributes
xcb_change_window_attributes.restype = xcb_void_cookie_t
xcb_change_window_attributes.argtypes = [POINTER(xcb_connection_t), xcb_window_t, c_uint32, POINTER(c_uint32)]

# /usr/include/xcb/xproto.h:5900
xcb_get_window_attributes = _lib.xcb_get_window_attributes
xcb_get_window_attributes.restype = xcb_get_window_attributes_cookie_t
xcb_get_window_attributes.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:5926
xcb_get_window_attributes_unchecked = _lib.xcb_get_window_attributes_unchecked
xcb_get_window_attributes_unchecked.restype = xcb_get_window_attributes_cookie_t
xcb_get_window_attributes_unchecked.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:5953
xcb_get_window_attributes_reply = _lib.xcb_get_window_attributes_reply
xcb_get_window_attributes_reply.restype = POINTER(xcb_get_window_attributes_reply_t)
xcb_get_window_attributes_reply.argtypes = [POINTER(xcb_connection_t), xcb_get_window_attributes_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:5981
xcb_destroy_window_checked = _lib.xcb_destroy_window_checked
xcb_destroy_window_checked.restype = xcb_void_cookie_t
xcb_destroy_window_checked.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:6004
xcb_destroy_window = _lib.xcb_destroy_window
xcb_destroy_window.restype = xcb_void_cookie_t
xcb_destroy_window.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:6030
xcb_destroy_subwindows_checked = _lib.xcb_destroy_subwindows_checked
xcb_destroy_subwindows_checked.restype = xcb_void_cookie_t
xcb_destroy_subwindows_checked.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:6053
xcb_destroy_subwindows = _lib.xcb_destroy_subwindows
xcb_destroy_subwindows.restype = xcb_void_cookie_t
xcb_destroy_subwindows.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:6080
xcb_change_save_set_checked = _lib.xcb_change_save_set_checked
xcb_change_save_set_checked.restype = xcb_void_cookie_t
xcb_change_save_set_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t]

# /usr/include/xcb/xproto.h:6105
xcb_change_save_set = _lib.xcb_change_save_set
xcb_change_save_set.restype = xcb_void_cookie_t
xcb_change_save_set.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t]

# /usr/include/xcb/xproto.h:6135
xcb_reparent_window_checked = _lib.xcb_reparent_window_checked
xcb_reparent_window_checked.restype = xcb_void_cookie_t
xcb_reparent_window_checked.argtypes = [POINTER(xcb_connection_t), xcb_window_t, xcb_window_t, c_int16, c_int16]

# /usr/include/xcb/xproto.h:6164
xcb_reparent_window = _lib.xcb_reparent_window
xcb_reparent_window.restype = xcb_void_cookie_t
xcb_reparent_window.argtypes = [POINTER(xcb_connection_t), xcb_window_t, xcb_window_t, c_int16, c_int16]

# /usr/include/xcb/xproto.h:6193
xcb_map_window_checked = _lib.xcb_map_window_checked
xcb_map_window_checked.restype = xcb_void_cookie_t
xcb_map_window_checked.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:6216
xcb_map_window = _lib.xcb_map_window
xcb_map_window.restype = xcb_void_cookie_t
xcb_map_window.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:6242
xcb_map_subwindows_checked = _lib.xcb_map_subwindows_checked
xcb_map_subwindows_checked.restype = xcb_void_cookie_t
xcb_map_subwindows_checked.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:6265
xcb_map_subwindows = _lib.xcb_map_subwindows
xcb_map_subwindows.restype = xcb_void_cookie_t
xcb_map_subwindows.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:6291
xcb_unmap_window_checked = _lib.xcb_unmap_window_checked
xcb_unmap_window_checked.restype = xcb_void_cookie_t
xcb_unmap_window_checked.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:6314
xcb_unmap_window = _lib.xcb_unmap_window
xcb_unmap_window.restype = xcb_void_cookie_t
xcb_unmap_window.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:6340
xcb_unmap_subwindows_checked = _lib.xcb_unmap_subwindows_checked
xcb_unmap_subwindows_checked.restype = xcb_void_cookie_t
xcb_unmap_subwindows_checked.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:6363
xcb_unmap_subwindows = _lib.xcb_unmap_subwindows
xcb_unmap_subwindows.restype = xcb_void_cookie_t
xcb_unmap_subwindows.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:6391
xcb_configure_window_checked = _lib.xcb_configure_window_checked
xcb_configure_window_checked.restype = xcb_void_cookie_t
xcb_configure_window_checked.argtypes = [POINTER(xcb_connection_t), xcb_window_t, c_uint16, POINTER(c_uint32)]

# /usr/include/xcb/xproto.h:6418
xcb_configure_window = _lib.xcb_configure_window
xcb_configure_window.restype = xcb_void_cookie_t
xcb_configure_window.argtypes = [POINTER(xcb_connection_t), xcb_window_t, c_uint16, POINTER(c_uint32)]

# /usr/include/xcb/xproto.h:6447
xcb_circulate_window_checked = _lib.xcb_circulate_window_checked
xcb_circulate_window_checked.restype = xcb_void_cookie_t
xcb_circulate_window_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t]

# /usr/include/xcb/xproto.h:6472
xcb_circulate_window = _lib.xcb_circulate_window
xcb_circulate_window.restype = xcb_void_cookie_t
xcb_circulate_window.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t]

# /usr/include/xcb/xproto.h:6496
xcb_get_geometry = _lib.xcb_get_geometry
xcb_get_geometry.restype = xcb_get_geometry_cookie_t
xcb_get_geometry.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t]

# /usr/include/xcb/xproto.h:6522
xcb_get_geometry_unchecked = _lib.xcb_get_geometry_unchecked
xcb_get_geometry_unchecked.restype = xcb_get_geometry_cookie_t
xcb_get_geometry_unchecked.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t]

# /usr/include/xcb/xproto.h:6549
xcb_get_geometry_reply = _lib.xcb_get_geometry_reply
xcb_get_geometry_reply.restype = POINTER(xcb_get_geometry_reply_t)
xcb_get_geometry_reply.argtypes = [POINTER(xcb_connection_t), xcb_get_geometry_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:6574
xcb_query_tree = _lib.xcb_query_tree
xcb_query_tree.restype = xcb_query_tree_cookie_t
xcb_query_tree.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:6600
xcb_query_tree_unchecked = _lib.xcb_query_tree_unchecked
xcb_query_tree_unchecked.restype = xcb_query_tree_cookie_t
xcb_query_tree_unchecked.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:6613
xcb_query_tree_children = _lib.xcb_query_tree_children
xcb_query_tree_children.restype = POINTER(xcb_window_t)
xcb_query_tree_children.argtypes = [POINTER(xcb_query_tree_reply_t)]

# /usr/include/xcb/xproto.h:6627
xcb_query_tree_children_length = _lib.xcb_query_tree_children_length
xcb_query_tree_children_length.restype = c_int
xcb_query_tree_children_length.argtypes = [POINTER(xcb_query_tree_reply_t)]

# /usr/include/xcb/xproto.h:6640
xcb_query_tree_children_iterator = _lib.xcb_query_tree_children_iterator
xcb_query_tree_children_iterator.restype = xcb_window_iterator_t
xcb_query_tree_children_iterator.argtypes = [POINTER(xcb_query_tree_reply_t)]

# /usr/include/xcb/xproto.h:6666
xcb_query_tree_reply = _lib.xcb_query_tree_reply
xcb_query_tree_reply.restype = POINTER(xcb_query_tree_reply_t)
xcb_query_tree_reply.argtypes = [POINTER(xcb_connection_t), xcb_query_tree_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:6693
xcb_intern_atom = _lib.xcb_intern_atom
xcb_intern_atom.restype = xcb_intern_atom_cookie_t
xcb_intern_atom.argtypes = [POINTER(xcb_connection_t), c_uint8, c_uint16, c_char_p]

# /usr/include/xcb/xproto.h:6723
xcb_intern_atom_unchecked = _lib.xcb_intern_atom_unchecked
xcb_intern_atom_unchecked.restype = xcb_intern_atom_cookie_t
xcb_intern_atom_unchecked.argtypes = [POINTER(xcb_connection_t), c_uint8, c_uint16, c_char_p]

# /usr/include/xcb/xproto.h:6752
xcb_intern_atom_reply = _lib.xcb_intern_atom_reply
xcb_intern_atom_reply.restype = POINTER(xcb_intern_atom_reply_t)
xcb_intern_atom_reply.argtypes = [POINTER(xcb_connection_t), xcb_intern_atom_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:6777
xcb_get_atom_name = _lib.xcb_get_atom_name
xcb_get_atom_name.restype = xcb_get_atom_name_cookie_t
xcb_get_atom_name.argtypes = [POINTER(xcb_connection_t), xcb_atom_t]

# /usr/include/xcb/xproto.h:6803
xcb_get_atom_name_unchecked = _lib.xcb_get_atom_name_unchecked
xcb_get_atom_name_unchecked.restype = xcb_get_atom_name_cookie_t
xcb_get_atom_name_unchecked.argtypes = [POINTER(xcb_connection_t), xcb_atom_t]

# /usr/include/xcb/xproto.h:6816
xcb_get_atom_name_name = _lib.xcb_get_atom_name_name
xcb_get_atom_name_name.restype = POINTER(c_uint8)
xcb_get_atom_name_name.argtypes = [POINTER(xcb_get_atom_name_reply_t)]

# /usr/include/xcb/xproto.h:6830
xcb_get_atom_name_name_length = _lib.xcb_get_atom_name_name_length
xcb_get_atom_name_name_length.restype = c_int
xcb_get_atom_name_name_length.argtypes = [POINTER(xcb_get_atom_name_reply_t)]

# /usr/include/xcb/xproto.h:6843
xcb_get_atom_name_name_end = _lib.xcb_get_atom_name_name_end
xcb_get_atom_name_name_end.restype = xcb_generic_iterator_t
xcb_get_atom_name_name_end.argtypes = [POINTER(xcb_get_atom_name_reply_t)]

# /usr/include/xcb/xproto.h:6869
xcb_get_atom_name_reply = _lib.xcb_get_atom_name_reply
xcb_get_atom_name_reply.restype = POINTER(xcb_get_atom_name_reply_t)
xcb_get_atom_name_reply.argtypes = [POINTER(xcb_connection_t), xcb_get_atom_name_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:6903
xcb_change_property_checked = _lib.xcb_change_property_checked
xcb_change_property_checked.restype = xcb_void_cookie_t
xcb_change_property_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, xcb_atom_t, xcb_atom_t, c_uint8, c_uint32, POINTER(None)]

# /usr/include/xcb/xproto.h:6938
xcb_change_property = _lib.xcb_change_property
xcb_change_property.restype = xcb_void_cookie_t
xcb_change_property.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, xcb_atom_t, xcb_atom_t, c_uint8, c_uint32, POINTER(None)]

# /usr/include/xcb/xproto.h:6971
xcb_delete_property_checked = _lib.xcb_delete_property_checked
xcb_delete_property_checked.restype = xcb_void_cookie_t
xcb_delete_property_checked.argtypes = [POINTER(xcb_connection_t), xcb_window_t, xcb_atom_t]

# /usr/include/xcb/xproto.h:6996
xcb_delete_property = _lib.xcb_delete_property
xcb_delete_property.restype = xcb_void_cookie_t
xcb_delete_property.argtypes = [POINTER(xcb_connection_t), xcb_window_t, xcb_atom_t]

# /usr/include/xcb/xproto.h:7025
xcb_get_property = _lib.xcb_get_property
xcb_get_property.restype = xcb_get_property_cookie_t
xcb_get_property.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, xcb_atom_t, xcb_atom_t, c_uint32, c_uint32]

# /usr/include/xcb/xproto.h:7061
xcb_get_property_unchecked = _lib.xcb_get_property_unchecked
xcb_get_property_unchecked.restype = xcb_get_property_cookie_t
xcb_get_property_unchecked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, xcb_atom_t, xcb_atom_t, c_uint32, c_uint32]

# /usr/include/xcb/xproto.h:7079
xcb_get_property_value = _lib.xcb_get_property_value
xcb_get_property_value.restype = POINTER(c_void)
xcb_get_property_value.argtypes = [POINTER(xcb_get_property_reply_t)]

# /usr/include/xcb/xproto.h:7093
xcb_get_property_value_length = _lib.xcb_get_property_value_length
xcb_get_property_value_length.restype = c_int
xcb_get_property_value_length.argtypes = [POINTER(xcb_get_property_reply_t)]

# /usr/include/xcb/xproto.h:7106
xcb_get_property_value_end = _lib.xcb_get_property_value_end
xcb_get_property_value_end.restype = xcb_generic_iterator_t
xcb_get_property_value_end.argtypes = [POINTER(xcb_get_property_reply_t)]

# /usr/include/xcb/xproto.h:7132
xcb_get_property_reply = _lib.xcb_get_property_reply
xcb_get_property_reply.restype = POINTER(xcb_get_property_reply_t)
xcb_get_property_reply.argtypes = [POINTER(xcb_connection_t), xcb_get_property_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:7157
xcb_list_properties = _lib.xcb_list_properties
xcb_list_properties.restype = xcb_list_properties_cookie_t
xcb_list_properties.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:7183
xcb_list_properties_unchecked = _lib.xcb_list_properties_unchecked
xcb_list_properties_unchecked.restype = xcb_list_properties_cookie_t
xcb_list_properties_unchecked.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:7196
xcb_list_properties_atoms = _lib.xcb_list_properties_atoms
xcb_list_properties_atoms.restype = POINTER(xcb_atom_t)
xcb_list_properties_atoms.argtypes = [POINTER(xcb_list_properties_reply_t)]

# /usr/include/xcb/xproto.h:7210
xcb_list_properties_atoms_length = _lib.xcb_list_properties_atoms_length
xcb_list_properties_atoms_length.restype = c_int
xcb_list_properties_atoms_length.argtypes = [POINTER(xcb_list_properties_reply_t)]

# /usr/include/xcb/xproto.h:7223
xcb_list_properties_atoms_iterator = _lib.xcb_list_properties_atoms_iterator
xcb_list_properties_atoms_iterator.restype = xcb_atom_iterator_t
xcb_list_properties_atoms_iterator.argtypes = [POINTER(xcb_list_properties_reply_t)]

# /usr/include/xcb/xproto.h:7249
xcb_list_properties_reply = _lib.xcb_list_properties_reply
xcb_list_properties_reply.restype = POINTER(xcb_list_properties_reply_t)
xcb_list_properties_reply.argtypes = [POINTER(xcb_connection_t), xcb_list_properties_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:7279
xcb_set_selection_owner_checked = _lib.xcb_set_selection_owner_checked
xcb_set_selection_owner_checked.restype = xcb_void_cookie_t
xcb_set_selection_owner_checked.argtypes = [POINTER(xcb_connection_t), xcb_window_t, xcb_atom_t, xcb_timestamp_t]

# /usr/include/xcb/xproto.h:7306
xcb_set_selection_owner = _lib.xcb_set_selection_owner
xcb_set_selection_owner.restype = xcb_void_cookie_t
xcb_set_selection_owner.argtypes = [POINTER(xcb_connection_t), xcb_window_t, xcb_atom_t, xcb_timestamp_t]

# /usr/include/xcb/xproto.h:7331
xcb_get_selection_owner = _lib.xcb_get_selection_owner
xcb_get_selection_owner.restype = xcb_get_selection_owner_cookie_t
xcb_get_selection_owner.argtypes = [POINTER(xcb_connection_t), xcb_atom_t]

# /usr/include/xcb/xproto.h:7357
xcb_get_selection_owner_unchecked = _lib.xcb_get_selection_owner_unchecked
xcb_get_selection_owner_unchecked.restype = xcb_get_selection_owner_cookie_t
xcb_get_selection_owner_unchecked.argtypes = [POINTER(xcb_connection_t), xcb_atom_t]

# /usr/include/xcb/xproto.h:7384
xcb_get_selection_owner_reply = _lib.xcb_get_selection_owner_reply
xcb_get_selection_owner_reply.restype = POINTER(xcb_get_selection_owner_reply_t)
xcb_get_selection_owner_reply.argtypes = [POINTER(xcb_connection_t), xcb_get_selection_owner_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:7416
xcb_convert_selection_checked = _lib.xcb_convert_selection_checked
xcb_convert_selection_checked.restype = xcb_void_cookie_t
xcb_convert_selection_checked.argtypes = [POINTER(xcb_connection_t), xcb_window_t, xcb_atom_t, xcb_atom_t, xcb_atom_t, xcb_timestamp_t]

# /usr/include/xcb/xproto.h:7447
xcb_convert_selection = _lib.xcb_convert_selection
xcb_convert_selection.restype = xcb_void_cookie_t
xcb_convert_selection.argtypes = [POINTER(xcb_connection_t), xcb_window_t, xcb_atom_t, xcb_atom_t, xcb_atom_t, xcb_timestamp_t]

# /usr/include/xcb/xproto.h:7480
xcb_send_event_checked = _lib.xcb_send_event_checked
xcb_send_event_checked.restype = xcb_void_cookie_t
xcb_send_event_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, c_uint32, c_char_p]

# /usr/include/xcb/xproto.h:7509
xcb_send_event = _lib.xcb_send_event
xcb_send_event.restype = xcb_void_cookie_t
xcb_send_event.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, c_uint32, c_char_p]

# /usr/include/xcb/xproto.h:7542
xcb_grab_pointer = _lib.xcb_grab_pointer
xcb_grab_pointer.restype = xcb_grab_pointer_cookie_t
xcb_grab_pointer.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, c_uint16, c_uint8, c_uint8, xcb_window_t, xcb_cursor_t, xcb_timestamp_t]

# /usr/include/xcb/xproto.h:7582
xcb_grab_pointer_unchecked = _lib.xcb_grab_pointer_unchecked
xcb_grab_pointer_unchecked.restype = xcb_grab_pointer_cookie_t
xcb_grab_pointer_unchecked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, c_uint16, c_uint8, c_uint8, xcb_window_t, xcb_cursor_t, xcb_timestamp_t]

# /usr/include/xcb/xproto.h:7616
xcb_grab_pointer_reply = _lib.xcb_grab_pointer_reply
xcb_grab_pointer_reply.restype = POINTER(xcb_grab_pointer_reply_t)
xcb_grab_pointer_reply.argtypes = [POINTER(xcb_connection_t), xcb_grab_pointer_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:7644
xcb_ungrab_pointer_checked = _lib.xcb_ungrab_pointer_checked
xcb_ungrab_pointer_checked.restype = xcb_void_cookie_t
xcb_ungrab_pointer_checked.argtypes = [POINTER(xcb_connection_t), xcb_timestamp_t]

# /usr/include/xcb/xproto.h:7667
xcb_ungrab_pointer = _lib.xcb_ungrab_pointer
xcb_ungrab_pointer.restype = xcb_void_cookie_t
xcb_ungrab_pointer.argtypes = [POINTER(xcb_connection_t), xcb_timestamp_t]

# /usr/include/xcb/xproto.h:7701
xcb_grab_button_checked = _lib.xcb_grab_button_checked
xcb_grab_button_checked.restype = xcb_void_cookie_t
xcb_grab_button_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, c_uint16, c_uint8, c_uint8, xcb_window_t, xcb_cursor_t, c_uint8, c_uint16]

# /usr/include/xcb/xproto.h:7740
xcb_grab_button = _lib.xcb_grab_button
xcb_grab_button.restype = xcb_void_cookie_t
xcb_grab_button.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, c_uint16, c_uint8, c_uint8, xcb_window_t, xcb_cursor_t, c_uint8, c_uint16]

# /usr/include/xcb/xproto.h:7776
xcb_ungrab_button_checked = _lib.xcb_ungrab_button_checked
xcb_ungrab_button_checked.restype = xcb_void_cookie_t
xcb_ungrab_button_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, c_uint16]

# /usr/include/xcb/xproto.h:7803
xcb_ungrab_button = _lib.xcb_ungrab_button
xcb_ungrab_button.restype = xcb_void_cookie_t
xcb_ungrab_button.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, c_uint16]

# /usr/include/xcb/xproto.h:7833
xcb_change_active_pointer_grab_checked = _lib.xcb_change_active_pointer_grab_checked
xcb_change_active_pointer_grab_checked.restype = xcb_void_cookie_t
xcb_change_active_pointer_grab_checked.argtypes = [POINTER(xcb_connection_t), xcb_cursor_t, xcb_timestamp_t, c_uint16]

# /usr/include/xcb/xproto.h:7860
xcb_change_active_pointer_grab = _lib.xcb_change_active_pointer_grab
xcb_change_active_pointer_grab.restype = xcb_void_cookie_t
xcb_change_active_pointer_grab.argtypes = [POINTER(xcb_connection_t), xcb_cursor_t, xcb_timestamp_t, c_uint16]

# /usr/include/xcb/xproto.h:7889
xcb_grab_keyboard = _lib.xcb_grab_keyboard
xcb_grab_keyboard.restype = xcb_grab_keyboard_cookie_t
xcb_grab_keyboard.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, xcb_timestamp_t, c_uint8, c_uint8]

# /usr/include/xcb/xproto.h:7923
xcb_grab_keyboard_unchecked = _lib.xcb_grab_keyboard_unchecked
xcb_grab_keyboard_unchecked.restype = xcb_grab_keyboard_cookie_t
xcb_grab_keyboard_unchecked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, xcb_timestamp_t, c_uint8, c_uint8]

# /usr/include/xcb/xproto.h:7954
xcb_grab_keyboard_reply = _lib.xcb_grab_keyboard_reply
xcb_grab_keyboard_reply.restype = POINTER(xcb_grab_keyboard_reply_t)
xcb_grab_keyboard_reply.argtypes = [POINTER(xcb_connection_t), xcb_grab_keyboard_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:7982
xcb_ungrab_keyboard_checked = _lib.xcb_ungrab_keyboard_checked
xcb_ungrab_keyboard_checked.restype = xcb_void_cookie_t
xcb_ungrab_keyboard_checked.argtypes = [POINTER(xcb_connection_t), xcb_timestamp_t]

# /usr/include/xcb/xproto.h:8005
xcb_ungrab_keyboard = _lib.xcb_ungrab_keyboard
xcb_ungrab_keyboard.restype = xcb_void_cookie_t
xcb_ungrab_keyboard.argtypes = [POINTER(xcb_connection_t), xcb_timestamp_t]

# /usr/include/xcb/xproto.h:8036
xcb_grab_key_checked = _lib.xcb_grab_key_checked
xcb_grab_key_checked.restype = xcb_void_cookie_t
xcb_grab_key_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, c_uint16, xcb_keycode_t, c_uint8, c_uint8]

# /usr/include/xcb/xproto.h:8069
xcb_grab_key = _lib.xcb_grab_key
xcb_grab_key.restype = xcb_void_cookie_t
xcb_grab_key.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, c_uint16, xcb_keycode_t, c_uint8, c_uint8]

# /usr/include/xcb/xproto.h:8102
xcb_ungrab_key_checked = _lib.xcb_ungrab_key_checked
xcb_ungrab_key_checked.restype = xcb_void_cookie_t
xcb_ungrab_key_checked.argtypes = [POINTER(xcb_connection_t), xcb_keycode_t, xcb_window_t, c_uint16]

# /usr/include/xcb/xproto.h:8129
xcb_ungrab_key = _lib.xcb_ungrab_key
xcb_ungrab_key.restype = xcb_void_cookie_t
xcb_ungrab_key.argtypes = [POINTER(xcb_connection_t), xcb_keycode_t, xcb_window_t, c_uint16]

# /usr/include/xcb/xproto.h:8158
xcb_allow_events_checked = _lib.xcb_allow_events_checked
xcb_allow_events_checked.restype = xcb_void_cookie_t
xcb_allow_events_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_timestamp_t]

# /usr/include/xcb/xproto.h:8183
xcb_allow_events = _lib.xcb_allow_events
xcb_allow_events.restype = xcb_void_cookie_t
xcb_allow_events.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_timestamp_t]

# /usr/include/xcb/xproto.h:8209
xcb_grab_server_checked = _lib.xcb_grab_server_checked
xcb_grab_server_checked.restype = xcb_void_cookie_t
xcb_grab_server_checked.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:8230
xcb_grab_server = _lib.xcb_grab_server
xcb_grab_server.restype = xcb_void_cookie_t
xcb_grab_server.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:8254
xcb_ungrab_server_checked = _lib.xcb_ungrab_server_checked
xcb_ungrab_server_checked.restype = xcb_void_cookie_t
xcb_ungrab_server_checked.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:8275
xcb_ungrab_server = _lib.xcb_ungrab_server
xcb_ungrab_server.restype = xcb_void_cookie_t
xcb_ungrab_server.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:8297
xcb_query_pointer = _lib.xcb_query_pointer
xcb_query_pointer.restype = xcb_query_pointer_cookie_t
xcb_query_pointer.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:8323
xcb_query_pointer_unchecked = _lib.xcb_query_pointer_unchecked
xcb_query_pointer_unchecked.restype = xcb_query_pointer_cookie_t
xcb_query_pointer_unchecked.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:8350
xcb_query_pointer_reply = _lib.xcb_query_pointer_reply
xcb_query_pointer_reply.restype = POINTER(xcb_query_pointer_reply_t)
xcb_query_pointer_reply.argtypes = [POINTER(xcb_connection_t), xcb_query_pointer_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:8374
xcb_timecoord_next = _lib.xcb_timecoord_next
xcb_timecoord_next.restype = None
xcb_timecoord_next.argtypes = [POINTER(xcb_timecoord_iterator_t)]

# /usr/include/xcb/xproto.h:8396
xcb_timecoord_end = _lib.xcb_timecoord_end
xcb_timecoord_end.restype = xcb_generic_iterator_t
xcb_timecoord_end.argtypes = [xcb_timecoord_iterator_t]

# /usr/include/xcb/xproto.h:8420
xcb_get_motion_events = _lib.xcb_get_motion_events
xcb_get_motion_events.restype = xcb_get_motion_events_cookie_t
xcb_get_motion_events.argtypes = [POINTER(xcb_connection_t), xcb_window_t, xcb_timestamp_t, xcb_timestamp_t]

# /usr/include/xcb/xproto.h:8450
xcb_get_motion_events_unchecked = _lib.xcb_get_motion_events_unchecked
xcb_get_motion_events_unchecked.restype = xcb_get_motion_events_cookie_t
xcb_get_motion_events_unchecked.argtypes = [POINTER(xcb_connection_t), xcb_window_t, xcb_timestamp_t, xcb_timestamp_t]

# /usr/include/xcb/xproto.h:8465
xcb_get_motion_events_events = _lib.xcb_get_motion_events_events
xcb_get_motion_events_events.restype = POINTER(xcb_timecoord_t)
xcb_get_motion_events_events.argtypes = [POINTER(xcb_get_motion_events_reply_t)]

# /usr/include/xcb/xproto.h:8479
xcb_get_motion_events_events_length = _lib.xcb_get_motion_events_events_length
xcb_get_motion_events_events_length.restype = c_int
xcb_get_motion_events_events_length.argtypes = [POINTER(xcb_get_motion_events_reply_t)]

# /usr/include/xcb/xproto.h:8492
xcb_get_motion_events_events_iterator = _lib.xcb_get_motion_events_events_iterator
xcb_get_motion_events_events_iterator.restype = xcb_timecoord_iterator_t
xcb_get_motion_events_events_iterator.argtypes = [POINTER(xcb_get_motion_events_reply_t)]

# /usr/include/xcb/xproto.h:8518
xcb_get_motion_events_reply = _lib.xcb_get_motion_events_reply
xcb_get_motion_events_reply.restype = POINTER(xcb_get_motion_events_reply_t)
xcb_get_motion_events_reply.argtypes = [POINTER(xcb_connection_t), xcb_get_motion_events_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:8546
xcb_translate_coordinates = _lib.xcb_translate_coordinates
xcb_translate_coordinates.restype = xcb_translate_coordinates_cookie_t
xcb_translate_coordinates.argtypes = [POINTER(xcb_connection_t), xcb_window_t, xcb_window_t, c_int16, c_int16]

# /usr/include/xcb/xproto.h:8578
xcb_translate_coordinates_unchecked = _lib.xcb_translate_coordinates_unchecked
xcb_translate_coordinates_unchecked.restype = xcb_translate_coordinates_cookie_t
xcb_translate_coordinates_unchecked.argtypes = [POINTER(xcb_connection_t), xcb_window_t, xcb_window_t, c_int16, c_int16]

# /usr/include/xcb/xproto.h:8608
xcb_translate_coordinates_reply = _lib.xcb_translate_coordinates_reply
xcb_translate_coordinates_reply.restype = POINTER(xcb_translate_coordinates_reply_t)
xcb_translate_coordinates_reply.argtypes = [POINTER(xcb_connection_t), xcb_translate_coordinates_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:8643
xcb_warp_pointer_checked = _lib.xcb_warp_pointer_checked
xcb_warp_pointer_checked.restype = xcb_void_cookie_t
xcb_warp_pointer_checked.argtypes = [POINTER(xcb_connection_t), xcb_window_t, xcb_window_t, c_int16, c_int16, c_uint16, c_uint16, c_int16, c_int16]

# /usr/include/xcb/xproto.h:8680
xcb_warp_pointer = _lib.xcb_warp_pointer
xcb_warp_pointer.restype = xcb_void_cookie_t
xcb_warp_pointer.argtypes = [POINTER(xcb_connection_t), xcb_window_t, xcb_window_t, c_int16, c_int16, c_uint16, c_uint16, c_int16, c_int16]

# /usr/include/xcb/xproto.h:8715
xcb_set_input_focus_checked = _lib.xcb_set_input_focus_checked
xcb_set_input_focus_checked.restype = xcb_void_cookie_t
xcb_set_input_focus_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, xcb_timestamp_t]

# /usr/include/xcb/xproto.h:8742
xcb_set_input_focus = _lib.xcb_set_input_focus
xcb_set_input_focus.restype = xcb_void_cookie_t
xcb_set_input_focus.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, xcb_timestamp_t]

# /usr/include/xcb/xproto.h:8766
xcb_get_input_focus = _lib.xcb_get_input_focus
xcb_get_input_focus.restype = xcb_get_input_focus_cookie_t
xcb_get_input_focus.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:8790
xcb_get_input_focus_unchecked = _lib.xcb_get_input_focus_unchecked
xcb_get_input_focus_unchecked.restype = xcb_get_input_focus_cookie_t
xcb_get_input_focus_unchecked.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:8816
xcb_get_input_focus_reply = _lib.xcb_get_input_focus_reply
xcb_get_input_focus_reply.restype = POINTER(xcb_get_input_focus_reply_t)
xcb_get_input_focus_reply.argtypes = [POINTER(xcb_connection_t), xcb_get_input_focus_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:8840
xcb_query_keymap = _lib.xcb_query_keymap
xcb_query_keymap.restype = xcb_query_keymap_cookie_t
xcb_query_keymap.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:8864
xcb_query_keymap_unchecked = _lib.xcb_query_keymap_unchecked
xcb_query_keymap_unchecked.restype = xcb_query_keymap_cookie_t
xcb_query_keymap_unchecked.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:8890
xcb_query_keymap_reply = _lib.xcb_query_keymap_reply
xcb_query_keymap_reply.restype = POINTER(xcb_query_keymap_reply_t)
xcb_query_keymap_reply.argtypes = [POINTER(xcb_connection_t), xcb_query_keymap_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:8920
xcb_open_font_checked = _lib.xcb_open_font_checked
xcb_open_font_checked.restype = xcb_void_cookie_t
xcb_open_font_checked.argtypes = [POINTER(xcb_connection_t), xcb_font_t, c_uint16, c_char_p]

# /usr/include/xcb/xproto.h:8947
xcb_open_font = _lib.xcb_open_font
xcb_open_font.restype = xcb_void_cookie_t
xcb_open_font.argtypes = [POINTER(xcb_connection_t), xcb_font_t, c_uint16, c_char_p]

# /usr/include/xcb/xproto.h:8975
xcb_close_font_checked = _lib.xcb_close_font_checked
xcb_close_font_checked.restype = xcb_void_cookie_t
xcb_close_font_checked.argtypes = [POINTER(xcb_connection_t), xcb_font_t]

# /usr/include/xcb/xproto.h:8998
xcb_close_font = _lib.xcb_close_font
xcb_close_font.restype = xcb_void_cookie_t
xcb_close_font.argtypes = [POINTER(xcb_connection_t), xcb_font_t]

# /usr/include/xcb/xproto.h:9020
xcb_fontprop_next = _lib.xcb_fontprop_next
xcb_fontprop_next.restype = None
xcb_fontprop_next.argtypes = [POINTER(xcb_fontprop_iterator_t)]

# /usr/include/xcb/xproto.h:9042
xcb_fontprop_end = _lib.xcb_fontprop_end
xcb_fontprop_end.restype = xcb_generic_iterator_t
xcb_fontprop_end.argtypes = [xcb_fontprop_iterator_t]

# /usr/include/xcb/xproto.h:9063
xcb_charinfo_next = _lib.xcb_charinfo_next
xcb_charinfo_next.restype = None
xcb_charinfo_next.argtypes = [POINTER(xcb_charinfo_iterator_t)]

# /usr/include/xcb/xproto.h:9085
xcb_charinfo_end = _lib.xcb_charinfo_end
xcb_charinfo_end.restype = xcb_generic_iterator_t
xcb_charinfo_end.argtypes = [xcb_charinfo_iterator_t]

# /usr/include/xcb/xproto.h:9107
xcb_query_font = _lib.xcb_query_font
xcb_query_font.restype = xcb_query_font_cookie_t
xcb_query_font.argtypes = [POINTER(xcb_connection_t), xcb_fontable_t]

# /usr/include/xcb/xproto.h:9133
xcb_query_font_unchecked = _lib.xcb_query_font_unchecked
xcb_query_font_unchecked.restype = xcb_query_font_cookie_t
xcb_query_font_unchecked.argtypes = [POINTER(xcb_connection_t), xcb_fontable_t]

# /usr/include/xcb/xproto.h:9146
xcb_query_font_properties = _lib.xcb_query_font_properties
xcb_query_font_properties.restype = POINTER(xcb_fontprop_t)
xcb_query_font_properties.argtypes = [POINTER(xcb_query_font_reply_t)]

# /usr/include/xcb/xproto.h:9160
xcb_query_font_properties_length = _lib.xcb_query_font_properties_length
xcb_query_font_properties_length.restype = c_int
xcb_query_font_properties_length.argtypes = [POINTER(xcb_query_font_reply_t)]

# /usr/include/xcb/xproto.h:9173
xcb_query_font_properties_iterator = _lib.xcb_query_font_properties_iterator
xcb_query_font_properties_iterator.restype = xcb_fontprop_iterator_t
xcb_query_font_properties_iterator.argtypes = [POINTER(xcb_query_font_reply_t)]

# /usr/include/xcb/xproto.h:9185
xcb_query_font_char_infos = _lib.xcb_query_font_char_infos
xcb_query_font_char_infos.restype = POINTER(xcb_charinfo_t)
xcb_query_font_char_infos.argtypes = [POINTER(xcb_query_font_reply_t)]

# /usr/include/xcb/xproto.h:9199
xcb_query_font_char_infos_length = _lib.xcb_query_font_char_infos_length
xcb_query_font_char_infos_length.restype = c_int
xcb_query_font_char_infos_length.argtypes = [POINTER(xcb_query_font_reply_t)]

# /usr/include/xcb/xproto.h:9212
xcb_query_font_char_infos_iterator = _lib.xcb_query_font_char_infos_iterator
xcb_query_font_char_infos_iterator.restype = xcb_charinfo_iterator_t
xcb_query_font_char_infos_iterator.argtypes = [POINTER(xcb_query_font_reply_t)]

# /usr/include/xcb/xproto.h:9238
xcb_query_font_reply = _lib.xcb_query_font_reply
xcb_query_font_reply.restype = POINTER(xcb_query_font_reply_t)
xcb_query_font_reply.argtypes = [POINTER(xcb_connection_t), xcb_query_font_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:9265
xcb_query_text_extents = _lib.xcb_query_text_extents
xcb_query_text_extents.restype = xcb_query_text_extents_cookie_t
xcb_query_text_extents.argtypes = [POINTER(xcb_connection_t), xcb_fontable_t, c_uint32, POINTER(xcb_char2b_t)]

# /usr/include/xcb/xproto.h:9295
xcb_query_text_extents_unchecked = _lib.xcb_query_text_extents_unchecked
xcb_query_text_extents_unchecked.restype = xcb_query_text_extents_cookie_t
xcb_query_text_extents_unchecked.argtypes = [POINTER(xcb_connection_t), xcb_fontable_t, c_uint32, POINTER(xcb_char2b_t)]

# /usr/include/xcb/xproto.h:9324
xcb_query_text_extents_reply = _lib.xcb_query_text_extents_reply
xcb_query_text_extents_reply.restype = POINTER(xcb_query_text_extents_reply_t)
xcb_query_text_extents_reply.argtypes = [POINTER(xcb_connection_t), xcb_query_text_extents_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:9339
xcb_str_name = _lib.xcb_str_name
xcb_str_name.restype = c_char_p
xcb_str_name.argtypes = [POINTER(xcb_str_t)]

# /usr/include/xcb/xproto.h:9353
xcb_str_name_length = _lib.xcb_str_name_length
xcb_str_name_length.restype = c_int
xcb_str_name_length.argtypes = [POINTER(xcb_str_t)]

# /usr/include/xcb/xproto.h:9366
xcb_str_name_end = _lib.xcb_str_name_end
xcb_str_name_end.restype = xcb_generic_iterator_t
xcb_str_name_end.argtypes = [POINTER(xcb_str_t)]

# /usr/include/xcb/xproto.h:9387
xcb_str_next = _lib.xcb_str_next
xcb_str_next.restype = None
xcb_str_next.argtypes = [POINTER(xcb_str_iterator_t)]

# /usr/include/xcb/xproto.h:9409
xcb_str_end = _lib.xcb_str_end
xcb_str_end.restype = xcb_generic_iterator_t
xcb_str_end.argtypes = [xcb_str_iterator_t]

# /usr/include/xcb/xproto.h:9433
xcb_list_fonts = _lib.xcb_list_fonts
xcb_list_fonts.restype = xcb_list_fonts_cookie_t
xcb_list_fonts.argtypes = [POINTER(xcb_connection_t), c_uint16, c_uint16, c_char_p]

# /usr/include/xcb/xproto.h:9463
xcb_list_fonts_unchecked = _lib.xcb_list_fonts_unchecked
xcb_list_fonts_unchecked.restype = xcb_list_fonts_cookie_t
xcb_list_fonts_unchecked.argtypes = [POINTER(xcb_connection_t), c_uint16, c_uint16, c_char_p]

# /usr/include/xcb/xproto.h:9479
xcb_list_fonts_names_length = _lib.xcb_list_fonts_names_length
xcb_list_fonts_names_length.restype = c_int
xcb_list_fonts_names_length.argtypes = [POINTER(xcb_list_fonts_reply_t)]

# /usr/include/xcb/xproto.h:9492
xcb_list_fonts_names_iterator = _lib.xcb_list_fonts_names_iterator
xcb_list_fonts_names_iterator.restype = xcb_str_iterator_t
xcb_list_fonts_names_iterator.argtypes = [POINTER(xcb_list_fonts_reply_t)]

# /usr/include/xcb/xproto.h:9518
xcb_list_fonts_reply = _lib.xcb_list_fonts_reply
xcb_list_fonts_reply.restype = POINTER(xcb_list_fonts_reply_t)
xcb_list_fonts_reply.argtypes = [POINTER(xcb_connection_t), xcb_list_fonts_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:9545
xcb_list_fonts_with_info = _lib.xcb_list_fonts_with_info
xcb_list_fonts_with_info.restype = xcb_list_fonts_with_info_cookie_t
xcb_list_fonts_with_info.argtypes = [POINTER(xcb_connection_t), c_uint16, c_uint16, c_char_p]

# /usr/include/xcb/xproto.h:9575
xcb_list_fonts_with_info_unchecked = _lib.xcb_list_fonts_with_info_unchecked
xcb_list_fonts_with_info_unchecked.restype = xcb_list_fonts_with_info_cookie_t
xcb_list_fonts_with_info_unchecked.argtypes = [POINTER(xcb_connection_t), c_uint16, c_uint16, c_char_p]

# /usr/include/xcb/xproto.h:9590
xcb_list_fonts_with_info_properties = _lib.xcb_list_fonts_with_info_properties
xcb_list_fonts_with_info_properties.restype = POINTER(xcb_fontprop_t)
xcb_list_fonts_with_info_properties.argtypes = [POINTER(xcb_list_fonts_with_info_reply_t)]

# /usr/include/xcb/xproto.h:9604
xcb_list_fonts_with_info_properties_length = _lib.xcb_list_fonts_with_info_properties_length
xcb_list_fonts_with_info_properties_length.restype = c_int
xcb_list_fonts_with_info_properties_length.argtypes = [POINTER(xcb_list_fonts_with_info_reply_t)]

# /usr/include/xcb/xproto.h:9617
xcb_list_fonts_with_info_properties_iterator = _lib.xcb_list_fonts_with_info_properties_iterator
xcb_list_fonts_with_info_properties_iterator.restype = xcb_fontprop_iterator_t
xcb_list_fonts_with_info_properties_iterator.argtypes = [POINTER(xcb_list_fonts_with_info_reply_t)]

# /usr/include/xcb/xproto.h:9629
xcb_list_fonts_with_info_name = _lib.xcb_list_fonts_with_info_name
xcb_list_fonts_with_info_name.restype = c_char_p
xcb_list_fonts_with_info_name.argtypes = [POINTER(xcb_list_fonts_with_info_reply_t)]

# /usr/include/xcb/xproto.h:9643
xcb_list_fonts_with_info_name_length = _lib.xcb_list_fonts_with_info_name_length
xcb_list_fonts_with_info_name_length.restype = c_int
xcb_list_fonts_with_info_name_length.argtypes = [POINTER(xcb_list_fonts_with_info_reply_t)]

# /usr/include/xcb/xproto.h:9656
xcb_list_fonts_with_info_name_end = _lib.xcb_list_fonts_with_info_name_end
xcb_list_fonts_with_info_name_end.restype = xcb_generic_iterator_t
xcb_list_fonts_with_info_name_end.argtypes = [POINTER(xcb_list_fonts_with_info_reply_t)]

# /usr/include/xcb/xproto.h:9682
xcb_list_fonts_with_info_reply = _lib.xcb_list_fonts_with_info_reply
xcb_list_fonts_with_info_reply.restype = POINTER(xcb_list_fonts_with_info_reply_t)
xcb_list_fonts_with_info_reply.argtypes = [POINTER(xcb_connection_t), xcb_list_fonts_with_info_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:9712
xcb_set_font_path_checked = _lib.xcb_set_font_path_checked
xcb_set_font_path_checked.restype = xcb_void_cookie_t
xcb_set_font_path_checked.argtypes = [POINTER(xcb_connection_t), c_uint16, c_uint32, c_char_p]

# /usr/include/xcb/xproto.h:9739
xcb_set_font_path = _lib.xcb_set_font_path
xcb_set_font_path.restype = xcb_void_cookie_t
xcb_set_font_path.argtypes = [POINTER(xcb_connection_t), c_uint16, c_uint32, c_char_p]

# /usr/include/xcb/xproto.h:9763
xcb_get_font_path = _lib.xcb_get_font_path
xcb_get_font_path.restype = xcb_get_font_path_cookie_t
xcb_get_font_path.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:9787
xcb_get_font_path_unchecked = _lib.xcb_get_font_path_unchecked
xcb_get_font_path_unchecked.restype = xcb_get_font_path_cookie_t
xcb_get_font_path_unchecked.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:9800
xcb_get_font_path_path_length = _lib.xcb_get_font_path_path_length
xcb_get_font_path_path_length.restype = c_int
xcb_get_font_path_path_length.argtypes = [POINTER(xcb_get_font_path_reply_t)]

# /usr/include/xcb/xproto.h:9813
xcb_get_font_path_path_iterator = _lib.xcb_get_font_path_path_iterator
xcb_get_font_path_path_iterator.restype = xcb_str_iterator_t
xcb_get_font_path_path_iterator.argtypes = [POINTER(xcb_get_font_path_reply_t)]

# /usr/include/xcb/xproto.h:9839
xcb_get_font_path_reply = _lib.xcb_get_font_path_reply
xcb_get_font_path_reply.restype = POINTER(xcb_get_font_path_reply_t)
xcb_get_font_path_reply.argtypes = [POINTER(xcb_connection_t), xcb_get_font_path_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:9871
xcb_create_pixmap_checked = _lib.xcb_create_pixmap_checked
xcb_create_pixmap_checked.restype = xcb_void_cookie_t
xcb_create_pixmap_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_pixmap_t, xcb_drawable_t, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:9902
xcb_create_pixmap = _lib.xcb_create_pixmap
xcb_create_pixmap.restype = xcb_void_cookie_t
xcb_create_pixmap.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_pixmap_t, xcb_drawable_t, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:9932
xcb_free_pixmap_checked = _lib.xcb_free_pixmap_checked
xcb_free_pixmap_checked.restype = xcb_void_cookie_t
xcb_free_pixmap_checked.argtypes = [POINTER(xcb_connection_t), xcb_pixmap_t]

# /usr/include/xcb/xproto.h:9955
xcb_free_pixmap = _lib.xcb_free_pixmap
xcb_free_pixmap.restype = xcb_void_cookie_t
xcb_free_pixmap.argtypes = [POINTER(xcb_connection_t), xcb_pixmap_t]

# /usr/include/xcb/xproto.h:9984
xcb_create_gc_checked = _lib.xcb_create_gc_checked
xcb_create_gc_checked.restype = xcb_void_cookie_t
xcb_create_gc_checked.argtypes = [POINTER(xcb_connection_t), xcb_gcontext_t, xcb_drawable_t, c_uint32, POINTER(c_uint32)]

# /usr/include/xcb/xproto.h:10013
xcb_create_gc = _lib.xcb_create_gc
xcb_create_gc.restype = xcb_void_cookie_t
xcb_create_gc.argtypes = [POINTER(xcb_connection_t), xcb_gcontext_t, xcb_drawable_t, c_uint32, POINTER(c_uint32)]

# /usr/include/xcb/xproto.h:10044
xcb_change_gc_checked = _lib.xcb_change_gc_checked
xcb_change_gc_checked.restype = xcb_void_cookie_t
xcb_change_gc_checked.argtypes = [POINTER(xcb_connection_t), xcb_gcontext_t, c_uint32, POINTER(c_uint32)]

# /usr/include/xcb/xproto.h:10071
xcb_change_gc = _lib.xcb_change_gc
xcb_change_gc.restype = xcb_void_cookie_t
xcb_change_gc.argtypes = [POINTER(xcb_connection_t), xcb_gcontext_t, c_uint32, POINTER(c_uint32)]

# /usr/include/xcb/xproto.h:10101
xcb_copy_gc_checked = _lib.xcb_copy_gc_checked
xcb_copy_gc_checked.restype = xcb_void_cookie_t
xcb_copy_gc_checked.argtypes = [POINTER(xcb_connection_t), xcb_gcontext_t, xcb_gcontext_t, c_uint32]

# /usr/include/xcb/xproto.h:10128
xcb_copy_gc = _lib.xcb_copy_gc
xcb_copy_gc.restype = xcb_void_cookie_t
xcb_copy_gc.argtypes = [POINTER(xcb_connection_t), xcb_gcontext_t, xcb_gcontext_t, c_uint32]

# /usr/include/xcb/xproto.h:10159
xcb_set_dashes_checked = _lib.xcb_set_dashes_checked
xcb_set_dashes_checked.restype = xcb_void_cookie_t
xcb_set_dashes_checked.argtypes = [POINTER(xcb_connection_t), xcb_gcontext_t, c_uint16, c_uint16, POINTER(c_uint8)]

# /usr/include/xcb/xproto.h:10188
xcb_set_dashes = _lib.xcb_set_dashes
xcb_set_dashes.restype = xcb_void_cookie_t
xcb_set_dashes.argtypes = [POINTER(xcb_connection_t), xcb_gcontext_t, c_uint16, c_uint16, POINTER(c_uint8)]

# /usr/include/xcb/xproto.h:10222
xcb_set_clip_rectangles_checked = _lib.xcb_set_clip_rectangles_checked
xcb_set_clip_rectangles_checked.restype = xcb_void_cookie_t
xcb_set_clip_rectangles_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_gcontext_t, c_int16, c_int16, c_uint32, POINTER(xcb_rectangle_t)]

# /usr/include/xcb/xproto.h:10255
xcb_set_clip_rectangles = _lib.xcb_set_clip_rectangles
xcb_set_clip_rectangles.restype = xcb_void_cookie_t
xcb_set_clip_rectangles.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_gcontext_t, c_int16, c_int16, c_uint32, POINTER(xcb_rectangle_t)]

# /usr/include/xcb/xproto.h:10286
xcb_free_gc_checked = _lib.xcb_free_gc_checked
xcb_free_gc_checked.restype = xcb_void_cookie_t
xcb_free_gc_checked.argtypes = [POINTER(xcb_connection_t), xcb_gcontext_t]

# /usr/include/xcb/xproto.h:10309
xcb_free_gc = _lib.xcb_free_gc
xcb_free_gc.restype = xcb_void_cookie_t
xcb_free_gc.argtypes = [POINTER(xcb_connection_t), xcb_gcontext_t]

# /usr/include/xcb/xproto.h:10340
xcb_clear_area_checked = _lib.xcb_clear_area_checked
xcb_clear_area_checked.restype = xcb_void_cookie_t
xcb_clear_area_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, c_int16, c_int16, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:10373
xcb_clear_area = _lib.xcb_clear_area
xcb_clear_area.restype = xcb_void_cookie_t
xcb_clear_area.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_window_t, c_int16, c_int16, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:10412
xcb_copy_area_checked = _lib.xcb_copy_area_checked
xcb_copy_area_checked.restype = xcb_void_cookie_t
xcb_copy_area_checked.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_drawable_t, xcb_gcontext_t, c_int16, c_int16, c_int16, c_int16, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:10451
xcb_copy_area = _lib.xcb_copy_area
xcb_copy_area.restype = xcb_void_cookie_t
xcb_copy_area.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_drawable_t, xcb_gcontext_t, c_int16, c_int16, c_int16, c_int16, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:10494
xcb_copy_plane_checked = _lib.xcb_copy_plane_checked
xcb_copy_plane_checked.restype = xcb_void_cookie_t
xcb_copy_plane_checked.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_drawable_t, xcb_gcontext_t, c_int16, c_int16, c_int16, c_int16, c_uint16, c_uint16, c_uint32]

# /usr/include/xcb/xproto.h:10535
xcb_copy_plane = _lib.xcb_copy_plane
xcb_copy_plane.restype = xcb_void_cookie_t
xcb_copy_plane.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_drawable_t, xcb_gcontext_t, c_int16, c_int16, c_int16, c_int16, c_uint16, c_uint16, c_uint32]

# /usr/include/xcb/xproto.h:10574
xcb_poly_point_checked = _lib.xcb_poly_point_checked
xcb_poly_point_checked.restype = xcb_void_cookie_t
xcb_poly_point_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_drawable_t, xcb_gcontext_t, c_uint32, POINTER(xcb_point_t)]

# /usr/include/xcb/xproto.h:10605
xcb_poly_point = _lib.xcb_poly_point
xcb_poly_point.restype = xcb_void_cookie_t
xcb_poly_point.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_drawable_t, xcb_gcontext_t, c_uint32, POINTER(xcb_point_t)]

# /usr/include/xcb/xproto.h:10639
xcb_poly_line_checked = _lib.xcb_poly_line_checked
xcb_poly_line_checked.restype = xcb_void_cookie_t
xcb_poly_line_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_drawable_t, xcb_gcontext_t, c_uint32, POINTER(xcb_point_t)]

# /usr/include/xcb/xproto.h:10670
xcb_poly_line = _lib.xcb_poly_line
xcb_poly_line.restype = xcb_void_cookie_t
xcb_poly_line.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_drawable_t, xcb_gcontext_t, c_uint32, POINTER(xcb_point_t)]

# /usr/include/xcb/xproto.h:10696
xcb_segment_next = _lib.xcb_segment_next
xcb_segment_next.restype = None
xcb_segment_next.argtypes = [POINTER(xcb_segment_iterator_t)]

# /usr/include/xcb/xproto.h:10718
xcb_segment_end = _lib.xcb_segment_end
xcb_segment_end.restype = xcb_generic_iterator_t
xcb_segment_end.argtypes = [xcb_segment_iterator_t]

# /usr/include/xcb/xproto.h:10746
xcb_poly_segment_checked = _lib.xcb_poly_segment_checked
xcb_poly_segment_checked.restype = xcb_void_cookie_t
xcb_poly_segment_checked.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_gcontext_t, c_uint32, POINTER(xcb_segment_t)]

# /usr/include/xcb/xproto.h:10775
xcb_poly_segment = _lib.xcb_poly_segment
xcb_poly_segment.restype = xcb_void_cookie_t
xcb_poly_segment.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_gcontext_t, c_uint32, POINTER(xcb_segment_t)]

# /usr/include/xcb/xproto.h:10807
xcb_poly_rectangle_checked = _lib.xcb_poly_rectangle_checked
xcb_poly_rectangle_checked.restype = xcb_void_cookie_t
xcb_poly_rectangle_checked.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_gcontext_t, c_uint32, POINTER(xcb_rectangle_t)]

# /usr/include/xcb/xproto.h:10836
xcb_poly_rectangle = _lib.xcb_poly_rectangle
xcb_poly_rectangle.restype = xcb_void_cookie_t
xcb_poly_rectangle.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_gcontext_t, c_uint32, POINTER(xcb_rectangle_t)]

# /usr/include/xcb/xproto.h:10868
xcb_poly_arc_checked = _lib.xcb_poly_arc_checked
xcb_poly_arc_checked.restype = xcb_void_cookie_t
xcb_poly_arc_checked.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_gcontext_t, c_uint32, POINTER(xcb_arc_t)]

# /usr/include/xcb/xproto.h:10897
xcb_poly_arc = _lib.xcb_poly_arc
xcb_poly_arc.restype = xcb_void_cookie_t
xcb_poly_arc.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_gcontext_t, c_uint32, POINTER(xcb_arc_t)]

# /usr/include/xcb/xproto.h:10931
xcb_fill_poly_checked = _lib.xcb_fill_poly_checked
xcb_fill_poly_checked.restype = xcb_void_cookie_t
xcb_fill_poly_checked.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_gcontext_t, c_uint8, c_uint8, c_uint32, POINTER(xcb_point_t)]

# /usr/include/xcb/xproto.h:10964
xcb_fill_poly = _lib.xcb_fill_poly
xcb_fill_poly.restype = xcb_void_cookie_t
xcb_fill_poly.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_gcontext_t, c_uint8, c_uint8, c_uint32, POINTER(xcb_point_t)]

# /usr/include/xcb/xproto.h:10998
xcb_poly_fill_rectangle_checked = _lib.xcb_poly_fill_rectangle_checked
xcb_poly_fill_rectangle_checked.restype = xcb_void_cookie_t
xcb_poly_fill_rectangle_checked.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_gcontext_t, c_uint32, POINTER(xcb_rectangle_t)]

# /usr/include/xcb/xproto.h:11027
xcb_poly_fill_rectangle = _lib.xcb_poly_fill_rectangle
xcb_poly_fill_rectangle.restype = xcb_void_cookie_t
xcb_poly_fill_rectangle.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_gcontext_t, c_uint32, POINTER(xcb_rectangle_t)]

# /usr/include/xcb/xproto.h:11059
xcb_poly_fill_arc_checked = _lib.xcb_poly_fill_arc_checked
xcb_poly_fill_arc_checked.restype = xcb_void_cookie_t
xcb_poly_fill_arc_checked.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_gcontext_t, c_uint32, POINTER(xcb_arc_t)]

# /usr/include/xcb/xproto.h:11088
xcb_poly_fill_arc = _lib.xcb_poly_fill_arc
xcb_poly_fill_arc.restype = xcb_void_cookie_t
xcb_poly_fill_arc.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_gcontext_t, c_uint32, POINTER(xcb_arc_t)]

# /usr/include/xcb/xproto.h:11127
xcb_put_image_checked = _lib.xcb_put_image_checked
xcb_put_image_checked.restype = xcb_void_cookie_t
xcb_put_image_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_drawable_t, xcb_gcontext_t, c_uint16, c_uint16, c_int16, c_int16, c_uint8, c_uint8, c_uint32, POINTER(c_uint8)]

# /usr/include/xcb/xproto.h:11170
xcb_put_image = _lib.xcb_put_image
xcb_put_image.restype = xcb_void_cookie_t
xcb_put_image.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_drawable_t, xcb_gcontext_t, c_uint16, c_uint16, c_int16, c_int16, c_uint8, c_uint8, c_uint32, POINTER(c_uint8)]

# /usr/include/xcb/xproto.h:11209
xcb_get_image = _lib.xcb_get_image
xcb_get_image.restype = xcb_get_image_cookie_t
xcb_get_image.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_drawable_t, c_int16, c_int16, c_uint16, c_uint16, c_uint32]

# /usr/include/xcb/xproto.h:11247
xcb_get_image_unchecked = _lib.xcb_get_image_unchecked
xcb_get_image_unchecked.restype = xcb_get_image_cookie_t
xcb_get_image_unchecked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_drawable_t, c_int16, c_int16, c_uint16, c_uint16, c_uint32]

# /usr/include/xcb/xproto.h:11266
xcb_get_image_data = _lib.xcb_get_image_data
xcb_get_image_data.restype = POINTER(c_uint8)
xcb_get_image_data.argtypes = [POINTER(xcb_get_image_reply_t)]

# /usr/include/xcb/xproto.h:11280
xcb_get_image_data_length = _lib.xcb_get_image_data_length
xcb_get_image_data_length.restype = c_int
xcb_get_image_data_length.argtypes = [POINTER(xcb_get_image_reply_t)]

# /usr/include/xcb/xproto.h:11293
xcb_get_image_data_end = _lib.xcb_get_image_data_end
xcb_get_image_data_end.restype = xcb_generic_iterator_t
xcb_get_image_data_end.argtypes = [POINTER(xcb_get_image_reply_t)]

# /usr/include/xcb/xproto.h:11319
xcb_get_image_reply = _lib.xcb_get_image_reply
xcb_get_image_reply.restype = POINTER(xcb_get_image_reply_t)
xcb_get_image_reply.argtypes = [POINTER(xcb_connection_t), xcb_get_image_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:11352
xcb_poly_text_8_checked = _lib.xcb_poly_text_8_checked
xcb_poly_text_8_checked.restype = xcb_void_cookie_t
xcb_poly_text_8_checked.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_gcontext_t, c_int16, c_int16, c_uint32, POINTER(c_uint8)]

# /usr/include/xcb/xproto.h:11385
xcb_poly_text_8 = _lib.xcb_poly_text_8
xcb_poly_text_8.restype = xcb_void_cookie_t
xcb_poly_text_8.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_gcontext_t, c_int16, c_int16, c_uint32, POINTER(c_uint8)]

# /usr/include/xcb/xproto.h:11421
xcb_poly_text_16_checked = _lib.xcb_poly_text_16_checked
xcb_poly_text_16_checked.restype = xcb_void_cookie_t
xcb_poly_text_16_checked.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_gcontext_t, c_int16, c_int16, c_uint32, POINTER(c_uint8)]

# /usr/include/xcb/xproto.h:11454
xcb_poly_text_16 = _lib.xcb_poly_text_16
xcb_poly_text_16.restype = xcb_void_cookie_t
xcb_poly_text_16.argtypes = [POINTER(xcb_connection_t), xcb_drawable_t, xcb_gcontext_t, c_int16, c_int16, c_uint32, POINTER(c_uint8)]

# /usr/include/xcb/xproto.h:11490
xcb_image_text_8_checked = _lib.xcb_image_text_8_checked
xcb_image_text_8_checked.restype = xcb_void_cookie_t
xcb_image_text_8_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_drawable_t, xcb_gcontext_t, c_int16, c_int16, c_char_p]

# /usr/include/xcb/xproto.h:11523
xcb_image_text_8 = _lib.xcb_image_text_8
xcb_image_text_8.restype = xcb_void_cookie_t
xcb_image_text_8.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_drawable_t, xcb_gcontext_t, c_int16, c_int16, c_char_p]

# /usr/include/xcb/xproto.h:11559
xcb_image_text_16_checked = _lib.xcb_image_text_16_checked
xcb_image_text_16_checked.restype = xcb_void_cookie_t
xcb_image_text_16_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_drawable_t, xcb_gcontext_t, c_int16, c_int16, POINTER(xcb_char2b_t)]

# /usr/include/xcb/xproto.h:11592
xcb_image_text_16 = _lib.xcb_image_text_16
xcb_image_text_16.restype = xcb_void_cookie_t
xcb_image_text_16.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_drawable_t, xcb_gcontext_t, c_int16, c_int16, POINTER(xcb_char2b_t)]

# /usr/include/xcb/xproto.h:11626
xcb_create_colormap_checked = _lib.xcb_create_colormap_checked
xcb_create_colormap_checked.restype = xcb_void_cookie_t
xcb_create_colormap_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_colormap_t, xcb_window_t, xcb_visualid_t]

# /usr/include/xcb/xproto.h:11655
xcb_create_colormap = _lib.xcb_create_colormap
xcb_create_colormap.restype = xcb_void_cookie_t
xcb_create_colormap.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_colormap_t, xcb_window_t, xcb_visualid_t]

# /usr/include/xcb/xproto.h:11684
xcb_free_colormap_checked = _lib.xcb_free_colormap_checked
xcb_free_colormap_checked.restype = xcb_void_cookie_t
xcb_free_colormap_checked.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t]

# /usr/include/xcb/xproto.h:11707
xcb_free_colormap = _lib.xcb_free_colormap
xcb_free_colormap.restype = xcb_void_cookie_t
xcb_free_colormap.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t]

# /usr/include/xcb/xproto.h:11734
xcb_copy_colormap_and_free_checked = _lib.xcb_copy_colormap_and_free_checked
xcb_copy_colormap_and_free_checked.restype = xcb_void_cookie_t
xcb_copy_colormap_and_free_checked.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t, xcb_colormap_t]

# /usr/include/xcb/xproto.h:11759
xcb_copy_colormap_and_free = _lib.xcb_copy_colormap_and_free
xcb_copy_colormap_and_free.restype = xcb_void_cookie_t
xcb_copy_colormap_and_free.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t, xcb_colormap_t]

# /usr/include/xcb/xproto.h:11786
xcb_install_colormap_checked = _lib.xcb_install_colormap_checked
xcb_install_colormap_checked.restype = xcb_void_cookie_t
xcb_install_colormap_checked.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t]

# /usr/include/xcb/xproto.h:11809
xcb_install_colormap = _lib.xcb_install_colormap
xcb_install_colormap.restype = xcb_void_cookie_t
xcb_install_colormap.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t]

# /usr/include/xcb/xproto.h:11835
xcb_uninstall_colormap_checked = _lib.xcb_uninstall_colormap_checked
xcb_uninstall_colormap_checked.restype = xcb_void_cookie_t
xcb_uninstall_colormap_checked.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t]

# /usr/include/xcb/xproto.h:11858
xcb_uninstall_colormap = _lib.xcb_uninstall_colormap
xcb_uninstall_colormap.restype = xcb_void_cookie_t
xcb_uninstall_colormap.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t]

# /usr/include/xcb/xproto.h:11881
xcb_list_installed_colormaps = _lib.xcb_list_installed_colormaps
xcb_list_installed_colormaps.restype = xcb_list_installed_colormaps_cookie_t
xcb_list_installed_colormaps.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:11907
xcb_list_installed_colormaps_unchecked = _lib.xcb_list_installed_colormaps_unchecked
xcb_list_installed_colormaps_unchecked.restype = xcb_list_installed_colormaps_cookie_t
xcb_list_installed_colormaps_unchecked.argtypes = [POINTER(xcb_connection_t), xcb_window_t]

# /usr/include/xcb/xproto.h:11920
xcb_list_installed_colormaps_cmaps = _lib.xcb_list_installed_colormaps_cmaps
xcb_list_installed_colormaps_cmaps.restype = POINTER(xcb_colormap_t)
xcb_list_installed_colormaps_cmaps.argtypes = [POINTER(xcb_list_installed_colormaps_reply_t)]

# /usr/include/xcb/xproto.h:11934
xcb_list_installed_colormaps_cmaps_length = _lib.xcb_list_installed_colormaps_cmaps_length
xcb_list_installed_colormaps_cmaps_length.restype = c_int
xcb_list_installed_colormaps_cmaps_length.argtypes = [POINTER(xcb_list_installed_colormaps_reply_t)]

# /usr/include/xcb/xproto.h:11947
xcb_list_installed_colormaps_cmaps_iterator = _lib.xcb_list_installed_colormaps_cmaps_iterator
xcb_list_installed_colormaps_cmaps_iterator.restype = xcb_colormap_iterator_t
xcb_list_installed_colormaps_cmaps_iterator.argtypes = [POINTER(xcb_list_installed_colormaps_reply_t)]

# /usr/include/xcb/xproto.h:11973
xcb_list_installed_colormaps_reply = _lib.xcb_list_installed_colormaps_reply
xcb_list_installed_colormaps_reply.restype = POINTER(xcb_list_installed_colormaps_reply_t)
xcb_list_installed_colormaps_reply.argtypes = [POINTER(xcb_connection_t), xcb_list_installed_colormaps_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:12001
xcb_alloc_color = _lib.xcb_alloc_color
xcb_alloc_color.restype = xcb_alloc_color_cookie_t
xcb_alloc_color.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t, c_uint16, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:12033
xcb_alloc_color_unchecked = _lib.xcb_alloc_color_unchecked
xcb_alloc_color_unchecked.restype = xcb_alloc_color_cookie_t
xcb_alloc_color_unchecked.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t, c_uint16, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:12063
xcb_alloc_color_reply = _lib.xcb_alloc_color_reply
xcb_alloc_color_reply.restype = POINTER(xcb_alloc_color_reply_t)
xcb_alloc_color_reply.argtypes = [POINTER(xcb_connection_t), xcb_alloc_color_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:12090
xcb_alloc_named_color = _lib.xcb_alloc_named_color
xcb_alloc_named_color.restype = xcb_alloc_named_color_cookie_t
xcb_alloc_named_color.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t, c_uint16, c_char_p]

# /usr/include/xcb/xproto.h:12120
xcb_alloc_named_color_unchecked = _lib.xcb_alloc_named_color_unchecked
xcb_alloc_named_color_unchecked.restype = xcb_alloc_named_color_cookie_t
xcb_alloc_named_color_unchecked.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t, c_uint16, c_char_p]

# /usr/include/xcb/xproto.h:12149
xcb_alloc_named_color_reply = _lib.xcb_alloc_named_color_reply
xcb_alloc_named_color_reply.restype = POINTER(xcb_alloc_named_color_reply_t)
xcb_alloc_named_color_reply.argtypes = [POINTER(xcb_connection_t), xcb_alloc_named_color_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:12177
xcb_alloc_color_cells = _lib.xcb_alloc_color_cells
xcb_alloc_color_cells.restype = xcb_alloc_color_cells_cookie_t
xcb_alloc_color_cells.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_colormap_t, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:12209
xcb_alloc_color_cells_unchecked = _lib.xcb_alloc_color_cells_unchecked
xcb_alloc_color_cells_unchecked.restype = xcb_alloc_color_cells_cookie_t
xcb_alloc_color_cells_unchecked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_colormap_t, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:12225
xcb_alloc_color_cells_pixels = _lib.xcb_alloc_color_cells_pixels
xcb_alloc_color_cells_pixels.restype = POINTER(c_uint32)
xcb_alloc_color_cells_pixels.argtypes = [POINTER(xcb_alloc_color_cells_reply_t)]

# /usr/include/xcb/xproto.h:12239
xcb_alloc_color_cells_pixels_length = _lib.xcb_alloc_color_cells_pixels_length
xcb_alloc_color_cells_pixels_length.restype = c_int
xcb_alloc_color_cells_pixels_length.argtypes = [POINTER(xcb_alloc_color_cells_reply_t)]

# /usr/include/xcb/xproto.h:12252
xcb_alloc_color_cells_pixels_end = _lib.xcb_alloc_color_cells_pixels_end
xcb_alloc_color_cells_pixels_end.restype = xcb_generic_iterator_t
xcb_alloc_color_cells_pixels_end.argtypes = [POINTER(xcb_alloc_color_cells_reply_t)]

# /usr/include/xcb/xproto.h:12264
xcb_alloc_color_cells_masks = _lib.xcb_alloc_color_cells_masks
xcb_alloc_color_cells_masks.restype = POINTER(c_uint32)
xcb_alloc_color_cells_masks.argtypes = [POINTER(xcb_alloc_color_cells_reply_t)]

# /usr/include/xcb/xproto.h:12278
xcb_alloc_color_cells_masks_length = _lib.xcb_alloc_color_cells_masks_length
xcb_alloc_color_cells_masks_length.restype = c_int
xcb_alloc_color_cells_masks_length.argtypes = [POINTER(xcb_alloc_color_cells_reply_t)]

# /usr/include/xcb/xproto.h:12291
xcb_alloc_color_cells_masks_end = _lib.xcb_alloc_color_cells_masks_end
xcb_alloc_color_cells_masks_end.restype = xcb_generic_iterator_t
xcb_alloc_color_cells_masks_end.argtypes = [POINTER(xcb_alloc_color_cells_reply_t)]

# /usr/include/xcb/xproto.h:12317
xcb_alloc_color_cells_reply = _lib.xcb_alloc_color_cells_reply
xcb_alloc_color_cells_reply.restype = POINTER(xcb_alloc_color_cells_reply_t)
xcb_alloc_color_cells_reply.argtypes = [POINTER(xcb_connection_t), xcb_alloc_color_cells_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:12347
xcb_alloc_color_planes = _lib.xcb_alloc_color_planes
xcb_alloc_color_planes.restype = xcb_alloc_color_planes_cookie_t
xcb_alloc_color_planes.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_colormap_t, c_uint16, c_uint16, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:12383
xcb_alloc_color_planes_unchecked = _lib.xcb_alloc_color_planes_unchecked
xcb_alloc_color_planes_unchecked.restype = xcb_alloc_color_planes_cookie_t
xcb_alloc_color_planes_unchecked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_colormap_t, c_uint16, c_uint16, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:12401
xcb_alloc_color_planes_pixels = _lib.xcb_alloc_color_planes_pixels
xcb_alloc_color_planes_pixels.restype = POINTER(c_uint32)
xcb_alloc_color_planes_pixels.argtypes = [POINTER(xcb_alloc_color_planes_reply_t)]

# /usr/include/xcb/xproto.h:12415
xcb_alloc_color_planes_pixels_length = _lib.xcb_alloc_color_planes_pixels_length
xcb_alloc_color_planes_pixels_length.restype = c_int
xcb_alloc_color_planes_pixels_length.argtypes = [POINTER(xcb_alloc_color_planes_reply_t)]

# /usr/include/xcb/xproto.h:12428
xcb_alloc_color_planes_pixels_end = _lib.xcb_alloc_color_planes_pixels_end
xcb_alloc_color_planes_pixels_end.restype = xcb_generic_iterator_t
xcb_alloc_color_planes_pixels_end.argtypes = [POINTER(xcb_alloc_color_planes_reply_t)]

# /usr/include/xcb/xproto.h:12454
xcb_alloc_color_planes_reply = _lib.xcb_alloc_color_planes_reply
xcb_alloc_color_planes_reply.restype = POINTER(xcb_alloc_color_planes_reply_t)
xcb_alloc_color_planes_reply.argtypes = [POINTER(xcb_connection_t), xcb_alloc_color_planes_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:12485
xcb_free_colors_checked = _lib.xcb_free_colors_checked
xcb_free_colors_checked.restype = xcb_void_cookie_t
xcb_free_colors_checked.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t, c_uint32, c_uint32, POINTER(c_uint32)]

# /usr/include/xcb/xproto.h:12514
xcb_free_colors = _lib.xcb_free_colors
xcb_free_colors.restype = xcb_void_cookie_t
xcb_free_colors.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t, c_uint32, c_uint32, POINTER(c_uint32)]

# /usr/include/xcb/xproto.h:12539
xcb_coloritem_next = _lib.xcb_coloritem_next
xcb_coloritem_next.restype = None
xcb_coloritem_next.argtypes = [POINTER(xcb_coloritem_iterator_t)]

# /usr/include/xcb/xproto.h:12561
xcb_coloritem_end = _lib.xcb_coloritem_end
xcb_coloritem_end.restype = xcb_generic_iterator_t
xcb_coloritem_end.argtypes = [xcb_coloritem_iterator_t]

# /usr/include/xcb/xproto.h:12588
xcb_store_colors_checked = _lib.xcb_store_colors_checked
xcb_store_colors_checked.restype = xcb_void_cookie_t
xcb_store_colors_checked.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t, c_uint32, POINTER(xcb_coloritem_t)]

# /usr/include/xcb/xproto.h:12615
xcb_store_colors = _lib.xcb_store_colors
xcb_store_colors.restype = xcb_void_cookie_t
xcb_store_colors.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t, c_uint32, POINTER(xcb_coloritem_t)]

# /usr/include/xcb/xproto.h:12647
xcb_store_named_color_checked = _lib.xcb_store_named_color_checked
xcb_store_named_color_checked.restype = xcb_void_cookie_t
xcb_store_named_color_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_colormap_t, c_uint32, c_uint16, c_char_p]

# /usr/include/xcb/xproto.h:12678
xcb_store_named_color = _lib.xcb_store_named_color
xcb_store_named_color.restype = xcb_void_cookie_t
xcb_store_named_color.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_colormap_t, c_uint32, c_uint16, c_char_p]

# /usr/include/xcb/xproto.h:12704
xcb_rgb_next = _lib.xcb_rgb_next
xcb_rgb_next.restype = None
xcb_rgb_next.argtypes = [POINTER(xcb_rgb_iterator_t)]

# /usr/include/xcb/xproto.h:12726
xcb_rgb_end = _lib.xcb_rgb_end
xcb_rgb_end.restype = xcb_generic_iterator_t
xcb_rgb_end.argtypes = [xcb_rgb_iterator_t]

# /usr/include/xcb/xproto.h:12750
xcb_query_colors = _lib.xcb_query_colors
xcb_query_colors.restype = xcb_query_colors_cookie_t
xcb_query_colors.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t, c_uint32, POINTER(c_uint32)]

# /usr/include/xcb/xproto.h:12780
xcb_query_colors_unchecked = _lib.xcb_query_colors_unchecked
xcb_query_colors_unchecked.restype = xcb_query_colors_cookie_t
xcb_query_colors_unchecked.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t, c_uint32, POINTER(c_uint32)]

# /usr/include/xcb/xproto.h:12795
xcb_query_colors_colors = _lib.xcb_query_colors_colors
xcb_query_colors_colors.restype = POINTER(xcb_rgb_t)
xcb_query_colors_colors.argtypes = [POINTER(xcb_query_colors_reply_t)]

# /usr/include/xcb/xproto.h:12809
xcb_query_colors_colors_length = _lib.xcb_query_colors_colors_length
xcb_query_colors_colors_length.restype = c_int
xcb_query_colors_colors_length.argtypes = [POINTER(xcb_query_colors_reply_t)]

# /usr/include/xcb/xproto.h:12822
xcb_query_colors_colors_iterator = _lib.xcb_query_colors_colors_iterator
xcb_query_colors_colors_iterator.restype = xcb_rgb_iterator_t
xcb_query_colors_colors_iterator.argtypes = [POINTER(xcb_query_colors_reply_t)]

# /usr/include/xcb/xproto.h:12848
xcb_query_colors_reply = _lib.xcb_query_colors_reply
xcb_query_colors_reply.restype = POINTER(xcb_query_colors_reply_t)
xcb_query_colors_reply.argtypes = [POINTER(xcb_connection_t), xcb_query_colors_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:12875
xcb_lookup_color = _lib.xcb_lookup_color
xcb_lookup_color.restype = xcb_lookup_color_cookie_t
xcb_lookup_color.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t, c_uint16, c_char_p]

# /usr/include/xcb/xproto.h:12905
xcb_lookup_color_unchecked = _lib.xcb_lookup_color_unchecked
xcb_lookup_color_unchecked.restype = xcb_lookup_color_cookie_t
xcb_lookup_color_unchecked.argtypes = [POINTER(xcb_connection_t), xcb_colormap_t, c_uint16, c_char_p]

# /usr/include/xcb/xproto.h:12934
xcb_lookup_color_reply = _lib.xcb_lookup_color_reply
xcb_lookup_color_reply.restype = POINTER(xcb_lookup_color_reply_t)
xcb_lookup_color_reply.argtypes = [POINTER(xcb_connection_t), xcb_lookup_color_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:12972
xcb_create_cursor_checked = _lib.xcb_create_cursor_checked
xcb_create_cursor_checked.restype = xcb_void_cookie_t
xcb_create_cursor_checked.argtypes = [POINTER(xcb_connection_t), xcb_cursor_t, xcb_pixmap_t, xcb_pixmap_t, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:13015
xcb_create_cursor = _lib.xcb_create_cursor
xcb_create_cursor.restype = xcb_void_cookie_t
xcb_create_cursor.argtypes = [POINTER(xcb_connection_t), xcb_cursor_t, xcb_pixmap_t, xcb_pixmap_t, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:13061
xcb_create_glyph_cursor_checked = _lib.xcb_create_glyph_cursor_checked
xcb_create_glyph_cursor_checked.restype = xcb_void_cookie_t
xcb_create_glyph_cursor_checked.argtypes = [POINTER(xcb_connection_t), xcb_cursor_t, xcb_font_t, xcb_font_t, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:13104
xcb_create_glyph_cursor = _lib.xcb_create_glyph_cursor
xcb_create_glyph_cursor.restype = xcb_void_cookie_t
xcb_create_glyph_cursor.argtypes = [POINTER(xcb_connection_t), xcb_cursor_t, xcb_font_t, xcb_font_t, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:13140
xcb_free_cursor_checked = _lib.xcb_free_cursor_checked
xcb_free_cursor_checked.restype = xcb_void_cookie_t
xcb_free_cursor_checked.argtypes = [POINTER(xcb_connection_t), xcb_cursor_t]

# /usr/include/xcb/xproto.h:13163
xcb_free_cursor = _lib.xcb_free_cursor
xcb_free_cursor.restype = xcb_void_cookie_t
xcb_free_cursor.argtypes = [POINTER(xcb_connection_t), xcb_cursor_t]

# /usr/include/xcb/xproto.h:13195
xcb_recolor_cursor_checked = _lib.xcb_recolor_cursor_checked
xcb_recolor_cursor_checked.restype = xcb_void_cookie_t
xcb_recolor_cursor_checked.argtypes = [POINTER(xcb_connection_t), xcb_cursor_t, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:13230
xcb_recolor_cursor = _lib.xcb_recolor_cursor
xcb_recolor_cursor.restype = xcb_void_cookie_t
xcb_recolor_cursor.argtypes = [POINTER(xcb_connection_t), xcb_cursor_t, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:13262
xcb_query_best_size = _lib.xcb_query_best_size
xcb_query_best_size.restype = xcb_query_best_size_cookie_t
xcb_query_best_size.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_drawable_t, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:13294
xcb_query_best_size_unchecked = _lib.xcb_query_best_size_unchecked
xcb_query_best_size_unchecked.restype = xcb_query_best_size_cookie_t
xcb_query_best_size_unchecked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_drawable_t, c_uint16, c_uint16]

# /usr/include/xcb/xproto.h:13324
xcb_query_best_size_reply = _lib.xcb_query_best_size_reply
xcb_query_best_size_reply.restype = POINTER(xcb_query_best_size_reply_t)
xcb_query_best_size_reply.argtypes = [POINTER(xcb_connection_t), xcb_query_best_size_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:13350
xcb_query_extension = _lib.xcb_query_extension
xcb_query_extension.restype = xcb_query_extension_cookie_t
xcb_query_extension.argtypes = [POINTER(xcb_connection_t), c_uint16, c_char_p]

# /usr/include/xcb/xproto.h:13378
xcb_query_extension_unchecked = _lib.xcb_query_extension_unchecked
xcb_query_extension_unchecked.restype = xcb_query_extension_cookie_t
xcb_query_extension_unchecked.argtypes = [POINTER(xcb_connection_t), c_uint16, c_char_p]

# /usr/include/xcb/xproto.h:13406
xcb_query_extension_reply = _lib.xcb_query_extension_reply
xcb_query_extension_reply.restype = POINTER(xcb_query_extension_reply_t)
xcb_query_extension_reply.argtypes = [POINTER(xcb_connection_t), xcb_query_extension_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:13430
xcb_list_extensions = _lib.xcb_list_extensions
xcb_list_extensions.restype = xcb_list_extensions_cookie_t
xcb_list_extensions.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:13454
xcb_list_extensions_unchecked = _lib.xcb_list_extensions_unchecked
xcb_list_extensions_unchecked.restype = xcb_list_extensions_cookie_t
xcb_list_extensions_unchecked.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:13467
xcb_list_extensions_names_length = _lib.xcb_list_extensions_names_length
xcb_list_extensions_names_length.restype = c_int
xcb_list_extensions_names_length.argtypes = [POINTER(xcb_list_extensions_reply_t)]

# /usr/include/xcb/xproto.h:13480
xcb_list_extensions_names_iterator = _lib.xcb_list_extensions_names_iterator
xcb_list_extensions_names_iterator.restype = xcb_str_iterator_t
xcb_list_extensions_names_iterator.argtypes = [POINTER(xcb_list_extensions_reply_t)]

# /usr/include/xcb/xproto.h:13506
xcb_list_extensions_reply = _lib.xcb_list_extensions_reply
xcb_list_extensions_reply.restype = POINTER(xcb_list_extensions_reply_t)
xcb_list_extensions_reply.argtypes = [POINTER(xcb_connection_t), xcb_list_extensions_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:13537
xcb_change_keyboard_mapping_checked = _lib.xcb_change_keyboard_mapping_checked
xcb_change_keyboard_mapping_checked.restype = xcb_void_cookie_t
xcb_change_keyboard_mapping_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_keycode_t, c_uint8, POINTER(xcb_keysym_t)]

# /usr/include/xcb/xproto.h:13566
xcb_change_keyboard_mapping = _lib.xcb_change_keyboard_mapping
xcb_change_keyboard_mapping.restype = xcb_void_cookie_t
xcb_change_keyboard_mapping.argtypes = [POINTER(xcb_connection_t), c_uint8, xcb_keycode_t, c_uint8, POINTER(xcb_keysym_t)]

# /usr/include/xcb/xproto.h:13593
xcb_get_keyboard_mapping = _lib.xcb_get_keyboard_mapping
xcb_get_keyboard_mapping.restype = xcb_get_keyboard_mapping_cookie_t
xcb_get_keyboard_mapping.argtypes = [POINTER(xcb_connection_t), xcb_keycode_t, c_uint8]

# /usr/include/xcb/xproto.h:13621
xcb_get_keyboard_mapping_unchecked = _lib.xcb_get_keyboard_mapping_unchecked
xcb_get_keyboard_mapping_unchecked.restype = xcb_get_keyboard_mapping_cookie_t
xcb_get_keyboard_mapping_unchecked.argtypes = [POINTER(xcb_connection_t), xcb_keycode_t, c_uint8]

# /usr/include/xcb/xproto.h:13635
xcb_get_keyboard_mapping_keysyms = _lib.xcb_get_keyboard_mapping_keysyms
xcb_get_keyboard_mapping_keysyms.restype = POINTER(xcb_keysym_t)
xcb_get_keyboard_mapping_keysyms.argtypes = [POINTER(xcb_get_keyboard_mapping_reply_t)]

# /usr/include/xcb/xproto.h:13649
xcb_get_keyboard_mapping_keysyms_length = _lib.xcb_get_keyboard_mapping_keysyms_length
xcb_get_keyboard_mapping_keysyms_length.restype = c_int
xcb_get_keyboard_mapping_keysyms_length.argtypes = [POINTER(xcb_get_keyboard_mapping_reply_t)]

# /usr/include/xcb/xproto.h:13662
xcb_get_keyboard_mapping_keysyms_iterator = _lib.xcb_get_keyboard_mapping_keysyms_iterator
xcb_get_keyboard_mapping_keysyms_iterator.restype = xcb_keysym_iterator_t
xcb_get_keyboard_mapping_keysyms_iterator.argtypes = [POINTER(xcb_get_keyboard_mapping_reply_t)]

# /usr/include/xcb/xproto.h:13688
xcb_get_keyboard_mapping_reply = _lib.xcb_get_keyboard_mapping_reply
xcb_get_keyboard_mapping_reply.restype = POINTER(xcb_get_keyboard_mapping_reply_t)
xcb_get_keyboard_mapping_reply.argtypes = [POINTER(xcb_connection_t), xcb_get_keyboard_mapping_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:13717
xcb_change_keyboard_control_checked = _lib.xcb_change_keyboard_control_checked
xcb_change_keyboard_control_checked.restype = xcb_void_cookie_t
xcb_change_keyboard_control_checked.argtypes = [POINTER(xcb_connection_t), c_uint32, POINTER(c_uint32)]

# /usr/include/xcb/xproto.h:13742
xcb_change_keyboard_control = _lib.xcb_change_keyboard_control
xcb_change_keyboard_control.restype = xcb_void_cookie_t
xcb_change_keyboard_control.argtypes = [POINTER(xcb_connection_t), c_uint32, POINTER(c_uint32)]

# /usr/include/xcb/xproto.h:13765
xcb_get_keyboard_control = _lib.xcb_get_keyboard_control
xcb_get_keyboard_control.restype = xcb_get_keyboard_control_cookie_t
xcb_get_keyboard_control.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:13789
xcb_get_keyboard_control_unchecked = _lib.xcb_get_keyboard_control_unchecked
xcb_get_keyboard_control_unchecked.restype = xcb_get_keyboard_control_cookie_t
xcb_get_keyboard_control_unchecked.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:13815
xcb_get_keyboard_control_reply = _lib.xcb_get_keyboard_control_reply
xcb_get_keyboard_control_reply.restype = POINTER(xcb_get_keyboard_control_reply_t)
xcb_get_keyboard_control_reply.argtypes = [POINTER(xcb_connection_t), xcb_get_keyboard_control_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:13843
xcb_bell_checked = _lib.xcb_bell_checked
xcb_bell_checked.restype = xcb_void_cookie_t
xcb_bell_checked.argtypes = [POINTER(xcb_connection_t), c_int8]

# /usr/include/xcb/xproto.h:13866
xcb_bell = _lib.xcb_bell
xcb_bell.restype = xcb_void_cookie_t
xcb_bell.argtypes = [POINTER(xcb_connection_t), c_int8]

# /usr/include/xcb/xproto.h:13896
xcb_change_pointer_control_checked = _lib.xcb_change_pointer_control_checked
xcb_change_pointer_control_checked.restype = xcb_void_cookie_t
xcb_change_pointer_control_checked.argtypes = [POINTER(xcb_connection_t), c_int16, c_int16, c_int16, c_uint8, c_uint8]

# /usr/include/xcb/xproto.h:13927
xcb_change_pointer_control = _lib.xcb_change_pointer_control
xcb_change_pointer_control.restype = xcb_void_cookie_t
xcb_change_pointer_control.argtypes = [POINTER(xcb_connection_t), c_int16, c_int16, c_int16, c_uint8, c_uint8]

# /usr/include/xcb/xproto.h:13953
xcb_get_pointer_control = _lib.xcb_get_pointer_control
xcb_get_pointer_control.restype = xcb_get_pointer_control_cookie_t
xcb_get_pointer_control.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:13977
xcb_get_pointer_control_unchecked = _lib.xcb_get_pointer_control_unchecked
xcb_get_pointer_control_unchecked.restype = xcb_get_pointer_control_cookie_t
xcb_get_pointer_control_unchecked.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:14003
xcb_get_pointer_control_reply = _lib.xcb_get_pointer_control_reply
xcb_get_pointer_control_reply.restype = POINTER(xcb_get_pointer_control_reply_t)
xcb_get_pointer_control_reply.argtypes = [POINTER(xcb_connection_t), xcb_get_pointer_control_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:14034
xcb_set_screen_saver_checked = _lib.xcb_set_screen_saver_checked
xcb_set_screen_saver_checked.restype = xcb_void_cookie_t
xcb_set_screen_saver_checked.argtypes = [POINTER(xcb_connection_t), c_int16, c_int16, c_uint8, c_uint8]

# /usr/include/xcb/xproto.h:14063
xcb_set_screen_saver = _lib.xcb_set_screen_saver
xcb_set_screen_saver.restype = xcb_void_cookie_t
xcb_set_screen_saver.argtypes = [POINTER(xcb_connection_t), c_int16, c_int16, c_uint8, c_uint8]

# /usr/include/xcb/xproto.h:14088
xcb_get_screen_saver = _lib.xcb_get_screen_saver
xcb_get_screen_saver.restype = xcb_get_screen_saver_cookie_t
xcb_get_screen_saver.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:14112
xcb_get_screen_saver_unchecked = _lib.xcb_get_screen_saver_unchecked
xcb_get_screen_saver_unchecked.restype = xcb_get_screen_saver_cookie_t
xcb_get_screen_saver_unchecked.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:14138
xcb_get_screen_saver_reply = _lib.xcb_get_screen_saver_reply
xcb_get_screen_saver_reply.restype = POINTER(xcb_get_screen_saver_reply_t)
xcb_get_screen_saver_reply.argtypes = [POINTER(xcb_connection_t), xcb_get_screen_saver_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:14169
xcb_change_hosts_checked = _lib.xcb_change_hosts_checked
xcb_change_hosts_checked.restype = xcb_void_cookie_t
xcb_change_hosts_checked.argtypes = [POINTER(xcb_connection_t), c_uint8, c_uint8, c_uint16, c_char_p]

# /usr/include/xcb/xproto.h:14198
xcb_change_hosts = _lib.xcb_change_hosts
xcb_change_hosts.restype = xcb_void_cookie_t
xcb_change_hosts.argtypes = [POINTER(xcb_connection_t), c_uint8, c_uint8, c_uint16, c_char_p]

# /usr/include/xcb/xproto.h:14214
xcb_host_address = _lib.xcb_host_address
xcb_host_address.restype = POINTER(c_uint8)
xcb_host_address.argtypes = [POINTER(xcb_host_t)]

# /usr/include/xcb/xproto.h:14228
xcb_host_address_length = _lib.xcb_host_address_length
xcb_host_address_length.restype = c_int
xcb_host_address_length.argtypes = [POINTER(xcb_host_t)]

# /usr/include/xcb/xproto.h:14241
xcb_host_address_end = _lib.xcb_host_address_end
xcb_host_address_end.restype = xcb_generic_iterator_t
xcb_host_address_end.argtypes = [POINTER(xcb_host_t)]

# /usr/include/xcb/xproto.h:14262
xcb_host_next = _lib.xcb_host_next
xcb_host_next.restype = None
xcb_host_next.argtypes = [POINTER(xcb_host_iterator_t)]

# /usr/include/xcb/xproto.h:14284
xcb_host_end = _lib.xcb_host_end
xcb_host_end.restype = xcb_generic_iterator_t
xcb_host_end.argtypes = [xcb_host_iterator_t]

# /usr/include/xcb/xproto.h:14305
xcb_list_hosts = _lib.xcb_list_hosts
xcb_list_hosts.restype = xcb_list_hosts_cookie_t
xcb_list_hosts.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:14329
xcb_list_hosts_unchecked = _lib.xcb_list_hosts_unchecked
xcb_list_hosts_unchecked.restype = xcb_list_hosts_cookie_t
xcb_list_hosts_unchecked.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:14342
xcb_list_hosts_hosts_length = _lib.xcb_list_hosts_hosts_length
xcb_list_hosts_hosts_length.restype = c_int
xcb_list_hosts_hosts_length.argtypes = [POINTER(xcb_list_hosts_reply_t)]

# /usr/include/xcb/xproto.h:14355
xcb_list_hosts_hosts_iterator = _lib.xcb_list_hosts_hosts_iterator
xcb_list_hosts_hosts_iterator.restype = xcb_host_iterator_t
xcb_list_hosts_hosts_iterator.argtypes = [POINTER(xcb_list_hosts_reply_t)]

# /usr/include/xcb/xproto.h:14381
xcb_list_hosts_reply = _lib.xcb_list_hosts_reply
xcb_list_hosts_reply.restype = POINTER(xcb_list_hosts_reply_t)
xcb_list_hosts_reply.argtypes = [POINTER(xcb_connection_t), xcb_list_hosts_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:14409
xcb_set_access_control_checked = _lib.xcb_set_access_control_checked
xcb_set_access_control_checked.restype = xcb_void_cookie_t
xcb_set_access_control_checked.argtypes = [POINTER(xcb_connection_t), c_uint8]

# /usr/include/xcb/xproto.h:14432
xcb_set_access_control = _lib.xcb_set_access_control
xcb_set_access_control.restype = xcb_void_cookie_t
xcb_set_access_control.argtypes = [POINTER(xcb_connection_t), c_uint8]

# /usr/include/xcb/xproto.h:14458
xcb_set_close_down_mode_checked = _lib.xcb_set_close_down_mode_checked
xcb_set_close_down_mode_checked.restype = xcb_void_cookie_t
xcb_set_close_down_mode_checked.argtypes = [POINTER(xcb_connection_t), c_uint8]

# /usr/include/xcb/xproto.h:14481
xcb_set_close_down_mode = _lib.xcb_set_close_down_mode
xcb_set_close_down_mode.restype = xcb_void_cookie_t
xcb_set_close_down_mode.argtypes = [POINTER(xcb_connection_t), c_uint8]

# /usr/include/xcb/xproto.h:14507
xcb_kill_client_checked = _lib.xcb_kill_client_checked
xcb_kill_client_checked.restype = xcb_void_cookie_t
xcb_kill_client_checked.argtypes = [POINTER(xcb_connection_t), c_uint32]

# /usr/include/xcb/xproto.h:14530
xcb_kill_client = _lib.xcb_kill_client
xcb_kill_client.restype = xcb_void_cookie_t
xcb_kill_client.argtypes = [POINTER(xcb_connection_t), c_uint32]

# /usr/include/xcb/xproto.h:14559
xcb_rotate_properties_checked = _lib.xcb_rotate_properties_checked
xcb_rotate_properties_checked.restype = xcb_void_cookie_t
xcb_rotate_properties_checked.argtypes = [POINTER(xcb_connection_t), xcb_window_t, c_uint16, c_int16, POINTER(xcb_atom_t)]

# /usr/include/xcb/xproto.h:14588
xcb_rotate_properties = _lib.xcb_rotate_properties
xcb_rotate_properties.restype = xcb_void_cookie_t
xcb_rotate_properties.argtypes = [POINTER(xcb_connection_t), xcb_window_t, c_uint16, c_int16, POINTER(xcb_atom_t)]

# /usr/include/xcb/xproto.h:14617
xcb_force_screen_saver_checked = _lib.xcb_force_screen_saver_checked
xcb_force_screen_saver_checked.restype = xcb_void_cookie_t
xcb_force_screen_saver_checked.argtypes = [POINTER(xcb_connection_t), c_uint8]

# /usr/include/xcb/xproto.h:14640
xcb_force_screen_saver = _lib.xcb_force_screen_saver
xcb_force_screen_saver.restype = xcb_void_cookie_t
xcb_force_screen_saver.argtypes = [POINTER(xcb_connection_t), c_uint8]

# /usr/include/xcb/xproto.h:14664
xcb_set_pointer_mapping = _lib.xcb_set_pointer_mapping
xcb_set_pointer_mapping.restype = xcb_set_pointer_mapping_cookie_t
xcb_set_pointer_mapping.argtypes = [POINTER(xcb_connection_t), c_uint8, POINTER(c_uint8)]

# /usr/include/xcb/xproto.h:14692
xcb_set_pointer_mapping_unchecked = _lib.xcb_set_pointer_mapping_unchecked
xcb_set_pointer_mapping_unchecked.restype = xcb_set_pointer_mapping_cookie_t
xcb_set_pointer_mapping_unchecked.argtypes = [POINTER(xcb_connection_t), c_uint8, POINTER(c_uint8)]

# /usr/include/xcb/xproto.h:14720
xcb_set_pointer_mapping_reply = _lib.xcb_set_pointer_mapping_reply
xcb_set_pointer_mapping_reply.restype = POINTER(xcb_set_pointer_mapping_reply_t)
xcb_set_pointer_mapping_reply.argtypes = [POINTER(xcb_connection_t), xcb_set_pointer_mapping_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:14744
xcb_get_pointer_mapping = _lib.xcb_get_pointer_mapping
xcb_get_pointer_mapping.restype = xcb_get_pointer_mapping_cookie_t
xcb_get_pointer_mapping.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:14768
xcb_get_pointer_mapping_unchecked = _lib.xcb_get_pointer_mapping_unchecked
xcb_get_pointer_mapping_unchecked.restype = xcb_get_pointer_mapping_cookie_t
xcb_get_pointer_mapping_unchecked.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:14780
xcb_get_pointer_mapping_map = _lib.xcb_get_pointer_mapping_map
xcb_get_pointer_mapping_map.restype = POINTER(c_uint8)
xcb_get_pointer_mapping_map.argtypes = [POINTER(xcb_get_pointer_mapping_reply_t)]

# /usr/include/xcb/xproto.h:14794
xcb_get_pointer_mapping_map_length = _lib.xcb_get_pointer_mapping_map_length
xcb_get_pointer_mapping_map_length.restype = c_int
xcb_get_pointer_mapping_map_length.argtypes = [POINTER(xcb_get_pointer_mapping_reply_t)]

# /usr/include/xcb/xproto.h:14807
xcb_get_pointer_mapping_map_end = _lib.xcb_get_pointer_mapping_map_end
xcb_get_pointer_mapping_map_end.restype = xcb_generic_iterator_t
xcb_get_pointer_mapping_map_end.argtypes = [POINTER(xcb_get_pointer_mapping_reply_t)]

# /usr/include/xcb/xproto.h:14833
xcb_get_pointer_mapping_reply = _lib.xcb_get_pointer_mapping_reply
xcb_get_pointer_mapping_reply.restype = POINTER(xcb_get_pointer_mapping_reply_t)
xcb_get_pointer_mapping_reply.argtypes = [POINTER(xcb_connection_t), xcb_get_pointer_mapping_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:14859
xcb_set_modifier_mapping = _lib.xcb_set_modifier_mapping
xcb_set_modifier_mapping.restype = xcb_set_modifier_mapping_cookie_t
xcb_set_modifier_mapping.argtypes = [POINTER(xcb_connection_t), c_uint8, POINTER(xcb_keycode_t)]

# /usr/include/xcb/xproto.h:14887
xcb_set_modifier_mapping_unchecked = _lib.xcb_set_modifier_mapping_unchecked
xcb_set_modifier_mapping_unchecked.restype = xcb_set_modifier_mapping_cookie_t
xcb_set_modifier_mapping_unchecked.argtypes = [POINTER(xcb_connection_t), c_uint8, POINTER(xcb_keycode_t)]

# /usr/include/xcb/xproto.h:14915
xcb_set_modifier_mapping_reply = _lib.xcb_set_modifier_mapping_reply
xcb_set_modifier_mapping_reply.restype = POINTER(xcb_set_modifier_mapping_reply_t)
xcb_set_modifier_mapping_reply.argtypes = [POINTER(xcb_connection_t), xcb_set_modifier_mapping_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:14939
xcb_get_modifier_mapping = _lib.xcb_get_modifier_mapping
xcb_get_modifier_mapping.restype = xcb_get_modifier_mapping_cookie_t
xcb_get_modifier_mapping.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:14963
xcb_get_modifier_mapping_unchecked = _lib.xcb_get_modifier_mapping_unchecked
xcb_get_modifier_mapping_unchecked.restype = xcb_get_modifier_mapping_cookie_t
xcb_get_modifier_mapping_unchecked.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:14975
xcb_get_modifier_mapping_keycodes = _lib.xcb_get_modifier_mapping_keycodes
xcb_get_modifier_mapping_keycodes.restype = POINTER(xcb_keycode_t)
xcb_get_modifier_mapping_keycodes.argtypes = [POINTER(xcb_get_modifier_mapping_reply_t)]

# /usr/include/xcb/xproto.h:14989
xcb_get_modifier_mapping_keycodes_length = _lib.xcb_get_modifier_mapping_keycodes_length
xcb_get_modifier_mapping_keycodes_length.restype = c_int
xcb_get_modifier_mapping_keycodes_length.argtypes = [POINTER(xcb_get_modifier_mapping_reply_t)]

# /usr/include/xcb/xproto.h:15002
xcb_get_modifier_mapping_keycodes_iterator = _lib.xcb_get_modifier_mapping_keycodes_iterator
xcb_get_modifier_mapping_keycodes_iterator.restype = xcb_keycode_iterator_t
xcb_get_modifier_mapping_keycodes_iterator.argtypes = [POINTER(xcb_get_modifier_mapping_reply_t)]

# /usr/include/xcb/xproto.h:15028
xcb_get_modifier_mapping_reply = _lib.xcb_get_modifier_mapping_reply
xcb_get_modifier_mapping_reply.restype = POINTER(xcb_get_modifier_mapping_reply_t)
xcb_get_modifier_mapping_reply.argtypes = [POINTER(xcb_connection_t), xcb_get_modifier_mapping_cookie_t, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xproto.h:15055
xcb_no_operation_checked = _lib.xcb_no_operation_checked
xcb_no_operation_checked.restype = xcb_void_cookie_t
xcb_no_operation_checked.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xproto.h:15076
xcb_no_operation = _lib.xcb_no_operation
xcb_no_operation.restype = xcb_void_cookie_t
xcb_no_operation.argtypes = [POINTER(xcb_connection_t)]

XCB_NONE = 0 	# /usr/include/xcb/xcb.h:146
XCB_COPY_FROM_PARENT = 0 	# /usr/include/xcb/xcb.h:149
XCB_CURRENT_TIME = 0 	# /usr/include/xcb/xcb.h:152
XCB_NO_SYMBOL = 0 	# /usr/include/xcb/xcb.h:155
class struct_xcb_auth_info_t(Structure):
    __slots__ = [
        'namelen',
        'name',
        'datalen',
        'data',
    ]
struct_xcb_auth_info_t._fields_ = [
    ('namelen', c_int),
    ('name', c_char_p),
    ('datalen', c_int),
    ('data', c_char_p),
]

xcb_auth_info_t = struct_xcb_auth_info_t 	# /usr/include/xcb/xcb.h:170
# /usr/include/xcb/xcb.h:183
xcb_flush = _lib.xcb_flush
xcb_flush.restype = c_int
xcb_flush.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xcb.h:200
xcb_get_maximum_request_length = _lib.xcb_get_maximum_request_length
xcb_get_maximum_request_length.restype = c_uint32
xcb_get_maximum_request_length.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xcb.h:219
xcb_prefetch_maximum_request_length = _lib.xcb_prefetch_maximum_request_length
xcb_prefetch_maximum_request_length.restype = None
xcb_prefetch_maximum_request_length.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xcb.h:233
xcb_wait_for_event = _lib.xcb_wait_for_event
xcb_wait_for_event.restype = POINTER(xcb_generic_event_t)
xcb_wait_for_event.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xcb.h:247
xcb_poll_for_event = _lib.xcb_poll_for_event
xcb_poll_for_event.restype = POINTER(xcb_generic_event_t)
xcb_poll_for_event.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xcb.h:265
xcb_request_check = _lib.xcb_request_check
xcb_request_check.restype = POINTER(xcb_generic_error_t)
xcb_request_check.argtypes = [POINTER(xcb_connection_t), xcb_void_cookie_t]

class struct_xcb_extension_t(Structure):
    __slots__ = [
    ]
struct_xcb_extension_t._fields_ = [
    ('_opaque_struct', c_int)
]

class struct_xcb_extension_t(Structure):
    __slots__ = [
    ]
struct_xcb_extension_t._fields_ = [
    ('_opaque_struct', c_int)
]

xcb_extension_t = struct_xcb_extension_t 	# /usr/include/xcb/xcb.h:273
# /usr/include/xcb/xcb.h:291
xcb_get_extension_data = _lib.xcb_get_extension_data
xcb_get_extension_data.restype = POINTER(xcb_query_extension_reply_t)
xcb_get_extension_data.argtypes = [POINTER(xcb_connection_t), POINTER(xcb_extension_t)]

# /usr/include/xcb/xcb.h:304
xcb_prefetch_extension_data = _lib.xcb_prefetch_extension_data
xcb_prefetch_extension_data.restype = None
xcb_prefetch_extension_data.argtypes = [POINTER(xcb_connection_t), POINTER(xcb_extension_t)]

# /usr/include/xcb/xcb.h:327
xcb_get_setup = _lib.xcb_get_setup
xcb_get_setup.restype = POINTER(xcb_setup_t)
xcb_get_setup.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xcb.h:337
xcb_get_file_descriptor = _lib.xcb_get_file_descriptor
xcb_get_file_descriptor.restype = c_int
xcb_get_file_descriptor.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xcb.h:352
xcb_connection_has_error = _lib.xcb_connection_has_error
xcb_connection_has_error.restype = c_int
xcb_connection_has_error.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xcb.h:366
xcb_connect_to_fd = _lib.xcb_connect_to_fd
xcb_connect_to_fd.restype = POINTER(xcb_connection_t)
xcb_connect_to_fd.argtypes = [c_int, POINTER(xcb_auth_info_t)]

# /usr/include/xcb/xcb.h:375
xcb_disconnect = _lib.xcb_disconnect
xcb_disconnect.restype = None
xcb_disconnect.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xcb.h:397
xcb_parse_display = _lib.xcb_parse_display
xcb_parse_display.restype = c_int
xcb_parse_display.argtypes = [c_char_p, POINTER(c_char_p), POINTER(c_int), POINTER(c_int)]

# /usr/include/xcb/xcb.h:411
xcb_connect = _lib.xcb_connect
xcb_connect.restype = POINTER(xcb_connection_t)
xcb_connect.argtypes = [c_char_p, POINTER(c_int)]

# /usr/include/xcb/xcb.h:425
xcb_connect_to_display_with_auth_info = _lib.xcb_connect_to_display_with_auth_info
xcb_connect_to_display_with_auth_info.restype = POINTER(xcb_connection_t)
xcb_connect_to_display_with_auth_info.argtypes = [c_char_p, POINTER(xcb_auth_info_t), POINTER(c_int)]

# /usr/include/xcb/xcb.h:438
xcb_generate_id = _lib.xcb_generate_id
xcb_generate_id.restype = c_uint32
xcb_generate_id.argtypes = [POINTER(xcb_connection_t)]

XCB_BIGREQUESTS_MAJOR_VERSION = 0 	# /usr/include/xcb/bigreq.h:17
XCB_BIGREQUESTS_MINOR_VERSION = 0 	# /usr/include/xcb/bigreq.h:18
class struct_xcb_big_requests_enable_cookie_t(Structure):
    __slots__ = [
        'sequence',
    ]
struct_xcb_big_requests_enable_cookie_t._fields_ = [
    ('sequence', c_uint),
]

xcb_big_requests_enable_cookie_t = struct_xcb_big_requests_enable_cookie_t 	# /usr/include/xcb/bigreq.h:27
XCB_BIG_REQUESTS_ENABLE = 0 	# /usr/include/xcb/bigreq.h:30
class struct_xcb_big_requests_enable_request_t(Structure):
    __slots__ = [
        'major_opcode',
        'minor_opcode',
        'length',
    ]
struct_xcb_big_requests_enable_request_t._fields_ = [
    ('major_opcode', c_uint8),
    ('minor_opcode', c_uint8),
    ('length', c_uint16),
]

xcb_big_requests_enable_request_t = struct_xcb_big_requests_enable_request_t 	# /usr/include/xcb/bigreq.h:39
class struct_xcb_big_requests_enable_reply_t(Structure):
    __slots__ = [
        'response_type',
        'pad0',
        'sequence',
        'length',
        'maximum_request_length',
    ]
struct_xcb_big_requests_enable_reply_t._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('maximum_request_length', c_uint32),
]

xcb_big_requests_enable_reply_t = struct_xcb_big_requests_enable_reply_t 	# /usr/include/xcb/bigreq.h:50
# /usr/include/xcb/bigreq.h:71
xcb_big_requests_enable = _lib.xcb_big_requests_enable
xcb_big_requests_enable.restype = xcb_big_requests_enable_cookie_t
xcb_big_requests_enable.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/bigreq.h:95
xcb_big_requests_enable_unchecked = _lib.xcb_big_requests_enable_unchecked
xcb_big_requests_enable_unchecked.restype = xcb_big_requests_enable_cookie_t
xcb_big_requests_enable_unchecked.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/bigreq.h:121
xcb_big_requests_enable_reply = _lib.xcb_big_requests_enable_reply
xcb_big_requests_enable_reply.restype = POINTER(xcb_big_requests_enable_reply_t)
xcb_big_requests_enable_reply.argtypes = [POINTER(xcb_connection_t), xcb_big_requests_enable_cookie_t, POINTER(POINTER(xcb_generic_error_t))]


__all__ = ['X_PROTOCOL', 'X_PROTOCOL_REVISION', 'X_TCP_PORT',
'xcb_connection_t', 'xcb_generic_iterator_t', 'xcb_generic_reply_t',
'xcb_generic_event_t', 'xcb_generic_error_t', 'xcb_void_cookie_t',
'xcb_char2b_t', 'xcb_char2b_iterator_t', 'xcb_window_t',
'xcb_window_iterator_t', 'xcb_pixmap_t', 'xcb_pixmap_iterator_t',
'xcb_cursor_t', 'xcb_cursor_iterator_t', 'xcb_font_t', 'xcb_font_iterator_t',
'xcb_gcontext_t', 'xcb_gcontext_iterator_t', 'xcb_colormap_t',
'xcb_colormap_iterator_t', 'xcb_atom_t', 'xcb_atom_iterator_t',
'xcb_drawable_t', 'xcb_drawable_iterator_t', 'xcb_fontable_t',
'xcb_fontable_iterator_t', 'xcb_visualid_t', 'xcb_visualid_iterator_t',
'xcb_timestamp_t', 'xcb_timestamp_iterator_t', 'xcb_keysym_t',
'xcb_keysym_iterator_t', 'xcb_keycode_t', 'xcb_keycode_iterator_t',
'xcb_button_t', 'xcb_button_iterator_t', 'xcb_point_t',
'xcb_point_iterator_t', 'xcb_rectangle_t', 'xcb_rectangle_iterator_t',
'xcb_arc_t', 'xcb_arc_iterator_t', 'xcb_format_t', 'xcb_format_iterator_t',
'xcb_visual_class_t', 'XCB_VISUAL_CLASS_STATIC_GRAY',
'XCB_VISUAL_CLASS_GRAY_SCALE', 'XCB_VISUAL_CLASS_STATIC_COLOR',
'XCB_VISUAL_CLASS_PSEUDO_COLOR', 'XCB_VISUAL_CLASS_TRUE_COLOR',
'XCB_VISUAL_CLASS_DIRECT_COLOR', 'xcb_visualtype_t',
'xcb_visualtype_iterator_t', 'xcb_depth_t', 'xcb_depth_iterator_t',
'xcb_screen_t', 'xcb_screen_iterator_t', 'xcb_setup_request_t',
'xcb_setup_request_iterator_t', 'xcb_setup_failed_t',
'xcb_setup_failed_iterator_t', 'xcb_setup_authenticate_t',
'xcb_setup_authenticate_iterator_t', 'xcb_image_order_t',
'XCB_IMAGE_ORDER_LSB_FIRST', 'XCB_IMAGE_ORDER_MSB_FIRST', 'xcb_setup_t',
'xcb_setup_iterator_t', 'xcb_mod_mask_t', 'XCB_MOD_MASK_SHIFT',
'XCB_MOD_MASK_LOCK', 'XCB_MOD_MASK_CONTROL', 'XCB_MOD_MASK_1',
'XCB_MOD_MASK_2', 'XCB_MOD_MASK_3', 'XCB_MOD_MASK_4', 'XCB_MOD_MASK_5',
'XCB_KEY_PRESS', 'xcb_key_press_event_t', 'XCB_KEY_RELEASE',
'xcb_key_release_event_t', 'xcb_button_mask_t', 'XCB_BUTTON_MASK_1',
'XCB_BUTTON_MASK_2', 'XCB_BUTTON_MASK_3', 'XCB_BUTTON_MASK_4',
'XCB_BUTTON_MASK_5', 'XCB_BUTTON_MASK_ANY', 'XCB_BUTTON_PRESS',
'xcb_button_press_event_t', 'XCB_BUTTON_RELEASE',
'xcb_button_release_event_t', 'xcb_motion_t', 'XCB_MOTION_NORMAL',
'XCB_MOTION_HINT', 'XCB_MOTION_NOTIFY', 'xcb_motion_notify_event_t',
'xcb_notify_detail_t', 'XCB_NOTIFY_DETAIL_ANCESTOR',
'XCB_NOTIFY_DETAIL_VIRTUAL', 'XCB_NOTIFY_DETAIL_INFERIOR',
'XCB_NOTIFY_DETAIL_NONLINEAR', 'XCB_NOTIFY_DETAIL_NONLINEAR_VIRTUAL',
'XCB_NOTIFY_DETAIL_POINTER', 'XCB_NOTIFY_DETAIL_POINTER_ROOT',
'XCB_NOTIFY_DETAIL_NONE', 'xcb_notify_mode_t', 'XCB_NOTIFY_MODE_NORMAL',
'XCB_NOTIFY_MODE_GRAB', 'XCB_NOTIFY_MODE_UNGRAB',
'XCB_NOTIFY_MODE_WHILE_GRABBED', 'XCB_ENTER_NOTIFY',
'xcb_enter_notify_event_t', 'XCB_LEAVE_NOTIFY', 'xcb_leave_notify_event_t',
'XCB_FOCUS_IN', 'xcb_focus_in_event_t', 'XCB_FOCUS_OUT',
'xcb_focus_out_event_t', 'XCB_KEYMAP_NOTIFY', 'xcb_keymap_notify_event_t',
'XCB_EXPOSE', 'xcb_expose_event_t', 'XCB_GRAPHICS_EXPOSURE',
'xcb_graphics_exposure_event_t', 'XCB_NO_EXPOSURE', 'xcb_no_exposure_event_t',
'xcb_visibility_t', 'XCB_VISIBILITY_UNOBSCURED',
'XCB_VISIBILITY_PARTIALLY_OBSCURED', 'XCB_VISIBILITY_FULLY_OBSCURED',
'XCB_VISIBILITY_NOTIFY', 'xcb_visibility_notify_event_t', 'XCB_CREATE_NOTIFY',
'xcb_create_notify_event_t', 'XCB_DESTROY_NOTIFY',
'xcb_destroy_notify_event_t', 'XCB_UNMAP_NOTIFY', 'xcb_unmap_notify_event_t',
'XCB_MAP_NOTIFY', 'xcb_map_notify_event_t', 'XCB_MAP_REQUEST',
'xcb_map_request_event_t', 'XCB_REPARENT_NOTIFY',
'xcb_reparent_notify_event_t', 'XCB_CONFIGURE_NOTIFY',
'xcb_configure_notify_event_t', 'XCB_CONFIGURE_REQUEST',
'xcb_configure_request_event_t', 'XCB_GRAVITY_NOTIFY',
'xcb_gravity_notify_event_t', 'XCB_RESIZE_REQUEST',
'xcb_resize_request_event_t', 'xcb_place_t', 'XCB_PLACE_ON_TOP',
'XCB_PLACE_ON_BOTTOM', 'XCB_CIRCULATE_NOTIFY', 'xcb_circulate_notify_event_t',
'XCB_CIRCULATE_REQUEST', 'xcb_circulate_request_event_t', 'xcb_property_t',
'XCB_PROPERTY_NEW_VALUE', 'XCB_PROPERTY_DELETE', 'XCB_PROPERTY_NOTIFY',
'xcb_property_notify_event_t', 'XCB_SELECTION_CLEAR',
'xcb_selection_clear_event_t', 'XCB_SELECTION_REQUEST',
'xcb_selection_request_event_t', 'XCB_SELECTION_NOTIFY',
'xcb_selection_notify_event_t', 'xcb_colormap_state_t',
'XCB_COLORMAP_STATE_UNINSTALLED', 'XCB_COLORMAP_STATE_INSTALLED',
'XCB_COLORMAP_NOTIFY', 'xcb_colormap_notify_event_t',
'xcb_client_message_data_t', 'xcb_client_message_data_iterator_t',
'XCB_CLIENT_MESSAGE', 'xcb_client_message_event_t', 'xcb_mapping_t',
'XCB_MAPPING_MODIFIER', 'XCB_MAPPING_KEYBOARD', 'XCB_MAPPING_POINTER',
'XCB_MAPPING_NOTIFY', 'xcb_mapping_notify_event_t', 'XCB_REQUEST',
'xcb_request_error_t', 'XCB_VALUE', 'xcb_value_error_t', 'XCB_WINDOW',
'xcb_window_error_t', 'XCB_PIXMAP', 'xcb_pixmap_error_t', 'XCB_ATOM',
'xcb_atom_error_t', 'XCB_CURSOR', 'xcb_cursor_error_t', 'XCB_FONT',
'xcb_font_error_t', 'XCB_MATCH', 'xcb_match_error_t', 'XCB_DRAWABLE',
'xcb_drawable_error_t', 'XCB_ACCESS', 'xcb_access_error_t', 'XCB_ALLOC',
'xcb_alloc_error_t', 'XCB_COLORMAP', 'xcb_colormap_error_t', 'XCB_G_CONTEXT',
'xcb_g_context_error_t', 'XCB_ID_CHOICE', 'xcb_id_choice_error_t', 'XCB_NAME',
'xcb_name_error_t', 'XCB_LENGTH', 'xcb_length_error_t', 'XCB_IMPLEMENTATION',
'xcb_implementation_error_t', 'xcb_window_class_t',
'XCB_WINDOW_CLASS_COPY_FROM_PARENT', 'XCB_WINDOW_CLASS_INPUT_OUTPUT',
'XCB_WINDOW_CLASS_INPUT_ONLY', 'xcb_cw_t', 'XCB_CW_BACK_PIXMAP',
'XCB_CW_BACK_PIXEL', 'XCB_CW_BORDER_PIXMAP', 'XCB_CW_BORDER_PIXEL',
'XCB_CW_BIT_GRAVITY', 'XCB_CW_WIN_GRAVITY', 'XCB_CW_BACKING_STORE',
'XCB_CW_BACKING_PLANES', 'XCB_CW_BACKING_PIXEL', 'XCB_CW_OVERRIDE_REDIRECT',
'XCB_CW_SAVE_UNDER', 'XCB_CW_EVENT_MASK', 'XCB_CW_DONT_PROPAGATE',
'XCB_CW_COLORMAP', 'XCB_CW_CURSOR', 'xcb_back_pixmap_t',
'XCB_BACK_PIXMAP_NONE', 'XCB_BACK_PIXMAP_PARENT_RELATIVE', 'xcb_gravity_t',
'XCB_GRAVITY_BIT_FORGET', 'XCB_GRAVITY_WIN_UNMAP', 'XCB_GRAVITY_NORTH_WEST',
'XCB_GRAVITY_NORTH', 'XCB_GRAVITY_NORTH_EAST', 'XCB_GRAVITY_WEST',
'XCB_GRAVITY_CENTER', 'XCB_GRAVITY_EAST', 'XCB_GRAVITY_SOUTH_WEST',
'XCB_GRAVITY_SOUTH', 'XCB_GRAVITY_SOUTH_EAST', 'XCB_GRAVITY_STATIC',
'xcb_backing_store_t', 'XCB_BACKING_STORE_NOT_USEFUL',
'XCB_BACKING_STORE_WHEN_MAPPED', 'XCB_BACKING_STORE_ALWAYS',
'xcb_event_mask_t', 'XCB_EVENT_MASK_NO_EVENT', 'XCB_EVENT_MASK_KEY_PRESS',
'XCB_EVENT_MASK_KEY_RELEASE', 'XCB_EVENT_MASK_BUTTON_PRESS',
'XCB_EVENT_MASK_BUTTON_RELEASE', 'XCB_EVENT_MASK_ENTER_WINDOW',
'XCB_EVENT_MASK_LEAVE_WINDOW', 'XCB_EVENT_MASK_POINTER_MOTION',
'XCB_EVENT_MASK_POINTER_MOTION_HINT', 'XCB_EVENT_MASK_BUTTON_1_MOTION',
'XCB_EVENT_MASK_BUTTON_2_MOTION', 'XCB_EVENT_MASK_BUTTON_3_MOTION',
'XCB_EVENT_MASK_BUTTON_4_MOTION', 'XCB_EVENT_MASK_BUTTON_5_MOTION',
'XCB_EVENT_MASK_BUTTON_MOTION', 'XCB_EVENT_MASK_KEYMAP_STATE',
'XCB_EVENT_MASK_EXPOSURE', 'XCB_EVENT_MASK_VISIBILITY_CHANGE',
'XCB_EVENT_MASK_STRUCTURE_NOTIFY', 'XCB_EVENT_MASK_RESIZE_REDIRECT',
'XCB_EVENT_MASK_SUBSTRUCTURE_NOTIFY', 'XCB_EVENT_MASK_SUBSTRUCTURE_REDIRECT',
'XCB_EVENT_MASK_FOCUS_CHANGE', 'XCB_EVENT_MASK_PROPERTY_CHANGE',
'XCB_EVENT_MASK_COLOR_MAP_CHANGE', 'XCB_EVENT_MASK_OWNER_GRAB_BUTTON',
'XCB_CREATE_WINDOW', 'xcb_create_window_request_t',
'XCB_CHANGE_WINDOW_ATTRIBUTES', 'xcb_change_window_attributes_request_t',
'xcb_map_state_t', 'XCB_MAP_STATE_UNMAPPED', 'XCB_MAP_STATE_UNVIEWABLE',
'XCB_MAP_STATE_VIEWABLE', 'xcb_get_window_attributes_cookie_t',
'XCB_GET_WINDOW_ATTRIBUTES', 'xcb_get_window_attributes_request_t',
'xcb_get_window_attributes_reply_t', 'XCB_DESTROY_WINDOW',
'xcb_destroy_window_request_t', 'XCB_DESTROY_SUBWINDOWS',
'xcb_destroy_subwindows_request_t', 'xcb_set_mode_t', 'XCB_SET_MODE_INSERT',
'XCB_SET_MODE_DELETE', 'XCB_CHANGE_SAVE_SET', 'xcb_change_save_set_request_t',
'XCB_REPARENT_WINDOW', 'xcb_reparent_window_request_t', 'XCB_MAP_WINDOW',
'xcb_map_window_request_t', 'XCB_MAP_SUBWINDOWS',
'xcb_map_subwindows_request_t', 'XCB_UNMAP_WINDOW',
'xcb_unmap_window_request_t', 'XCB_UNMAP_SUBWINDOWS',
'xcb_unmap_subwindows_request_t', 'xcb_config_window_t',
'XCB_CONFIG_WINDOW_X', 'XCB_CONFIG_WINDOW_Y', 'XCB_CONFIG_WINDOW_WIDTH',
'XCB_CONFIG_WINDOW_HEIGHT', 'XCB_CONFIG_WINDOW_BORDER_WIDTH',
'XCB_CONFIG_WINDOW_SIBLING', 'XCB_CONFIG_WINDOW_STACK_MODE',
'xcb_stack_mode_t', 'XCB_STACK_MODE_ABOVE', 'XCB_STACK_MODE_BELOW',
'XCB_STACK_MODE_TOP_IF', 'XCB_STACK_MODE_BOTTOM_IF',
'XCB_STACK_MODE_OPPOSITE', 'XCB_CONFIGURE_WINDOW',
'xcb_configure_window_request_t', 'xcb_circulate_t',
'XCB_CIRCULATE_RAISE_LOWEST', 'XCB_CIRCULATE_LOWER_HIGHEST',
'XCB_CIRCULATE_WINDOW', 'xcb_circulate_window_request_t',
'xcb_get_geometry_cookie_t', 'XCB_GET_GEOMETRY', 'xcb_get_geometry_request_t',
'xcb_get_geometry_reply_t', 'xcb_query_tree_cookie_t', 'XCB_QUERY_TREE',
'xcb_query_tree_request_t', 'xcb_query_tree_reply_t',
'xcb_intern_atom_cookie_t', 'XCB_INTERN_ATOM', 'xcb_intern_atom_request_t',
'xcb_intern_atom_reply_t', 'xcb_get_atom_name_cookie_t', 'XCB_GET_ATOM_NAME',
'xcb_get_atom_name_request_t', 'xcb_get_atom_name_reply_t', 'xcb_prop_mode_t',
'XCB_PROP_MODE_REPLACE', 'XCB_PROP_MODE_PREPEND', 'XCB_PROP_MODE_APPEND',
'XCB_CHANGE_PROPERTY', 'xcb_change_property_request_t', 'XCB_DELETE_PROPERTY',
'xcb_delete_property_request_t', 'xcb_get_property_type_t',
'XCB_GET_PROPERTY_TYPE_ANY', 'xcb_get_property_cookie_t', 'XCB_GET_PROPERTY',
'xcb_get_property_request_t', 'xcb_get_property_reply_t',
'xcb_list_properties_cookie_t', 'XCB_LIST_PROPERTIES',
'xcb_list_properties_request_t', 'xcb_list_properties_reply_t',
'XCB_SET_SELECTION_OWNER', 'xcb_set_selection_owner_request_t',
'xcb_get_selection_owner_cookie_t', 'XCB_GET_SELECTION_OWNER',
'xcb_get_selection_owner_request_t', 'xcb_get_selection_owner_reply_t',
'XCB_CONVERT_SELECTION', 'xcb_convert_selection_request_t',
'xcb_send_event_dest_t', 'XCB_SEND_EVENT_DEST_POINTER_WINDOW',
'XCB_SEND_EVENT_DEST_ITEM_FOCUS', 'XCB_SEND_EVENT',
'xcb_send_event_request_t', 'xcb_grab_mode_t', 'XCB_GRAB_MODE_SYNC',
'XCB_GRAB_MODE_ASYNC', 'xcb_grab_status_t', 'XCB_GRAB_STATUS_SUCCESS',
'XCB_GRAB_STATUS_ALREADY_GRABBED', 'XCB_GRAB_STATUS_INVALID_TIME',
'XCB_GRAB_STATUS_NOT_VIEWABLE', 'XCB_GRAB_STATUS_FROZEN',
'xcb_grab_pointer_cookie_t', 'XCB_GRAB_POINTER', 'xcb_grab_pointer_request_t',
'xcb_grab_pointer_reply_t', 'XCB_UNGRAB_POINTER',
'xcb_ungrab_pointer_request_t', 'xcb_button_index_t', 'XCB_BUTTON_INDEX_ANY',
'XCB_BUTTON_INDEX_1', 'XCB_BUTTON_INDEX_2', 'XCB_BUTTON_INDEX_3',
'XCB_BUTTON_INDEX_4', 'XCB_BUTTON_INDEX_5', 'XCB_GRAB_BUTTON',
'xcb_grab_button_request_t', 'XCB_UNGRAB_BUTTON',
'xcb_ungrab_button_request_t', 'XCB_CHANGE_ACTIVE_POINTER_GRAB',
'xcb_change_active_pointer_grab_request_t', 'xcb_grab_keyboard_cookie_t',
'XCB_GRAB_KEYBOARD', 'xcb_grab_keyboard_request_t',
'xcb_grab_keyboard_reply_t', 'XCB_UNGRAB_KEYBOARD',
'xcb_ungrab_keyboard_request_t', 'xcb_grab_t', 'XCB_GRAB_ANY', 'XCB_GRAB_KEY',
'xcb_grab_key_request_t', 'XCB_UNGRAB_KEY', 'xcb_ungrab_key_request_t',
'xcb_allow_t', 'XCB_ALLOW_ASYNC_POINTER', 'XCB_ALLOW_SYNC_POINTER',
'XCB_ALLOW_REPLAY_POINTER', 'XCB_ALLOW_ASYNC_KEYBOARD',
'XCB_ALLOW_SYNC_KEYBOARD', 'XCB_ALLOW_REPLAY_KEYBOARD',
'XCB_ALLOW_ASYNC_BOTH', 'XCB_ALLOW_SYNC_BOTH', 'XCB_ALLOW_EVENTS',
'xcb_allow_events_request_t', 'XCB_GRAB_SERVER', 'xcb_grab_server_request_t',
'XCB_UNGRAB_SERVER', 'xcb_ungrab_server_request_t',
'xcb_query_pointer_cookie_t', 'XCB_QUERY_POINTER',
'xcb_query_pointer_request_t', 'xcb_query_pointer_reply_t', 'xcb_timecoord_t',
'xcb_timecoord_iterator_t', 'xcb_get_motion_events_cookie_t',
'XCB_GET_MOTION_EVENTS', 'xcb_get_motion_events_request_t',
'xcb_get_motion_events_reply_t', 'xcb_translate_coordinates_cookie_t',
'XCB_TRANSLATE_COORDINATES', 'xcb_translate_coordinates_request_t',
'xcb_translate_coordinates_reply_t', 'XCB_WARP_POINTER',
'xcb_warp_pointer_request_t', 'xcb_input_focus_t', 'XCB_INPUT_FOCUS_NONE',
'XCB_INPUT_FOCUS_POINTER_ROOT', 'XCB_INPUT_FOCUS_PARENT',
'XCB_SET_INPUT_FOCUS', 'xcb_set_input_focus_request_t',
'xcb_get_input_focus_cookie_t', 'XCB_GET_INPUT_FOCUS',
'xcb_get_input_focus_request_t', 'xcb_get_input_focus_reply_t',
'xcb_query_keymap_cookie_t', 'XCB_QUERY_KEYMAP', 'xcb_query_keymap_request_t',
'xcb_query_keymap_reply_t', 'XCB_OPEN_FONT', 'xcb_open_font_request_t',
'XCB_CLOSE_FONT', 'xcb_close_font_request_t', 'xcb_font_draw_t',
'XCB_FONT_DRAW_LEFT_TO_RIGHT', 'XCB_FONT_DRAW_RIGHT_TO_LEFT',
'xcb_fontprop_t', 'xcb_fontprop_iterator_t', 'xcb_charinfo_t',
'xcb_charinfo_iterator_t', 'xcb_query_font_cookie_t', 'XCB_QUERY_FONT',
'xcb_query_font_request_t', 'xcb_query_font_reply_t',
'xcb_query_text_extents_cookie_t', 'XCB_QUERY_TEXT_EXTENTS',
'xcb_query_text_extents_request_t', 'xcb_query_text_extents_reply_t',
'xcb_str_t', 'xcb_str_iterator_t', 'xcb_list_fonts_cookie_t',
'XCB_LIST_FONTS', 'xcb_list_fonts_request_t', 'xcb_list_fonts_reply_t',
'xcb_list_fonts_with_info_cookie_t', 'XCB_LIST_FONTS_WITH_INFO',
'xcb_list_fonts_with_info_request_t', 'xcb_list_fonts_with_info_reply_t',
'XCB_SET_FONT_PATH', 'xcb_set_font_path_request_t',
'xcb_get_font_path_cookie_t', 'XCB_GET_FONT_PATH',
'xcb_get_font_path_request_t', 'xcb_get_font_path_reply_t',
'XCB_CREATE_PIXMAP', 'xcb_create_pixmap_request_t', 'XCB_FREE_PIXMAP',
'xcb_free_pixmap_request_t', 'xcb_gc_t', 'XCB_GC_FUNCTION',
'XCB_GC_PLANE_MASK', 'XCB_GC_FOREGROUND', 'XCB_GC_BACKGROUND',
'XCB_GC_LINE_WIDTH', 'XCB_GC_LINE_STYLE', 'XCB_GC_CAP_STYLE',
'XCB_GC_JOIN_STYLE', 'XCB_GC_FILL_STYLE', 'XCB_GC_FILL_RULE', 'XCB_GC_TILE',
'XCB_GC_STIPPLE', 'XCB_GC_TILE_STIPPLE_ORIGIN_X',
'XCB_GC_TILE_STIPPLE_ORIGIN_Y', 'XCB_GC_FONT', 'XCB_GC_SUBWINDOW_MODE',
'XCB_GC_GRAPHICS_EXPOSURES', 'XCB_GC_CLIP_ORIGIN_X', 'XCB_GC_CLIP_ORIGIN_Y',
'XCB_GC_CLIP_MASK', 'XCB_GC_DASH_OFFSET', 'XCB_GC_DASH_LIST',
'XCB_GC_ARC_MODE', 'xcb_gx_t', 'XCB_GX_CLEAR', 'XCB_GX_AND',
'XCB_GX_AND_REVERSE', 'XCB_GX_COPY', 'XCB_GX_AND_INVERTED', 'XCB_GX_NOOP',
'XCB_GX_XOR', 'XCB_GX_OR', 'XCB_GX_NOR', 'XCB_GX_EQUIV', 'XCB_GX_INVERT',
'XCB_GX_OR_REVERSE', 'XCB_GX_COPY_INVERTED', 'XCB_GX_OR_INVERTED',
'XCB_GX_NAND', 'XCB_GX_SET', 'xcb_line_style_t', 'XCB_LINE_STYLE_SOLID',
'XCB_LINE_STYLE_ON_OFF_DASH', 'XCB_LINE_STYLE_DOUBLE_DASH', 'xcb_cap_style_t',
'XCB_CAP_STYLE_NOT_LAST', 'XCB_CAP_STYLE_BUTT', 'XCB_CAP_STYLE_ROUND',
'XCB_CAP_STYLE_PROJECTING', 'xcb_join_style_t', 'XCB_JOIN_STYLE_MITRE',
'XCB_JOIN_STYLE_ROUND', 'XCB_JOIN_STYLE_BEVEL', 'xcb_fill_style_t',
'XCB_FILL_STYLE_SOLID', 'XCB_FILL_STYLE_TILED', 'XCB_FILL_STYLE_STIPPLED',
'XCB_FILL_STYLE_OPAQUE_STIPPLED', 'xcb_fill_rule_t', 'XCB_FILL_RULE_EVEN_ODD',
'XCB_FILL_RULE_WINDING', 'xcb_subwindow_mode_t',
'XCB_SUBWINDOW_MODE_CLIP_BY_CHILDREN', 'XCB_SUBWINDOW_MODE_INCLUDE_INFERIORS',
'xcb_arc_mode_t', 'XCB_ARC_MODE_CHORD', 'XCB_ARC_MODE_PIE_SLICE',
'XCB_CREATE_GC', 'xcb_create_gc_request_t', 'XCB_CHANGE_GC',
'xcb_change_gc_request_t', 'XCB_COPY_GC', 'xcb_copy_gc_request_t',
'XCB_SET_DASHES', 'xcb_set_dashes_request_t', 'xcb_clip_ordering_t',
'XCB_CLIP_ORDERING_UNSORTED', 'XCB_CLIP_ORDERING_Y_SORTED',
'XCB_CLIP_ORDERING_YX_SORTED', 'XCB_CLIP_ORDERING_YX_BANDED',
'XCB_SET_CLIP_RECTANGLES', 'xcb_set_clip_rectangles_request_t', 'XCB_FREE_GC',
'xcb_free_gc_request_t', 'XCB_CLEAR_AREA', 'xcb_clear_area_request_t',
'XCB_COPY_AREA', 'xcb_copy_area_request_t', 'XCB_COPY_PLANE',
'xcb_copy_plane_request_t', 'xcb_coord_mode_t', 'XCB_COORD_MODE_ORIGIN',
'XCB_COORD_MODE_PREVIOUS', 'XCB_POLY_POINT', 'xcb_poly_point_request_t',
'XCB_POLY_LINE', 'xcb_poly_line_request_t', 'xcb_segment_t',
'xcb_segment_iterator_t', 'XCB_POLY_SEGMENT', 'xcb_poly_segment_request_t',
'XCB_POLY_RECTANGLE', 'xcb_poly_rectangle_request_t', 'XCB_POLY_ARC',
'xcb_poly_arc_request_t', 'xcb_poly_shape_t', 'XCB_POLY_SHAPE_COMPLEX',
'XCB_POLY_SHAPE_NONCONVEX', 'XCB_POLY_SHAPE_CONVEX', 'XCB_FILL_POLY',
'xcb_fill_poly_request_t', 'XCB_POLY_FILL_RECTANGLE',
'xcb_poly_fill_rectangle_request_t', 'XCB_POLY_FILL_ARC',
'xcb_poly_fill_arc_request_t', 'xcb_image_format_t',
'XCB_IMAGE_FORMAT_XY_BITMAP', 'XCB_IMAGE_FORMAT_XY_PIXMAP',
'XCB_IMAGE_FORMAT_Z_PIXMAP', 'XCB_PUT_IMAGE', 'xcb_put_image_request_t',
'xcb_get_image_cookie_t', 'XCB_GET_IMAGE', 'xcb_get_image_request_t',
'xcb_get_image_reply_t', 'XCB_POLY_TEXT_8', 'xcb_poly_text_8_request_t',
'XCB_POLY_TEXT_16', 'xcb_poly_text_16_request_t', 'XCB_IMAGE_TEXT_8',
'xcb_image_text_8_request_t', 'XCB_IMAGE_TEXT_16',
'xcb_image_text_16_request_t', 'xcb_colormap_alloc_t',
'XCB_COLORMAP_ALLOC_NONE', 'XCB_COLORMAP_ALLOC_ALL', 'XCB_CREATE_COLORMAP',
'xcb_create_colormap_request_t', 'XCB_FREE_COLORMAP',
'xcb_free_colormap_request_t', 'XCB_COPY_COLORMAP_AND_FREE',
'xcb_copy_colormap_and_free_request_t', 'XCB_INSTALL_COLORMAP',
'xcb_install_colormap_request_t', 'XCB_UNINSTALL_COLORMAP',
'xcb_uninstall_colormap_request_t', 'xcb_list_installed_colormaps_cookie_t',
'XCB_LIST_INSTALLED_COLORMAPS', 'xcb_list_installed_colormaps_request_t',
'xcb_list_installed_colormaps_reply_t', 'xcb_alloc_color_cookie_t',
'XCB_ALLOC_COLOR', 'xcb_alloc_color_request_t', 'xcb_alloc_color_reply_t',
'xcb_alloc_named_color_cookie_t', 'XCB_ALLOC_NAMED_COLOR',
'xcb_alloc_named_color_request_t', 'xcb_alloc_named_color_reply_t',
'xcb_alloc_color_cells_cookie_t', 'XCB_ALLOC_COLOR_CELLS',
'xcb_alloc_color_cells_request_t', 'xcb_alloc_color_cells_reply_t',
'xcb_alloc_color_planes_cookie_t', 'XCB_ALLOC_COLOR_PLANES',
'xcb_alloc_color_planes_request_t', 'xcb_alloc_color_planes_reply_t',
'XCB_FREE_COLORS', 'xcb_free_colors_request_t', 'xcb_color_flag_t',
'XCB_COLOR_FLAG_RED', 'XCB_COLOR_FLAG_GREEN', 'XCB_COLOR_FLAG_BLUE',
'xcb_coloritem_t', 'xcb_coloritem_iterator_t', 'XCB_STORE_COLORS',
'xcb_store_colors_request_t', 'XCB_STORE_NAMED_COLOR',
'xcb_store_named_color_request_t', 'xcb_rgb_t', 'xcb_rgb_iterator_t',
'xcb_query_colors_cookie_t', 'XCB_QUERY_COLORS', 'xcb_query_colors_request_t',
'xcb_query_colors_reply_t', 'xcb_lookup_color_cookie_t', 'XCB_LOOKUP_COLOR',
'xcb_lookup_color_request_t', 'xcb_lookup_color_reply_t', 'XCB_CREATE_CURSOR',
'xcb_create_cursor_request_t', 'XCB_CREATE_GLYPH_CURSOR',
'xcb_create_glyph_cursor_request_t', 'XCB_FREE_CURSOR',
'xcb_free_cursor_request_t', 'XCB_RECOLOR_CURSOR',
'xcb_recolor_cursor_request_t', 'xcb_query_shape_of_t',
'XCB_QUERY_SHAPE_OF_LARGEST_CURSOR', 'XCB_QUERY_SHAPE_OF_FASTEST_TILE',
'XCB_QUERY_SHAPE_OF_FASTEST_STIPPLE', 'xcb_query_best_size_cookie_t',
'XCB_QUERY_BEST_SIZE', 'xcb_query_best_size_request_t',
'xcb_query_best_size_reply_t', 'xcb_query_extension_cookie_t',
'XCB_QUERY_EXTENSION', 'xcb_query_extension_request_t',
'xcb_query_extension_reply_t', 'xcb_list_extensions_cookie_t',
'XCB_LIST_EXTENSIONS', 'xcb_list_extensions_request_t',
'xcb_list_extensions_reply_t', 'XCB_CHANGE_KEYBOARD_MAPPING',
'xcb_change_keyboard_mapping_request_t', 'xcb_get_keyboard_mapping_cookie_t',
'XCB_GET_KEYBOARD_MAPPING', 'xcb_get_keyboard_mapping_request_t',
'xcb_get_keyboard_mapping_reply_t', 'xcb_kb_t', 'XCB_KB_KEY_CLICK_PERCENT',
'XCB_KB_BELL_PERCENT', 'XCB_KB_BELL_PITCH', 'XCB_KB_BELL_DURATION',
'XCB_KB_LED', 'XCB_KB_LED_MODE', 'XCB_KB_KEY', 'XCB_KB_AUTO_REPEAT_MODE',
'xcb_led_mode_t', 'XCB_LED_MODE_OFF', 'XCB_LED_MODE_ON',
'xcb_auto_repeat_mode_t', 'XCB_AUTO_REPEAT_MODE_OFF',
'XCB_AUTO_REPEAT_MODE_ON', 'XCB_AUTO_REPEAT_MODE_DEFAULT',
'XCB_CHANGE_KEYBOARD_CONTROL', 'xcb_change_keyboard_control_request_t',
'xcb_get_keyboard_control_cookie_t', 'XCB_GET_KEYBOARD_CONTROL',
'xcb_get_keyboard_control_request_t', 'xcb_get_keyboard_control_reply_t',
'XCB_BELL', 'xcb_bell_request_t', 'XCB_CHANGE_POINTER_CONTROL',
'xcb_change_pointer_control_request_t', 'xcb_get_pointer_control_cookie_t',
'XCB_GET_POINTER_CONTROL', 'xcb_get_pointer_control_request_t',
'xcb_get_pointer_control_reply_t', 'xcb_blanking_t',
'XCB_BLANKING_NOT_PREFERRED', 'XCB_BLANKING_PREFERRED',
'XCB_BLANKING_DEFAULT', 'xcb_exposures_t', 'XCB_EXPOSURES_NOT_ALLOWED',
'XCB_EXPOSURES_ALLOWED', 'XCB_EXPOSURES_DEFAULT', 'XCB_SET_SCREEN_SAVER',
'xcb_set_screen_saver_request_t', 'xcb_get_screen_saver_cookie_t',
'XCB_GET_SCREEN_SAVER', 'xcb_get_screen_saver_request_t',
'xcb_get_screen_saver_reply_t', 'xcb_host_mode_t', 'XCB_HOST_MODE_INSERT',
'XCB_HOST_MODE_DELETE', 'xcb_family_t', 'XCB_FAMILY_INTERNET',
'XCB_FAMILY_DECNET', 'XCB_FAMILY_CHAOS', 'XCB_FAMILY_SERVER_INTERPRETED',
'XCB_FAMILY_INTERNET_6', 'XCB_CHANGE_HOSTS', 'xcb_change_hosts_request_t',
'xcb_host_t', 'xcb_host_iterator_t', 'xcb_list_hosts_cookie_t',
'XCB_LIST_HOSTS', 'xcb_list_hosts_request_t', 'xcb_list_hosts_reply_t',
'xcb_access_control_t', 'XCB_ACCESS_CONTROL_DISABLE',
'XCB_ACCESS_CONTROL_ENABLE', 'XCB_SET_ACCESS_CONTROL',
'xcb_set_access_control_request_t', 'xcb_close_down_t',
'XCB_CLOSE_DOWN_DESTROY_ALL', 'XCB_CLOSE_DOWN_RETAIN_PERMANENT',
'XCB_CLOSE_DOWN_RETAIN_TEMPORARY', 'XCB_SET_CLOSE_DOWN_MODE',
'xcb_set_close_down_mode_request_t', 'xcb_kill_t', 'XCB_KILL_ALL_TEMPORARY',
'XCB_KILL_CLIENT', 'xcb_kill_client_request_t', 'XCB_ROTATE_PROPERTIES',
'xcb_rotate_properties_request_t', 'xcb_screen_saver_t',
'XCB_SCREEN_SAVER_RESET', 'XCB_SCREEN_SAVER_ACTIVE', 'XCB_FORCE_SCREEN_SAVER',
'xcb_force_screen_saver_request_t', 'xcb_mapping_status_t',
'XCB_MAPPING_STATUS_SUCCESS', 'XCB_MAPPING_STATUS_BUSY',
'XCB_MAPPING_STATUS_FAILURE', 'xcb_set_pointer_mapping_cookie_t',
'XCB_SET_POINTER_MAPPING', 'xcb_set_pointer_mapping_request_t',
'xcb_set_pointer_mapping_reply_t', 'xcb_get_pointer_mapping_cookie_t',
'XCB_GET_POINTER_MAPPING', 'xcb_get_pointer_mapping_request_t',
'xcb_get_pointer_mapping_reply_t', 'xcb_map_index_t', 'XCB_MAP_INDEX_SHIFT',
'XCB_MAP_INDEX_LOCK', 'XCB_MAP_INDEX_CONTROL', 'XCB_MAP_INDEX_1',
'XCB_MAP_INDEX_2', 'XCB_MAP_INDEX_3', 'XCB_MAP_INDEX_4', 'XCB_MAP_INDEX_5',
'xcb_set_modifier_mapping_cookie_t', 'XCB_SET_MODIFIER_MAPPING',
'xcb_set_modifier_mapping_request_t', 'xcb_set_modifier_mapping_reply_t',
'xcb_get_modifier_mapping_cookie_t', 'XCB_GET_MODIFIER_MAPPING',
'xcb_get_modifier_mapping_request_t', 'xcb_get_modifier_mapping_reply_t',
'XCB_NO_OPERATION', 'xcb_no_operation_request_t', 'xcb_char2b_next',
'xcb_char2b_end', 'xcb_window_next', 'xcb_window_end', 'xcb_pixmap_next',
'xcb_pixmap_end', 'xcb_cursor_next', 'xcb_cursor_end', 'xcb_font_next',
'xcb_font_end', 'xcb_gcontext_next', 'xcb_gcontext_end', 'xcb_colormap_next',
'xcb_colormap_end', 'xcb_atom_next', 'xcb_atom_end', 'xcb_drawable_next',
'xcb_drawable_end', 'xcb_fontable_next', 'xcb_fontable_end',
'xcb_visualid_next', 'xcb_visualid_end', 'xcb_timestamp_next',
'xcb_timestamp_end', 'xcb_keysym_next', 'xcb_keysym_end', 'xcb_keycode_next',
'xcb_keycode_end', 'xcb_button_next', 'xcb_button_end', 'xcb_point_next',
'xcb_point_end', 'xcb_rectangle_next', 'xcb_rectangle_end', 'xcb_arc_next',
'xcb_arc_end', 'xcb_format_next', 'xcb_format_end', 'xcb_visualtype_next',
'xcb_visualtype_end', 'xcb_depth_visuals', 'xcb_depth_visuals_length',
'xcb_depth_visuals_iterator', 'xcb_depth_next', 'xcb_depth_end',
'xcb_screen_allowed_depths_length', 'xcb_screen_allowed_depths_iterator',
'xcb_screen_next', 'xcb_screen_end',
'xcb_setup_request_authorization_protocol_name',
'xcb_setup_request_authorization_protocol_name_length',
'xcb_setup_request_authorization_protocol_name_end',
'xcb_setup_request_authorization_protocol_data',
'xcb_setup_request_authorization_protocol_data_length',
'xcb_setup_request_authorization_protocol_data_end', 'xcb_setup_request_next',
'xcb_setup_request_end', 'xcb_setup_failed_reason',
'xcb_setup_failed_reason_length', 'xcb_setup_failed_reason_end',
'xcb_setup_failed_next', 'xcb_setup_failed_end',
'xcb_setup_authenticate_reason', 'xcb_setup_authenticate_reason_length',
'xcb_setup_authenticate_reason_end', 'xcb_setup_authenticate_next',
'xcb_setup_authenticate_end', 'xcb_setup_vendor', 'xcb_setup_vendor_length',
'xcb_setup_vendor_end', 'xcb_setup_pixmap_formats',
'xcb_setup_pixmap_formats_length', 'xcb_setup_pixmap_formats_iterator',
'xcb_setup_roots_length', 'xcb_setup_roots_iterator', 'xcb_setup_next',
'xcb_setup_end', 'xcb_client_message_data_next',
'xcb_client_message_data_end', 'xcb_create_window_checked',
'xcb_create_window', 'xcb_change_window_attributes_checked',
'xcb_change_window_attributes', 'xcb_get_window_attributes',
'xcb_get_window_attributes_unchecked', 'xcb_get_window_attributes_reply',
'xcb_destroy_window_checked', 'xcb_destroy_window',
'xcb_destroy_subwindows_checked', 'xcb_destroy_subwindows',
'xcb_change_save_set_checked', 'xcb_change_save_set',
'xcb_reparent_window_checked', 'xcb_reparent_window',
'xcb_map_window_checked', 'xcb_map_window', 'xcb_map_subwindows_checked',
'xcb_map_subwindows', 'xcb_unmap_window_checked', 'xcb_unmap_window',
'xcb_unmap_subwindows_checked', 'xcb_unmap_subwindows',
'xcb_configure_window_checked', 'xcb_configure_window',
'xcb_circulate_window_checked', 'xcb_circulate_window', 'xcb_get_geometry',
'xcb_get_geometry_unchecked', 'xcb_get_geometry_reply', 'xcb_query_tree',
'xcb_query_tree_unchecked', 'xcb_query_tree_children',
'xcb_query_tree_children_length', 'xcb_query_tree_children_iterator',
'xcb_query_tree_reply', 'xcb_intern_atom', 'xcb_intern_atom_unchecked',
'xcb_intern_atom_reply', 'xcb_get_atom_name', 'xcb_get_atom_name_unchecked',
'xcb_get_atom_name_name', 'xcb_get_atom_name_name_length',
'xcb_get_atom_name_name_end', 'xcb_get_atom_name_reply',
'xcb_change_property_checked', 'xcb_change_property',
'xcb_delete_property_checked', 'xcb_delete_property', 'xcb_get_property',
'xcb_get_property_unchecked', 'xcb_get_property_value',
'xcb_get_property_value_length', 'xcb_get_property_value_end',
'xcb_get_property_reply', 'xcb_list_properties',
'xcb_list_properties_unchecked', 'xcb_list_properties_atoms',
'xcb_list_properties_atoms_length', 'xcb_list_properties_atoms_iterator',
'xcb_list_properties_reply', 'xcb_set_selection_owner_checked',
'xcb_set_selection_owner', 'xcb_get_selection_owner',
'xcb_get_selection_owner_unchecked', 'xcb_get_selection_owner_reply',
'xcb_convert_selection_checked', 'xcb_convert_selection',
'xcb_send_event_checked', 'xcb_send_event', 'xcb_grab_pointer',
'xcb_grab_pointer_unchecked', 'xcb_grab_pointer_reply',
'xcb_ungrab_pointer_checked', 'xcb_ungrab_pointer', 'xcb_grab_button_checked',
'xcb_grab_button', 'xcb_ungrab_button_checked', 'xcb_ungrab_button',
'xcb_change_active_pointer_grab_checked', 'xcb_change_active_pointer_grab',
'xcb_grab_keyboard', 'xcb_grab_keyboard_unchecked', 'xcb_grab_keyboard_reply',
'xcb_ungrab_keyboard_checked', 'xcb_ungrab_keyboard', 'xcb_grab_key_checked',
'xcb_grab_key', 'xcb_ungrab_key_checked', 'xcb_ungrab_key',
'xcb_allow_events_checked', 'xcb_allow_events', 'xcb_grab_server_checked',
'xcb_grab_server', 'xcb_ungrab_server_checked', 'xcb_ungrab_server',
'xcb_query_pointer', 'xcb_query_pointer_unchecked', 'xcb_query_pointer_reply',
'xcb_timecoord_next', 'xcb_timecoord_end', 'xcb_get_motion_events',
'xcb_get_motion_events_unchecked', 'xcb_get_motion_events_events',
'xcb_get_motion_events_events_length',
'xcb_get_motion_events_events_iterator', 'xcb_get_motion_events_reply',
'xcb_translate_coordinates', 'xcb_translate_coordinates_unchecked',
'xcb_translate_coordinates_reply', 'xcb_warp_pointer_checked',
'xcb_warp_pointer', 'xcb_set_input_focus_checked', 'xcb_set_input_focus',
'xcb_get_input_focus', 'xcb_get_input_focus_unchecked',
'xcb_get_input_focus_reply', 'xcb_query_keymap', 'xcb_query_keymap_unchecked',
'xcb_query_keymap_reply', 'xcb_open_font_checked', 'xcb_open_font',
'xcb_close_font_checked', 'xcb_close_font', 'xcb_fontprop_next',
'xcb_fontprop_end', 'xcb_charinfo_next', 'xcb_charinfo_end', 'xcb_query_font',
'xcb_query_font_unchecked', 'xcb_query_font_properties',
'xcb_query_font_properties_length', 'xcb_query_font_properties_iterator',
'xcb_query_font_char_infos', 'xcb_query_font_char_infos_length',
'xcb_query_font_char_infos_iterator', 'xcb_query_font_reply',
'xcb_query_text_extents', 'xcb_query_text_extents_unchecked',
'xcb_query_text_extents_reply', 'xcb_str_name', 'xcb_str_name_length',
'xcb_str_name_end', 'xcb_str_next', 'xcb_str_end', 'xcb_list_fonts',
'xcb_list_fonts_unchecked', 'xcb_list_fonts_names_length',
'xcb_list_fonts_names_iterator', 'xcb_list_fonts_reply',
'xcb_list_fonts_with_info', 'xcb_list_fonts_with_info_unchecked',
'xcb_list_fonts_with_info_properties',
'xcb_list_fonts_with_info_properties_length',
'xcb_list_fonts_with_info_properties_iterator',
'xcb_list_fonts_with_info_name', 'xcb_list_fonts_with_info_name_length',
'xcb_list_fonts_with_info_name_end', 'xcb_list_fonts_with_info_reply',
'xcb_set_font_path_checked', 'xcb_set_font_path', 'xcb_get_font_path',
'xcb_get_font_path_unchecked', 'xcb_get_font_path_path_length',
'xcb_get_font_path_path_iterator', 'xcb_get_font_path_reply',
'xcb_create_pixmap_checked', 'xcb_create_pixmap', 'xcb_free_pixmap_checked',
'xcb_free_pixmap', 'xcb_create_gc_checked', 'xcb_create_gc',
'xcb_change_gc_checked', 'xcb_change_gc', 'xcb_copy_gc_checked',
'xcb_copy_gc', 'xcb_set_dashes_checked', 'xcb_set_dashes',
'xcb_set_clip_rectangles_checked', 'xcb_set_clip_rectangles',
'xcb_free_gc_checked', 'xcb_free_gc', 'xcb_clear_area_checked',
'xcb_clear_area', 'xcb_copy_area_checked', 'xcb_copy_area',
'xcb_copy_plane_checked', 'xcb_copy_plane', 'xcb_poly_point_checked',
'xcb_poly_point', 'xcb_poly_line_checked', 'xcb_poly_line',
'xcb_segment_next', 'xcb_segment_end', 'xcb_poly_segment_checked',
'xcb_poly_segment', 'xcb_poly_rectangle_checked', 'xcb_poly_rectangle',
'xcb_poly_arc_checked', 'xcb_poly_arc', 'xcb_fill_poly_checked',
'xcb_fill_poly', 'xcb_poly_fill_rectangle_checked', 'xcb_poly_fill_rectangle',
'xcb_poly_fill_arc_checked', 'xcb_poly_fill_arc', 'xcb_put_image_checked',
'xcb_put_image', 'xcb_get_image', 'xcb_get_image_unchecked',
'xcb_get_image_data', 'xcb_get_image_data_length', 'xcb_get_image_data_end',
'xcb_get_image_reply', 'xcb_poly_text_8_checked', 'xcb_poly_text_8',
'xcb_poly_text_16_checked', 'xcb_poly_text_16', 'xcb_image_text_8_checked',
'xcb_image_text_8', 'xcb_image_text_16_checked', 'xcb_image_text_16',
'xcb_create_colormap_checked', 'xcb_create_colormap',
'xcb_free_colormap_checked', 'xcb_free_colormap',
'xcb_copy_colormap_and_free_checked', 'xcb_copy_colormap_and_free',
'xcb_install_colormap_checked', 'xcb_install_colormap',
'xcb_uninstall_colormap_checked', 'xcb_uninstall_colormap',
'xcb_list_installed_colormaps', 'xcb_list_installed_colormaps_unchecked',
'xcb_list_installed_colormaps_cmaps',
'xcb_list_installed_colormaps_cmaps_length',
'xcb_list_installed_colormaps_cmaps_iterator',
'xcb_list_installed_colormaps_reply', 'xcb_alloc_color',
'xcb_alloc_color_unchecked', 'xcb_alloc_color_reply', 'xcb_alloc_named_color',
'xcb_alloc_named_color_unchecked', 'xcb_alloc_named_color_reply',
'xcb_alloc_color_cells', 'xcb_alloc_color_cells_unchecked',
'xcb_alloc_color_cells_pixels', 'xcb_alloc_color_cells_pixels_length',
'xcb_alloc_color_cells_pixels_end', 'xcb_alloc_color_cells_masks',
'xcb_alloc_color_cells_masks_length', 'xcb_alloc_color_cells_masks_end',
'xcb_alloc_color_cells_reply', 'xcb_alloc_color_planes',
'xcb_alloc_color_planes_unchecked', 'xcb_alloc_color_planes_pixels',
'xcb_alloc_color_planes_pixels_length', 'xcb_alloc_color_planes_pixels_end',
'xcb_alloc_color_planes_reply', 'xcb_free_colors_checked', 'xcb_free_colors',
'xcb_coloritem_next', 'xcb_coloritem_end', 'xcb_store_colors_checked',
'xcb_store_colors', 'xcb_store_named_color_checked', 'xcb_store_named_color',
'xcb_rgb_next', 'xcb_rgb_end', 'xcb_query_colors',
'xcb_query_colors_unchecked', 'xcb_query_colors_colors',
'xcb_query_colors_colors_length', 'xcb_query_colors_colors_iterator',
'xcb_query_colors_reply', 'xcb_lookup_color', 'xcb_lookup_color_unchecked',
'xcb_lookup_color_reply', 'xcb_create_cursor_checked', 'xcb_create_cursor',
'xcb_create_glyph_cursor_checked', 'xcb_create_glyph_cursor',
'xcb_free_cursor_checked', 'xcb_free_cursor', 'xcb_recolor_cursor_checked',
'xcb_recolor_cursor', 'xcb_query_best_size', 'xcb_query_best_size_unchecked',
'xcb_query_best_size_reply', 'xcb_query_extension',
'xcb_query_extension_unchecked', 'xcb_query_extension_reply',
'xcb_list_extensions', 'xcb_list_extensions_unchecked',
'xcb_list_extensions_names_length', 'xcb_list_extensions_names_iterator',
'xcb_list_extensions_reply', 'xcb_change_keyboard_mapping_checked',
'xcb_change_keyboard_mapping', 'xcb_get_keyboard_mapping',
'xcb_get_keyboard_mapping_unchecked', 'xcb_get_keyboard_mapping_keysyms',
'xcb_get_keyboard_mapping_keysyms_length',
'xcb_get_keyboard_mapping_keysyms_iterator', 'xcb_get_keyboard_mapping_reply',
'xcb_change_keyboard_control_checked', 'xcb_change_keyboard_control',
'xcb_get_keyboard_control', 'xcb_get_keyboard_control_unchecked',
'xcb_get_keyboard_control_reply', 'xcb_bell_checked', 'xcb_bell',
'xcb_change_pointer_control_checked', 'xcb_change_pointer_control',
'xcb_get_pointer_control', 'xcb_get_pointer_control_unchecked',
'xcb_get_pointer_control_reply', 'xcb_set_screen_saver_checked',
'xcb_set_screen_saver', 'xcb_get_screen_saver',
'xcb_get_screen_saver_unchecked', 'xcb_get_screen_saver_reply',
'xcb_change_hosts_checked', 'xcb_change_hosts', 'xcb_host_address',
'xcb_host_address_length', 'xcb_host_address_end', 'xcb_host_next',
'xcb_host_end', 'xcb_list_hosts', 'xcb_list_hosts_unchecked',
'xcb_list_hosts_hosts_length', 'xcb_list_hosts_hosts_iterator',
'xcb_list_hosts_reply', 'xcb_set_access_control_checked',
'xcb_set_access_control', 'xcb_set_close_down_mode_checked',
'xcb_set_close_down_mode', 'xcb_kill_client_checked', 'xcb_kill_client',
'xcb_rotate_properties_checked', 'xcb_rotate_properties',
'xcb_force_screen_saver_checked', 'xcb_force_screen_saver',
'xcb_set_pointer_mapping', 'xcb_set_pointer_mapping_unchecked',
'xcb_set_pointer_mapping_reply', 'xcb_get_pointer_mapping',
'xcb_get_pointer_mapping_unchecked', 'xcb_get_pointer_mapping_map',
'xcb_get_pointer_mapping_map_length', 'xcb_get_pointer_mapping_map_end',
'xcb_get_pointer_mapping_reply', 'xcb_set_modifier_mapping',
'xcb_set_modifier_mapping_unchecked', 'xcb_set_modifier_mapping_reply',
'xcb_get_modifier_mapping', 'xcb_get_modifier_mapping_unchecked',
'xcb_get_modifier_mapping_keycodes',
'xcb_get_modifier_mapping_keycodes_length',
'xcb_get_modifier_mapping_keycodes_iterator',
'xcb_get_modifier_mapping_reply', 'xcb_no_operation_checked',
'xcb_no_operation', 'XCB_NONE', 'XCB_COPY_FROM_PARENT', 'XCB_CURRENT_TIME',
'XCB_NO_SYMBOL', 'xcb_auth_info_t', 'xcb_flush',
'xcb_get_maximum_request_length', 'xcb_prefetch_maximum_request_length',
'xcb_wait_for_event', 'xcb_poll_for_event', 'xcb_request_check',
'xcb_extension_t', 'xcb_get_extension_data', 'xcb_prefetch_extension_data',
'xcb_get_setup', 'xcb_get_file_descriptor', 'xcb_connection_has_error',
'xcb_connect_to_fd', 'xcb_disconnect', 'xcb_parse_display', 'xcb_connect',
'xcb_connect_to_display_with_auth_info', 'xcb_generate_id',
'XCB_BIGREQUESTS_MAJOR_VERSION', 'XCB_BIGREQUESTS_MINOR_VERSION',
'xcb_big_requests_enable_cookie_t', 'XCB_BIG_REQUESTS_ENABLE',
'xcb_big_requests_enable_request_t', 'xcb_big_requests_enable_reply_t',
'xcb_big_requests_enable', 'xcb_big_requests_enable_unchecked',
'xcb_big_requests_enable_reply']
