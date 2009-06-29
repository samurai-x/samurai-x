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

from cStringIO import StringIO
from struct import pack, unpack, calcsize

class MarshallingError(Exception):
    pass

def get_alignment(count, align):
    return (align - (count % align)) % align

def align(stream, align_to):
    stream.write(get_alignment(stream.tell(), align_to) * '\x00')

def skip_alignment(stream, align_to):
    stream.seek(get_alignment(stream.tell(), align_to), 1)

def unpack_from_stream(fmt, stream):
    return unpack(fmt, stream.read(calcsize(fmt)))

MARSHALLERS = {}
SIMPLE_MARSHALLERS = [
        ('y', 'b', 1),
        ('b', 'I', 4),
        ('n', 'h', 2),
        ('q', 'H', 2),
        ('i', 'i', 4),
        ('u', 'I', 4),
        ('x', 'q', 8),
        ('t', 'Q', 8),
        ('d', 'd', 8),
        ]

def _setup():
    for dbuscode, pycode, align_to in SIMPLE_MARSHALLERS:    
        MARSHALLERS[dbuscode] = SimpleMarshaller(pycode, dbuscode, align_to)
    MARSHALLERS['s'] = StringMarshaller()
    MARSHALLERS['o'] = ObjectPathMarshaller()
    MARSHALLERS['g'] = SignatureMarshaller()
    MARSHALLERS['v'] = VariantMarshaller()

class Marshaller(object):
    def __init__(self, dbuscode, align_to=1):
        self.align_to = align_to
        self.dbuscode = dbuscode

    def marshal_simple(self, obj):
        buf = StringIO()
        self.marshal(buf, obj)
        return buf.getvalue()

    def marshal(self, stream, obj):
        raise NotImplementedError()

    def unmarshal_simple(self, string):
        buf = StringIO(string)
        return self.unmarshal(buf)

    def unmarshal(self, stream):
        raise NotImplementedError()

class SimpleMarshaller(Marshaller):
    def __init__(self, pycode, dbuscode, align_to):
        Marshaller.__init__(self, dbuscode, align_to)
        self.pycode = pycode
        self.structcode = '=' + pycode

    def marshal(self, stream, obj):
        align(stream, self.align_to)
        stream.write(pack(self.structcode, obj))

    def unmarshal(self, stream):
        skip_alignment(stream, self.align_to)
        return unpack_from_stream(self.structcode, stream)[0]

class Struct(Marshaller):
    def __init__(self, dbuscode, marshallers, align_to=8):
        Marshaller.__init__(self, dbuscode, align_to)
        self.marshallers = marshallers

    def marshal(self, stream, members):
        align(stream, self.align_to)
        for obj, marshaller in zip(members, self.marshallers):
            assert obj is not None and marshaller is not None
            marshaller.marshal(stream, obj)

    def unmarshal(self, stream):
        skip_alignment(stream, self.align_to)
        ret = []
        for marshaller in self.marshallers:
            ret.append(marshaller.unmarshal(stream))
        return tuple(ret)

class DictEntry(Struct):
    def __init__(self, dbuscode, marshallers):
        if len(marshallers) != 2:
            raise MarshallingError('DICT_ENTRY is required to have exactly two fields')
        if isinstance(marshallers[0], (Struct, DictEntry, Array)):
            raise MarshallingError('DICT_ENTRY\'s first field is required to be a basic type')
        Struct.__init__(self, dbuscode, marshallers)

class Array(Marshaller):
    def __init__(self, dbuscode, marshaller):
        Marshaller.__init__(self, dbuscode, 4)
        self.marshaller = marshaller

    def marshal(self, stream, members):
        align(stream, self.align_to)
        # Python dict -> array of DICT_ENTRY
        if isinstance(self.marshaller, DictEntry):
            members = members.items()
        substream = StringIO()
        for obj in members:
            self.marshaller.marshal(substream, obj)
        stream.write(pack('=I', substream.tell()))
        align(stream, self.marshaller.align_to)
        stream.write(substream.getvalue())

    def unmarshal(self, stream):
        skip_alignment(stream, self.align_to)
        size = unpack_from_stream('=I', stream)[0]
        skip_alignment(stream, self.marshaller.align_to)
        root = stream.tell()
        ret = []
        if size == 0:
            return ret
        while True:
            ret.append(self.marshaller.unmarshal(stream))
            if (stream.tell() - root) >= size:
                break
        # array of DICT_ENTRY -> Python dict
        if isinstance(self.marshaller, DictEntry):
            ret = dict(ret)
        return ret

class StringMarshaller(Marshaller):
    def __init__(self, dbuscode='s', align_to=4):
        Marshaller.__init__(self, dbuscode, align_to)

    def marshal(self, stream, obj):
        align(stream, self.align_to)
        if isinstance(obj, unicode):
            obj = obj.encode('utf-8')
        stream.write(pack('=I', len(obj)) + obj + '\x00')

    def unmarshal(self, stream):
        skip_alignment(stream, self.align_to)
        length = unpack_from_stream('=I', stream)[0]
        string = stream.read(length)
        assert stream.read(1) == '\x00'
        return string.decode('utf-8')

class SignatureMarshaller(Marshaller):
    def __init__(self):
        Marshaller.__init__(self, 'g', 1)

    def marshal(self, stream, obj):
        align(stream, self.align_to)
        if isinstance(obj, unicode):
            obj = obj.encode('utf-8')
        stream.write(pack('=B', len(obj)) + obj + '\x00')

    def unmarshal(self, stream):
        skip_alignment(stream, self.align_to)
        length = unpack_from_stream('=B', stream)[0]
        string = stream.read(length)
        assert stream.read(1) == '\x00'
        return string.decode('utf-8')

class ObjectPathMarshaller(StringMarshaller):
    def __init__(self):
        StringMarshaller.__init__(self, 'o')

class VariantMarshaller(Marshaller):
    """
        for the marshalling of VARIANT, you have to pass
        a tuple (dbuscode, value). Example::

            marshaller.marshal_simple([('s', 'hey!')])

        If you unmarshal it, you'll get a simple value
        as return value (no tuple here!)

    """
    def __init__(self):
        Marshaller.__init__(self, 'v', 1)

    def marshal(self, stream, obj):
        # No alignment here. The StringMarshaller already does that.
        #align(stream, self.align_to)
        dbuscode, value = obj
        # first the typecode
        MARSHALLERS['g'].marshal(stream, dbuscode)
        # then the value
        # read it from a substream. I think that has something
        # to do with alignmnt, though I am not sure :)
        parse_signature(dbuscode).marshal(stream, (value,))

    def unmarshal(self, stream):
        # No alignment skipping here because StringMarshaller.unmarshal
        # already does that.
        #skip_alignment(stream, self.align_to)
        dbuscode = MARSHALLERS['g'].unmarshal(stream)
        val = parse_signature(dbuscode).unmarshal(stream)[0]
        return val

class Signature(Struct):
    def __init__(self, dbuscode, marshallers):
        # Don't align signatures.
        Struct.__init__(self, dbuscode, marshallers, 1)

def _parse_once(signature, idx=0, accept_dict_entry=False):
    marshaller = None
    length = 0
    char = signature[idx]
    if char in MARSHALLERS:
        marshaller = MARSHALLERS[char]
        length = 1
    elif char == 'a':
        submarshaller, length = _parse_once(signature, idx + 1, True)
        marshaller = Array(signature[idx:idx+length+1], submarshaller)
        length += 1 # count the 'a'
    elif char == '(': # a struct ...
        marshallers = []
        length = 1
        while signature[idx + length] != ')':
            submarshaller, length_add = _parse_once(signature, idx + length)
            marshallers.append(submarshaller)
            length += length_add
        length += 1
        marshaller = Struct(signature[idx:idx+length], marshallers)
    elif char == '{': # dict_entry
        marshallers = []
        length = 1
        while signature[idx + length] != '}':
            submarshaller, length_add = _parse_once(signature, idx + length)
            marshallers.append(submarshaller)
            length += length_add
        length += 1
        marshaller = DictEntry(signature[idx:idx+length], marshallers)
        # reject dict_entry if it isn't inside an array
        if not accept_dict_entry:
            raise MarshallingError('DICT_ENTRY is only allowed as array value type')
    return (marshaller, length)

def parse_signature(signature):
    idx = 0
    # remove the trailing null byte
    signature = signature.rstrip('\x00')
    length = len(signature)
    marshallers = []
    while idx < length:
        marshaller, length_add = _parse_once(signature, idx)
        marshallers.append(marshaller)
        idx += length_add
    return Signature(signature, marshallers)

_setup()
