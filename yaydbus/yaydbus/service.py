import inspect

from types import FunctionType

from . import introspection
from .dbus_types import get_signature
from .matchrules import MatchRule

class MethodError(Exception):
    pass

def get_signature_from_annotations(func, get_in=True, get_out=True):
    try:
        annotations = func.func_annotations
    except AttributeError:
        raise MethodError("Exported methods need function annotations.")
    args, varargs, varkw, defaults = inspect.getargspec(func)
    if varargs or varkw:
        raise MethodError("Exported methods can't have varargs or varkws.")
    in_signature = ''
    if get_in:
        for arg in args:
            if arg not in annotations:
                raise MethodError("Missing annotation for %s!" % arg)
            else:
                in_signature += get_signature(annotations[arg])
    if get_out:
        try:
            out_signature = annotations['return']
        except KeyError:
            raise MethodError("Missing annotation for return type!")
    return (in_signature, out_signature)
    
class Method(object):
    def __init__(self, callable, name=None, in_signature=None, out_signature=None):
        if name is None:
            name = callable.__name__
        self.name = name
        self.callable = callable
        self.introspection = introspection.Method(name, [], [])
        if (in_signature is None or out_signature is None):
            in_s, out_s = get_signature_from_annotations(callable, in_signature is None, out_signature is None)
            if in_signature is None:
                in_signature = in_s
            if out_signature is None:
                out_signature = out_s
        self.in_signature = in_signature
        self.out_signature = out_signature

    def call(self, obj, msg):
        assert msg.signature == self.in_signature
        ret = self.callable(obj, *msg.body)
        return (ret,)

class Interface(object):
    def __init__(self, name):
        self.name = name
        self.introspection = introspection.Interface(name, [])

class ObjectMeta(type):
    def __new__(mcs, name, bases, dct):
        dct['_methods'] = []
        for name, member in dct.iteritems():
            if hasattr(member, '_dbus_method'):
                dct['_methods'].append((member._dbus_interface, member._dbus_method))
                del member._dbus_method
                del member._dbus_interface
        return type.__new__(mcs, name, bases, dct)

class Interface(object):
    def __init__(self, bus, name):
        self.bus = bus
        self.name = name
        self.members = {}

    def add_member(self, member):
        self.members[member.name] = member

class Object(object):
    __metaclass__ = ObjectMeta

    def __init__(self, bus, path):
        self._bus = bus
        self._path = path
        self._interfaces = set()
        self._register()

    def _register(self):
        # register a match rule
        self._bus.add_match(MatchRule(path=self._path))
        # register all methods
        for interface_name, method in type(self)._methods:
            interface = self._bus.make_interface(interface_name)
            interface.add_member(method)
            # now we're implementing a method from this interface!
            self._interfaces.add(interface)

    def get_interface_implementing(self, name):
        for interface in self._interfaces:
            if name in interface.members:
                return interface
        return None

    def dispatch_call(self, msg):
        name = msg.member
        interface = self.get_interface_implementing(name)
        assert interface
        member = interface.members[name]
        self._bus.send_method_return(msg, member.out_signature, member.call(self, msg))

def method(interface, name=None, in_signature=None, out_signature=None):
    def deco(func):
        func._dbus_method = Method(func, name, in_signature, out_signature)
        func._dbus_interface = interface
        return func
    return deco

