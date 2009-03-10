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
import weakref

from ooxcb import xproto
from ooxcb.xproto import EventMask
from ooxcb.sizehints import SizeHints

from .rect import Rect
from .base import SXObject
from .util import ClientMessageHandlers

class Client(SXObject):
    all_clients = []
    window_2_client_map = weakref.WeakValueDictionary()
    
    @classmethod
    def get_by_window(cls, window):
        return cls.window_2_client_map.get(window)

    def __init__(self, screen, window, wa, geometry):
        SXObject.__init__(self)

        self.conn = window.conn
        self.app = screen.app
        self.geom = Rect.from_object(geometry)
        self.client_message_handlers = ClientMessageHandlers()
        self.install_handlers()

        self.net_wm_state = set() # a set of Atom instances, values for _NET_WM_STATE
        self.net_wm_states = dict((name, self.conn.atoms[name]) for name in (
            '_NET_WM_STATE_MODAL', '_NET_WM_STATE_STICKY',
            '_NET_WM_STATE_MAXIMIZED_VERT', '_NET_WM_STATE_MAXIMIZED_HORZ',
            '_NET_WM_STATE_SHADED', '_NET_WM_STATE_SKIP_TASKBAR',
            '_NET_WM_STATE_SKIP_PAGER', '_NET_WM_STATE_HIDDEN',
            '_NET_WM_STATE_FULLSCREEN', '_NET_WM_STATE_ABOVE',
            '_NET_WM_STATE_BELOW', '_NET_WM_STATE_DEMANDS_ATTENTION'
            ))

        self.screen = screen
        self.window = window
        self.window.valid = True

        self.actor = window
        self.window.push_handlers(self)
        log.info('New client: Client=%s Window=%s Actor=%s' % (self, self.window, self.actor))
        
        self.window.change_attributes(
                event_mask =
                    EventMask.StructureNotify |
                    EventMask.PropertyChange
        )

        self.all_clients.append(self)
        self.window_2_client_map[self.window] = self

        self.apply_normal_hints()
        self.window.map()
        self.conn.flush()

    def __repr__(self):
        return '<Client at 0x%x for %s>' % (id(self), repr(self.window))

    def is_focused(self):
        return self.screen.focused_client is self

    def init(self):
        """ called after actor is set. That's not so nice. """
        self.actor.push_handlers(on_configure_notify=self.actor_on_configure_notify)

    def msg_active_window(self, evt):
        """
            Handler for the _NET_ACTIVE_WINDOW client message.

            If it is called on an unmanaged window, it will not
            be handled - that's what we want.
        """
        self.screen.focus(self)

    def msg_change_state(self, evt):
        """
            handler for WM_CHANGE_STATE.

            This will iconify(?) me.
        """
        if evt.data.data32[0] == xproto.WMState.Iconic:
            self.iconify()
        else:
            log.warning('Unhandled WM_CHANGE_STATE: data: %s' % str(evt.data.data32))

    def process_netwm_client_message(self, evt):
        """
            process an EWMH / NETWM client message event.
        """
        return self.client_message_handlers.handle(evt)

    def install_handlers(self):
        self.client_message_handlers.register_handler(
                self.conn.atoms['_NET_ACTIVE_WINDOW'],
                self.msg_active_window
                )
        self.client_message_handlers.register_handler(
                self.conn.atoms['WM_CHANGE_STATE'],
                self.msg_change_state
                )

    def on_property_notify(self, evt):
        log.debug('Got property notify event: %s changed in %s.' % 
                (evt.atom.get_name().reply().name.to_string(), evt.window))

    def on_client_message(self, evt):
        log.debug('Got client message event: %s, data32: %s' % 
                (evt.type.get_name().reply().name.to_string(), evt.data.data32))
        self.process_netwm_client_message(evt)

    def actor_on_configure_notify(self, evt):
        """
            Event handler: update the geometry
        """
        self.geom = Rect.from_object(evt)

    def apply_normal_hints(self, hints=None, geom=None):
        """
            apply the WM_NORMAL_HINTS (TODO: complete)

            :param hints: A `SizeHints` object or None (fetch it)
            :param geom: received geom - will not be modified; if None,
                use a copy of `self.geom`
        """
        apply_style = True
        if hints is None:
            values = self.window.get_property('WM_NORMAL_HINTS', 'WM_SIZE_HINTS').reply().value
            hints = SizeHints.from_values(values)
        if geom is None:
            geom = self.geom.copy()
        
        log.debug('client=%s size hints=%s', self, hints)
        if (hints.valid and geom.width > 1): # that one is a hack. TODO
            hints.compute(geom)
            self.resize(geom)
        else:
            log.warning('Invalid hints received!')

    def resize(self, geom):
        """
            Configure the main window (not the actor)
            to use width and height from `geom`.
        """
        log.debug('Resizing: %s' % geom)
        self.window.configure_checked(width=geom.width, height=geom.height).check()
        self.conn.flush()

    def on_destroy_notify(self, evt):
        log.warning('Got destroy notify event, Client=%s Window=%s' % (self, evt.window))
        if evt.window is self.window:
            self.remove()

    def remove(self):
        log.info('Removed me=%s! clients=%s' % (self, self.all_clients))
        self.window.valid = False
        self.dispatch_event('on_removed', self)
        
    def unmanage(self):
        """ called by the screen """
        if self.window.valid:
            # We don't want to receive any further events.
            self.window.change_attributes(event_mask=0)
            self.unban()
        try:
            self.all_clients.remove(self)
            del self.window_2_client_map[self.window]
        except (ValueError, KeyError), e:
            log.warning(e)
        self.window.remove_handlers(self)

    def ban(self, withdrawn=True):
        """
            Unmap the actor window and set WM_STATE.

            :Parameters:
                `withdrawn`: bool
                    If True, the WM_STATE is set to withdrawn
                    If False, it's Iconic.
        """
        # TODO: respect sticky?
        log.debug('banning %s' % self)
        self.actor.unmap()
        self.conn.flush()

        state = xproto.WMState.Withdrawn if withdrawn else xproto.WMState.Iconic
        self.window.change_property(
                'WM_STATE',
                'CARDINAL',
                32,
                [state, 0]) # TODO: icon window?
        self.conn.flush()

    def iconify(self):
        """
            same as `self.ban(False)`
        """
        self.ban(False)

    def unban(self):
        """
            Map the actor window.
        """
        # TODO: respect sticky?
        log.debug('unbanning %s' % self)
        self.actor.map()
        self.window.change_property(
                'WM_STATE',
                'CARDINAL',
                32,
                [xproto.WMState.Normal, 0]) # TODO: icon window?
        self.conn.flush()

    def focus(self):
        """
            Focus the client. Do not call that, use
            `Screen.focus` instead.
        """
        # grab the input focus
        self.window.set_input_focus()
        # set it abvoe
        self.actor.configure(stack_mode=xproto.StackMode.Above)
        self.conn.flush()
        # TODO: grab buttons etc
        self.dispatch_event('on_focus', self)

    def blur(self):
        """
            Blur / Unfocus the client.
            Do not call, use `Screen.focus`.
        """
        self.dispatch_event('on_blur', self)

Client.register_event_type('on_focus')
Client.register_event_type('on_blur')
Client.register_event_type('on_removed')