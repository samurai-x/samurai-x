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

from UserDict import DictMixin

import logging
log = logging.getLogger(__name__)

from ooxcb.xproto import ModMask

class ClientMessageHandlers(object):
    """
        a little helper class for client message event handlers.
        You just connect an atom to a handler function and
        pass every :class:`ooxcb.xproto.ClientMessageEvent` to
        :meth:`handle`, and you will get the events handled.
    """
    def __init__(self):
        self._handlers = {}

    def register_handler(self, atom, func):
        """
            :param func: function taking one argument,
                         the client message event.
            :param atom: is the (cached!) atom object.
        """
        self._handlers[atom] = func

    def handle(self, evt):
        """
            call the matching handler function for *evt*
            and return the result or print a warning to the log
            if there is no matching handler.
        """
        try:
            return self._handlers[evt.type](evt)
        except KeyError:
            log.warning('No handler for the %s client message yet!' % \
                    (evt.type.get_name().reply().name.to_string()))

class OrderedDict(DictMixin):
    """
        an ordered dictionary, from http://code.activestate.com/recipes/496761/
    """
    def __init__(self, data=None, **kwdata):
        self._keys = []
        self._data = {}
        if data is not None:
            if hasattr(data, 'items'):
                items = data.items()
            else:
                items = list(data)
            for i in xrange(len(items)):
                length = len(items[i])
                if length != 2:
                    raise ValueError('dictionary update sequence element '
                        '#%d has length %d; 2 is required' % (i, length))
                self._keys.append(items[i][0])
                self._data[items[i][0]] = items[i][1]
        if kwdata:
            self._merge_keys(kwdata.iterkeys())
            self.update(kwdata)

    def __repr__(self):
        result = []
        for key in self._keys:
            result.append('(%s, %s)' % (repr(key), repr(self._data[key])))
        return ''.join(['OrderedDict', '([', ', '.join(result), '])'])

    def _merge_keys(self, keys):
        self._keys.extend(keys)
        newkeys = {}
        self._keys = [newkeys.setdefault(x, x) for x in self._keys
            if x not in newkeys]

    def update(self, data):
        if data is not None:
            if hasattr(data, 'iterkeys'):
                self._merge_keys(data.iterkeys())
            else:
                self._merge_keys(data.keys())
            self._data.update(data)

    def __setitem__(self, key, value):
        if key not in self._data:
            self._keys.append(key)
        self._data[key] = value

    def __getitem__(self, key):
        if isinstance(key, slice):
            result = [(k, self._data[k]) for k in self._keys[key]]
            return OrderedDict(result)
        return self._data[key]

    def __delitem__(self, key):
        del self._data[key]
        self._keys.remove(key)

    def keys(self):
        return list(self._keys)

    def copy(self):
        copyDict = odict()
        copyDict._data = self._data.copy()
        copyDict._keys = self._keys[:]
        return copyDict


from UserDict import DictMixin


#TODO use UserDict DictMixin or (2.6) collections.MutableMapping
class DictProxy(object):
    """ a dict proxy 
    creates a proxy to a dict
    the prefix argument is prefixed to all key operations so that 

    >>> d = {'a.b':1}
    >>> pd = DictProxy(d, 'a.')
    >>> pd['b'] == d['a.b']
    True
    
    all other dict operations should also work 
    """

    def __init__(self, other, prefix):
        self.prefix = prefix 
        self.other = other

    def __len__(self):
        return len(self.keys())

    def __getitem__(self, key):
        return self.other[self.prefix + key]

    def __setitem__(self, key, value):
        self.other[self.prefix + key] = value

    def __delitem__(self, key):
        del self.other[self.prefix + key]

    def __contains__(self, key):
        return self.other.__contains__(self.prefix + key)

    def get(self, key, default=None):
        return self.other.get(self.prefix+key, default)

    def iterkeys(self):
        return (key for key in self.other if key.startswith(self.prefix))

    def itervalues(self):
        return (value for key, value in self.other if key.startswith(self.prefix))

    def iteritems(self):
        return ((key, value) for key, value in self.other.iteritems() if key.startswith(self.prefix))

    def keys(self):
        return list(self.iterkeys())

    def values(self):
        return list(self.itervalues())

    def items(self):
        return list(self.iteritems())

    def update(self, values):
        for key, value in values.iteritems():
            self[key] = value


def parse_buttonstroke(s):
    """
        Return (modifiers, button id), extracted from the string `s`.

        It has to contain several modifiers and a button index,
        joined together with a '+'::

            CTRL+1
            MOD4+2

        1 is the left mouse button,
        2 the middle,
        3 the right button.
    """
    modmask, button = 0, 0

    parts = s.split('+')
    modifiers = parts[:-1]
    buttonpart = parts[-1]

    # create modmask
    for mod in modifiers:
        try:
            modmask |= MODIFIERS[mod.lower()]
        except KeyError:
            log.error('Unknown modifier: "%s"' % mod)

    # get button
    try:
        button = int(buttonpart)
    except ValueError:
        log.error('Invalid button: "%s"' % buttonpart)

    return modmask, button


MODIFIERS = {
        # TODO: I am not sure about the
        # following four modifiers.
        'alt': ModMask._1,
        'numlock': ModMask._2,
        'meta': ModMask._4,
        'altgr': ModMask._5,

        'shift': ModMask.Shift,
        'lock': ModMask.Lock,
        'ctrl': ModMask.Control,
        'control': ModMask.Control,

        'mod1': ModMask._1,
        'mod2': ModMask._2,
        'mod3': ModMask._3,
        'mod4': ModMask._4,
        'mod5': ModMask._5,
        }
