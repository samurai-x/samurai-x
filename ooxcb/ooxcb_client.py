#!/usr/bin/env python

import sys
import re

import yaml

import wraplib
from wraplib.struct import Struct
from wraplib.names import prefix_if_needed
from wraplib.utils import pythonize_camelcase_name
from wraplib.codegen import Codegen, INDENT, DEDENT
from wraplib.pymember import PyMethod, PyClassMethod, PyAttribute
from wraplib.template import template
from wraplib.pyclass import PyClass

# setup yaml
def construct_indent(loader, node):
    return INDENT

def construct_dedent(loader, node):
    return DEDENT

def construct_xizer(loader, node):
    ident = loader.construct_scalar(node)
    return lambda ident=ident: XIZERS[ident]

yaml.add_constructor('!indent', construct_indent)
yaml.add_constructor('!dedent', construct_dedent)
yaml.add_constructor('!xizer', construct_xizer)


_pyname_except_re = re.compile('^Bad') # regular expression for Exceptions
CARDINAL_TYPES = {'CARD8':  'B', 'uint8_t': 'B',
                   'CARD16': 'H','uint16_t': 'H',
                   'CARD32': 'I','uint32_t': 'I',
                   'INT8':   'b', 'int8_t':  'b',
                   'INT16':  'h', 'int16_t': 'h',
                   'INT32':  'i', 'int32_t': 'i',
                   'BYTE': 'B',
                   'BOOL': 'B',
                   'char': 'b',
#                   'void': 'B',
                   'float': 'f',
                   'double' : 'd'}
MODIFIERS = {'resource': 'conn.get_from_cache_fallback(%%s, %s)'}

py = Codegen()

NAMESPACE = None
ALL = {} # contains classes, functions, globals ...
WRAPPERS = {}

ERRORS = {} # {Opcode: (Blargh, Blargh)} - no idea what.
EVENTS = {} # {Opcode: classname}

def is_ignored(tup):
    return strip_ns(tup) in INTERFACE.get('Ignored', [])

def get_custom_classes():
    return INTERFACE.get('Classes', {})

def pythonize_classname(name):
    return INTERFACE.get('ClassAliases', {}).get(name, name.capitalize())

def pythonize_name(name):
    return INTERFACE.get('NameAliases', None) or pythonize_camelcase_name(name)

def get_request_info(name):
    return INTERFACE.get('Requests', {}).get(name, {})

def strip_ns(tup):
    """
        ('xcb', 'foo') -> 'foo'
    """
    return tup[-1]

def get_field_by_name(fields, name):
    for field in fields:
        if prefix_if_needed(field.field_name) == name:
            return field
    raise KeyError('No field named "%s" found!' % name)
    
def get_wrapped(name):
    if name in WRAPPERS:
        return WRAPPERS[name].name
    else:
        return name

def get_modifier(field):
    if field.py_type in INTERFACE.get('ResourceClasses', []):
        return MODIFIERS['resource'] % get_wrapped(field.py_type)
    elif field.py_type in MODIFIERS:
        return MODIFIERS.get(field.py_type, None)
    elif field.py_type in WRAPPERS:
        return '%s(conn, %%s)' % WRAPPERS[field.py_type].name
    else:
        return '%s'

# --- xizers

def make_seq_xizer(seq_in='value', seq_out='value', length_out='value_len'):
    code = []
    code.append(template('$length_out = len($seq_in)', length_out=length_out, seq_in=seq_in))
    if seq_in != seq_out:
        code.append(template('$seq_out = $seq_in', seq_out=seq_out, seq_in=seq_in))
    return lambda code=code: code

def make_lazy_atom_xizer(name, conn='self.conn'):
    code = []
    code.append(template("if isinstance($name, basestring):", name=name))
    code.append(INDENT)
    code.append(template("$name = $conn.atoms[$name]", conn=conn, name=name))
    code.append(DEDENT)
    return lambda code=code: code

def make_values_xizer(enum_name, values_dict_name, mask_out='value_mask', list_out='value_list', xize=[]):
    """ 
        make a simple values xizer code list and return it.
        A values xizer takes all values from the values dict
        and stores it in a values list and a values mask.
    """
    enum = ALL[enum_name]
    code = []
    pyvalues = []

    code.append(template("$mask_out, $list_out = 0, []",
        mask_out=mask_out,
        list_out=list_out
        ))
    for member in enum.members:#key, value in enum.values:
        if not isinstance(member, PyAttribute):
            continue

        key = pythonize_camelcase_name(member.name)
        value = member.value
        code.append(template('if "${key}" in ${values_dict_name}:',
                    key=key,
                    values_dict_name=values_dict_name))
        code.append(INDENT)
        code.append(template('$mask_out |= $value',
            mask_out=mask_out,
            value=value
            ))

        suffix = ''
        if key in xize:
            suffix += '.get_internal()'

        code.append(template('$list_out.append($values_dict_name["$key"]$suffix)',
            list_out=list_out,
            values_dict_name=values_dict_name,
            key=key,
            suffix=suffix
            ))
        code.append(DEDENT)
    
    return lambda code=code: code 

XIZER_MAKERS = {'values': make_values_xizer,
        'seq': make_seq_xizer,
        'lazy_atom': make_lazy_atom_xizer}
XIZERS = {}

def get_length_field(expr):
    '''
    Figures out what C code is needed to get a length field.
    For fields that follow a variable-length field, use the accessor.
    Otherwise, just reference the structure field directly.
    '''
    if expr.lenfield_name != None:
        return 'self.%s' % expr.lenfield_name
    else:
        return str(expr.nmemb)

def setup_type(self, name, postfix=''):
    '''
    Sets up all the C-related state by adding additional data fields to
    all Field and Type objects.  Here is where we figure out most of our
    variable and function names.

    Recurses into child fields and list member types.
    '''
    self.py_type = strip_ns(name) + postfix

    self.py_request_name = strip_ns(name)
    self.py_checked_name = strip_ns(name) + 'Checked'
    self.py_unchecked_name = strip_ns(name) + 'Unchecked'
    self.py_reply_name = strip_ns(name) + 'Reply'
    self.py_event_name = strip_ns(name) + 'Event'
    self.py_cookie_name = strip_ns(name) + 'Cookie'

    if _pyname_except_re.match(strip_ns(name)):
        self.py_error_name = strip_ns(name).replace('Bad') + 'Error'
        self.py_except_name = strip_ns(name)
    else:
        self.py_error_name = strip_ns(name) + 'Error'
        self.py_except_name = 'Bad' + strip_ns(name)

    if self.is_pad:
        self.py_format_str = 'x' * self.nmemb # TODO: not using struct's multipliers. ok?
        self.py_format_len = 0

    elif self.is_simple or self.is_expr:
        # so, it's simple. it may be a wrapped object. check.
        self.py_format_str = CARDINAL_TYPES[strip_ns(self.name)]
        self.py_format_len = 1
    elif self.is_list:
        if self.fixed_size():
            self.py_format_str = str(self.nmemb) + CARDINAL_TYPES[strip_ns(self.member.name)]
            self.py_format_len = self.nmemb
        else:
            self.py_format_str = None
            self.py_format_len = -1

    elif self.is_container:
        self.py_format_str = ''
        self.py_format_len = 0
        self.py_fixed_size = 0

        for field in self.fields:
            setup_type(field.type, field.field_type)
            field.py_type = strip_ns(field.field_type)

            if field.type.py_format_len < 0:
                self.py_format_str = None
                self.py_format_len = -1
            elif self.py_format_len >= 0:
                self.py_format_str += field.type.py_format_str
                self.py_format_len += field.type.py_format_len
            
            if field.type.is_list:
                setup_type(field.type.member, field.field_type)
                
                field.py_listtype = get_wrapped(strip_ns(field.type.member.name))
                if field.type.member.is_simple:
                    field.py_listtype = "'" + field.type.member.py_format_str + "'"

                field.py_listsize = -1
                if field.type.member.fixed_size():
                    field.py_listsize = field.type.member.size
            if field.type.fixed_size():
                self.py_fixed_size += field.type.size

def align_size(field):
    if field.type.is_list:
        return field.type.member.size if field.type.member.fixed_size() else 4 # .. pointer size??
    if field.type.is_container:
        return field.type.size if field.type.fixed_size() else 4
    return field.type.size

def get_expr(expr):
    '''
    Figures out what C code is needed to get the length of a list field.
    Recurses for math operations.
    Returns bitcount for value-mask fields.
    Otherwise, uses the value of the length field.
    '''
    lenexp = get_length_field(expr)

    if expr.op != None:
        return '(' + get_expr(expr.lhs) + ' ' + expr.op + ' ' + get_expr(expr.rhs) + ')'
    elif expr.bitfield:
        return 'ooxcb.popcount(' + lenexp + ')'
    else:
        return lenexp

def py_complex(self, name):
    code = []
    
    def _add_fields(fields):
        code.append('_unpacked = unpack_ex("%s", self, count)' % fmt)
        for idx, field in enumerate(fields):
            # try if we can get a modifier
            modifier = get_modifier(field)
            value = modifier % ('_unpacked[%d]' % idx)
            code.append(template('self.$fieldname = $value', 
                fieldname=prefix_if_needed(field.field_name),
                value=value
            ))

    need_alignment = False
    code.append('count = 0')
    struct = Struct()
    for field in self.fields:
        if field.auto:
            struct.push_pad(field.type.size)
            continue
        if field.type.is_simple:
            struct.push_format(field)
            continue
        if field.type.is_pad:
            struct.push_pad(field.type.nmemb)
            continue
        fields, size, fmt = struct.flush()
        if fields:
            _add_fields(fields)
        if size > 0:
            code.append(template('count += $size', size=size))

        if need_alignment:
            code.append('count += ooxcb.type_pad(%d, count)' % align_size(field))
        need_alignment = True

        if field.type.is_list:
            lcode = ('ooxcb.List(conn, self, count, %s, %s, %d)' % \
                    (get_expr(field.type.expr), 
                        field.py_listtype, 
                        field.py_listsize))
            if field.py_type in INTERFACE.get('ResourceClasses'):
                # is a resource. wrap them.
                lcode = '[%s for w in %s]' % (get_modifier(field) % 'w', lcode)
            code.append('self.%s = %s' % (field.field_name, lcode))
            code.append('count += len(self.%s.buf())' % prefix_if_needed(field.field_name))
        elif field.type.is_container and field.type.fixed_size():
            code.append('self.%s = %s(self, count, %s)' % (prefix_if_needed(field.field_name), 
                    field.py_type, field.type.size))
            code.append('count += %s' % field.type.size)
        else:
            code.append('self.%s = %s(self, count)' % (prefix_if_needed(field.field_name), 
                field.py_type))
            code.append('count += len(self.%s)', prefix_if_needed(field.field_name))

    fields, size, fmt = struct.flush()
    if fields:
        if need_alignment:
            code.append('count += ooxcb.type_pad(4, count)')
        _add_fields(fields)
        code.append('count += %d' % size)

    if self.fixed_size() or self.is_reply:
        if self.fields:
            code.pop()
    
    return code

def py_open(self):
    global NAMESPACE
    NAMESPACE = self.namespace

    py('# auto generated. yay.') \
      ('import ooxcb') \
      ('try:').indent() \
                ('import cStringIO as StringIO') \
                .dedent() \
      ('except ImportError:').indent() \
                ('import StringIO') \
                .dedent() \
      ('from struct import pack, unpack_from, calcsize') \
      ('from array import array') \
      () \
      ('def unpack_ex(fmt, protobj, offset=0):') \
      .indent() \
                ('s = protobj.get_slice(calcsize(fmt), offset)') \
                ('return unpack_from(fmt, s, 0)') \
                .dedent() \
      ()

def py_close(self):
    pass

def py_enum(self, name):
    '''
    Exported function that handles enum declarations.
    '''
    cls = PyClass(strip_ns(name)) 

    count = 0

    for (enam, evalue) in self.values: 
        cls.new_attribute(prefix_if_needed(enam), evalue if evalue != '' else count)
        count += 1

    ALL[cls.name] = cls

def py_simple(self, name):
    '''
    Exported function that handles cardinal declarations.
    These are types which are typedef'd to one of the CARDx's char, float, etc.
    '''
    setup_type(self, name, '')
    if not is_ignored(name): # create a class ...
        clsname = pythonize_classname(strip_ns(name))
        cls = PyClass(clsname)
        cls.base = 'ooxcb.Resource'
        init = cls.new_method('__init__')
        init.arguments.extend(['conn', 'xid'])
        init.code.append('ooxcb.Resource.__init__(self, conn, xid)')
        # the magic `get_internal` method is from `Resource`
        WRAPPERS[strip_ns(name)] = cls
        ALL[clsname] = cls

def py_struct(self, oldname):
    name = (oldname[0], pythonize_classname(oldname[1]))
    setup_type(self, name)

    cls = PyClass(self.py_type)
    cls.base = 'ooxcb.Struct'
    init = cls.new_method('__init__')

    if self.fixed_size():
        init.arguments += ['conn', 'parent', 'offset', 'size']
        init.code.append('ooxcb.Struct.__init__(self, conn, parent, offset, size)')
    else:
        init.arguments += ['conn', 'parent', 'offset']
        init.code.append('ooxcb.Struct.__init__(self, conn, parent, offset)')
   
    init.code += py_complex(self, name)

    if self.fixed_size():
        init.code.append('ooxcb._resize_obj(self, count)')

    ALL[strip_ns(name)] = cls
    WRAPPERS[strip_ns(oldname)] = cls

def py_union(self, name):
    '''
    Exported function that handles union declarations.
    '''
    setup_type(self, name)

    cls = PyClass(self.py_type)
    cls.base = 'ooxcb.Union'

    init = cls.new_method('__init__')

    if self.fixed_size():
        init.arguments += ['conn', 'parent', 'offset', 'size']
        init.code.append('ooxcb.Union.__init__(self, conn, parent, offset, size)')
    else:
        init.arguments += ['conn', 'parent', 'offset']
        init.code.append('ooxcb.Union.__init__(self, conn, parent, offset)')

    init.code.append('count = 0')
    for field in self.fields:
        if field.type.is_simple:
            init.code.append('self.%s = unpack_ex("%s", self)' % \
                    (prefix_if_needed(field.field_name), 
                    field.type.py_format_str))
            init.code.append('count = max(count, %s)', field.type.size)
        elif field.type.is_list:
            init.code.append('self.%s = ooxcb.List(conn, self, 0, %s, %s, %s)' % \
                    (prefix_if_needed(field.field_name), 
                    get_expr(field.type.expr), 
                    field.py_listtype, 
                    field.py_listsize))
            init.code.append('count = max(count, len(self.%s.buf()))' % prefix_if_needed(field.field_name))
        elif field.type.is_container and field.type.fixed_size():
            init.code.append('self.%s = %s(self, 0, %s)' % (prefix_if_needed(field.field_name),
                    field.py_type, 
                    field.type.size))
            init.code.append('count = max(count, %s)' % field.type.size)
        else:
            init.code.append('self.%s = %s(self, 0)' % (prefix_if_needed(field.field_name), field.py_type))
            init.code.append('count = max(count, len(self.%s))' % prefix_if_needed(field.field_name))

    if not self.fixed_size():
        init.code.append('ooxcb._resize_obj(self, count)')

    ALL[cls.name] = cls
    WRAPPERS[strip_ns(name)] = cls

def request_helper(self, name, void, regular):
    '''
    Declares a request function.
    '''

    # Four stunningly confusing possibilities here:
    #
    #   Void            Non-void
    # ------------------------------
    # "req"            "req"
    # 0 flag           CHECKED flag   Normal Mode
    # void_cookie      req_cookie
    # ------------------------------
    # "req_checked"    "req_unchecked"
    # CHECKED flag     0 flag         Abnormal Mode
    # void_cookie      req_cookie
    # ------------------------------
    reqinfo = get_request_info(strip_ns(name))
    defaults = reqinfo.get('defaults', {})

    # Whether we are _checked or _unchecked
    checked = void and not regular
    unchecked = not void and not regular

    # What kind of cookie we return
    func_cookie = 'ooxcb.VoidCookie' if void else self.py_cookie_name

    # What flag is passed to xcb_request
    func_flags = checked or (not void and regular)

    # What our function name is
    func_name = self.py_request_name
    if checked:
        func_name = self.py_checked_name
    if unchecked:
        func_name = self.py_unchecked_name

    # now pythonize the name ...
    if not 'name' in reqinfo:
        func_name = pythonize_name(func_name)
    else:
        func_name = reqinfo['name']
        if checked:
            func_name += '_checked'
        if unchecked:
            func_name += '_unchecked'

    param_fields = []
    wire_fields = []
    optional_param_fields = []

    meth = PyMethod(func_name)
    # now decide to which class that stuff belongs to, and
    # determinate the `self` parameter
    subject_field = None
    # Check for a subject parameter, use extension class as fallback
    if 'subject' in reqinfo:
        # yep, there's a subject. so, try to get the py class of the
        # subject. or, maybe it's givin explicitly!
        subject_field = get_field_by_name(self.fields, reqinfo['subject'])
        clsname = reqinfo.get('class', None)
        if not clsname:
            cls = WRAPPERS[subject_field.py_type]
        else:
            cls = ALL[clsname]
    else:
        clsname = reqinfo.get('class', None)
        if clsname is None:
            cls = EXTCLS
        else:
            cls = ALL[clsname]
    cls.add_member(meth)
    
    for field in self.fields:
        if field.wire:
            wire_fields.append(field)

        if field is subject_field:
            # It's `self`. skippit.
            continue

        if field.visible:
            # The field should appear as a call parameter
            f = prefix_if_needed(field.field_name)
            if field.py_type in WRAPPERS:
                f += '_' # postfix it with a 'oh look at me i am not xized yet' _.

            if f in defaults: # interface provides with a default value
                f += '=' + str(defaults[f])
                optional_param_fields.append(f)
            else:
                param_fields.append(f)

    if 'arguments' in reqinfo:
        param_fields = reqinfo['arguments']
        optional_param_fields = []

    meth.arguments.extend(param_fields)
    meth.arguments.extend(optional_param_fields)
    
    if 'precode' in reqinfo:
        meth.code.extend(reqinfo['precode'])

    # Check if we have to append some `.get_internal()` somewhere
    for field in self.fields:
        if field.py_type in WRAPPERS and field is not subject_field:
            meth.code.append('%s = %s_.get_internal()' %  (field.field_name, field.field_name))
        if field is subject_field:
            meth.code.append('%s = self.get_internal()' % field.field_name)

    meth.code.append('buf = StringIO.StringIO()')
    
    struct = Struct()
    for field in wire_fields:
        if field.auto:
            struct.push_pad(field.type.size)
            continue
        if field.type.is_simple:
            struct.push_format(field)
            continue
        if field.type.is_pad:
            struct.push_pad(field.type.nmemb)
            continue

        fields, size, format = struct.flush()

        if size > 0:
            meth.code.append('buf.write(pack("%s", %s))' % (format, \
                    ', '.join([prefix_if_needed(f.field_name) for f in fields])))

        if field.type.is_expr:
            #_py('        buf.write(pack(\'%s\', %s))', field.type.py_format_str, _py_get_expr(field.type.expr))
            meth.code.append('buf.write(pack("%s", %s))' % (field.type.py_format_str,
                get_expr(field.type.expr)))

        elif field.type.is_pad:
            meth.code.append('buf.write(pack("%sx"))' % field.type.nmemb)
        elif field.type.is_container:
            meth.code.append('for elt in ooxcb.Iterator(%s, %d, "%s", False):' % \
                    (prefix_if_needed(field.field_name), 
                        field.type.py_format_len, 
                        prefix_if_needed(field.field_name)))
            meth.code.append(INDENT)
            meth.code.append('buf.write(pack("%s", *elt))' % field.type.py_format_str)
            meth.code.append(DEDENT)
        elif field.type.is_list and field.type.member.is_simple:
            meth.code.append('buf.write(array("%s", %s).tostring())' % \
                    (field.type.member.py_format_str, 
                    prefix_if_needed(field.field_name)))
        else:
            meth.code.append('for elt in ooxcb.Iterator(%s, %d, "%s", True):' % \
                (prefix_if_needed(field.field_name), 
                    field.type.member.py_format_len, 
                    prefix_if_needed(field.field_name)))
            meth.code.append(INDENT)
            meth.code.append('buf.write(pack("%s", *elt))' % field.type.member.py_format_str)
            meth.code.append(DEDENT)

    fields, size, format = struct.flush()
    if size > 0:
        meth.code.append('buf.write(pack("%s", %s))' % (format, ', '.join(
            [prefix_if_needed(f.field_name) for f in fields])))

    meth.code.append('return self.conn.%s.send_request(ooxcb.Request(self.conn, buf.getvalue(), %s, %s, %s), \\' % \
            (NAMESPACE.header, self.opcode, void, func_flags))
    meth.code.append(INDENT)
    meth.code.append('%s()%s' % (func_cookie, ')' if void else ','))
    if not void:
        meth.code.append('%s)' % self.py_reply_name)
    meth.code.append(DEDENT)
   
def py_request(self, name):
    '''
    Exported function that handles request declarations.
    '''
    setup_type(self, name, 'Request')

    if self.reply:
        # Cookie class declaration
        cookiecls = PyClass(self.py_cookie_name)
        cookiecls.base = 'ooxcb.Cookie'
        ALL[self.py_cookie_name] = cookiecls

    if self.reply:
        # Reply class definition
        py_reply(self.reply, name)
        # Request prototypes
        request_helper(self, name, False, True)
        request_helper(self, name, False, False)
    else:
        # Request prototypes
        request_helper(self, name, True, False)
        request_helper(self, name, True, True)

def py_reply(self, name):
    '''
    Handles reply declarations.
    '''
    setup_type(self, name, 'Reply')

    cls = PyClass(self.py_reply_name)
    cls.base = 'ooxcb.Reply'
    init = cls.new_method('__init__')
    init.arguments.extend(['conn', 'parent'])
    init.code.append('ooxcb.Reply.__init__(self, conn, parent)')
    init.code.extend(py_complex(self, name))
    
    ALL[cls.name] = cls # TODO: to WRAPPERS, too?

def py_error(self, name):
    setup_type(self, name, 'Error')

    struct = PyClass(self.py_error_name)
    struct.base = 'ooxcb.Error'
    init = struct.new_method('__init__')
    init.arguments.extend(['conn', 'parent'])
    init.code.append('ooxcb.Error.__init__(self, conn, parent)')
    ALL[self.py_error_name] = WRAPPERS[self.py_error_name] = struct

    init.code.extend(py_complex(self, name))

    # Exception definition
    exc = PyClass(self.py_except_name)
    exc.base = 'ooxcb.ProtocolException'
    ALL[self.py_except_name] = exc

    # Opcode define
    ERRORS[self.opcodes[name]] = '(%s, %s)' % (self.py_error_name, self.py_except_name)

def py_event(self, name):
    setup_type(self, name, 'Event')

    struct = PyClass(self.py_event_name)
    struct.base = 'ooxcb.Event'
    struct.new_attribute('event_name', '"on_%s"' % pythonize_camelcase_name(strip_ns(name)))

    entry = INTERFACE.get('Events', {}).get(strip_ns(name), None)
    if entry is None:
        clsname, membername = ('ooxcb.Connection', 'conn')
    else:
        membername = entry['member']
        clsname = '"%s"' % entry.get('class', get_wrapped(get_field_by_name(self.fields, membername).py_type))
        # the classnames are resolved later. see generate_all.

    struct.new_attribute('event_target_class', clsname)

    init = struct.new_method('__init__')
    init.arguments.extend(['conn', 'parent'])
    init.code.append('ooxcb.Event.__init__(self, conn, parent)')
    ALL[self.py_event_name] = WRAPPERS[self.py_event_name] = struct

    init.code.extend(py_complex(self, name))

    init.code.append('self.event_target = self.%s' % membername)

    # Opcode define
    EVENTS[self.opcodes[name]] = self.py_event_name

def add_custom_member(cls, mtype, minfo):
    def _handle_method(meth):
        meth.code.extend(minfo['code'])
        meth.arguments.extend(minfo.get('arguments', []))

    def _add_method():
        meth = cls.new_method(minfo['name'])
        _handle_method(meth)

    def _add_classmethod():
        meth = PyClassMethod(minfo['name'])
        cls.add_member(meth)
        _handle_method(meth)

    types = {'method': _add_method,
        'classmethod': _add_classmethod,
        }
    return types[mtype]()

def process_custom_classes(classes):
    for clsname, members in classes.iteritems():
        if clsname in ALL:
            cls = ALL.get(clsname)
        else:
            cls = PyClass(clsname)
            ALL[clsname] = cls
        for dct in members:
            assert len(dct) == 1, "strange syntax ... %s" % dct
            mtype, minfo = dct.items()[0]
            add_custom_member(cls, mtype, minfo)

def make_xizers():
    for name, info in INTERFACE.get('Xizers', {}).iteritems():
        typ = info['type']
        del info['type']
        XIZERS[name] = XIZER_MAKERS[typ](**info)

def generate_all():
    for item in ALL.itervalues():
        map(py, item.generate_code())
    # and last but not least: the events, errors, and registring!
    py('_events = {')
    py.indent()
    map(py, ['%s: %s,' % (key, value) for key, value in EVENTS.iteritems()]) # TODO: sort
    py.dedent()
    py('}')()
    py('_errors = {')
    py.indent()
    map(py, ['%s: %s,' % (key, value) for key, value in ERRORS.iteritems()]) # TODO: sort
    py.dedent()
    py('}')()

    py('for ev in _events.itervalues():').indent()\
            ('if isinstance(ev.event_target_class, str):').indent() \
                ('ev.event_target_class = globals()[ev.event_target_class]') \
                .dedent() \
            .dedent() \
            ()

    if NAMESPACE.is_ext:
        py('ooxcb._add_ext(key, %sExtension, _events, _errors)' % MODNAME)
    else:
        py('ooxcb._add_core(%sExtension, Setup, _events, _errors)' % MODNAME)

# Must create an "output" dictionary before any xcbgen imports.
output = {'open'    : py_open,
          'close'   : py_close,
          'simple'  : py_simple,
          'enum'    : py_enum,
          'struct'  : py_struct,
          'union'   : py_union,
          'request' : py_request,
          'event'   : py_event,
          'error'   : py_error
          }


# Check for the argument that specifies path to the xcbgen python package.
# Import the module class

try:
    from xcbgen.state import Module
except ImportError:
    print ''
    print 'Failed to load the xcbgen Python package!'
    print 'Make sure that xcb/proto installed it on your Python path.'
    print 'If not, you will need to create a .pth file or define $PYTHONPATH'
    print 'to extend the path.'
    print 'Refer to the README file in xcb/proto for more info.'
    print ''
    raise

if len(sys.argv) > 1: # provided with a module name
    MODNAME = sys.argv[1]
else:
    MODNAME = 'xproto'

print >>sys.stderr, 'Wrapping %s ...' % MODNAME

EXTCLS = PyClass('%sExtension' % MODNAME)
EXTCLS.new_attribute('header', '"%s"' % MODNAME)

EXTCLS.base = 'ooxcb.Extension'
ALL['%sExtenstion' % MODNAME] = EXTCLS

try:
    ifile = open('%s.i' % MODNAME, 'r')
    INTERFACE = yaml.load(ifile.read())
finally:
    ifile.close()


module = Module('%s.xml' % MODNAME, output)

module.register()
module.resolve()

module.generate()
make_xizers()
process_custom_classes(get_custom_classes())
generate_all()
print py.buf
