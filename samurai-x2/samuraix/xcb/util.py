import ctypes
import _xcb

import logging
log = logging.getLogger(__name__)

CACHE_KEYWORD = '_cached'

def cached(func):
    # TODO: UGLY UGLY UGLY
    def do_cache(self, *args, **kwargs):
        if CACHE_KEYWORD not in func.func_dict: # table does not exist
            func.func_dict[CACHE_KEYWORD] = {}
        if self not in func.func_dict[CACHE_KEYWORD]:
            func.func_dict[CACHE_KEYWORD][self] = func(self, *args, **kwargs)
        return func.func_dict[CACHE_KEYWORD][self]
    return do_cache

def cached_property(func):
    return property(cached(func))

def reverse_dict(d):
    return dict((value, key) for key, value in d.iteritems())

def xize_attributes(attributes, attributes_list):
    attributes = attributes.copy()
    mask = 0
    values = []
    for tup in attributes_list:
        if len(tup) > 2: # has a xizer
            key, attr_mask, xizer = tup
        else: # has no xizer
            key, attr_mask = tup
            xizer = None
        if key in attributes:
            mask |= attr_mask
            val = attributes[key]
            if xizer:
                val = xizer(val)
            values.append(val)
    return (ctypes.c_uint * len(values))(*values), mask


XUTIL_SUCCESS = 0                                                                                  
XUTIL_BAD_REQUEST = 1
XUTIL_BAD_VALUE = 2
XUTIL_BAD_WINDOW = 3
XUTIL_BAD_PIXMAP = 4
XUTIL_BAD_ATOM = 5
XUTIL_BAD_CURSOR = 6                                                                               
XUTIL_BAD_FONT = 7                                                                                 
XUTIL_BAD_MATCH = 8
XUTIL_BAD_DRAWABLE = 9                                                                             
XUTIL_BAD_ACCESS = 10
XUTIL_BAD_ALLOC = 11                                                                               
XUTIL_BAD_COLOR = 12                                                                               
XUTIL_BAD_GC = 13
XUTIL_BAD_ID_CHOICE = 14
XUTIL_BAD_NAME = 15
XUTIL_BAD_LENGTH = 16                                                                              
XUTIL_BAD_IMPLEMENTATION = 17

err_help = {
    XUTIL_SUCCESS:              "Everything's okay",
    XUTIL_BAD_REQUEST:          "Bad request code",
    XUTIL_BAD_VALUE:            "Int parameter out of range",
    XUTIL_BAD_WINDOW:           "Parameter not a Window",
    XUTIL_BAD_PIXMAP:           "Parameter not a Pixmap",
    XUTIL_BAD_ATOM:             "Parameter not an Atom",
    XUTIL_BAD_CURSOR:           "Parameter not a Cursor",
    XUTIL_BAD_FONT:             "Parameter not a Font",
    XUTIL_BAD_MATCH:            "Parameter mismatch",
    XUTIL_BAD_DRAWABLE:         "Parameter not a Pixmap or Window",
    XUTIL_BAD_ACCESS:           """\
Depending on context:
  - key/button already grabbed
  - attempt to free an illegal
    cmap entry
  - attempt to store into a read-only
    color map entry.
  - attempt to modify the access control
    list from other than the local host. 
""",
    XUTIL_BAD_ALLOC:            "Insufficient resources",
    XUTIL_BAD_COLOR:            "No such colormap",
    XUTIL_BAD_GC:               "Parameter not a GC",
    XUTIL_BAD_ID_CHOICE:        "Choice not in range or already used",
    XUTIL_BAD_NAME:             "Font or color name doesn't exist",
    XUTIL_BAD_LENGTH:           "Request length incorrect",
    XUTIL_BAD_IMPLEMENTATION:   "Server is defective",
}


class XCBException(Exception):
    def __init__(self, err):
        self.err = err

    def __str__(self):
        return "(%s)" % (self.err.error_code, err_help.get(self.err.error_code, 'Unknown'))


def check_for_error(err):
    if err and not err.contents.error_code == 0:
        raise XCBException(err.contents)

def check_void_cookie(connection, cookie):
    check_for_error(_xcb.xcb_request_check(connection, cookie))


