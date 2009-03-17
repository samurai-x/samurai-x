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

from ooxcb.eventsys import EventDispatcher

class SXObject(EventDispatcher):
    """
        *SXObject* is the base class for all important
        samurai-x2 classes. It is an event dispatcher
        (samurai-x2 uses the event system of ooxcb which
        is the event system of pyglet), but it also has
        a convenient method for plugins.

        .. attribute:: data

            A dictionary connecting keys to data.
    """
    def __init__(self):
        EventDispatcher.__init__(self)
        self.data = {} # key: data

    def attach_data(self, key, data):
        """
            Attaches the object *data* to *self*,
            identified by the key *key*. You can access
            the attached data using :attr:`SXObject.data`.

            That's a convenient method for plugins.
            They can easily attach any value to any
            samurai-x2 object.

            However, plugins shouldn't use
            :meth:`SXObject.attach_data` directly. Use
            :meth:`Plugin.attach_data_to`.
        """
        self.data[key] = data
