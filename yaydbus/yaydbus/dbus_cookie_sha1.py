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
