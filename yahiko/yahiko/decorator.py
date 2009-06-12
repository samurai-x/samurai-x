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

from samuraix import config
from samuraix.plugin import Plugin
from samuraix.cairo_ext import create_surface
from samuraix.rect import Rect
from ooxcb import xproto
from ooxcb.contrib import cairo

from yahiko import ui

# TODO does this make any difference?
#import psyco
#psyco.full()


class ClientWindow(ui.Window):
    def __init__(self, window, **kwargs):
        self.window = window 
        ui.Window.__init__(self, **kwargs)

    def set_render_coords(self, x, y, width, height):
        if x != self.rx or y != self.ry or width != self.width or height != self.height:
            ui.Window.set_render_coords(self, x, y, width, height)
            self.window.configure(x=x, y=y, width=width, height=height)


class Decorator(object):

    default_actor_style={
        'background.color': (0.2, 0.2, 0.2),
        'background.style': 'gradient',
        'background.fill-line': (0.0, 0.0, 0.0, 200.0),
        'background.fill-stops': [
            (0.0, 0.2, 0.2, 0.2),
            (0.7, 0.7, 0.7, 0.75),
            (1.0, 0.4, 0.4, 0.4),
        ],
        'border.color': (1, 1, 1),
        'border.style': 'gradient',
        'border.fill-line': (0.0, 0.0, 0.0, 200.0),
        'border.fill-stops': [
            (1.0, 0.2, 0.2, 0.2),
            (0.7, 0.7, 0.7, 0.75),
            (0.0, 0.4, 0.4, 0.4),
        ],
        'border.width': 4.0,
        'layout.padding': 6,
    }

    default_title_style={
        'text.color': (9, 9, 9),
        #'border.color': (1, 0, 0),
        #'border.width': 1.0,
        'layout.margin': 1,
    }

    default_clientwindow_style={
        'layout.margin': 1,
    }

    def __init__(self, plugin, screen, client):
        self.plugin = plugin
        self.client = client
        self.screen = screen

        self._obsolete = False
        self._active = True

        # This counter ensures that we don't run into
        # an infinite loop. If the window is configured,
        # we configure the actor. If the actor is configured,
        # we configure the window --> much fun.
        # Now, we increment the counter if we configure the
        # window. The actor will only be configured if
        # the counter equals 0. If it is greater than 0,
        # it is simply decremented.
        # Maybe that's not necessary, but it seems to be.
        self._window_configures = 0

        self.watched_atoms = [plugin.app.conn.atoms[name] for name in
                ["WM_NAME", "_NET_WM_NAME", "_NET_WM_VISIBLE_NAME"]
        ]

        self.create_actor_window()

    def create_actor_window(self):
        screen = self.screen
        client = self.client
        colormap = client.window.get_attributes().reply().colormap
        config = self.plugin.config

        geom = self.client.window.get_geometry().reply()
        # dont know how to get this from client.window so setting it to 0 
        client.window.configure(border_width=0)
        window_border = 0
        border = 2
        title_height = config.get('decorator.title.height', 20)

        client.actor = xproto.Window.create(self.plugin.app.conn,
                screen.root,
                screen.info.root_depth,
                screen.info.root_visual,
                geom.x,
                geom.y,
                # dont forget the borders of client.border in this calculation
                geom.width + (2*border) + (2*window_border),
                geom.height + title_height + (2*border) + (2*window_border),
                override_redirect=True,
                back_pixel=screen.info.white_pixel,
                colormap=colormap,
                # does this help flickering probs? im not sure...
                backing_store=xproto.BackingStore.WhenMapped,
                event_mask=
                    xproto.EventMask.Exposure |
                    xproto.EventMask.StructureNotify |
                    # Child.StructureNotify and Parent.SubstructureNotify
                    # seem to block each other. That's not what we want.
                    # I commented this out, and it seems to work.
                    #xproto.EventMask.SubstructureNotify |
                    xproto.EventMask.ButtonPress,
                )

        client.window.reparent(client.actor)

        client.actor.map()
        log.debug('created client actor client=%s actor=%s', client, client.actor)
        
        self.ui = ui.TopLevelContainer(
                client.actor, 
                screen.info.get_root_visual_type(),
                style=config.get('decorator.actor.style', self.default_actor_style),
                layouter=ui.VerticalLayouter,
        )
        window_title = self.client.get_window_title().encode('utf-8')

        title_sizer = ui.Container(
            height=title_height,
            layouter=ui.HorizontalLayouter,
        )
        self.ui.add_child(title_sizer)

        def make_func(f):
            if type(f) == str:
                def r(e):
                    self.plugin.app.plugins['actions'].emit(f, {
                            'screen': screen,
                            'x': e.event_x,
                            'y': e.event_y,
                            'client': self.client,
                    })
                return r
            return f

        for button in config.get('decorator.buttons.leftside', []):
            but = ui.Label(
                text=button.get('text'),
                width=button.get('width'),
                style=button.get('style'),
                on_button_press=make_func(button.get('func')),
            )
            title_sizer.add_child(but)

        self.title = ui.Label(
            text=window_title,
            style=config.get('decorator.title.style', self.default_title_style),
            on_button_press=make_func(config.get('decorator.title.func')),
        )
        title_sizer.add_child(self.title)

        for button in config.get('decorator.buttons.rightside', []):
            but = ui.Label(
                text=button.get('text'),
                width=button.get('width'),
                style=button.get('style'),
                on_button_press=make_func(button.get('func')),
            )
            title_sizer.add_child(but)

        self.clientwin = ClientWindow(
            client.window,
            style=config.get('decorator.clientwindow.style', self.default_clientwindow_style),
            width=geom.width,
            height=geom.height,
        )
        self.ui.add_child(self.clientwin)
        #self.ui.layout()
        #log.debug('after layout size is %s %s', self.ui.width, self.ui.height)
        #self.ui.render()

        client.push_handlers(
                on_focus=self.on_focus,
                #on_updated_geom=self.on_updated_geom,
                on_blur=self.on_blur,
        )

        client.window.push_handlers(
                on_property_notify=self.on_property_notify,
                on_configure_notify=self.window_on_configure_notify,
                #on_unmap_notify=self.on_unmap_notify,
                #on_map_notify=self.on_map_notify,
        )
        # TODO: dirty. something's wrong with substructure and structure notify.
        #client.screen.root.push_handlers(
        #        #on_configure_notify=self.screen_on_configure_notify,
        #)

        self.ui.fit()
        self.clientwin.width = None
        self.clientwin.height = None

    def window_on_configure_notify(self, event):
        if self._window_configures != 0:
            self._window_configures -=1
        else:
            self._window_configures += 1
            geom = Rect.from_object(event)
            if geom.width != self.clientwin.width or geom.height != self.clientwin.height:
                self.clientwin.width = geom.width
                self.clientwin.height = geom.height 
                self.ui.fit()
                # put the width and height back because we want these to be
                # automatic 
                self.clientwin.width = None
                self.clientwin.height = None
            
            #actor.configure(
            #        # dont forget the borders of client.border in this calculation
            #        width = geom.width + (2*border) + (2*window_border),
            #        height = geom.height + title_height + (2*border) + (2*window_border),
            #)

            #self.ui.layout()

    def on_focus(self, client):
        if (self._active and not self._obsolete):
            self.ui.render()

    def on_blur(self, client):
        if (self._active and not self._obsolete):
            self.ui.render()

    def on_property_notify(self, evt):
        """
            if a window changes a watched atom, redraw
            the title bar.
        """
        if (evt.atom in self.watched_atoms and not self._obsolete):
            self.title.text = self.client.get_window_title().encode('utf-8') # <- TODO: is that too expensive?
            self.ui.render()

    def remove(self):
        """ the end. """
        log.debug('removing deco for %s' % self.client)
        if self.client.window.valid:
            self.client.window.reparent(self.client.screen.root,
                    self.client.geom.x,
                    self.client.geom.y)
        self.client.actor.valid = False
        self.client.actor.destroy()
        self.client.conn.flush()
        self._obsolete = True
        # remove all handlers of everything
        self.client.remove_handlers(self)

        self.client.window.remove_handlers(
                on_property_notify=self.on_property_notify,
        )

        self.plugin.remove_data(self.client)
        del self.client


class DecoratorPlugin(Plugin):
    key = 'decoration'

    def __init__(self, app):
        self.app = app
        app.push_handlers(self)
        self.bindings = {}

    def on_load_config(self, config):
        self.config = config

    def on_ready(self, app):
        for screen in app.screens:
            screen.push_handlers(self)
            for client in screen.clients:
                self.create_decoration(screen, client)

    def on_new_client(self, screen, client):
        self.create_decoration(screen, client)

    def on_unmanage_client(self, screen, client):
        self.get_data(client).remove()

    def create_decoration(self, screen, client):
        # to have proper transparency, the actor window
        # has to use the same colormap as the foreign window.
        decorator = Decorator(self, screen, client)
        self.attach_data_to(client, decorator)
