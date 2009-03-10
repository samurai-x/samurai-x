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

#
# This file generated automatically from xtest.xml by py_client.py.
# Edit at your peril.
#

import xcb
import cStringIO
import ctypes
from struct import pack, unpack_from, calcsize
from array import array

def unpack_ex(fmt, protobj, offset=0):
    s = protobj.get_slice(calcsize(fmt), offset)
    return unpack_from(fmt, s, 0)

import xproto

MAJOR_VERSION = 2
MINOR_VERSION = 1

key = xcb.ExtensionKey('XTEST')

class GetVersionCookie(xcb.Cookie):
    pass

class GetVersionReply(xcb.Reply):
    def __init__(self, parent):
        xcb.Reply.__init__(self, parent)
        count = 0
        (self.major_version, self.minor_version,) = unpack_ex('xB2x4xH', self, count)

class Cursor:
    _None = 0
    Current = 1

class CompareCursorCookie(xcb.Cookie):
    pass

class CompareCursorReply(xcb.Reply):
    def __init__(self, parent):
        xcb.Reply.__init__(self, parent)
        count = 0
        (self.same,) = unpack_ex('xB2x4x', self, count)

class xtestExtension(xcb.Extension):

    def GetVersion(self, major_version, minor_version):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2xBxH', major_version, minor_version))
        return self.send_request(xcb.Request(buf.getvalue(), 0, False, True),
                                 GetVersionCookie(),
                                 GetVersionReply)

    def GetVersionUnchecked(self, major_version, minor_version):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2xBxH', major_version, minor_version))
        return self.send_request(xcb.Request(buf.getvalue(), 0, False, False),
                                 GetVersionCookie(),
                                 GetVersionReply)

    def CompareCursor(self, window, cursor):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2xII', window, cursor))
        return self.send_request(xcb.Request(buf.getvalue(), 1, False, True),
                                 CompareCursorCookie(),
                                 CompareCursorReply)

    def CompareCursorUnchecked(self, window, cursor):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2xII', window, cursor))
        return self.send_request(xcb.Request(buf.getvalue(), 1, False, False),
                                 CompareCursorCookie(),
                                 CompareCursorReply)

    def FakeInputChecked(self, type, detail, time, window, rootX, rootY, deviceid):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2xBB2xII8xHH7xB', type, detail, time, window, rootX, rootY, deviceid))
        return self.send_request(xcb.Request(buf.getvalue(), 2, True, True),
                                 xcb.VoidCookie())

    def FakeInput(self, type, detail, time, window, rootX, rootY, deviceid):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2xBB2xII8xHH7xB', type, detail, time, window, rootX, rootY, deviceid))
        return self.send_request(xcb.Request(buf.getvalue(), 2, True, False),
                                 xcb.VoidCookie())

    def GrabControlChecked(self, impervious):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2xB3x', impervious))
        return self.send_request(xcb.Request(buf.getvalue(), 3, True, True),
                                 xcb.VoidCookie())

    def GrabControl(self, impervious):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2xB3x', impervious))
        return self.send_request(xcb.Request(buf.getvalue(), 3, True, False),
                                 xcb.VoidCookie())

_events = {
}

_errors = {
}

xcb._add_ext(key, xtestExtension, _events, _errors)
