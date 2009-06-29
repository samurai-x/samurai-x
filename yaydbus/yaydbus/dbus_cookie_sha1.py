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

from __future__ import with_statement

import os.path
import hashlib
from uuid import uuid4
from binascii import hexlify, unhexlify

COOKIE_BASE = os.path.expanduser('~/.dbus-keyrings/')

class Cookie(object):
    def __init__(self, cookie_id, timestamp, data):
        self.id = cookie_id
        self.timestamp = timestamp
        self.data = data

def parse_cookie_file(filename):
    cookies = {}
    with open(filename, 'r') as f:
        for line in f.xreadlines():
            line = line.strip('\n')
            cookie_id, timestamp, hexdata = line.split(' ')
            cookie_id = int(cookie_id)
            timestamp = int(timestamp)
            data = unhexlify(hexdata)
            cookies[cookie_id] = Cookie(cookie_id, timestamp, data)
    return cookies

def get_cookie_file(context):
    return os.path.join(COOKIE_BASE, context)

def get_cookie_data(context, cookie_id):
    return parse_cookie_file(get_cookie_file(context))[cookie_id].data

def handle_auth_line(data):
    context, cookie_id, hexserverchallenge = data.split(' ')
    cookie_id = int(cookie_id)
    hexdata = hexlify(get_cookie_data(context, cookie_id))
    hexchallenge = uuid4().hex
    composite = ':'.join((hexserverchallenge, hexchallenge, hexdata))
    hash = hashlib.sha1(composite).hexdigest()
    # important to hexlify it ...
    return hexlify(' '.join((hexchallenge, hash)))
