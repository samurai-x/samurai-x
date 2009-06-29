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

from __future__ import with_statement

import os
import socket
import re
from getpass import getuser

from . import protocol
from .introspection import parse_introspection
from .proxy import ProxyObject
from .protocol import Message
from .service import Object, Interface
from .streams import SocketStream
from .matchrules import MatchRule
from .auth import AuthHandler

class SessionError(Exception):
    pass

class DBusException(Exception):
    def __init__(self, name, description=''):
        self.name = name
        self.description = description

    def __str__(self):
        return '%s: %s' % (self.name, self.description)

DBUS_NAME_FLAG_ALLOW_REPLACEMENT = 0x1
DBUS_NAME_FLAG_REPLACE_EXISTING = 0x2
DBUS_NAME_FLAG_DO_NOT_QUEUE = 0x4

DBUS_REQUEST_NAME_REPLY_PRIMARY_OWNER = 1
DBUS_REQUEST_NAME_REPLY_IN_QUEUE = 2
DBUS_REQUEST_NAME_REPLY_EXISTS = 3
DBUS_REQUEST_NAME_REPLY_ALREADY_OWNER = 4

class Bus(object):
    def __init__(self, path):
        self.address = None
        self.guid = None
        self.path = None
        self.unique_name = ''
        self.bus_names = []
        self.signal_handlers = {} # {(path, member, interface): [func, func]}
        self.objects = {}
        self.interfaces = {}
        
        self.socket = None
        self.socket_stream = None
        self.calls = {}
        self.replies = {}
        self.type = ''
        self._parse_path(path)
        self.connect()

    def make_object(self, name, cls=Object):
        ret = self.objects[name] = cls(self, name)
        return ret

    def request_name(self, name, allow_replacement=True, replace_existing=True, do_not_queue=False):
        """
            returns True if self could get the name.
        """
        flags = 0
        if allow_replacement:
            flags |= DBUS_NAME_FLAG_ALLOW_REPLACEMENT
        if replace_existing:
            flags |= DBUS_NAME_FLAG_REPLACE_EXISTING
        if do_not_queue:
            flags |= DBUS_NAME_FLAG_DO_NOT_QUEUE
        code = self.proxy.RequestName(name, flags)
        if code in (DBUS_REQUEST_NAME_REPLY_PRIMARY_OWNER,
                DBUS_REQUEST_NAME_REPLY_ALREADY_OWNER):
            self.bus_names.append(name)
            return True
        else:
            # TODO: should raise an exception?
            return False

    def _parse_path(self, path):
        for elem in path.split(','):
            key, value = elem.split('=')
            if key == 'unix':
                self.address = value
                self.type = 'unix'
            elif key == 'unix:abstract':
                self.address = '\x00' + value
                self.type = 'unix:abstract'
            elif key == 'guid':
                self.guid = value
            else:
                raise SessionError("Unknown key/value pair: %r=%r" % (key, value))

    def fileno(self):
        """
            returns socket's file descriptor to make `select` happy.
        """
        return self.socket.fileno()

    def get_reply_by_serial(self, serial):
        while serial not in self.replies:
            self.receive_one()
        return self.replies.pop(serial)

    def get_reply(self, msg):
        del self.calls[msg.serial]
        return self.get_reply_by_serial(msg.serial)

    def get_object(self, path, destination, introspect=True):
        return ProxyObject(self, path, destination, introspect)

    def make_interface(self, interface):
        if interface not in self.interfaces:
            self.interfaces[interface] = Interface(self, interface)
        return self.interfaces[interface]

    def add_match(self, matchrule):
        self.proxy.AddMatch(matchrule.to_dbus())

    def remove_match(self, matchrule):
        self.proxy.RemoveMatch(matchrule.to_dbus())

    def add_signal_handler(self, path, member, interface, func):
        self.signal_handlers.setdefault((path, member, interface), []).append(func)
        # register a match rule ...
        self.add_match(MatchRule(
            type='signal',
            path=path,
            member=member
            ))

    def signal_handler(self, path, member, interface):
        def deco(func):
            self.add_signal_handler(path, member, interface, func)
            return func
        return deco

    def remove_signal_handler(self, path, member, interface, func):
        info = (path, member, interface)
        if info in self.signal_handlers:
            self.signal_handlers[info].remove(func)
        self.remove_match(MatchRule(
            type='signal',
            path=path,
            member=member
            ))

    def dispatch_signal(self, msg):
        info = (msg.path, msg.member, msg.interface)
        if info not in self.signal_handlers:
            return False
        for func in reversed(self.signal_handlers[info]):
            if func(msg):
                return
        
    def connect(self):
        # Doesn't need to be locked because it happens
        # in the initialization.
        if self.type in ('unix', 'unix:abstract'):
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.socket.connect(self.address)
        else:
            raise SessionError("Unknown connection type: %r" % self.type)
        self.socket.setblocking(1)
        self.socket.sendall('\0')
        self.socket_stream = SocketStream(self.socket.fileno())
        self.auth()

        self.send_hello()
        # after having sent the Hello, we can use Introspect and create
        # a nice proxy object!
        self.proxy = self.get_object('/org/freedesktop/DBus', 'org.freedesktop.DBus')

    def send_hello(self):
        reply = self.send_method_call_sync(
                path='/org/freedesktop/DBus',
                destination='org.freedesktop.DBus',
                interface='org.freedesktop.DBus',
                member='Hello',
                )
        self.unique_name = reply.body[0]
        self.bus_names.append(self.unique_name)

    def send_method_return(self, msg, signature, body):
        msg = Message(
                type=protocol.METHOD_RETURN,
                serial=protocol.SERIALS.next(), # TODO: want one?
                reply_serial=msg.serial,
                destination=msg.sender,
                signature=signature,
                body=body,
                )
        if signature:
            msg.marshal_body()
        self.send(msg)
        return msg

    def send_signal(self, path, interface, signal, signature='', body=()):
        serial = protocol.SERIALS.next()
        msg = Message(
                type=protocol.SIGNAL,
                serial=serial,
                path=path,
                interface=interface,
                member=signal,
                signature=signature,
                body=body)
        if signature:
            msg.marshal_body()
        self.send(msg)
        return msg

    def send_method_call(self, path, destination, member, interface='', signature='', body=()):
        serial = protocol.SERIALS.next()
        msg = Message(
                type=protocol.METHOD_CALL,
                serial=serial,
                path=path,
                interface=interface,
                destination=destination,
                member=member,
                signature=signature,
                body=body
                )
        if signature:
            msg.marshal_body()
        self.calls[serial] = msg
        self.send(msg)
        return msg

    def send_method_call_sync(self, *args, **kwargs):
        return self.get_reply(self.send_method_call(*args, **kwargs))

    def send_error(self, msg, name, description=''):
        signature = ''
        body = ()
        if description:
            signature = 's'
            body = (description,)
        error = Message(
                type=protocol.ERROR,
                reply_serial=msg.serial,
                serial=protocol.SERIALS.next(), # do we need any?
                destination=msg.sender,
                error_name=name,
                signature=signature,
                body=body
                )
        self.send(error)
        return error

    def dispatch_call(self, msg):
        path = msg.path
        try:
            return self.objects[path].dispatch_call(msg)
            # TODO: catch keyerror
        except DBusException, e:
            seld.send_error(msg, e.name, e.description)

    def send(self, msg):
        self.socket.sendall(msg.marshal_simple())

    def auth(self):
        """
            authenticate.
        """
        au = AuthHandler(self.socket)
        mechanisms = au.get_mechanisms()
        if 'DBUS_COOKIE_SHA1' in mechanisms:
            au.auth_dbus_cookie_sha1(getuser())
        else:
            raise NotImplementedError("No implemented auth mechanisms available: %r" % mechanisms)

    def receive_one(self):
        self.socket_stream.reset_count()
        msg = Message.create_from_socketstream(self.socket_stream)
        if msg.type == protocol.METHOD_RETURN:
            self.replies[msg.reply_serial] = msg
        elif msg.type == protocol.SIGNAL:
            self.dispatch_signal(msg)
        elif msg.type == protocol.ERROR:
            self.raise_error(msg)
        elif msg.type == protocol.METHOD_CALL:
            self.dispatch_call(msg)
        else:
            print vars(msg)
            print 'Unknown message type'

    def raise_error(self, msg):
        name = msg.error_name
        description = '(no description given)'
        if (len(msg.body) == 1 and isinstance(msg.body, basestring)):
            description = msg.body[0]
        raise DBusException(name, description)

    def introspect(self, path, destination):
        return parse_introspection(path,
                    self.send_method_call_sync(
                    path,
                    destination,
                    'Introspect',
                    'org.freedesktop.DBus.Introspectable',
                    ).body[0])

SESSION_PATH_VAR = "DBUS_SESSION_BUS_ADDRESS"
SESSION_FILE = os.path.expanduser('~/.dbus/session-bus/%s-%d')
DISPLAY_REGEX = r'([^:]+)*:{1,2}(\d+)(?:\.(\d+))?'
MACHINE_ID_FILE = '/var/lib/dbus/machine-id'

def get_session_bus_path_from_file(filename):
    with open(filename, 'r') as f:
        for line in f.xreadlines():
            if line.startswith(SESSION_PATH_VAR):
                var, value = line.split('=', 1)
                return value
    raise SessionError("No session bus address found in %s" % filename)

def get_machine_id():
    """
        return the id of the machine.
        We could also use `dbus-uuidgen`.
    """
    with open(MACHINE_ID_FILE, 'r') as f:
        return f.read().strip()

def parse_display(display):
    all = re.findall(DISPLAY_REGEX, display)
    matches = all[0]
    if matches[0]:
        raise NotImplementedError('foreign servers not yet implemented')
    host = ''
    number = int(matches[1])
    screen = 0
    if matches[2]:
        screen = int(matches[2])
    return (host, number, screen)

def get_display_id():
    return parse_display(os.environ["DISPLAY"])[1]

def get_session_bus_path():
    if SESSION_PATH_VAR in os.environ:
        return os.environ[SESSION_PATH_VAR]
    else:
        machine = get_machine_id()
        display = get_display_id()
        return get_session_bus_path_from_file(SESSION_FILE % (machine, display))

class SessionBus(Bus):
    def __init__(self):
        Bus.__init__(self, get_session_bus_path())

