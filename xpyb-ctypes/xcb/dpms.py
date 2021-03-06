#
# This file generated automatically from dpms.xml by py_client.py.
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


MAJOR_VERSION = 0
MINOR_VERSION = 0

key = xcb.ExtensionKey('DPMS')

class GetVersionCookie(xcb.Cookie):
    pass

class GetVersionReply(xcb.Reply):
    def __init__(self, parent):
        xcb.Reply.__init__(self, parent)
        count = 0
        (self.server_major_version, self.server_minor_version,) = unpack_ex('xx2x4xHH', self, count)

class CapableCookie(xcb.Cookie):
    pass

class CapableReply(xcb.Reply):
    def __init__(self, parent):
        xcb.Reply.__init__(self, parent)
        count = 0
        (self.capable,) = unpack_ex('xx2x4xB', self, count)

class GetTimeoutsCookie(xcb.Cookie):
    pass

class GetTimeoutsReply(xcb.Reply):
    def __init__(self, parent):
        xcb.Reply.__init__(self, parent)
        count = 0
        (self.standby_timeout, self.suspend_timeout, self.off_timeout,) = unpack_ex('xx2x4xHHH', self, count)

class InfoCookie(xcb.Cookie):
    pass

class InfoReply(xcb.Reply):
    def __init__(self, parent):
        xcb.Reply.__init__(self, parent)
        count = 0
        (self.power_level, self.state,) = unpack_ex('xx2x4xHB', self, count)

class dpmsExtension(xcb.Extension):

    def GetVersion(self, client_major_version, client_minor_version):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2xHH', client_major_version, client_minor_version))
        return self.send_request(xcb.Request(buf.getvalue(), 0, False, True),
                                 GetVersionCookie(),
                                 GetVersionReply)

    def GetVersionUnchecked(self, client_major_version, client_minor_version):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2xHH', client_major_version, client_minor_version))
        return self.send_request(xcb.Request(buf.getvalue(), 0, False, False),
                                 GetVersionCookie(),
                                 GetVersionReply)

    def Capable(self, ):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2x', ))
        return self.send_request(xcb.Request(buf.getvalue(), 1, False, True),
                                 CapableCookie(),
                                 CapableReply)

    def CapableUnchecked(self, ):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2x', ))
        return self.send_request(xcb.Request(buf.getvalue(), 1, False, False),
                                 CapableCookie(),
                                 CapableReply)

    def GetTimeouts(self, ):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2x', ))
        return self.send_request(xcb.Request(buf.getvalue(), 2, False, True),
                                 GetTimeoutsCookie(),
                                 GetTimeoutsReply)

    def GetTimeoutsUnchecked(self, ):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2x', ))
        return self.send_request(xcb.Request(buf.getvalue(), 2, False, False),
                                 GetTimeoutsCookie(),
                                 GetTimeoutsReply)

    def SetTimeoutsChecked(self, standby_timeout, suspend_timeout, off_timeout):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2xHHH', standby_timeout, suspend_timeout, off_timeout))
        return self.send_request(xcb.Request(buf.getvalue(), 3, True, True),
                                 xcb.VoidCookie())

    def SetTimeouts(self, standby_timeout, suspend_timeout, off_timeout):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2xHHH', standby_timeout, suspend_timeout, off_timeout))
        return self.send_request(xcb.Request(buf.getvalue(), 3, True, False),
                                 xcb.VoidCookie())

    def EnableChecked(self, ):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2x', ))
        return self.send_request(xcb.Request(buf.getvalue(), 4, True, True),
                                 xcb.VoidCookie())

    def Enable(self, ):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2x', ))
        return self.send_request(xcb.Request(buf.getvalue(), 4, True, False),
                                 xcb.VoidCookie())

    def DisableChecked(self, ):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2x', ))
        return self.send_request(xcb.Request(buf.getvalue(), 5, True, True),
                                 xcb.VoidCookie())

    def Disable(self, ):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2x', ))
        return self.send_request(xcb.Request(buf.getvalue(), 5, True, False),
                                 xcb.VoidCookie())

    def ForceLevelChecked(self, power_level):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2xH', power_level))
        return self.send_request(xcb.Request(buf.getvalue(), 6, True, True),
                                 xcb.VoidCookie())

    def ForceLevel(self, power_level):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2xH', power_level))
        return self.send_request(xcb.Request(buf.getvalue(), 6, True, False),
                                 xcb.VoidCookie())

    def Info(self, ):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2x', ))
        return self.send_request(xcb.Request(buf.getvalue(), 7, False, True),
                                 InfoCookie(),
                                 InfoReply)

    def InfoUnchecked(self, ):
        buf = cStringIO.StringIO()
        buf.write(pack('xx2x', ))
        return self.send_request(xcb.Request(buf.getvalue(), 7, False, False),
                                 InfoCookie(),
                                 InfoReply)

_events = {
}

_errors = {
}

xcb._add_ext(key, dpmsExtension, _events, _errors)
