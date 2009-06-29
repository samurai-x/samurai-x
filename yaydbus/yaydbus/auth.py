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

from binascii import hexlify, unhexlify

from . import dbus_cookie_sha1

class AuthError(Exception):
    pass

class RejectedError(AuthError):
    def __init__(self, mechanisms):
        self.mechanisms = mechanisms

    def __str__(self):
        return 'Authentication was rejected. Available mechanisms: %r' % self.mechanisms

def command(line):
    return '%s\r\n' % line

def auth(mechanism='', initial_response=''):
    cmd = 'AUTH'
    if mechanism:
        cmd += ' ' + mechanism
    if initial_response:
        cmd += ' ' + initial_response
    return command(cmd)

def cancel():
    return command('CANCEL')

def data(hex_data):
    return command('DATA %s' % hex_data)

def begin():
    return command('BEGIN')

def error(msg):
    return command('ERROR %s' % msg)

def handler(verb):
    def deco(f):
        HANDLERS[verb] = f
        return f
    return deco

HANDLERS = {}

class AuthHandler(object):
    def __init__(self, socket):
        self.socket = socket
        self.guid = None
        self.ok = False
        self.mechanisms = []
        self.data_received = []
        self._buf = ''

    def _send(self, line):
        length = len(line)
        sent = 0
        while sent < length:
            sent += self.socket.send(line[sent:])
    
    def auth(self, mechanism='', initial_response=''):
        self._send(auth(mechanism, initial_response))

    def cancel(self):
        self._send(cancel())

    def data(self, hex_data):
        self._send(data(hex_data))

    def begin(self):
        self._send(begin())

    def error(self, msg):
        self._send(error(msg))

    def handle_one(self):
        chunk = ''
        while True:
            chunk = self.socket.recv(1024)
            if '\r\n' in chunk:
                line, self._buf = (self._buf + chunk).split('\r\n', 1)
                return self.handle_line(line)

    def handle_line(self, line):
        verb = line.split(' ')[0]
        if verb not in HANDLERS:
            raise AuthError('Unknown verb received: %s' % verb)
        return HANDLERS[verb](self, line)

    def get_mechanisms(self):
        self.auth()
        try:
            self.handle_one()
        except RejectedError, e:
            return e.mechanisms
        else:
            raise AuthError("eek? authentication was successful?")
    
    @handler('REJECTED')
    def handle_rejected(self, line):
        mechanisms = line.split(' ')[1:]
        self.mechanisms = mechanisms
        raise RejectedError(mechanisms)

    @handler('OK')
    def handle_ok(self, line):
        self.guid = line.split(' ', 1)[1]
        self.ok = True
        return 'OK'

    @handler('DATA')
    def handle_data(self, line):
        self.data_received.append(line.split(' ', 1)[1])
        return 'DATA'

    @handler('ERROR')
    def handle_error(self, line):
        raise AuthError('Error: "%s"' % line)

    def auth_dbus_cookie_sha1(self, username):
        self.auth('DBUS_COOKIE_SHA1', hexlify(username))
        if self.handle_one() != 'DATA':
            raise AuthError("Bus doesn't like DBUS_COOKIE_SHA1")
        data = dbus_cookie_sha1.handle_auth_line(
                unhexlify(self.data_received.pop(-1)))
        self.data(data)
        if self.handle_one() != 'OK':
            raise AuthError("DBUS_COOKIE_SHA1 authentication failed")
        self.begin()

