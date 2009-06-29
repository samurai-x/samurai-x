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

import sys
from cStringIO import StringIO

from . import marshal
from .streams import SocketStream

BIG_ENDIAN = ord('B')
LITTLE_ENDIAN = ord('l')

INVALID = 0
METHOD_CALL = 1
METHOD_RETURN = 2
ERROR = 3
SIGNAL = 4

NO_REPLY_EXPECTED = 0x01
NO_AUTO_START = 0x02

PATH_SEP = '/'

HEADER_SIGNATURE_RAW = 'yyyyuua(yv)'
HEADER_SIGNATURE = marshal.parse_signature(HEADER_SIGNATURE_RAW)
HEADER_FIELDS = {
        'PATH': (1, 'o'),
        'INTERFACE': (2, 's'),
        'MEMBER': (3, 's'),
        'ERROR_NAME': (4, 's'),
        'REPLY_SERIAL': (5, 'u'),
        'DESTINATION': (6, 's'),
        'SENDER': (7, 's'),
        'SIGNATURE': (8, 'g'),
        }

MAJOR_PROTOCOL = 1

def _generate_serials():
    while True:
        for serial in xrange(23, 2 ** 16):
            yield serial

SERIALS = _generate_serials()

def get_endianness():
    return {'little': LITTLE_ENDIAN,
            'big': BIG_ENDIAN}[sys.byteorder]

ENDIANNESS = get_endianness()

class Message(object):
    def __init__(self, **properties):
        self.type = 0
        self.flags = 0
        self.serial = 0
        self.body_data = ''
        self.body = ()
        # header fields
        self.path = None
        self.interface = None
        self.member = None
        self.error_name = None
        self.reply_serial = None
        self.destination = None
        self.sender = None
        self.signature = ''

        self.__dict__.update(properties)

    def unmarshal_body(self):
        self.body = marshal.parse_signature(self.signature).unmarshal_simple(self.body_data)

    def marshal_body(self):
        self.body_data = marshal.parse_signature(self.signature).marshal_simple(self.body)

    def _get_header_fields(self):
        ret = []
        # TODO: make boilerplate code
        for key, (ordinal, type) in HEADER_FIELDS.iteritems():
            key = key.lower()
            if getattr(self, key) is not None:
                ret.append((ordinal, (type, getattr(self, key))))
        return ret

    def _set_header_fields(self, data):
        datadict = dict(data)
        for key, (ordinal, type) in HEADER_FIELDS.iteritems():
            key = key.lower()
            if ordinal in datadict:
                setattr(self, key, datadict[ordinal])

    def marshal(self, stream):
        assert self.type != 0
        assert self.serial != 0
        HEADER_SIGNATURE.marshal(stream,
                   (ENDIANNESS,
                    self.type,
                    self.flags,
                    MAJOR_PROTOCOL,
                    len(self.body_data),
                    self.serial,
                    self._get_header_fields()
                    )
                   )
        marshal.align(stream, 8)
        stream.write(self.body_data)

    def marshal_simple(self):
        stream = StringIO()
        self.marshal(stream)
        return stream.getvalue()

    def unmarshal(self, stream):
        data = HEADER_SIGNATURE.unmarshal(stream)
        (endianness, type, flags, major_protocol, body_length,
            serial, header_fields) = data
        # read body
        marshal.skip_alignment(stream, 8)
        body = stream.read(body_length)
        assert endianness == ENDIANNESS
        assert type != 0
        assert major_protocol == MAJOR_PROTOCOL
        self.type = type
        self.flags = flags
        self.body_data = body
        self.serial = serial
        self._set_header_fields(header_fields)
        if (self.signature and self.body_data):
            self.unmarshal_body()

    def unmarshal_simple(self, data):
        return self.unmarshal(StringIO(data))

    @classmethod
    def create_from_data(cls, data):
        self = cls()
        self.unmarshal_simple(data)
        return self

    @classmethod
    def create_from_stream(cls, stream):
        self = cls()
        self.unmarshal(stream)
        return self

    @classmethod
    def create_from_fd(cls, fd):
        return cls.create_from_socketstream(SocketStream(fd))

    @classmethod
    def create_from_socketstream(cls, reader):
        self = cls()
        self.unmarshal(reader)
        return self

def join_path(*args):
    return PATH_SEP.join(args)

def get_surname(path):
    return path.rsplit(path, 1)[-1]

