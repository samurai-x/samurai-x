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

from operator import itemgetter

from .marshal import parse_signature

BUILTIN_SIGNATURES = (
        (bool, 'b'),
        (int, 'i'),
        (long, 'x'),
        (float, 'd'),
        (str, 's'),
        (unicode, 's')
        )

class DBusTypeError(Exception):
    pass

def get_signature(obj):
    if isinstance(obj, type):
        if issubclass(obj, DBusType):
            return obj.get_signature()
        else:
            for builtin, signature in BUILTIN_SIGNATURES:
                if issubclass(obj, builtin):
                    return signature
            else:
                raise DBusTypeError("Couldn't guess signature of %r" % obj)
    else:
        if isinstance(obj, DBusType):
            return type(obj).get_signature()
        elif isinstance(obj, list) and obj:
            return 'a' + get_signature(obj[0])
        else:
            for builtin, signature in BUILTIN_SIGNATURES:
                if isinstance(obj, builtin):
                    return signature
            else:
                raise DBusTypeError("Couldn't guess signature of %r" % obj)

def is_marshallable(obj):
    if isinstance(obj, DBusType):
        return True
    elif isinstance(obj, tuple(map(itemgetter(0), BUILTIN_SIGNATURES))):
        return True
    else:
        return False

def get_marshallable(code, obj):
    if code == 'v':
        # Should be a variant ...
        if not isinstance(obj, Variant):
            return Variant(obj)
        else:
            return obj
    elif code[0] == 'a':
        # is an array.
        return Array_from_signature(code)(obj)
    elif is_marshallable(obj):
        return obj
    else:
        raise DBusTypeError("Couldn't guess how to make %r marshallable!" % obj)

def guess_signature(args):
    return ''.join([get_signature(arg) for arg in args])

def get_marshallable_bunch(signature, args):
    sig = parse_signature(signature)
    margs = []
    for marshaller, arg in zip(sig.marshallers, args):
        margs.append(get_marshallable(marshaller.dbuscode, arg))
    return margs

class DBusType(object):
    pass

class Byte(int, DBusType):
    @classmethod
    def get_signature(cls):
        return 'y'

class Int16(int, DBusType):
    @classmethod
    def get_signature(cls):
        return 'n'

class Int32(int, DBusType):
    @classmethod
    def get_signature(cls):
        return 'i'

class Int64(int, DBusType):
    @classmethod
    def get_signature(cls):
        return 'x'

class UInt16(int, DBusType):
    @classmethod
    def get_signature(cls):
        return 'q'

class UInt32(int, DBusType):
    @classmethod
    def get_signature(cls):
        return 'u'

class UInt64(int, DBusType):
    @classmethod
    def get_signature(cls):
        return 't'

class ObjectPath(str, DBusType):
    @classmethod
    def get_signature(cls):
        return 'o'

class Signature(str, DBusType):
    @classmethod
    def get_signature(cls):
        return 'g'

class Variant(list, DBusType):
    @classmethod
    def get_signature(cls):
        return 'v'

    def __init__(self, value):
        list.__init__(self, [get_signature(value), value])

def Struct(*elems):
    sig = '(%s)' % ''.join(map(get_signature, elems))
    class _DBusStruct(list, DBusType):
        @classmethod
        def get_signature(cls):
            return sig
    return _DBusStruct

def Array(elem):
    sig = 'a' + get_signature(elem)
    class _DBusArray(list, DBusType):
        @classmethod
        def get_signature(cls):
            return sig
    return _DBusArray

def Array_from_signature(elem):
    sig = 'a' + elem
    class _DBusArray(list, DBusType):
        @classmethod
        def get_signature(cls):
            return sig
    return _DBusArray

def DictEntry(*elems):
    sig = '{%s}' % ''.join(map(get_signature, elems))
    class _DBusDictEntry(list, DBusType):
        @classmethod
        def get_signature(cls):
            return sig
    return _DBusEntry

