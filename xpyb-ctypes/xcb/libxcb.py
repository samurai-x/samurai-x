from ctypes import *
from ctypes import util

def load_lib(name):
    libname = util.find_library(name)
    if not libname:
        raise OSError("Could not find library '%s'" % name)
    else:
        return CDLL(libname)

_lib = load_lib('xcb')

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]

XCB_REQUEST_CHECKED = 1 << 0
XCB_REQUEST_RAW = 1 << 1
XCB_REQUEST_DISCARD_REPLY = 1 << 2


X_PROTOCOL = 11 	# /usr/include/xcb/xcb.h:60
X_PROTOCOL_REVISION = 0 	# /usr/include/xcb/xcb.h:63
X_TCP_PORT = 6000 	# /usr/include/xcb/xcb.h:66

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
        'pad0',
        'sequence',
        'length',
        'event_type',
        'pad1',
        'pad',
        'full_sequence',
    ]
struct_anon_28._fields_ = [
    ('response_type', c_uint8),
    ('pad0', c_uint8),
    ('sequence', c_uint16),
    ('length', c_uint32),
    ('event_type', c_uint16),
    ('pad1', c_uint16),
    ('pad', c_uint32 * 5),
    ('full_sequence', c_uint32),
]

xcb_ge_event_t = struct_anon_28 	# /usr/include/xcb/xcb.h:133
class struct_anon_29(Structure):
    __slots__ = [
        'response_type',
        'error_code',
        'sequence',
        'pad',
        'full_sequence',
    ]
struct_anon_29._fields_ = [
    ('response_type', c_uint8),
    ('error_code', c_uint8),
    ('sequence', c_uint16),
    ('pad', c_uint32 * 7),
    ('full_sequence', c_uint32),
]

xcb_generic_error_t = struct_anon_29 	# /usr/include/xcb/xcb.h:146
class struct_anon_30(Structure):
    __slots__ = [
        'sequence',
    ]
struct_anon_30._fields_ = [
    ('sequence', c_uint),
]

xcb_void_cookie_t = struct_anon_30 	# /usr/include/xcb/xcb.h:155
XCB_NONE = 0 	# /usr/include/xcb/xcb.h:163
XCB_COPY_FROM_PARENT = 0 	# /usr/include/xcb/xcb.h:166
XCB_CURRENT_TIME = 0 	# /usr/include/xcb/xcb.h:169
XCB_NO_SYMBOL = 0 	# /usr/include/xcb/xcb.h:172
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

xcb_auth_info_t = struct_xcb_auth_info_t 	# /usr/include/xcb/xcb.h:187
# /usr/include/xcb/xcb.h:200
xcb_flush = _lib.xcb_flush
xcb_flush.restype = c_int
xcb_flush.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xcb.h:217
xcb_get_maximum_request_length = _lib.xcb_get_maximum_request_length
xcb_get_maximum_request_length.restype = c_uint32
xcb_get_maximum_request_length.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xcb.h:236
xcb_prefetch_maximum_request_length = _lib.xcb_prefetch_maximum_request_length
xcb_prefetch_maximum_request_length.restype = None
xcb_prefetch_maximum_request_length.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xcb.h:250
xcb_wait_for_event = _lib.xcb_wait_for_event
xcb_wait_for_event.restype = POINTER(xcb_generic_event_t)
xcb_wait_for_event.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xcb.h:264
xcb_poll_for_event = _lib.xcb_poll_for_event
xcb_poll_for_event.restype = POINTER(xcb_generic_event_t)
xcb_poll_for_event.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xcb.h:282
xcb_request_check = _lib.xcb_request_check
xcb_request_check.restype = POINTER(xcb_generic_error_t)
xcb_request_check.argtypes = [POINTER(xcb_connection_t), xcb_void_cookie_t]

class struct_xcb_extension_t(Structure):
    _fields_ = [('name', c_char_p),
            ('global_id', c_int)] # xpyb needs it ... cannot be opaque, so changed it.

xcb_extension_t = struct_xcb_extension_t 	# /usr/include/xcb/xcb.h:290
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

xcb_query_extension_reply_t = struct_xcb_query_extension_reply_t 	# /usr/include/xcb/xproto.h:3667
# /usr/include/xcb/xcb.h:308
xcb_get_extension_data = _lib.xcb_get_extension_data
xcb_get_extension_data.restype = POINTER(xcb_query_extension_reply_t)
xcb_get_extension_data.argtypes = [POINTER(xcb_connection_t), POINTER(xcb_extension_t)]

# /usr/include/xcb/xcb.h:321
xcb_prefetch_extension_data = _lib.xcb_prefetch_extension_data
xcb_prefetch_extension_data.restype = None
xcb_prefetch_extension_data.argtypes = [POINTER(xcb_connection_t), POINTER(xcb_extension_t)]

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
xcb_keycode_t = c_uint8 	# /usr/include/xcb/xproto.h:166
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
# /usr/include/xcb/xcb.h:344
xcb_get_setup = _lib.xcb_get_setup
xcb_get_setup.restype = POINTER(xcb_setup_t)
xcb_get_setup.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xcb.h:354
xcb_get_file_descriptor = _lib.xcb_get_file_descriptor
xcb_get_file_descriptor.restype = c_int
xcb_get_file_descriptor.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xcb.h:369
xcb_connection_has_error = _lib.xcb_connection_has_error
xcb_connection_has_error.restype = c_int
xcb_connection_has_error.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xcb.h:383
xcb_connect_to_fd = _lib.xcb_connect_to_fd
xcb_connect_to_fd.restype = POINTER(xcb_connection_t)
xcb_connect_to_fd.argtypes = [c_int, POINTER(xcb_auth_info_t)]

# /usr/include/xcb/xcb.h:392
xcb_disconnect = _lib.xcb_disconnect
xcb_disconnect.restype = None
xcb_disconnect.argtypes = [POINTER(xcb_connection_t)]

# /usr/include/xcb/xcb.h:414
xcb_parse_display = _lib.xcb_parse_display
xcb_parse_display.restype = c_int
xcb_parse_display.argtypes = [c_char_p, POINTER(c_char_p), POINTER(c_int), POINTER(c_int)]

# /usr/include/xcb/xcb.h:428
xcb_connect = _lib.xcb_connect
xcb_connect.restype = POINTER(xcb_connection_t)
xcb_connect.argtypes = [c_char_p, POINTER(c_int)]

# /usr/include/xcb/xcb.h:442
xcb_connect_to_display_with_auth_info = _lib.xcb_connect_to_display_with_auth_info
xcb_connect_to_display_with_auth_info.restype = POINTER(xcb_connection_t)
xcb_connect_to_display_with_auth_info.argtypes = [c_char_p, POINTER(xcb_auth_info_t), POINTER(c_int)]

# /usr/include/xcb/xcb.h:455
xcb_generate_id = _lib.xcb_generate_id
xcb_generate_id.restype = c_uint32
xcb_generate_id.argtypes = [POINTER(xcb_connection_t)]

# .... sys/uio.h

class iovec(Structure):
    _fields_ = [('iov_base', c_void_p),
            ('iov_len', c_size_t)]


# ... xcbext.h

class struct_anon_31(Structure):
    __slots__ = [
        'count',
        'ext',
        'opcode',
        'isvoid',
    ]

struct_anon_31._fields_ = [
    ('count', c_size_t),
    ('ext', POINTER(xcb_extension_t)),
    ('opcode', c_uint8),
    ('isvoid', c_uint8),
]

xcb_protocol_request_t = struct_anon_31 	# /usr/include/xcb/xcbext.h:52

# /usr/include/xcb/xcbext.h:60
xcb_send_request = _lib.xcb_send_request
xcb_send_request.restype = c_uint
xcb_send_request.argtypes = [POINTER(xcb_connection_t), c_int, POINTER(iovec), POINTER(xcb_protocol_request_t)]

class struct_anon_29(Structure):
    __slots__ = [
        'response_type',
        'error_code',
        'sequence',
        'pad',
        'full_sequence',
    ]
struct_anon_29._fields_ = [
    ('response_type', c_uint8),
    ('error_code', c_uint8),
    ('sequence', c_uint16),
    ('pad', c_uint32 * 7),
    ('full_sequence', c_uint32),
]

xcb_generic_error_t = struct_anon_29 	# /usr/include/xcb/xcb.h:146
# /usr/include/xcb/xcbext.h:65
xcb_wait_for_reply = _lib.xcb_wait_for_reply
xcb_wait_for_reply.restype = c_void_p
xcb_wait_for_reply.argtypes = [POINTER(xcb_connection_t), c_uint, POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xcbext.h:66
xcb_poll_for_reply = _lib.xcb_poll_for_reply
xcb_poll_for_reply.restype = c_int
xcb_poll_for_reply.argtypes = [POINTER(xcb_connection_t), c_uint, POINTER(POINTER(None)), POINTER(POINTER(xcb_generic_error_t))]

# /usr/include/xcb/xcbext.h:71
xcb_popcount = _lib.xcb_popcount
xcb_popcount.restype = c_int
xcb_popcount.argtypes = [c_uint32]

__all__ = [ \
# xcb.h
'X_PROTOCOL', 'X_PROTOCOL_REVISION', 'X_TCP_PORT',
'xcb_connection_t', 'xcb_generic_iterator_t', 'xcb_generic_reply_t',
'xcb_generic_event_t', 'xcb_ge_event_t', 'xcb_generic_error_t',
'xcb_void_cookie_t', 'XCB_NONE', 'XCB_COPY_FROM_PARENT', 'XCB_CURRENT_TIME',
'XCB_NO_SYMBOL', 'xcb_auth_info_t', 'xcb_flush',
'xcb_get_maximum_request_length', 'xcb_prefetch_maximum_request_length',
'xcb_wait_for_event', 'xcb_poll_for_event', 'xcb_request_check',
'xcb_extension_t', 'xcb_get_extension_data', 'xcb_prefetch_extension_data',
'xcb_get_setup', 'xcb_get_file_descriptor', 'xcb_connection_has_error',
'xcb_connect_to_fd', 'xcb_disconnect', 'xcb_parse_display', 'xcb_connect',
'xcb_connect_to_display_with_auth_info', 'xcb_generate_id',
# xcbext.h
'xcb_protocol_request_t', 'xcb_send_request', 'xcb_wait_for_reply',
'xcb_poll_for_reply', 'xcb_popcount'
# sys/uio.h
'iovec']

