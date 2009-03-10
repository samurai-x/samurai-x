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

class AtomDict(dict):
    """
        A dictionary which is able to lazily load an atom:

        ::

            dic = AtomDict(my_connection)
            print dic['WM_CLASS'] # Yay, it is lazily loaded!

        You should not modify that manually.

    """
    def __init__(self, conn, *boo, **far):
        dict.__init__(self, *boo, **far)
        self.conn = conn
        self._by_id = {}

    def __missing__(self, key):
        self[key] = value = self.conn.core.intern_atom(key, False).reply().atom
        self._by_id[value.get_internal()] = value
        return value

    def get_by_id(self, aid):
        from .xproto import Atom # TODO: uuuuuuuugly
        if aid == 0:
            return None # TODO: That's basically AnyProperty ... better solution?
        try:
            return self._by_id[aid]
        except KeyError:
            self._by_id[aid] = atom = Atom(self.conn, aid)
            name = atom.get_name().reply().name.to_string()
            self[name] = aid
            return atom
