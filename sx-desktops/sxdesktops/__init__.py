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

import logging
log = logging.getLogger(__name__)

from samuraix.plugin import Plugin
from ooxcb.eventsys import EventDispatcher

def cycle_indices(current, offset, length):
    """
        Return the index `current`, cycled 
        by `offset` indices.
    """
    return ((current or length) + offset) % length

class Desktop(object):
    def __init__(self, plugin, screen, name):
        self.plugin = plugin
        self.screen = screen
        self.name = name
        self.clients = [] # uh. maybe weak references are a good idea.

    def __repr__(self):
        return '<Desktop "%s">' % self.name

class ScreenData(EventDispatcher):
    def __init__(self, screen, desktops):
        EventDispatcher.__init__(self)

        self.screen = screen
        self.desktops = desktops
        self.active_desktop = desktops[0]
        self.active_desktop_idx = 0
        self.screen.push_handlers(self)
        self.scan()

    def scan(self):
        """
            scan the screen for already existing clients which are not
            catched by the `on_new_client` event handler
        """
        map(self.active_desktop.clients.append, self.screen.clients)

    def on_new_client(self, screen, client):
        #data = ClientData(self.active_desktop, client)
        #...attach_data_to(client, data)
        self.active_desktop.clients.append(client) 

    def set_active_desktop(self, desktop):
        #assert desktop in self.desktops # let's trust the user
        prev = self.active_desktop
        self.active_desktop = desktop
        self.active_desktop_idx = self.desktops.index(0)
        self.dispatch_event('on_change_desktop', self, prev)

    def on_change_desktop(self, fles, prev):
        self.update_clients(prev)
        # focus any client on the new desktop,
        # we don't want an off screen focus.
        self.screen.focus(self.active_desktop.clients.get(0, None))

    def set_active_desktop_idx(self, idx):
        prev = self.active_desktop
        self.active_desktop_idx = idx
        self.active_desktop = self.desktops[idx]
        self.dispatch_event('on_change_desktop', self, prev)

    def update_clients(self, previous_desktop):
        """
            ban and unban clients
        """
        log.debug('... updating %s %s %s' % (previous_desktop, self.active_desktop, previous_desktop.clients))
        for client in previous_desktop.clients:
            client.ban()

        for client in self.active_desktop.clients:
            client.unban()

    def cycle_desktops(self, offset=+1):
        self.set_active_desktop_idx(cycle_indices(self.active_desktop_idx, offset, len(self.desktops)))

    def cycle_clients(self, offset=+1):
        clients = self.active_desktop.clients
        if self.screen.focused_client is None:
            idx = 0
        else:
            idx = clients.index(self.screen.focused_client)
        try:
            client = clients[cycle_indices(idx, offset, len(clients))]
        except IndexError:
            client = None
        self.screen.focus(client)

ScreenData.register_event_type('on_change_desktop')

class ClientData(object):
    def __init__(self, desktop, client):
        self.client = client
        self.desktop = desktop

class SXDesktops(Plugin):
    # atm, every screen has the same amount of desktops
    key = 'desktops'

    def __init__(self, app):
        self.app = app
        app.push_handlers(self)
        app.plugins['actions'].register('desktops.cycle', self.action_cycle)
        app.plugins['actions'].register('desktops.cycle_clients', self.action_cycle_clients)
        app.plugins['actions'].register('desktops.goto', self.action_goto)

    def on_load_config(self, config):
        self.names = config.get('desktops.names', ['one desktop'])
        self.create_desktops(self.app.screens, self.names)

    def create_desktops(self, screens, names):
        for screen in screens:
            desktops = [Desktop(self, screen, name) for name in self.names]
            self.attach_data_to(screen, ScreenData(screen, desktops))

    def action_cycle(self, info):
        """
            cycle desktop

            parameters:
                `offset`: int
                    optional, defaults to 1

        """
        self.get_data(info['screen']).cycle_desktops(info.get('offset', 1))

    def action_cycle_clients(self, info):
        self.get_data(info['screen']).cycle_clients(info.get('offset', 1))

    def action_goto(self, info):
        """
            go to a specified desktop

            parameters:
                `index`: int
                    index, starting at 0 (required)

        """
        self.get_data(info['screen']).set_active_desktop_idx(info['index'])

