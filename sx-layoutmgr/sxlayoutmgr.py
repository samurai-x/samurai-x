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

"""
    sx-layoutmgr is a plugin that adds layout algorithms to desktops. 

    Actions
    -------

    .. function:: layoutmgr.set_layout()
        :module:

        sets the layout of a desktop 

    .. function:: layoutmgr.cycle()
        :module:
        
        cycles through the different desktop layouts

"""

from samuraix.plugin import Plugin
from samuraix.util import OrderedDict
from samuraix import app

from ooxcb import xproto

import logging
log = logging.getLogger(__name__)


class Layout(object):
    def __init__(self, desktop):
        self.desktop = desktop    
        desktop.push_handlers(self)

    def detach(self):
        self.desktop.remove_handlers(self)

    def on_rearrange(self, desktop):
        self.layout()

    def layout(self):
        raise NotImplemented()


class FloatingLayout(Layout):
    """ do nothing. """
    name = 'floating'

    def layout(self):
        # raise the currently focused window to the top
        if self.desktop.clients:
            self.desktop.clients.current() \
                    .actor.configure(stack_mode=xproto.StackMode.Above)
            app.conn.flush()


class MaxLayout(Layout):
    """ make the focused window fill the screen """

    name = 'max'

    def layout(self):
        geom = self.desktop.screen.get_geometry()
        client = self.desktop.clients.current()
        client.actor.configure(x=geom.x, y=geom.y, width=geom.width, height=geom.height)
        app.conn.flush()


class VertLayout(Layout):
    """ arrange windows vertically with equal height """

    name = 'vert'

    def layout(self):
        if self.desktop.clients:
            geom = self.desktop.screen.get_geometry()
            h = geom.height / len(self.desktop.clients)
            t = 0 
            for client in self.desktop.clients:
                client.actor.configure(x=0, y=t, width=geom.width, height=h)
                t += h
            app.conn.flush()


class HorizLayout(Layout):
    """ arrange windows horizontally with equal width """

    name = 'horiz'

    def layout(self):
        if self.desktop.clients:
            geom = self.desktop.screen.get_geometry()
            w = geom.width / len(self.desktop.clients)
            t = 0 
            for client in self.desktop.clients:
                client.actor.configure(x=t, y=0, width=w, height=geom.height)
                t += w
            app.conn.flush()


class SXLayoutMgr(Plugin):
    key = 'layoutmgr'

    def __init__(self, app):
        self.layouters = OrderedDict()
        self.register(FloatingLayout)
        self.register(MaxLayout)
        self.register(VertLayout)
        self.register(HorizLayout)

        self.app = app
        app.push_handlers(self)

        # register actions
        app.plugins['actions'].register('layoutmgr.set_layout',
                self.action_set_layout)
        app.plugins['actions'].register('layoutmgr.cycle',
                self.action_cycle)

    def action_set_layout(self, info):
        """
            set the layout of the current desktop.

            parameters:
                `name`: str
                    identifier of the layout

            needed:
                `screen`
        """
        self.attach_layouter(
                info['screen'].data['desktops'].active_desktop,
                self.layouters[info['name']]
                )

    def action_cycle(self, info):
        """
            cycle the layouts for the current desktop

            parameters:
                `offset`: int
                    offset to cycle, defaults to +1

            needed:
                `screen`
        """
        offset = info.get('offset', 1)
        desktop = info['screen'].data['desktops'].active_desktop
        layouter_cls = self.get_data(desktop).__class__
        current_name = getattr(layouter_cls, 'name', layouter_cls.__name__)

        keys = self.layouters.keys()
        length = len(keys)
        index = keys.index(current_name)
        new_index = ((index or length) + offset) % length
        new_layouter_cls = self.layouters[keys[new_index]]
        self.attach_layouter(desktop, new_layouter_cls)

    def register(self, layouter_cls):
        name = getattr(layouter_cls, 'name', layouter_cls.__name__)
        log.info('registering layouter %s = %s', name, layouter_cls)
        self.layouters[name] = layouter_cls

    def on_ready(self, app):
        # should potentially do this in on_create_screen but 
        # that means making sure desktop.on_create_screen is called 
        # first...
        for screen in app.screens:
            screendata = screen.data['desktops']
            screendata.push_handlers(self)
            for desktop in screendata.desktops:
                log.debug('trying to attach to %s...', desktop)
                layouter_name = desktop.config.get('layout')
                if not layouter_name:
                    log.debug('no layouter_name')
                    continue
                layouter_cls = self.layouters.get(layouter_name)
                if not layouter_cls:
                    log.error('cant find layouter %s', name)
                    return
                self.attach_layouter(desktop, layouter_cls)

    def attach_layouter(self, desktop, layouter_cls):
        """
            attach the layouter class *layouter_cls* to *desktop*.
            That will overwrite any layouter that was
            attached before.
        """
        if self.has_data(desktop):
            self.get_data(desktop).detach()
            self.remove_data(desktop)
        log.debug('attached %s', layouter_cls)
        layouter = layouter_cls(desktop)
        self.attach_data_to(desktop, layouter)
        #desktop.push_handlers(on_rearrange=self.on_rearrange)
        # rearrange it automatically
        layouter.layout()
