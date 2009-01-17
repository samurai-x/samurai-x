import ctypes
from . import (libxcb, exception)
from .conn import Connection
from ooxcb.constant import *

SETUP = None

CORE = None
CORE_EVENTS = {} 
CORE_ERRORS = {}

EXTDICT = {}
EXT_EVENTS = {}
EXT_ERRORS = {}

def parse_auth(authstr):
    name, data = authstr.split(':')
    auth = libxcb.xcb_auth_info()
    auth.namelen = len(name)
    auth.name = name
    auth.datalen = len(data)
    auth.data = data
    return auth
     
def connect(display='', fd=None, auth_string=None):
    auth = None

    if CORE is None:
        raise exception.XcbException("No core protocol object has been set.  Did you import xcb.xproto?")

    conn = Connection(CORE)
    if auth_string is not None:
        auth = parse_auth(auth_string)

    if fd is not None:
        conn.conn = libxcb.xcb_connect_to_fd(fd, ctypes.byref(auth))
    elif auth is not None:
        pref_screen = ctypes.c_int()
        conn.conn = libxcb.xcb_connect_to_display_with_auth_info(display, ctypes.byref(auth), ctypes.byref(pref_screen))
        conn.pref_screen = pref_screen.value
    else:
        pref_screen = ctypes.c_int()
        conn.conn = libxcb.xcb_connect(display, ctypes.byref(pref_screen))
        conn.pref_screen = pref_screen.value

    conn.setup()
    return conn

def popcount(i):
    return libxcb.xcb_popcount(i)

def type_pad(t, i):
    return -i & (3 if t > 4 else t - 1)

def _add_core(value, setup, events, errors):
    global CORE, CORE_EVENTS, CORE_ERRORS, SETUP # eeeeeevil
    # TODO: I skipped the error checking blah blah
    if CORE is not None:
        print "module core not none oh noez!"
        return None
    CORE = value
    CORE_EVENTS = events
    CORE_ERRORS = errors
    SETUP = setup

def _add_ext(key, value, events, errors):
    EXTDICT[key] = value
    EXT_EVENTS[key] = events
    EXT_ERRORS[key] = errors

def _resize_obj(obj, size):
    obj.size = size

from ooxcb.list import *
from ooxcb.event import *
from ooxcb.structure import *
from ooxcb.request import *
from ooxcb.union import *
from ooxcb.error import *
from ooxcb.iter import *
from ooxcb.exception import *
from ooxcb.cookie import *
from ooxcb.void import *
from ooxcb.reply import *
from ooxcb.ext import *
from ooxcb.extkey import *
from ooxcb.resource import *

__all__ = [ 'xproto', 'bigreq', 'xc_misc' ]
