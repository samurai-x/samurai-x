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
from ooxcb.list import List
from ooxcb.eventsys import EventDispatcher

def cycle_indices(current, offset, length):
    """
        Return the index `current`, cycled
        by `offset` indices.
    """
    return ((current or length) + offset) % length

class FocusStack(list):
    def move_to_top(self, client):
        if self.current() is client:
            return
        try:
            self.remove(client)
            self.append(client)
        except IndexError:
            log.warn('cant move client %s to top! not in list!' % client)

    def prev(self):
        c = self.pop(-1)
        self.insert(0, c)
        return self.current()

    def next(self):
        c = self.pop(0)
        self.append(c)
        return self.current()

    def current(self):
        try:
            return self[-1]
        except IndexError:
            return None

class Desktop(EventDispatcher):
    def __init__(self, plugin, screen, name, layouter, idx):
        EventDispatcher.__init__(self)

        self.plugin = plugin
        self.screen = screen
        self.name = name
        self.layouter = layouter
        self.clients = FocusStack() # maybe weak references are a good idea.
        self.idx = idx

    def register(self, info):
        self.layouter.register_desktop(self, info)

    def __repr__(self):
        return '<Desktop "%s">' % self.name

    def on_focus(self, client):
        """ a client was focused: move it to top of the focus stack """
        self.clients.move_to_top(client)
        self.rearrange()

    def add_client(self, client):
        self.clients.append(client)
        self.dispatch_event('on_new_client', self, client)

        client.push_handlers(on_focus=self.on_focus)
        client.window.change_property(
                '_NET_WM_DESKTOP',
                'CARDINAL',
                32,
                [self.idx])

    def rearrange(self):
        self.dispatch_event('on_rearrange', self)

    def remove_client(self, client):
        try:
            self.clients.remove(client)
        except ValueError:
            return False
        else:
            client.remove_handlers(on_focus=self.on_focus)
            self.dispatch_event('on_unmanage_client', self, client)
            return True

Desktop.register_event_type('on_new_client')
Desktop.register_event_type('on_rearrange')
Desktop.register_event_type('on_unmanage_client')

class ScreenData(EventDispatcher):
    def __init__(self, screen, desktops):
        EventDispatcher.__init__(self)

        self.screen = screen
        self.desktops = desktops
        self.active_desktop = desktops[0]
        self.active_desktop_idx = 0
        self.update_hints()

        self.screen.push_handlers(self)
        self.install_handlers()
        self.scan()

    def msg_current_desktop(self, evt):
        """
            handler for the _NET_CURRENT_DESKTOP client message
        """
        self.set_active_desktop_idx(evt.data.data32[0])

    def install_handlers(self):
        self.screen.client_message_handlers.register_handler(
                self.screen.conn.atoms['_NET_CURRENT_DESKTOP'],
                self.msg_current_desktop)

    def scan(self):
        """
            scan the screen for already existing clients which are not
            catched by the `on_new_client` event handler
        """
        map(self.active_desktop.add_client, self.screen.clients)

    def on_new_client(self, screen, client):
        #data = ClientData(self.active_desktop, client)
        #...attach_data_to(client, data)
        self.active_desktop.add_client(client)
        # TODO: focus it?
        self.active_desktop.rearrange()

    def on_unmanage_client(self, screen, client):
        for desktop in self.desktops:
            if desktop.remove_client(client):
                break # a client is only on one desktop
        else:
            log.error('Could not unmanage client %s' % client)
            return
        # display the next one ...
        #self.screen.focus(self.active_desktop.clients.current())
        self.active_desktop.rearrange()

    def set_active_desktop(self, desktop):
        #assert desktop in self.desktops # let's trust the user
        prev = self.active_desktop
        self.active_desktop = desktop
        self.active_desktop_idx = self.desktops.index(desktop)
        self.dispatch_event('on_change_desktop', self, prev)

    def update_hints(self):
        """
            Update _NET_CURRENT_DESKTOP.
        """
        self.screen.root.change_property('_NET_CURRENT_DESKTOP',
                'CARDINAL', 32, [self.active_desktop_idx])
        self.screen.conn.flush()

    def on_change_desktop(self, fles, prev):
        self.update_clients(prev)
        self.update_hints()
        # focus any client on the new desktop,
        # we don't want an off screen focus.
        self.screen.focus(self.active_desktop.clients.current())

    def set_active_desktop_idx(self, idx):
        prev = self.active_desktop
        self.active_desktop_idx = idx
        self.active_desktop = self.desktops[idx]
        self.dispatch_event('on_change_desktop', self, prev)

    def update_clients(self, previous_desktop):
        """
            ban and unban clients
        """
        log.debug('... updating %s %s %s' % (previous_desktop,
            self.active_desktop, previous_desktop.clients))
        for client in previous_desktop.clients:
            client.ban()

        for client in self.active_desktop.clients:
            client.unban()

    def cycle_desktops(self, offset=+1):
        self.set_active_desktop_idx(cycle_indices(self.active_desktop_idx,
            offset, len(self.desktops)))

    def cycle_clients(self, offset=+1):
        clients = self.active_desktop.clients
        self.screen.focus(clients.next()) # TODO: respect offset

ScreenData.register_event_type('on_change_desktop')

class ClientData(object):
    def __init__(self, desktop, client):
        self.client = client
        self.desktop = desktop

class Layouter(object):
    def register_desktop(self, desktop, info):
        raise NotImplementedError()

class FloatingLayouter(Layouter):
    """ just do nothing. no layout is floating layout. """
    def register_desktop(self, desktop, info):
        pass

class SXDesktops(Plugin):
    # atm, every screen has the same amount of desktops
    key = 'desktops'

    def __init__(self, app):
        self.app = app
        self.config = {}
        self.layouters = {
                'floating': FloatingLayouter()
                }

        app.push_handlers(self)
        app.plugins['actions'].register('desktops.cycle', self.action_cycle)
        app.plugins['actions'].register('desktops.cycle_clients',
                self.action_cycle_clients)
        app.plugins['actions'].register('desktops.goto', self.action_goto)

    def on_load_config(self, config):
        #self.names = config.get('desktops.names', ['one desktop'])
        self.config = config.get('desktops.desktops', {})

    def on_ready(self, app):
        self.create_desktops(app.screens, self.config)

    def register_layouter(self, name, layouter):
        self.layouters[name] = layouter

    def create_desktops(self, screens, config):
        for screen in screens:
            # TODO: every screen has the same desktops?
            desktops = []
            for idx, (name, info) in enumerate(self.config):
                desktop = Desktop(self, screen, name,
                        self.layouters[info.get('layout', 'floating')], idx)
                desktop.register(info)
                desktops.append(desktop)
            self.attach_data_to(screen, ScreenData(screen, desktops))

            screen.root.change_property('_NET_NUMBER_OF_DESKTOPS', 'CARDINAL',
                    32, [len(desktops)])

            # We don't support large desktops here.
            # But that could be added by a plugin.
            root_geom = screen.get_geometry()
            screen.root.change_property('_NET_DESKTOP_GEOMETRY',
                    'CARDINAL', 32,
                    [root_geom.width, root_geom.height])
            screen.root.change_property('_NET_DESKTOP_VIEWPORT',
                    'CARDINAL', 32, [0, 0])
            screen.root.change_property('_NET_DESKTOP_NAMES',
                    'UTF8_STRING', 8,
                    List.from_stringlist(
                        (desktop.name for desktop in desktops)
                    )
            )

            # TODO: support _NET_WORKAREA, maybe _NET_SHOWING_DESKTOP?

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
