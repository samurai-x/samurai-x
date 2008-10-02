import ctypes
import _xcb

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

def check_for_error(cookie):
    assert cookie.error_code == 0

def check_void_cookie(cookie):
    check_for_error(ctypes.cast(ctypes.pointer(cookie), ctypes.POINTER(_xcb.xcb_generic_error_t)).contents)
