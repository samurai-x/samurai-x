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

from .marshal import parse_signature
from .protocol import join_path
from .dbus_types import get_signature

class ProxyError(Exception):
    pass

class ProxyMethod(object):
    def __init__(self, bus, path, destination):
        self.bus = bus
        self.path = path
        self.destination = destination
        self.interface = destination

    def async(self, *args, **kwargs):
        raise NotImplementedError()

    def __call__(self, *args, **kwargs):
        ret = self.bus.get_reply(self.async(*args, **kwargs)).body
        if ret:
            assert len(ret) == 1
            return ret[0]
        else:
            return None

class SillyProxyMethod(ProxyMethod):
    def __init__(self, bus, path, destination, name):
        ProxyMethod.__init__(self, bus, path, destination)
        self.name = name
        self.signature = None

    def async(self, *args, **kwargs):
        interface = self.interface
        if '__interface__' in kwargs:
            interface = kwargs.pop('__interface__')
        if kwargs:
            raise ProxyError("silly proxy methods don't support keyword arguments.")
        # if we have no signature set, try to guess it from the arguments
        if self.signature is None:
            self.signature = ''.join(map(get_signature, map(type, args)))
        return self.bus.send_method_call(
                self.path,
                self.destination,
                self.name,
                interface,
                self.signature,
                args
                )

class IntrospectableProxyMethod(ProxyMethod):
    def __init__(self, bus, path, destination, method):
        ProxyMethod.__init__(self, bus, path, destination)
        self.method = method

    def async(self, *py_args, **kwargs):
        interface = self.interface
        if '__interface__' in kwargs:
            interface = kwargs.pop('__interface__')
        if kwargs:
            raise ProxyError("introspectable proxy methods don't support keyword arguments (yet)")
        signature = self.method.get_input_signature()
        if len(self.method.get_arguments('in')) != len(py_args):
            raise ProxyError("You passed an incorrect number of arguments (required: %d, got: %d)" % (
                len(self.method.get_arguments('in')), len(py_args)))
        return self.bus.send_method_call(
                self.path,
                self.destination,
                self.method.name,
                interface,
                signature,
                py_args
                )

class ProxyObject(object):
    def __init__(self, bus, path, destination, introspect=True):
        self._bus = bus
        self._path = path
        self._destination = destination
        if introspect:
            self._node = bus.introspect(self._path, self._destination)
            self._valid_introspection = self._node.valid
        else:
            self._node = None
            self._valid_introspection = False

    def __getattr__(self, name):
        proxy = None
        # Do we have introspeeeection?
        if self._valid_introspection:
            method = self._node.get_method(name)
            # has a method!
            if method is not None:
                interface = self._node.get_interface_implementing_method(name).name
                proxy = IntrospectableProxyMethod(self._bus, self._path, self._destination, method)
            else:
                node = self._node.get_node(name)
                # has a node!
                if node is not None:
                    # TODO: if there is introspection data included, why not use it?
                    proxy = ProxyObject(
                            self._bus,
                            join_path(self.path, name),
                            destination,
                            )
                else:
                    raise ProxyError("No such subproxy: '%s'" % name)
        # No! We are silly!
        else:
            # Let's guess it's a method.
            proxy = SillyProxyMethod(self._bus, self._path, self._destination, name)
        setattr(self, name, proxy)
        return proxy

    def get_bound(self, interface):
        return BoundInterfaceProxy(self._bus, self, interface)

    def add_signal_handler(self, member, interface, func):
        self._bus.add_signal_handler(self._path, member, interface, func)

    def remove_signal_handler(self, member, interface, func):
        self._bus.remove_signal_handler(self._path, member, interface, func)

    def signal_handler(self, member, interface):
        return self._bus.signal_handler(self._path, member, interface)

class BoundInterfaceProxy(object):
    def __init__(self, bus, proxy, interface):
        self._bus = bus
        self._proxy = proxy
        self._interface = interface

    def __getattr__(self, name):
        p = self._proxy.__getattr__(name)
        p.interface = self._interface
        return p

    def add_signal_handler(self, member, func):
        self._proxy.add_signal_handler(member, self._interface, func)

    def remove_signal_handler(self, member, interface, func):
        self._proxy.remove_signal_handler(member, self._interface, func)

    def signal_handler(self, wtf):
        if isinstance(wtf, basestring):
            return self._proxy.signal_handler(wtf, self._interface)
        else:
            self.add_signal_handler(wtf.__name__, wtf)
            return wtf

