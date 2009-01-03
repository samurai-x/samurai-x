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

import weakref
import functools

import pyxcb
from samuraix.focus import FocusStack

import logging
log = logging.getLogger(__name__)

class DesktopList(list):
    def previous(self, i):
        return self[(i or len(self)) - 1]

    def next(self, i):
        return self[(i + 1) % len(self)]

class Desktop(pyxcb.eventsystem.EventDispatcher):
    """ 
        relationship:
        Screen -> Desktop -> Client
    """
    def __init__(self, screen, name):
        self.screen = screen
        self.name = name
        self.clients = []
        self.focus_stack = FocusStack()

        log.info('created new desktop: %s' % self)

    def __repr__(self):
        return "<Desktop '%s' on '%s'>" % (self.name, self.screen)

    def add_client(self, client):
        log.debug('adding client %s to desktop %s' % (client, self))
        weakclient = weakref.ref(client)
        self.clients.append(weakclient)
        self.focus_stack.add(weakclient)
        self.focus_client(client)
        client.desktop = self
        client.push_handlers(
            on_removed=functools.partial(self._client_removed, client),
            on_focus=functools.partial(self._client_focused, client),
        )
        if self.screen.active_desktop is self:
            client.unban()
        else:
            client.ban()

        # this doesnt make any difference to showing the window decorations...
        client.connection.flush()

    def _client_removed(self, client):
        log.debug("desktop %s removing %s" % (self, client))
        weakclient = weakref.ref(client)
        self.clients.remove(weakclient)
        self.focus_stack.remove(weakclient)

    def _client_focused(self, client):
        log.debug('_client_focused %s' % client)
        self.focus_stack.move_to_top(client)

    def focus_client(self, client):
        # if config['focus_new'] .. etc
        client.focus()

    def focus_next(self):
        log.debug('%s focus_next' % self)
        cli = self.focus_stack.next()()
        if cli:
            cli.focus()
        else:
            log.debug('client dissappeared!')

    def focus_prev(self):
        log.debug('%s focus_prev' % self)
        cli = self.focus_stack.prev()()
        if cli:
            cli.focus()
        else:
            log.debug('client dissappeared!')

    def remove_client(self, client):
        assert client.desktop is self
        log.debug('removing client %s from desktop %s' % (client, self))
        client.desktop = None

    def on_show(self):
        log.info('showing desktop %s' % self)
        for client in self.clients:
            c = client()
            if c is not None:
                c.unban()
        
    def on_hide(self):
        log.info('hiding desktop %s' % self)
        for client in self.clients:
            c = client()
            if c is not None:
                c.ban()
    
Desktop.register_event_type('on_show')
Desktop.register_event_type('on_hide')
