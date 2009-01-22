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

import os.path

import pkg_resources
from ooxcb import xproto
from ooxcb.xproto import EventMask

from .client import Client
from .rect import Rect
from .base import SXObject

def configure_request_to_dict(evt):
    cnf = {}
    mask = evt.value_mask
    # TODO: get rid of that boilerplate code
    if mask & xproto.ConfigWindow.X:
        cnf['x'] = evt.x
    if mask & xproto.ConfigWindow.Y:
        cnf['y'] = evt.y
    if mask & xproto.ConfigWindow.Width:
        cnf['width'] = evt.width
    if mask & xproto.ConfigWindow.Height:
        cnf['height'] = evt.height
    if mask & xproto.ConfigWindow.BorderWidth:
        cnf['border_width'] = evt.border_width
    if mask & xproto.ConfigWindow.Sibling:
        cnf['sibling'] = evt.sibling # does that work?
    if mask & xproto.ConfigWindow.StackMode:
        cnf['stack_mode'] = evt.stack_mode
    return cnf

class Screen(SXObject):
    client_class = Client

    def __init__(self, app, num):
        SXObject.__init__(self)

        self.app = app
        
        self.clients = set() 
        self.focused_client = None

        self.info = app.conn.get_setup().roots[num]
        self.root = self.info.root

        self.root.change_attributes(
            event_mask=
                EventMask.SubstructureRedirect |
                EventMask.SubstructureNotify |
                EventMask.StructureNotify |
                EventMask.Exposure |
                EventMask.PropertyChange
        )

        self.root.push_handlers(self)

        self.set_supported_hints()

    def get_geometry(self):
        return Rect.from_object(self.root.get_geometry().reply())

    def on_configure_request(self, evt):
        """
            Event's parent window is the event target of the
            configure request because sometimes we have a 
            window that isn't managed yet, but sends a configure
            request. This configure request would be lost.
        """
        cnf = configure_request_to_dict(evt)
        if cnf:
            evt.window.configure_checked(**cnf).check()
        else:
            log.warning('Strange configure request: No attributes set')

    def on_map_request(self, evt):
        #if evt.override_redirect:
        #    return # TODO: strange override_redirect values (88? oO)
        client = Client.get_by_window(evt.window)
        if client is None:
            # not created yet
            # NB we still not might manage this window - check manage()
            self.manage(evt.window)

    def on_destroy_notify(self, evt):
        win = evt.window
        client = Client.get_by_window(evt.window)
        log.debug('Root window got destroy notify event for window %s client %s' % (evt.window, client))
        if client is not None:
            client.window.valid = False # TODO: shouldn't be here.
            client.remove()

    def manage(self, window):
        """ 
            manage a new window - this may *not* result in a window being managed 
            if it is unsuitable 
        """
        attributes = window.get_attributes().reply()
        geom = window.get_geometry().reply()

        # override redirect windows need to be ignored - theyre not for us
        if attributes.override_redirect:
            log.debug('%s not managing %s override_redirect is set', self, window)
            return False

        client = self.client_class(self, window, attributes, geom)
        self.clients.add(client)

        self.dispatch_event('on_new_client', self, client)
        logging.debug('screen %s is now managing %s' % (self, client))
        client.push_handlers(on_removed=lambda foo: self.update_client_list,
                             on_focus=self.update_active_window)
        client.push_handlers(on_removed=self.on_client_removed)

        client.init()

        # If we have no focused client yet, use the newly managed client.
        if self.focused_client is None: 
            self.focus(client)

#        try:
#            window_type = window.get_property('_NET_WM_WINDOW_TYPE')[0].name
#            if window_type == '_NET_WM_WINDOW_TYPE_DOCK':
#                # make it sticky!
#                # ugly ugly
#                client.sticky = True
#            log.info('window is a %s' % window_type)
#        except Exception, e:
#            log.info('window does not seem to have size hints: %s' % repr(e))
        self.update_client_list()
        return client

    def unmanage(self, client):
        """
            Unmanage the client `client`.
            That means: map it. If we don't map it,
            it is unmapped. If it is unmapped, 
            samurai-x won't manage it if it's
            restarted.
        """
        log.info('Unmanaging %s ...' % client)
        self.clients.remove(client)
        client.actor.map()
        self.dispatch_event('on_unmanage_client', self, client)

    def on_unmanage_client(self, screen, client):
        """
            default handler: if the focused client is
            unmanaged, a random other client is focused.
            You May Override This.
        """
        if self.focused_client is client:
            new_client = None
            try:
                new_client = iter(self.clients).next() # TODO: expensive?
            except StopIteration:
                pass

    def on_client_removed(self, client):
        """
            if a client's window is removed, unmanage the client.
        """
        self.unmanage(client)

    def unmanage_all(self):
        while self.clients:
            self.unmanage(iter(self.clients).next()) # TODO: expensive?

    def update_client_list(self):
        # re-set _NET_CLIENT_LIST
        self.root.change_property('_NET_CLIENT_LIST', 
                'WINDOW',
                32,
                [c.window.get_internal() for c in self.client_class.all_clients])
        # TODO: calling get_internal() is not that nice. we'll have to change that.

    def update_active_window(self, client):
        """
            Update _NET_ACTIVE_WINDOW;
            self.focused_client is the new focused client
        """
        if self.focused_client is not None:
            self.root.change_property('_NET_ACTIVE_WINDOW', 'WINDOW', 32, [self.focused_client.window.get_internal()])

    def focus(self, client):
        """
            focus the client `client`.
            It may be None => No focus.
        """
        if client:
            log.debug('Screen. I am focusing %s %s %s' % (client, client.window, client.actor))
        else:
            log.debug('Screen. I am focusing nothing.')
        if self.focused_client is not None:
            self.focused_client.blur()
        self.focused_client = client
        if client is not None:
            client.focus()

    def scan(self):
        """ scan a screen for windows to manage """
        children = self.root.query_tree().reply().children
        for child in children:
            log.debug('%s found child %s', self, child)
            attr = child.get_attributes().reply()
            log.debug('attr %s', attr)

            # according to awesome we only do this when scanning...
            # ( not 100% sure why yet... )
            if attr.map_state != xproto.MapState.Viewable:
                log.debug('%s not managing %s - not viewable', self, child)
                continue
            # TODO: we receive the attributes two times here.
            self.manage(child)

    def set_supported_hints(self):
        pass

#        connection = self.root.connection # TODO?
#        atoms = [
#            connection.atoms['_NET_SUPPORTED'],
#            connection.atoms['_NET_CLIENT_LIST'],
#            connection.atoms['_NET_NUMBER_OF_DESKTOPS'],
#            connection.atoms['_NET_CURRENT_DESKTOP'],
#            connection.atoms['_NET_DESKTOP_NAMES'],
#            connection.atoms['_NET_ACTIVE_WINDOW'],
#            connection.atoms['_NET_CLOSE_WINDOW'],
#
#            connection.atoms['_NET_WM_NAME'],
#            connection.atoms['_NET_WM_ICON_NAME'],
#            connection.atoms['_NET_WM_WINDOW_TYPE'],
#            connection.atoms['_NET_WM_WINDOW_TYPE_NORMAL'],
#            connection.atoms['_NET_WM_WINDOW_TYPE_DOCK'],
#            connection.atoms['_NET_WM_WINDOW_TYPE_SPLASH'],
#            connection.atoms['_NET_WM_WINDOW_TYPE_DIALOG'],
#            connection.atoms['_NET_WM_STATE'],
#            connection.atoms['_NET_WM_STATE_STICKY'],
#            connection.atoms['_NET_WM_STATE_SKIP_TASKBAR'],
#            connection.atoms['_NET_WM_STATE_FULLSCREEN'],
#
#            connection.atoms['UTF8_STRING'],
#        ]
#        self.root.set_property('_NET_SUPPORTED', atoms, 32, 'ATOM')

Screen.register_event_type('on_new_client')
Screen.register_event_type('on_unmanage_client')
