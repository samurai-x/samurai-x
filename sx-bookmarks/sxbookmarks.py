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

import logging
log = logging.getLogger(__name__)

from samuraix.plugin import Plugin
from samuraix.util import wait_for_key

from ooxcb import keysymdef

class SXBookmarks(Plugin):
    key = 'bookmarks'

    def __init__(self, app):
        self.app = app
        app.plugins['actions'].register('bookmarks.set', self.action_set)
        app.plugins['actions'].register('bookmarks.set_key', self.action_set_key)
        app.plugins['actions'].register('bookmarks.activate', self.action_activate)
        app.plugins['actions'].register('bookmarks.activate_key', self.action_activate_key)
        app.push_handlers(self)

    def on_new_screen(self, screen):
        self.attach_data_to(
                screen,
                {})
    
    def action_set(self, info):
        screen = info['screen']
        name = info['name']
        log.debug('Setting bookmark "%s" to %s' % (name, screen.focused_client))
        self.get_data(screen)[name] = screen.focused_client

    def action_activate(self, info):
        screen = info['screen']
        name = info['name']
        client = self.get_data(screen).get(name, None)
        if client is None:
            log.warning('There is no bookmark named "%s"' % name)
        else:
            log.debug('Activating bookmark "%s"' % name)
            screen.focus(client)

    def action_set_key(self, info):
        screen = info['screen']
        def callback(keycode):
            keysym = screen.conn.keysyms.get_keysym(keycode, 0)
            if not keysym:
                log.warning('Unknown keysym: %s' % keysym)
                return
            name = keysymdef.names[keysym]
            info['name'] = name
            self.action_set(info)

        wait_for_key(screen, callback)

    def action_activate_key(self, info):
        screen = info['screen']
        def callback(keycode):
            keysym = screen.conn.keysyms.get_keysym(keycode, 0)
            if not keysym:
                log.warning('Unknown keysym: %s' % keysym)
                return
            name = keysymdef.names[keysym]
            info['name'] = name
            self.action_activate(info)

        wait_for_key(screen, callback)
