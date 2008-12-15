# Copyright (c) 2008, samurai-x.org
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

from . import cookie
from .util import cached_property
from .pythonize import Pythonizer

class Atom(object):
    def __init__(self, connection, _atom):
        self.connection = connection
        self._atom = _atom

    def __repr__(self):
        return '<XCB Atom ID: %d>' % self._atom

    def xize(self):
        return self._atom

    @cached_property
    def name(self):
        return self.get_name()

    def get_name(self):
        return self.request_name().value

    def request_name(self):
        return cookie.AtomNameRequest(self.connection, self)

    def __eq__(self, other):
        return self._atom == other._atom

    def __ne__(self, other):
        return self._atom != other._atom

    def __bool__(self):
        return self._atom > 0

@Pythonizer.pythonizer('ATOM')
def pythonize_atom(connection, xid):
    return Atom(connection, xid)

class AtomDict(dict):
    def __init__(self, connection, *boo, **far):
        super(AtomDict, self).__init__(*boo, **far)
        self.connection = connection

    def __missing__(self, key):
        self[key] = value = self.connection.get_atom_by_name(key)
        return value
