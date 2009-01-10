import json
import re
import keyword
import string

NAMESPACE = None
MODULENAME = ''
EXTNAME = ''
INTERNAL_ATTR = '_internal'
REQUESTS = {}
WRAP_MAP = {} # struct name -> PyClass
MAKE_GET_METHOD = True # make a lazy get method and move the raw reply to ..._request?
IGNORE_REPLY_FIELDS = ['response_type', 'sequence']
ENUMS = {}

INDENT = object()
DEDENT = object()

def field_string(field):
    return [tmpl("self.$field_name = ''.join(map(chr, self.$field_name))", field_name=field.field_name)]

def field_atoms(field):
    return [tmpl("self.$field_name = [Atom(conn, xid) for xid in self.$field_name]", field_name=field.field_name)]
    # TODO: what for external modules? `Atom` will be undefined.


FIELD_PYTHONIZERS = {
        'string': field_string,
        'atoms': field_atoms
        }

def check_field_names(fields):
    for field in fields:
        if keyword.iskeyword(field.field_name): # change the name if it's a python keyword
            field.field_name = '_' + field.field_name

def tmpl(tmpl, **kwargs):
    return string.Template(tmpl).substitute(kwargs)

def get_modulename():
    return '.'.join(['.'.join(NAMESPACE.prefix), NAMESPACE.header])

def get_foreign(name):
    return '.'.join([NAMESPACE.header, name])

def pythonize_camelcase_name(name):
    def repl(match):
        return '_' + match.group(0).lower()

    s = re.sub(r'([A-Z])', repl, name)
    if s.startswith('_'):
        return s[1:]
    else:
        return s


def is_ignored_reply_field(name):
    if (name.startswith('pad') or name in IGNORE_REPLY_FIELDS):
        return True
    else:
        return False

def todict(iterable):
    iterator = iter(iterable)
    while True:
        try:
            key = iterator.next()
        except StopIteration:
            break
        try:
            value = iterator.next()
        except StopIteration:
            raise Exception('Incomplete list! value missing')
        yield (key, value)

def make_values_xizer(enum_name, values_dict_name, mask_out='value_mask', list_out='value_list', xize=[]):
    """ 
        make a simple values xizer code list and return it.
        A values xizer takes all values from the values dict
        and stores it in a values list and a values mask.
    """
    enum = ENUMS[enum_name]
    code = []
    pyvalues = []

    code.append(tmpl("$mask_out, $list_out = 0, []",
        mask_out=mask_out,
        list_out=list_out
        ))

    for key, value in enum.values:
        key = pythonize_camelcase_name(key)
        code.append(tmpl('if "${key}" in ${values_dict_name}:',
                    key=key,
                    values_dict_name=values_dict_name))
        code.append(INDENT)
        code.append(tmpl('$mask_out |= $value',
            mask_out=mask_out,
            value=value
            ))

        suffix = ''
        if key in xize:
            suffix += '.' + INTERNAL_ATTR

        code.append(tmpl('$list_out.append($values_dict_name["$key"]$suffix)',
            list_out=list_out,
            values_dict_name=values_dict_name,
            key=key,
            suffix=suffix
            ))
        code.append(DEDENT)
    
    return code 

def make_seq_xizer(seq_in='value', seq_out='value', length_out='value_len'):
    code = []
    code.append(tmpl('$length_out = len($seq_in)', length_out=length_out, seq_in=seq_in))
    if seq_in != seq_out:
        code.append(tmpl('$seq_out = $seq_in', seq_out=seq_out, seq_in=seq_in))
    return code

class Codegen(object):
    def __init__(self):
        self.buf = ''
        self.indent_level = 0

    def __call__(self, fmt=''):
        if fmt is INDENT:
            self.indent()
        elif fmt is DEDENT:
            self.dedent()
        else:
            if not fmt:
                self.buf += '\n' # no unneeded indentation spaces
            else:
                self.buf += '    ' * self.indent_level + fmt + '\n'
        return self

    def indent(self, level=1):
        self.indent_level += level
        return self

    def dedent(self, level=1):
        self.indent_level -= level
        return self

class PyMethod(object):
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.code = []
        self.first_arg = 'self'
        self.decorators = []

    def generate(self):
        for deco in self.decorators:
            py('@' + deco)

        args = ', '.join(self.args)
        if args:
            args = ', ' + args

        py(tmpl('def $meth_name($first_arg$args):', 
            first_arg=self.first_arg,
            meth_name=self.name,
            args=args))
        py.indent()
        for line in self.code:
            py(line)
        py.dedent()

def make_reply_for(reqname, req, reply_pythonizers=None):
    """
        create a reply wrapper class
    """
    if reply_pythonizers is None:
        reply_pythonizers = {}

    reply = req.reply
    clsname = reqname + 'Reply'
    CLASSES[clsname] = make_simple_wrapper(clsname, reply, reply_pythonizers)

def make_simple_wrapper(clsname, obj, pythonizers=None):
    if pythonizers is None:
        pythonizers = {}
    cls = PyClass(None, clsname) # TODO: PyClass.__init__.type is obsolete?
    m__init__ = PyMethod('__init__', ['conn', INTERNAL_ATTR])
    cls.methods['__init__'] = m__init__
    
    m__init__.code.append(tmpl('$base.__init__(self, conn, $internal_attr)', 
        base=cls.base,
        internal_attr=INTERNAL_ATTR))
    
    check_field_names(obj.fields)
    for field in obj.fields:
        prefix = ''
        suffix = ''
        if isinstance(field.type, xcbgen.xtypes.ListType):
            # is a list ... wrap
            if field.type.name in WRAP_MAP: # it is a class type
                m__init__.code.append(tmpl(
                'self.$name = [$clsname(conn, d) for d in $name]',
                name=field.field_name,
                clsname=WRAP_MAP[field.type.name].name,
                ))
                continue
            else: # not a class, wrap ordinary
                pass
        if (field.field_type and not field.field_name in pythonizers): # pythonizing fields ...
            if is_ignored_reply_field(field.field_name):
                #print 'Ignoring - ignored field name'
                continue
            
            # otherwise ... wrap
            wrapped = WRAP_MAP.get(field.field_type, None)
            if wrapped is None: # not wrapped
                #print 'Ignoring', field.field_type, '- not a wrapped object - TODO?'
                pass
            else: # wrapped, so set the pythonizer class 
                prefix = wrapped.name + '(self.conn, '
                suffix = ')'

        # just an ordinary parameter ...
        m__init__.code.append(tmpl('self.$name = $prefix${internal_attr}.$name$suffix', 
            name=field.field_name,
            internal_attr=INTERNAL_ATTR,
            prefix=prefix,
            suffix=suffix
            ))
        # pythonizers redefine an attribute. best way.
        if field.field_name in pythonizers: # custom pythonizers yay
            fnc = FIELD_PYTHONIZERS[pythonizers[field.field_name]]
            m__init__.code += fnc(field)
            continue


    return cls

def make_cookie_for(clsname, replyclsname, req):
    """
        create a cookie wrapper class
    """
    cls = PyClass(None, clsname) # TODO: PyClass.__init__.type is obsolete?
    CLASSES[clsname] = WRAP_MAP[clsname] = cls
    
    #m__init__ = PyMethod('__init__', [INTERNAL_ATTR]) # no need for a custom __init__, we're a Wrapper subclass
    #cls.methods['__init__'] = m__init__
    #m__init__.code.append(tmpl('self.${internal_attr} = $internal_attr', 
    #    internal_attr=INTERNAL_ATTR))
    
    m_reply = PyMethod('reply', [])
    cls.methods['reply'] = m_reply
    m_reply.code.append(tmpl('return ${prefix}self.${internal_attr}.reply()${suffix}',
        prefix=replyclsname + '(self.conn, ',
        internal_attr=INTERNAL_ATTR,
        suffix=')'))

    m_check = PyMethod('check', [])
    cls.methods['check'] = m_check
    m_check.code.append(tmpl('return self.${internal_attr}.check()', # no need to pythonize, is only a bool
        internal_attr=INTERNAL_ATTR
        )) 

    CLASSES[clsname] = cls


class PyClass(object):
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.base = 'Wrapper'

        self.methods = {}

    def add_request(self, name, req, self_field, reqinfo):
        args = []
        
        ignore = CONF.get('ignore_parameters', []) + reqinfo.get('ignore_parameters', [])
        defaults = reqinfo.get('defaults', {})
        reply_pythonizers = reqinfo.get('reply_pythonizers', {})

        # ... we have to create cookie + reply wrapper classes,
        # but only if the request actually has a reply.
        # otherwise the original classes are ok
        replyclsname = name + 'Reply'
        cookieclsname = name + 'Cookie'
        if req.reply is not None:
            make_reply_for(name, req, reply_pythonizers)
            make_cookie_for(cookieclsname, replyclsname, req)

        args = reqinfo.get('methargs', [])
        decorators = reqinfo.get('decorators', [])
        make_get_method = reqinfo.get('make_get', MAKE_GET_METHOD)

        methname = reqinfo.get('methname', pythonize_camelcase_name(name))
        mreqname = methname
        if make_get_method:
            mreqname += '_request' # get *and* request
            if not req.reply: # void replys need checked
                name += "Checked"

        if not args:
            for field in req.fields:
                if field.field_name.startswith('pad'):
                    continue
                if (field is not self_field and
                        field.field_name not in ignore):
                    args.append(field.field_name)
                    if field.field_name in defaults:
                        args[-1] += '=%s' % defaults[field.field_name]

        check_field_names(req.fields)

        mreq = PyMethod(mreqname, args)
        if 'classmethod' in decorators:
            args.insert(0, 'conn') # explicit conn for classmethods
            mreq.first_arg = 'cls'
        self.methods[mreqname] = mreq
        mreq.decorators = decorators

        code = reqinfo.get('code', '')
        precode = reqinfo.get('precode', [])
        mreq.code += self.make_extended(reqinfo.get('extended', {}))

        if not code:
            # add code
            req_args = []
            for field in req.fields:
                if field.field_name in ignore:
                    continue

                if field.field_name.startswith('pad'):
                    continue

                if field is self_field:
                    req_args.append('self.%s' % INTERNAL_ATTR)
                    continue

                elif field.field_type: # xizing fields ...
                    if len(field.field_type) == 1: # is most likely something like uint8_t ...
                        #print 'Ignoring', field.field_type, '- no namespace'
                        pass
                    else:
                        wrapped = WRAP_MAP.get(field.field_type, None)
                        if wrapped is None: # not wrapped
                            #print 'Ignoring', field.field_type, '- not a wrapped object - TODO?'
                            pass
                        else: # wrapped, so let the user pass objects
                            req_args.append('%s.%s' % (field.field_name, INTERNAL_ATTR))
                            continue
                # just an ordinary parameter ...
                req_args.append(field.field_name) # TODO
            
            prefix = ''
            suffix = ''
            if req.reply is not None: # wrapped cookie class
                prefix += cookieclsname + '(self.conn, '
                suffix += ')'

            if not 'classmethod' in decorators:
                prefix += 'self.'

            mreq.code += precode

            mreq.code.append(tmpl('return ${prefix}conn.$ext.$reqname($args)${suffix}',
                ext = NAMESPACE.header,
                reqname = name,
                args = ', '.join(req_args),
                prefix = prefix,
                suffix = suffix
                ))
        else:
            mreq.code += code
        
        if make_get_method:
            mget = PyMethod(methname, ['*args', '**kwargs']) # dirty, but seems to be the best way
            if req.reply: # has cookie
                suffix = '.reply()'
            else: # check
                suffix = '.check()'

            mget.decorators = decorators
            if 'classmethod' in decorators:
                mget.first_arg = 'cls'

            mget.code.append(tmpl('return ${prefix}${mreqname}($args)$suffix',
                mreqname=mreqname,
                args = '*args, **kwargs',
                prefix = 'self.' if not 'classmethod' in decorators else 'cls.',
                suffix=suffix
                ))
            self.methods[methname] = mget

    def make_extended(self, ext):
        def make_make_values_xizer(info):
            kwargs = dict((str(key), value) for key, value in info.iteritems())
            return make_values_xizer(**kwargs)

        def make_make_seq_xizer(info):
            kwargs = dict((str(key), value) for key, value in info.iteritems())
            return make_seq_xizer(**kwargs)

        ophandlers = {'make_values_xizer': make_make_values_xizer,
                'make_seq_xizer': make_make_seq_xizer}
        ret = []
        for op, info in ext.iteritems():
            ret += ophandlers[op](info)
        return ret
            
    def make_method(self, info):
        if 'request' in info: # is a request wrapper!
            name = info['request']
            self_name = info.get('subjectname', None)
            req = REQUESTS[name]
            reqinfo = info
            self_field = ([f for f in req.fields if f.field_name == self_name] or [None])[0]
            self.add_request(name, req, self_field, reqinfo)
            return
        else: # is a method.
            methname = info['methname']
            args = info['methargs']
            codes = info['code']

            meth = PyMethod(methname, args)
            meth.decorators = info.get('decorators', [])

            meth.code += codes
            self.methods[methname] = meth

    def make_basecls(self, info):
        """ set the base class name """
        self.base = info

    def make_member(self, key, info):
        return {'method': self.make_method,
                'basecls': self.make_basecls,
                'order_id': lambda aa: None, # ignore order_id
                }[key](info)

    @staticmethod
    def pythonize_name(name):
        if name[1] in CONF.get('aliases', {}):
            return CONF['aliases'][name[1]]
        else:
            if name[1].isupper(): # WINDOW -> Window
                return name[1].capitalize()
            else: # otherwise: let it be
                return name[1]

    def __repr__(self):
        return '<Python class "%s">' % (self.name,)

    def generate(self):
        py(tmpl('class $name($base):', name=self.name, base=self.base))
        py.indent()
        for meth in self.methods.itervalues():
            meth.generate()
            py()
        if not self.methods:
            py('pass')
            py()
        py.dedent()

py = Codegen()
CLASSES = {}
CONF = {}

def py_open(self):
    global NAMESPACE, MODULENAME, EXTNAME
    NAMESPACE = self.namespace
    MODULENAME = get_modulename()
    EXTNAME = '%sExtension' % NAMESPACE.header

def py_close(self):
    pass

def py_simple(self, name):
    if name[1] not in CONF.get('ignore_classes', []):
        pyname = PyClass.pythonize_name(name)
        WRAP_MAP[name] = CLASSES[pyname] = PyClass(self, pyname)

def py_enum(self, name):
    ENUMS[name[1]] = self

def py_struct(self, name):
    if name[1] not in CONF.get('ignore_classes', []):
        pyname = PyClass.pythonize_name(name)
        WRAP_MAP[name] = CLASSES[pyname] = make_simple_wrapper(pyname, self)

def py_union(self, name):
    #print 'union', self, name
    pass

def py_request(self, name):
    if name[1] in CONF.get('requests', {}):
        reqinfo = CONF['requests'][name[1]]
        fieldname = reqinfo['subjectname']
        classname = reqinfo['classname']

        field = [f for f in self.fields if f.field_name == fieldname][0]
        klass = CLASSES[classname]
        klass.add_request(name[1], self, field, reqinfo)

    WRAP_MAP[name] = REQUESTS[name[1]] = self

def py_error(self, name):
    #print 'error', self, name
    pass

def py_event(self, name):
    if name[1] not in CONF.get('ignore_classes', []):
        pyname = PyClass.pythonize_name(name) + 'Event'
        WRAP_MAP[name] = CLASSES[pyname] = make_simple_wrapper(pyname, self)

def process_custom_classes():
    """ process the `classes` section in the config """
    # sort classes by order id. higher order ids are processed later
    def key(dct):
        return dict(todict(dct[1])).get('order_id', 0)
    sorted_classes = sorted(CONF.get('classes', {}).iteritems(), key=key)

    for classname, members in sorted_classes:
        klass = CLASSES[classname]
        for membertype, info in todict(members):
             klass.make_member(membertype, info)

def generate():
    for klass in CLASSES.itervalues():
        klass.generate()

output = {'open': py_open,
        'close': py_close,
        'simple': py_simple,
        'enum': py_enum,
        'struct': py_struct,
        'union': py_union,
        'request': py_request,
        'event': py_event,
        'error': py_error,
        }

from xcbgen.state import Module
import xcbgen

modname = 'xproto'

def load_config(modname):
    with open('%s.i' % modname, 'r') as f:
        c = json.load(f)
    return c

CONF = load_config(modname)
module = Module('%s.xml' % modname, output)

py('import xcb.%s' % modname) \
  ('from oobase import Wrapper') \
  ()

module.register()
module.resolve()
module.generate()

process_custom_classes()
generate()
print py.buf
