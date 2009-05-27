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

import os.path

from ooxcb import xproto
from ooxcb.xproto import EventMask

from .client import Client
from .rect import Rect
from .base import SXObject
from .util import ClientMessageHandlers

def configure_request_to_dict(evt):
    """
        Convert the :class:`ooxcb.xproto.ConfigureRequestEvent` *evt*
        to a dictionary containing only the values that are requested
        to be changed and return it.
    """
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
    """
        A wrapper for a physical X screen. For many users, there will
        only be one Screen. For some others, there will be more.

        The class attribute client_class is the class that will be used
        to create new clients. You can change it, but that's maybe not
        such a good idea.

    """
    client_class = Client

    def __init__(self, app, num):
        SXObject.__init__(self)

        self.app = app
        self.conn = app.conn

        self.clients = set()
        self.client_message_handlers = ClientMessageHandlers()
        self.focused_client = None
        # possible states for _NET_WM_STATE.
        self.possible_states = dict((name, self.conn.atoms[name]) for name in (
            '_NET_WM_STATE_MODAL', '_NET_WM_STATE_STICKY',
            '_NET_WM_STATE_MAXIMIZED_VERT', '_NET_WM_STATE_MAXIMIZED_HORZ',
            '_NET_WM_STATE_SHADED', '_NET_WM_STATE_SKIP_TASKBAR',
            '_NET_WM_STATE_SKIP_PAGER', '_NET_WM_STATE_HIDDEN',
            '_NET_WM_STATE_FULLSCREEN', '_NET_WM_STATE_ABOVE',
            '_NET_WM_STATE_BELOW', '_NET_WM_STATE_DEMANDS_ATTENTION'
            ))

        self.info = app.conn.get_setup().roots[num]
        self.root = self.info.root

        self.root.change_attributes(
            event_mask=
                EventMask.SubstructureRedirect |
                EventMask.SubstructureNotify |
                EventMask.StructureNotify |
                EventMask.Exposure |
                EventMask.PropertyChange,
            cursor=
                app.cursors['Normal']
        )

        self.root.push_handlers(self)

        self.set_supported_hints()

        self.check_window = self.create_check_window()

    def get_geometry(self):
        """
            return a :class:`samuraix.rect.Rect` describing the
            geometry of the physical screen.
        """
        return Rect.from_object(self.root.get_geometry().reply())

    def create_check_window(self):
        """
            The 'check window' is the window required by the
            `_NET_SUPPORTING_WM_CHECK hint`, specified in the
            netwm standard. It only has a `_NET_WM_NAME` property,
            set to 'samurai-x2'. It's override-redirected and
            invisible.
            This also sets the `_NET_SUPPORTING_WM_CHECK` hint.
        """
        win = xproto.Window.create(self.conn,
                self.root,
                self.info.root_depth,
                self.info.root_visual,
                0,
                0,
                1,
                1,
                0,
                override_redirect=True)
        self.root.change_property('_NET_SUPPORTING_WM_CHECK', 'WINDOW', 32, [win.get_internal()])
        win.change_property('_NET_SUPPORTING_WM_CHECK', 'WINDOW', 32, [win.get_internal()])
        win.change_property('_NET_WM_NAME', 'UTF8_STRING', 8, map(ord, 'samurai-x')) # TODO: nicer conversion
        return win

    def process_netwm_client_message(self, evt):
        """
            process the netwm client message *evt*.
        """
        return self.client_message_handlers.handle(evt)

    def on_client_message(self, evt):
        """
            Root windows' event handler for
            :class:`ooxcb.xproto.ClientMessageEvent`:
            pass the client message event *evt* to
            :meth:`process_netwm_client_message`.
        """
        self.process_netwm_client_message(evt)

    def on_configure_request(self, evt):
        """
            Root windows' event handler for
            :class:`ooxcb.xproto.ConfigureRequestEvent`.
            Fulfill the request, or give a warning if we received a very
            strange configure request: one that doesn't request to change
            any values o_O

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
        """
            Root windows' event handler for
            :class:`ooxcb.xproto.MapRequestEvent`. That will
            create a client for the window if there isn't one already.
            In any case, this will map the window as requested.
        """
        #if evt.override_redirect:
        #    return # TODO: strange override_redirect values (88? oO)
        client = Client.get_by_window(evt.window)
        if client is None:
            # not created yet
            # NB we still not might manage this window - check manage()
            if self.manage(evt.window):
                return
        # uh, did we forget that?
        evt.window.map()

    def on_destroy_notify(self, evt):
        """
            Root windows' event handler for
            :class:`ooxcb.xproto.DestroyNotifyEvent`.
            If there is a client managing *evt*'s window, call
            :meth:`samuraix.client.Client.remove` and set
            its window.valid to False.
        """
        win = evt.window
        client = Client.get_by_window(evt.window)
        log.debug('Root window got destroy notify event for '
                  'window %s client %s' % (evt.window, client))
        if client is not None:
            client.window.valid = False # TODO: shouldn't be here.
            client.remove()

    def manage(self, window):
        """
            manage a new window - this may *not* result in a window
            being managed if it is unsuitable (ie a dock
            or override-redirected window)
        """
        # check window type
        window_type = map(self.conn.atoms.get_by_id,
            window.get_property('_NET_WM_WINDOW_TYPE', 'ATOM').reply().value)
        if self.conn.atoms['_NET_WM_WINDOW_TYPE_DOCK'] in window_type:
            log.debug('%s not managing %s - is a dock.' % (self, window))
            # TODO: ignore other types, too?
            return

        attributes = window.get_attributes().reply()
        geom = window.get_geometry().reply()

        # override redirect windows need to be ignored - theyre not for us
        if attributes.override_redirect:
            log.debug('%s not managing %s override_redirect is set' % \
                    (self, window))
            return False

        client = self.client_class(self, window, geom)
        logging.debug('screen %s is now managing %s' % (self, client))
        self.clients.add(client)

        self.dispatch_event('on_new_client', self, client)
        client.push_handlers(on_removed=self.on_client_removed)

        client.init()

        # If we have no focused client yet, use the newly managed client.
        if self.focused_client is None:
            self.focus(client)

        self.update_client_list()
        return client

    def unmanage(self, client):
        """
            Unmanage the client *client*.
            That means: unban it. If we don't unban it, it is unmapped.
            If it is unmapped, samurai-x won't manage it if it's restarted.
        """
        log.info('Unmanaging %s ...' % client)
        client.unmanage()
        self.update_client_list()
        self.clients.remove(client)
        self.dispatch_event('on_unmanage_client', self, client)
        log.info('Unmanaged %s' % client)

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
            event handler: if a client's window is removed,
            unmanage the client.

            :todo: is that necessary?
        """
        self.unmanage(client)

    def unmanage_all(self):
        """
            Unmanage all my clients. That is usually called at
            the end of samurai-x' lifetime.
        """
        while self.clients:
            self.unmanage(iter(self.clients).next()) # TODO: expensive?

    def update_client_list(self):
        """
            update the root window's `_NET_CLIENT_LIST` property as described
            in the netwm standard.
        """
        # re-set _NET_CLIENT_LIST
        self.root.change_property('_NET_CLIENT_LIST',
                'WINDOW',
                32,
                [c.window.get_internal() for c in self.client_class.all_clients])
        # TODO: calling get_internal() is not that nice. we'll have to change that.

    def update_active_window(self):
        """
            Update `_NET_ACTIVE_WINDOW`; set it to *self.focused_client*.
        """
        if self.focused_client is not None:
            self.root.change_property('_NET_ACTIVE_WINDOW', 'WINDOW', 32,
                    [self.focused_client.window.get_internal()])

    def focus(self, client):
        """
            focus the client `client`.
            It may be None => No focus.
        """
        if client:
            log.debug('Screen. I am focusing %s %s %s' % (client, client.window, client.actor))
        else:
            log.debug('Screen. I am focusing nothing.')
        # set the new focused client before calling `blur`. A client's
        # "on_blur" event handlers can use `Client.is_focused` then.
        # Only call `blur` if the client's window is valid (ie not already destroyed)
        old_client = self.focused_client
        self.focused_client = client
        if (old_client is not None and old_client.window.valid):
            old_client.blur()
        # set the hint
        self.update_active_window()
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
        """
            set the `_NET_SUPPORTED` atom to a bunch of atoms that
            we might not support yet, but in the future. Until then,
            let's hope that nobody notices that.
        """
        atoms = self.conn.atoms

        supported = [
            atoms['_NET_SUPPORTED'],
            atoms['_NET_CLIENT_LIST'],
            atoms['_NET_NUMBER_OF_DESKTOPS'], # by sx-desktops
            atoms['_NET_CURRENT_DESKTOP'],
            atoms['_NET_DESKTOP_NAMES'],
            atoms['_NET_ACTIVE_WINDOW'],
            atoms['_NET_CLOSE_WINDOW'],

            atoms['_NET_WM_NAME'],
            atoms['_NET_WM_ICON_NAME'],
            atoms['_NET_WM_WINDOW_TYPE'],
            atoms['_NET_WM_WINDOW_TYPE_NORMAL'],
            atoms['_NET_WM_WINDOW_TYPE_DOCK'],
            atoms['_NET_WM_WINDOW_TYPE_SPLASH'],
            atoms['_NET_WM_WINDOW_TYPE_DIALOG'],
            atoms['_NET_WM_STATE'],
            atoms['_NET_WM_STATE_STICKY'],
            atoms['_NET_WM_STATE_SKIP_TASKBAR'],
            atoms['_NET_WM_STATE_FULLSCREEN'],

            atoms['UTF8_STRING'],
        ]
        # We are not using the reparenting-to-a-fakeroot technique
        # described in the netwm standard,
        # so we don't need to set _NET_VIRTUAL_ROOTS.
        # TODO: ... do we need to set _NET_DESKTOP_LAYOUT? Are we a pager?
        self.root.change_property('_NET_SUPPORTED', 'ATOM', 32,
                [s.get_internal() for s in supported]) # TODO: nicer conversion

Screen.register_event_type('on_new_client')
Screen.register_event_type('on_unmanage_client')
