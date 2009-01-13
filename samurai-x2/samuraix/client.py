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
import weakref

from ooxcb import xproto
from ooxcb.eventsys import EventDispatcher
from ooxcb.xproto import EventMask
from ooxcb.sizehints import SizeHints

from .rect import Rect

class Client(EventDispatcher):
    all_clients = []
    window_2_client_map = weakref.WeakValueDictionary()
    
    @classmethod
    def get_by_window(cls, window):
        return cls.window_2_client_map.get(window)

    def __init__(self, screen, window, wa, geometry):
        EventDispatcher.__init__(self)

        self.conn = window.conn
        self.geom = geometry
        
        self.screen = screen
        self.window = window
        self.actor = window
        self.window.push_handlers(self)
        log.info('New client: Client=%s Window=%s Actor=%s' % (self, self.window, self.actor))
        
        self.window.change_attributes(
                event_mask =
                    EventMask.StructureNotify |
                    EventMask.SubstructureNotify |
                    EventMask.PropertyChange
        )

        self.all_clients.append(self)
        self.window_2_client_map[self.window] = self

        self.apply_normal_hints()
        self.window.map()

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
            geom = Rect.from_class(self.geom)
        
        log.debug('client=%s size hints=%s', self, hints)
        if (hints.valid and geom.width > 1): # that one is a hack. TODO
            hints.compute(geom)
            self.resize(geom)
        else:
            log.warning('Invalid hints received!')

    def resize(self, geom):
        log.debug('Resizing: %s' % geom)
        self.window.configure_checked(width=geom.width, height=geom.height).check()
        self.conn.flush()

    # No map and unmap notify handlers here. 
    # Normally, we don't have another window
    # that needs to be mapped. The decoration plugin 
    # will have to setup this.
    #
    #def on_unmap_notify(self, evt):
    #    if evt.window is self.window:
    #        # if i am focused, unfocus me 
    #        if self.screen.focused_client is self:
    #            self.screen.focused_client = None
    #        self.actor.unmap()
    #
    #def on_map_notify(self, evt):
    #    self.actor.map()

    def on_destroy_notify(self, evt):
        log.warning('Got destroy notify event, Client=%s' % (self))
        self.remove()

    def remove(self):
        try:
            self.all_clients.remove(self)
            del self.window_2_client_map[self.window]
        except (ValueError, KeyError), e:
            log.warning(e)
        log.info('Removed me=%s! clients=%s' % (self, self.all_clients))
        if self.screen.focused_client is self:
            self.screen.focused_client = None

        self.dispatch_event('on_removed', self)

    def ban(self):
        if self.sticky:
            return # TODO?
        log.debug('banning %s' % self)
        self.window.unmap()
        # TODO: multiple decoration
        #self.actor.unmap()
        # TODO: set window state

    def unban(self):
        if self.sticky:
            return # TODO?
        log.debug('unbanning %s' % self)
        self.window.map()
        # TODO: multiple decoration
        #self.actor.map()
        # TODO: set window state

    def maximize(self):
        self.maximized = True
        self.backup_geom = self.frame_geom
        self.resize(self.screen.get_geometry())

    def unmaximize(self):
        self.maximized = False
        assert self.backup_geom
        self.resize(self.backup_geom)

    def toggle_maximize(self):
        if not self.maximized:
            self.maximize()
        else:
            self.unmaximize()

    def focus(self):
        #self.window.set_input_focus()

        if self.screen.focused_client is not None:
            self.screen.focused_client.blur()

        self.screen.focused_client = self
        self.dispatch_event('on_focus', self)
        # have to configure `frame` here!
        #self.actor.configure(stack_mode=pyxcb.window.STACK_MODE_ABOVE) 
        # TODO: grab buttons etc

    def blur(self):
        """
            Oh no! I am no longer focused!

            Grab the focus button and dispatch 'on_blur'.
        """
        self.dispatch_event('on_blur', self)

Client.register_event_type('on_focus')
Client.register_event_type('on_blur')
Client.register_event_type('on_removed')
