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

import inspect

from types import FunctionType

from . import introspection
from .marshal import parse_signature
from .dbus_types import get_signature
from .matchrules import MatchRule

class MethodError(Exception):
    pass

def _get_signature_lazily(s):
    if isinstance(s, basestring):
        return s
    else:
        return get_signature(s)

def get_signature_from_annotations(func, get_in=True, get_out=True):
    try:
        annotations = func.func_annotations
    except AttributeError:
        raise MethodError("Exported methods need function annotations.")
    args, varargs, varkw, defaults = inspect.getargspec(func)
    if varargs or varkw:
        raise MethodError("Exported methods can't have varargs or varkws.")
    in_signature = ''
    out_signature = ''
    if get_in:
        for arg in args[1:]: # skip `self`
            if arg not in annotations:
                raise MethodError("Missing annotation for %s!" % arg)
            else:
                in_signature += _get_signature_lazily(annotations[arg])
    if get_out:
        try:
            out_signature = _get_signature_lazily(annotations['return'])
        except KeyError:
            #raise MethodError("Missing annotation for return type!")
            # If the return value is left out, the method does not
            # have a return type.
            pass
    return (in_signature, out_signature)

class Introspectable(object):
    @property
    def introspection(self):
        if self._introspection is None:
            self.update_introspection()
        return self._introspection

    def update_introspection(self):
        raise NotImplementedError()
    
class Method(Introspectable):
    def __init__(self, callable, name=None, in_signature=None, out_signature=None, annotations=None):
        if name is None:
            name = callable.__name__
        if annotations is None:
            annotations = {}
        if hasattr(callable, '_dbus_annotations'):
            annotations.update(getattr(callable, '_dbus_annotations'))
        self.name = name
        self.callable = callable
        if in_signature is None:
            if len(inspect.getargspec(callable)[0]) == 1: # no args except self, no in_signature
                in_signature = ''
        if (in_signature is None or out_signature is None):
            in_s, out_s = get_signature_from_annotations(callable, in_signature is None, out_signature is None)
            if in_signature is None:
                in_signature = in_s
            if out_signature is None:
                out_signature = out_s
        self.in_signature = in_signature
        self.out_signature = out_signature
        self.annotations = annotations
        self._introspection = None
        self.update_introspection()

    def update_introspection(self):
        # get the introspection object
        in_args_dbuscodes = [m.dbuscode for m in parse_signature(self.in_signature).marshallers]
        in_args_names = inspect.getargspec(self.callable)[0][1:] # TODO: default arguments and stuff
        args = []
        for dbuscode, name in zip(in_args_dbuscodes, in_args_names):
            args.append(introspection.MethodArgument(name, dbuscode, 'in'))
        if self.out_signature:
            args.append(introspection.MethodArgument(None, parse_signature(self.out_signature).dbuscode, 'out'))
        self._introspection = introspection.Method(self.name, args, self.annotations)

    def call(self, obj, msg):
        assert msg.signature == self.in_signature
        ret = self.callable(obj, *msg.body)
        return (ret,)

class Signal(Introspectable):
    def __init__(self, callable, name=None, signature=None, annotations=None):
        if name is None:
            name = callable.__name__
        if annotations is None:
            annotations = {}
        if hasattr(callable, '_dbus_annotations'):
            annotations.update(getattr(callable, '_dbus_annotations'))
        if signature is None:
            signature, _ = get_signature_from_annotations(callable, True, False)
        self.name = name
        self.callable = callable
        self.signature = signature
        self.annotations = annotations
        self._introspection = None
        self.update_introspection()

    def update_introspection(self):
        # get the introspection object
        args = [introspection.SignalArgument(None, t.dbuscode, 'out')
                for t in  parse_signature(self.signature).marshallers]
        self._introspection = introspection.Method(self.name, args, self.annotations)

    def __call__(self, obj, *args, **kwargs):
        assert not kwargs # TODO
        try:
            self.callable(obj, *args)
        except:
            raise
        else:
            # successful.
            obj.emit_signal(self, args)

class ObjectMeta(type):
    def __new__(mcs, clsname, bases, dct):
        methods = []
        for base in bases:
            if hasattr(base, '_methods'):
                methods.extend(base._methods)
        for name, member in dct.iteritems():
            if hasattr(member, '_dbus_method'):
                methods.append((member._dbus_interface, member._dbus_method))
                del member._dbus_method
                del member._dbus_interface
            if hasattr(member, '_dbus_signal'):
                methods.append((member._dbus_interface, member._dbus_signal))
                del member._dbus_signal
                del member._dbus_interface
        dct['_methods'] = methods
        return type.__new__(mcs, clsname, bases, dct)

class Interface(Introspectable):
    def __init__(self, bus, name):
        self.bus = bus
        self.name = name
        self.members = {}
        self._introspection = None

    def update_introspection(self):
        self._introspection = introspection.Interface(self.name,
                [m.introspection for m in self.members.itervalues()])

    def add_member(self, member):
        self.members[member.name] = member

def method(interface, name=None, in_signature=None, out_signature=None):
    def deco(func):
        func._dbus_method = Method(func, name, in_signature, out_signature)
        func._dbus_interface = interface
        return func
    return deco

def signal(interface, name=None, signature=None):
    def deco(func):
        signal = Signal(func, name, signature)
        def f(*args, **kwargs):
            return signal(*args, **kwargs)
        f._dbus_signal = signal
        f._dbus_interface = interface
        return f
    return deco

def dbus_annotation(key, value):
    def deco(func):
        if not hasattr(func, '_dbus_annotations'):
            func._dbus_annotations = {}
        func._dbus_annotations[key] = value
        return func
    return deco

class Object(Introspectable):
    __metaclass__ = ObjectMeta

    def __init__(self, bus, path):
        self._bus = bus
        self._path = path
        self._interfaces = set()
        self._register()
        self._introspection = None

    def _register(self):
        # register a match rule
        self._bus.add_match(MatchRule(path=self._path))
        # register all methods
        for interface_name, method in type(self)._methods:
            interface = self._bus.make_interface(interface_name)
            interface.add_member(method)
            # now we're implementing a method from this interface!
            self._interfaces.add(interface)

    def update_introspection(self):
        self._introspection = introspection.Node(self._path,
                [m.introspection for m in self._interfaces])

    def emit_signal(self, signal, args):
        interface = self.get_interface_implementing(signal.name)
        assert interface, "no interface implementing %s - wtf?" % signal.name
        self._bus.send_signal(
                self._path,
                interface.name,
                signal.name,
                signal.signature,
                args)

    def get_interface_implementing(self, name):
        for interface in self._interfaces:
            if name in interface.members:
                return interface
        return None

    def dispatch_call(self, msg):
        name = msg.member
        interface = self.get_interface_implementing(name)
        assert interface, "couldnt find %s" % name 
        member = interface.members[name]
        self._bus.send_method_return(msg, member.out_signature, member.call(self, msg))

    @method('org.freedesktop.DBus.Introspectable', in_signature='', out_signature='s')
    def Introspect(self):
        return introspection.to_string(self.introspection)
