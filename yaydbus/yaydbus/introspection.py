from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from .protocol import join_path, get_surname

class IntrospectionError(Exception):
    pass

DOCTYPE = """<!DOCTYPE node PUBLIC "-//freedesktop//DTD D-BUS Object Introspection 1.0//EN"
"http://www.freedesktop.org/standards/dbus/1.0/introspect.dtd">"""

class Interface(object):
    def __init__(self, name, members):
        self.name = name
        self.members = members

    def __repr__(self):
        return '<Interface "%s" at 0x%x>' % (self.name, id(self))

    def to_xml(self):
        element = Element('interface', name=self.name)
        for member in self.members:
            element.append(member.to_xml())
        return element

    def get_method(self, name):
        for member in self.members:
            if (isinstance(member, Method) and member.name == name):
                return member
        return None

class Argument(object):
    def __init__(self, name, type, direction):
        self.name = name
        self.type = type
        self.direction = direction

    def __repr__(self):
        if self.name is not None:
            return '<Argument "%s" ("%s", "%s") at 0x%x>' % (self.name,
                    self.type, self.direction, id(self))
        else:
            return '<Unnamed Argument ("%s", "%s") at 0x%x>' % (
                    self.type, self.direction, id(self))

    def to_xml(self):
        element = Element('arg',
            type=self.type,
            direction=self.direction)
        if self.name is not None:
            element.attrib['name'] = self.name
        return element

class MethodArgument(Argument):
    def __init__(self, name, type, direction):
        if direction is None:
            direction = 'out'
        Argument.__init__(self, name, type, direction)

class SignalArgument(Argument):
    def __init__(self, name, type, direction):
        if direction is None:
            direction = 'in'
        Argument.__init__(self, name, type, direction)

class Method(object):
    def __init__(self, name, args, annotations):
        self.name = name
        self.args = args
        self.annotations = annotations

    def __repr__(self):
        return '<Method "%s" at 0x%x>' % (self.name, id(self))

    def get_input_signature(self):
        return ''.join(arg.type for arg in self.args if arg.direction == 'in')

    def to_xml(self):
        element = Element('method', name=self.name)
        for arg in self.args:
            element.append(arg.to_xml())
        for name, value in self.annotations.iteritems():
            element.append(
                    Element('annotation',
                        name=name,
                        value=value
                        )
                    )
        return element

class Signal(object):
    def __init__(self, name, args, annotations):
        self.name = name
        self.args = args
        self.annotations = annotations

    def __repr__(self):
        return '<Signal "%s" at 0x%x>' % (self.name, id(self))

    def to_xml(self):
        element = Element('signal', name=self.name)
        for arg in self.args:
            element.append(arg.to_xml())
        for name, value in self.annotations.iteritems():
            element.append(
                    Element('annotation',
                        name=name,
                        value=value
                        )
                    )
        return element

class Property(object):
    def __init__(self, name, type, access):
        self.name = name
        self.type = type
        self.access = access

    def __repr__(self):
        return '<Property "%s" at 0x%x>' % (self.name, id(self))

    def to_xml(self):
        return Element('property',
                name=self.name,
                type=self.type,
                access=self.access
                )

class Node(object):
    def __init__(self, name, interfaces=None, nodes=None):
        self.name = name
        if interfaces is None:
            interfaces = []
        if nodes is None:
            nodes = []
        self.interfaces = interfaces
        self.nodes = nodes
    
    def __repr__(self):
        if self.name is None:
            return '<Unnamed Node at 0x%x>' % id(self)
        else:
            return '<Node "%s" at 0x%x>' % (self.name, id(self))

    def to_xml(self):
        element = Element('node')
        if self.name is not None:
            element.attrib['name'] = self.name
        for interface in self.interfaces:
            element.append(interface.to_xml())
        return element

    def get_method(self, name):
        for interface in self.interfaces:
            member = interface.get_method(name)
            if member is not None:
                return member
        return None

    def get_interface_implementing_method(self, name):
        for interface in self.interfaces:
            member = interface.get_method(name)
            if member is not None:
                return interface
        return None

    def get_node(self, surname):
        for node in self.nodes:
            if get_surname(node.name) == surname:
                return node
        return None

    @property
    def valid(self):
        return bool(self.interfaces) or bool(self.nodes)

def parse_arg(element, cls=MethodArgument):
    name = element.attrib.get('name')
    type = element.attrib['type']
    direction = element.attrib.get('direction')
    return cls(name, type, direction)

def _parse_member_children(element, cls, argcls):
    name = element.attrib['name']
    args = []
    annotations = {}
    for child in element.getchildren():
        if child.tag == 'arg':
            args.append(parse_arg(child, argcls))
        elif child.tag == 'annotation':
            annotations[child.attrib['name']] = child.attrib['value']
        else:
            raise IntrospectionError('Unknown tag: "%s"' % child.tag)
    return cls(name, args, annotations)

def parse_method(element):
    return _parse_member_children(element, Method, MethodArgument)

def parse_signal(element):
    return _parse_member_children(element, Signal, SignalArgument)

def parse_property(element):
    name = element.attrib['name']
    type = element.attrib['type']
    access = element.attrib['access']
    return Property(name, type, access)

INTERFACE_MEMBER_PARSERS = {
        'method': parse_method,
        'signal': parse_signal,
        'property': parse_property
        }

def parse_interface(element):
    name = element.attrib['name']
    members = []
    for child in element.getchildren():
        members.append(INTERFACE_MEMBER_PARSERS[child.tag](child))
    return Interface(name, members)

def parse_node(element, is_root=False, firstname=''):
    name = element.attrib.get('name', None)
    # name is optional the root node
    if (name is None and not is_root):
        raise IntrospectionError('Malformed XML data: non-root <node> has no name attribute')
    if name is None:
        name = firstname
    else:
        name = join_path(firstname, name)
    interfaces = []
    nodes = []
    for element in element.getchildren():
        if element.tag == 'interface':
            interfaces.append(parse_interface(element))
        elif element.tag == 'node':
            nodes.append(parse_node(element, firstname=name))
        else:
            raise IntrospectionError("Unknown child: '%s'" % element.tag)
    return Node(name, interfaces, nodes)

def parse_introspection(firstname, data):
    root = ElementTree.fromstring(data)
    return parse_node(root, True, firstname)

def indent(elem, level=0):
    """
        a nice indentation helper function for prettier xml,
        taken from http://infix.se/2007/02/06/gentlemen-indent-your-xml
        Thank you!
    """
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "  "
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def to_string(node):
    element = node.to_xml()
    indent(element)
    return DOCTYPE + "\n" + ElementTree.tostring(element)

