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

class Plugin(object):
    """
        Base class for Plugins. You should derive your plugin
        from it. Every plugin is required to have a key describing its
        task. For example, the sx-simpledeco plugin has the
        'decoration' key. There are just a few constant plugin
        keys, so you are relatively free to use any key you like.
        Reserved keys are 'desktops' (there has to be a desktops plugin
        loaded, otherwise samurai-x2 will quit), ...

        .. data:: key

            The plugin key, usually a string

        :todo: complete the list of reserved keys.
    """
    key = NotImplemented

    def attach_data_to(self, obj, data):
        """
            Attaches *data* to the object *obj*, identified by
            :data:`key`. That's just a shortcut for

            ::

                obj.attach_data(self.key, data)

        """
        obj.attach_data(self.key, data)

    def get_data(self, obj):
        """
            Get the formerly attached data from *obj*, identified by
            :data:`key`. That's just a shortcut for

            ::

                return obj.data[self.key]

        """
        return obj.data[self.key]
