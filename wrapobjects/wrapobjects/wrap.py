#!/usr/bin/env python

'''Generate a Python ctypes wrapper file for a header file.

Usage example::
    wrap.py -lGL -oGL.py /usr/include/GL/gl.h

    >>> from GL import *

'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: wrap.py 1694 2008-01-30 23:12:00Z Alex.Holkner $'

from contextlib import contextmanager

from wraplib.pyclass import PyClass
from wraplib.pymember import PyClassMethod
from wraplib.codegen import Codegen
from odict import odict
from ctypesparser import *
import textwrap
import sys
import re

class CtypesWrapper(CtypesParser, CtypesTypeVisitor):
    file=None
    def __init__(self):
        CtypesParser.__init__(self)
        CtypesTypeVisitor.__init__(self)
        self.rules = []
        self.objects = odict()
        self.wrappers = {}
        self.synonyms = odict()
        self.init_redirects = {}
        self.wrappers_visitors = []

        self._wrapper = _wrapper = PyClass('_Wrapper')
        meth = PyClassMethod('_from_internal')
        self._wrapper.add_member(meth)
        meth.arguments.append('internal')
        meth.code.extend((
            'self = object.__new__(cls)',
            'self._internal = internal',
            'return self'))

    def wrap_function(self, name, restype, argtypes, vararg):
        for rule in self.rules[::-1]:
            if rule(self, name, restype, argtypes, vararg):
                return
        print 'No rule!', name

    def add_wrappers_visitor(self, visitor):
        self.wrappers_visitors.append(visitor)

    def handle_wrappers_visitors(self):
        for visitor in self.wrappers_visitors:
            for wrapper in self.wrappers.itervalues():
                visitor(self, wrapper)

    def add_synonym(self, pattern, repl):
        self.synonyms[pattern] = repl

    def add_synonyms(self, *tuples):
        for pattern, repl in tuples:
            self.add_synonym(pattern, repl)

    def handle_synonyms(self):
        synonyms = self.synonyms.items()[::-1]
        for name in self.all_names[:]:
            for pattern, repl in synonyms:
                new_name, subs = re.subn(pattern, repl, name)
                if subs:
                    #self.all_names.remove(name) # TODO: I don't think we should remove the original ones. Trouble with link_modules if we do.
                    self.all_names.append(new_name)
                    print >>self.file, "%s = %s" % (new_name, name)
                    break

    def get_pyclass(self, name):
        if name in self.objects:
            return self.objects[name]
        else:
            ret = self.objects[name] = PyClass(name)
            ret.base = '_Wrapper'
            return ret

    def get_wrapper(self, tag):
        return self.wrappers.get(tag, None)

    def add_rule(self, rule):
        self.rules.append(rule)

    def add_rules(self, *rules):
        map(self.add_rule, rules)

    def add_init_redirect(self, clsname, funcname):
        self.init_redirects[clsname] = funcname

    def add_init_redirects(self, *tuples):
        for clsname, funcname in tuples:
            self.add_init_redirect(clsname, funcname)

    def handle_init_redirects(self):
        for clsname, funcname in self.init_redirects.iteritems():
            cls = self.get_pyclass(clsname)
            try:
                meth = cls.get_member_by_name('__init__')
            except KeyError:
                meth = cls.new_method('__init__')
            meth.arguments.extend(('*args', '**kwargs'))
            meth.code.append('self._internal = %s(*args, **kwargs)._internal' % funcname)

    def add_class_wrapper(self, structname, clsname):
        self.wrappers[structname] = self.get_pyclass(clsname)
        self.wrappers[structname].tag = structname
        # force class construction
        self.get_pyclass(clsname)

    def add_pointer_class_wrappers(self, *wrappers):
        for structname, clsname in wrappers:
            self.add_class_wrapper('POINTER(%s)' % structname, clsname)

    def begin_output(self, output_file, library, link_modules=(),
                     emit_filenames=(), all_headers=False):
        self.library = library
        self.file = output_file
        self.all_names = []
        self.known_types = {}
        self.structs = set()
        self.enums = set()
        self.emit_filenames = emit_filenames
        self.all_headers = all_headers

        self.linked_symbols = {}
        for name in link_modules:
            module = __import__(name, globals(), locals(), ['foo'])
            for symbol in module.__all__:
                if symbol not in self.linked_symbols:
                    self.linked_symbols[symbol] = '%s.%s' % (name, symbol)

        self.link_modules = link_modules

        self.print_preamble()
        self.print_link_modules_imports()

    def generate_oo_code(self):
        py = Codegen()
        py(self._wrapper.generate_code())
        for object in self.objects.itervalues():
            py(object.generate_code())
        print >>self.file, py.buf

    def wrap(self, filename, source=None):
        assert self.file, 'Call begin_output first'
        self.parse(filename, source)

    def end_output(self):
        self.handle_synonyms()
        self.print_epilogue()
        self.file = None

    def does_emit(self, symbol, filename):
        return self.all_headers or filename in self.emit_filenames

    def print_preamble(self):
        import textwrap
        import time
        print >> self.file, textwrap.dedent("""
            '''Wrapper for %(library)s

            Generated with:
            %(argv)s

            Do not modify this file.
            '''

            __docformat__ =  'restructuredtext'
            __version__ = '$Id: wrap.py 1694 2008-01-30 23:12:00Z Alex.Holkner $'

            import ctypes
            from ctypes import *

            import pyglet.lib

            _lib = pyglet.lib.load_library(%(library)r)

            _int_types = (c_int16, c_int32)
            if hasattr(ctypes, 'c_int64'):
                # Some builds of ctypes apparently do not have c_int64
                # defined; it's a pretty good bet that these builds do not
                # have 64-bit pointers.
                _int_types += (ctypes.c_int64,)
            for t in _int_types:
                if sizeof(t) == sizeof(c_size_t):
                    c_ptrdiff_t = t

            class c_void(Structure):
                # c_void_p is a buggy return type, converting to int, so
                # POINTER(None) == c_void_p is actually written as
                # POINTER(c_void), so it can be treated as a real pointer.
                _fields_ = [('dummy', c_int)]

        """ % {
            'library': self.library,
            'date': time.ctime(),
            'class': self.__class__.__name__,
            'argv': ' '.join(sys.argv),
        }).lstrip()

    def print_link_modules_imports(self):
        for name in self.link_modules:
            print >> self.file, 'import %s' % name
        print >> self.file

    def print_epilogue(self):
        self.all_names.extend(self.objects.keys())
        print >> self.file
        print >> self.file,  '\n'.join(textwrap.wrap(
            '__all__ = [%s]' % ', '.join([repr(n) for n in self.all_names]),
            width=78,
            break_long_words=False))

    def handle_ctypes_constant(self, name, value, filename, lineno):
        if self.does_emit(name, filename):
            print >> self.file, '%s = %r' % (name, value),
            print >> self.file, '\t# %s:%d' % (filename, lineno)
            self.all_names.append(name)

    def handle_ctypes_type_definition(self, name, ctype, filename, lineno):
        if self.does_emit(name, filename):
            self.all_names.append(name)
            if name in self.linked_symbols:
                print >> self.file, '%s = %s' % \
                    (name, self.linked_symbols[name])
            else:
                ctype.visit(self)
                self.emit_type(ctype)
                print >> self.file, '%s = %s' % (name, str(ctype)),
                print >> self.file, '\t# %s:%d' % (filename, lineno)
        else:
            self.known_types[name] = (ctype, filename, lineno)

    def emit_type(self, t):
        t.visit(self)
        for s in t.get_required_type_names():
            if s in self.known_types:
                if s in self.linked_symbols:
                    print >> self.file, '%s = %s' % (s, self.linked_symbols[s])
                else:
                    s_ctype, s_filename, s_lineno = self.known_types[s]
                    s_ctype.visit(self)

                    self.emit_type(s_ctype)
                    print >> self.file, '%s = %s' % (s, str(s_ctype)),
                    print >> self.file, '\t# %s:%d' % (s_filename, s_lineno)
                del self.known_types[s]

    def visit_struct(self, struct):
        if struct.tag in self.structs:
            return
        self.structs.add(struct.tag)

        base = {True: 'Union', False: 'Structure'}[struct.is_union]
        print >> self.file, 'class struct_%s(%s):' % (struct.tag, base)
        print >> self.file, '    __slots__ = ['
        if not struct.opaque:
            for m in struct.members:
                print >> self.file, "        '%s'," % m[0]
        print >> self.file, '    ]'

        # Set fields after completing class, so incomplete structs can be
        # referenced within struct.
        for name, typ in struct.members:
            self.emit_type(typ)

        print >> self.file, 'struct_%s._fields_ = [' % struct.tag
        if struct.opaque:
            print >> self.file, "    ('_opaque_struct', c_int)"
            self.structs.remove(struct.tag)
        else:
            for m in struct.members:
                print >> self.file, "    ('%s', %s)," % (m[0], m[1])
        print >> self.file, ']'
        print >> self.file

    def visit_enum(self, enum):
        if enum.tag in self.enums:
            return
        self.enums.add(enum.tag)

        print >> self.file, 'enum_%s = c_int' % enum.tag
        for name, value in enum.enumerators:
            self.all_names.append(name)
            print >> self.file, '%s = %d' % (name, value)

    def handle_ctypes_function(self, name, restype, argtypes, vararg, filename, lineno):
        if self.does_emit(name, filename):
            if name in self.linked_symbols:
                print >> self.file, '%s = %s' % (name, self.linked_symbols[name])
            else:
                # Also emit any types this func requires that haven't yet been
                # written.
                self.emit_type(restype)
                for a in argtypes:
                    self.emit_type(a)

                self.all_names.append(name)
                print >> self.file, '# %s:%d' % (filename, lineno)
                print >> self.file, '%s = _lib.%s' % (name, name)
                print >> self.file, '%s.restype = %s' % (name, str(restype))
                print >> self.file, '%s.argtypes = [%s]' % \
                    (name, ', '.join([str(a) for a in argtypes]))
                print >> self.file

                # and now ... the object oriented wrapping stuff!
                self.wrap_function(name, restype, argtypes, vararg)

    def handle_ctypes_variable(self, name, ctype, filename, lineno):
        # This doesn't work.
        #self.all_names.append(name)
        #print >> self.file, '%s = %s.indll(_lib, %r)' % \
        #    (name, str(ctype), name)
        pass

@contextmanager
def wrap(headers,
        include_dirs=(),
        include_files=(),
        library=None,
        output=None,
        link_modules=(),
        defines=(),
        all_headers=False):
    if library is None:
        library = os.path.splitext(headers[0])[0]
    if output is None:
        output = '%s.py' % library

    wrapper = CtypesWrapper()

    yield wrapper

    wrapper.begin_output(open(output, 'w'),
                         library=library,
                         emit_filenames=headers,
                         link_modules=link_modules,
                         all_headers=all_headers)
    wrapper.preprocessor_parser.include_path += include_dirs
    if defines:
        for name, value in defines.iteritems():
            wrapper.preprocessor_parser.define(name, value)
    for file in include_files:
        wrapper.wrap(file)
    for header in headers:
        wrapper.wrap(header)
    wrapper.handle_init_redirects()
    wrapper.handle_wrappers_visitors()
    wrapper.generate_oo_code()
    wrapper.end_output()

    print 'Wrapped to %s' % output

