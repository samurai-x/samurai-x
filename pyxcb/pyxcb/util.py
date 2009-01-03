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

import logging
log = logging.getLogger(__name__)

# There is operator.methodcaller in Python 2.6!
methodcaller = lambda method: lambda value: getattr(value, method)()

def cached_property(func):
    """
        `property`, but cached;

        taken from http://code.activestate.com/recipes/576563/ - thanks.
    """
    def getter(self):
        try:
            return self._property_cache[func]
        except AttributeError:
            self._property_cache = {}
            self._property_cache[func] = ret = func(self)
            return ret
        except KeyError:
            self._property_cache[func] = ret = func(self)
            return ret
    return property(getter)

def reverse_dict(d):
    return dict((value, key) for key, value in d.iteritems())

def xize_attributes(attributes, attributes_list):
    attributes = attributes.copy()
    mask = 0
    values = []
    for tup in attributes_list:
        if len(tup) > 2: # has a xizer information
            key, attr_mask, xizer = tup
            # * if xizer is False, nothing will be xized
            # * if it is something else, it should be a callable. 
            # * if it is not a callable, it'll crash.
        else: # use `.xize` method
            key, attr_mask = tup
            xizer = methodcaller('xize')
        if key in attributes:
            mask |= attr_mask
            val = attributes[key]
            if xizer:
                assert hasattr(xizer, '__call__')
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
        return "(%s: %s)" % (self.err.error_code, err_help.get(self.err.error_code, 'Unknown'))

def check_for_error(err):
    if err and not err.contents.error_code == 0:
        raise XCBException(err.contents)

def check_void_cookie(connection, cookie):
    check_for_error(_xcb.xcb_request_check(connection, cookie))


