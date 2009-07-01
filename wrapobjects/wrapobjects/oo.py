# -*- coding: utf -*-

import re

from wraplib.template import template

def _compiled(regex):
    if isinstance(regex, basestring):
        return re.compile(regex)
    else:
        return regex

def regex_match(regex, submatch):
    regex = _compiled(regex)
    def match(wrapper, name, restype, argtypes, varargs):
        if regex.match(name):
            return submatch(wrapper, name, restype, argtypes, varargs)
        else:
            return False
    return match

def fail(wrapper, name, restype, argtypes, varargs):
    return False

def succeed(wrapper, name, restype, argtypes, varargs):
    return True

class method(object):
    def __init__(self, clsname, name_regex, self_arg=0):
        self.clsname = clsname
        self.name_regex = _compiled(name_regex)
        self.self_arg = self_arg

    def _strip_prefix(self, name):
        return self.name_regex.match(name).group(1)

    def __call__(self, wrapper, name, restype, argtypes, varargs):
        cls = wrapper.get_pyclass(self.clsname)
        methname = name
        methname = self._strip_prefix(methname)
        meth = cls.new_method(methname)
        args = []
        for idx, param in enumerate(argtypes):
            if idx == self.self_arg:
                if not str(param) == cls.tag:
                    print '`self` argument tags not matching in %s: parameter: %s / class: %s' % (name, str(param), cls.tag)
                args.append('self._internal')
                continue
            argname = 'arg%d' % idx
            meth.arguments.append('arg%d' % idx)
            if wrapper.get_wrapper(str(param)):
                args.append('%s._internal' % argname)
            else:
                args.append(argname)
        if varargs:
            meth.arguments.append('*varargs')
            args.append('*varargs')
        t = template(
            '$funcname($args)',
                funcname=name,
                args=', '.join(args))
        if wrapper.get_wrapper(str(restype)):
            t = template("$cls._from_internal($t)",
                    cls=wrapper.get_wrapper(str(restype)).name,
                    t=t)
        t = template('return $t', t=t)
        meth.code.append(t)
        return True

class classmethod_(object):
    def __init__(self, clsname, name_regex):
        self.clsname = clsname
        self.name_regex = _compiled(name_regex)

    def _strip_prefix(self, name):
        return self.name_regex.match(name).group(1)

    def __call__(self, wrapper, name, restype, argtypes, varargs):
        cls = wrapper.get_pyclass(self.clsname)
        methname = name
        methname = self._strip_prefix(methname)
        meth = cls.new_method(methname)
        meth.decorators.append('classmethod')
        args = []
        for idx, param in enumerate(argtypes, varargs):
            argname = 'arg%d' % idx
            meth.arguments.append('arg%d' % idx)
            if wrapper.get_wrapper(str(param)):
                args.append('%s._internal' % argname)
            else:
                args.append(argname)
        if varargs:
            meth.arguments.append('*varargs')
            args.append('*varargs')
        t = template(
            '$funcname($args)',
                funcname=name,
                args=', '.join(args))
        t = template("$cls._from_internal($t)",
                cls=self.clsname,
                t=t)
        t = template('return $t', t=t)
        meth.code.append(t)
        return True

def regex_method(regex, clsname, self_arg=0):
    regex = _compiled(regex)
    return regex_match(regex,
            method(
                clsname, regex, self_arg
                )
            )

def regex_classmethod(regex, clsname):
    regex = _compiled(regex)
    return regex_match(regex,
            classmethod_(
                clsname, regex
                )
            )

def argument_tag(arg, tag, submatch):
    def match(wrapper, name, restype, argtypes, varargs):
        try:
            if str(argtypes[arg]) == tag:
                return submatch(wrapper, name, restype, argtypes, varargs)
        except IndexError:
            pass
        return False
    return match

def argument_count(argcount, submatch):
    def match(wrapper, name, restype, argtypes, varargs):
        if len(argtypes, varargs) == argcount:
            return submatch(wrapper, name, restype, argtypes, varargs)
        else:
            return False
    return match

