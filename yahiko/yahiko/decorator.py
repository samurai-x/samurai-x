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
# DISCLAIMED. in no event shall samurai-x.org  be liable for any
# direct, indirect, incidental, special, exemplary, or consequential damages
# (including, but not limited to, procurement of substitute goods or services;
# loss of use, data, or profits; or business interruption) however caused and
# on any theory of liability, whether in contract, strict liability, or tort
# (including negligence or otherwise) arising in any way out of the use of this
# software, even if advised of the possibility of such damage.
"""
    yahiko.decorator is a window decorator plugin for samurai-x

    Configuration
    -------------

    .. attribute:: decorator.actor.style

        A dictionary describing the style. Read yahiko.ui.Window for more 

    .. attribute:: decorator.title.style
        
        A dictionary describing the style. Read yahiko.ui.Window for more 

    .. attribute:: decorator.leftside.buttons

        A list of dictionaries describing buttons on the left side of the 
        window. For example::

            {
                'text': 'X',
                'width': '20',
                'style': {
                    # yahiko.ui style...
                },
                'bindings': {
                    '1': 'some.action',
                },                      
            }

    .. attribute:: decorator.rightside.buttons

        See the documentation for decorator.leftside.buttons.

"""

import logging
log = logging.getLogger(__name__)

from samuraix import config
from samuraix.plugin import Plugin
from samuraix.cairo_ext import create_surface
from samuraix.rect import Rect
from samuraix.util import parse_buttonstroke
from ooxcb.protocol import xproto
from ooxcb.contrib import cairo
from ooxcb import XNone

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
        'text.color': (1.0, 1.0, 1.0),
        #'border.style': 'fill',
        #'border.color': (1, 0, 0),
        #'border.width': 1.0,
        'layout.margin': 1,
        'clip': True,
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

        conn = screen.conn


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
                    xproto.EventMask.SubstructureRedirect |
                    xproto.EventMask.ButtonPress,
                )

        client.window.reparent(client.actor)
        log.debug('created client actor client=%s actor=%s', client, client.actor)

        # check if we are on the active desktop. unban/ban
        # the client to get a valid WM_STATE and map the
        # actor window if needed.
        current = client.screen.info.ewmh_get_current_desktop()
        desktop = client.window.ewmh_get_desktop()
        if (current is None or current == desktop):
            log.debug('Unbanning %s because it is on the active desktop.' % client)
            client.unban()
        else:
            log.debug('Banning %s because it is not on an active desktop (active=%s, client\'s=%s)' % (client, current, desktop))
            client.ban(False, False)

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

        def make_func(bindings):
            parsed_bindings = {}
            for k, v in bindings.iteritems():
                parsed_bindings[parse_buttonstroke(k)] = v
            def r(e):
                try:
                    func = parsed_bindings[(e.state, e.detail)]
                except KeyError:
                    return 
                if type(func) == str:
                    self.plugin.app.plugins['actions'].emit(func, {
                            'screen': screen,
                            'x': e.event_x,
                            'y': e.event_y,
                            'client': self.client,
                    })
                else:
                    func()
            return r

        for button in config.get('decorator.buttons.leftside', []):
            but = ui.Label(
                text=button.get('text'),
                width=button.get('width'),
                style=button.get('style'),
                on_button_press=make_func(button.get('bindings')),
            )
            title_sizer.add_child(but)

        self.title = ui.Label(
            text=window_title,
            style=config.get('decorator.title.style', self.default_title_style),
            on_button_press=make_func(config.get('decorator.title.bindings')),
        )
        title_sizer.add_child(self.title)

        for button in config.get('decorator.buttons.rightside', []):
            but = ui.Label(
                text=button.get('text'),
                width=button.get('width'),
                style=button.get('style'),
                on_button_press=make_func(button.get('bindings')),
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
                #on_handle_net_wm_state=self.on_handle_net_wm_state,
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

        client.actor.push_handlers(
                on_configure_request=self.actor_on_configure_request,
        )

        self.ui.fit()
        self.clientwin.width = None
        self.clientwin.height = None

    def actor_on_configure_request(self, event):
        if event.window == self.client.window:
            self.client.actor.configure(x=event.x, y=event.y)

            geom = self.client.actor.get_geometry().reply()

            evt = xproto.ConfigureNotifyEvent(self.client.window.conn)
            evt.event = self.client.window
            evt.window = self.client.window
            evt.above_sibling = XNone
            # i think this should be the actual location of the client.window
            evt.x = geom.x + self.clientwin.rx
            evt.y = geom.y + self.clientwin.ry
            evt.width = self.clientwin.rwidth
            evt.height = self.clientwin.rheight
            evt.border_width = 1
            evt.override_redirect = False
            self.client.window.send_event(xproto.EventMask.StructureNotify, evt)
            self.client.window.conn.flush()

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
        if self._obsolete:
            return 

        conn = self.screen.conn

        if (evt.atom in (
                conn.atoms['WM_NAME'],
                conn.atoms['_NET_WM_NAME'],
                conn.atoms['_NET_WM_VISIBLE_NAME'],
            )):
            title_text = self.client.get_window_title().encode('utf-8') # <- TODO: is that too expensive?
            if title_text != self.title.text:
                self.title.text = title_text
                self.title.dirty()

    def on_handle_net_wm_state(self, present, atom, source_indication):
        if atom == self.conn.atoms['_NET_WM_STATE_FULLSCREEN']:
            if present:
                self.temporary_remove()
            else:
                self.restore_temporary_remove()

    def temporary_remove(self):
        self._stashed_actor = self.client.actor
        self._stashed_actor.ban()
        self.client.window.reparent(self.client.screen.root,
                self.client.geom.x,
                self.client.geom.y)
        self.client.actor = self.client.window
    
    def restore_temporary_remove(self):
        self.client.actor = self._stashed_actor
        self.client.actor.unban()
        self.client.window.reparent(self.client.actor,
                self.client.geom.x,
                self.client.geom.y)

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
        self.ui.remove_handlers()

        self.plugin.remove_data(self.client)
        self.client.actor = self.client.window

        del self.client
        del self.ui


class DecoratorPlugin(Plugin):
    key = 'decoration'

    def __init__(self, app):
        self.app = app
        app.push_handlers(self)
        app.plugins['actions'].register(
                'decorator.toggle_decoration', self.action_toggle_decoration)

    def on_load_config(self, config):
        self.config = config

    def on_ready(self, app):
        for screen in app.screens:
            screen.push_handlers(self)
            for client in screen.clients:
                self.create_decoration(screen, client)

    def on_new_client(self, screen, client):
        if client.conn.atoms['_NET_WM_WINDOW_TYPE_DOCK'] not in client.window_type:
            self.create_decoration(screen, client)

    def on_unmanage_client(self, screen, client):
        # attempt to remove the decoration 
        # the window might not actually of been decorated
        try:
            self.get_data(client).remove()
        except KeyError:
            pass

    def create_decoration(self, screen, client):
        # to have proper transparency, the actor window
        # has to use the same colormap as the foreign window.
        decorator = Decorator(self, screen, client)
        self.attach_data_to(client, decorator)

    def action_toggle_decoration(self, info):
        screen = info['screen']
        client = info.get('client', screen.focused_client)
        try:
            decorator = self.get_data(client)
        except KeyError:
            self.create_decoration(screen, client)
        else:
            decorator.remove()
    




