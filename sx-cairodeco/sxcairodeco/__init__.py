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

from sxbind import MODIFIERS # Oh no, we depend on sxbind! TODO? (maybe move into samuraix.contrib or something like that?)
from sxactions import ActionInfo

def parse_buttonstroke(s):
    """
        Return (modifiers, button id), extracted from the string `s`.

        It has to contain several modifiers and a button index,
        joined together with a '+':

        CTRL+1
        MOD4+2

        1 is the left mouse button,
        2 the middle,
        3 the right button.
    """
    modmask, button = 0, 0

    parts = s.split('+')
    modifiers = parts[:-1]
    buttonpart = parts[-1]

    # create modmask
    for mod in modifiers:
        try:
            modmask |= MODIFIERS[mod.lower()]
        except KeyError:
            log.error('Unknown modifier: "%s"' % mod)

    # get button
    try:
        button = int(buttonpart)
    except ValueError:
        log.error('Invalid button: "%s"' % buttonpart)

    return modmask, button

def compute_window_geom(geom):
    """ convert the 'frame geom' to the 'window geom' """
    geom.y += config['cairodeco.height']
    geom.height -= config['cairodeco.height']

def compute_actor_geom(geom):
    """ convert the 'window geom' to the 'geom geom' """
    geom.y = max(0, geom.y - config['cairodeco.height'])
    geom.height = max(1, geom.height + config['cairodeco.height'])

def hex_to_cairo_color(color):
    """
        convert a color in hexadecimal form (e.g. '#ff00ee').
        return a 3-element tuple of (R, G, B), where R, G
        and B are 0..255.
    """
    color = color.lstrip('#')
    return tuple(int(p, 16) for p in (color[:2], color[2:4], color[4:]))

class ClientData(object):
    def __init__(self, plugin, screen, client):
        self.plugin = plugin
        self.client = client

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

        # create the cairo stuff
        self.surface = create_surface(client.actor,
                client.screen.info.get_root_visual_type())
        self.cr = cairo.cairo_create(self.surface)
        cairo.cairo_set_operator(self.cr, cairo.CAIRO_OPERATOR_SOURCE)
        cairo.cairo_set_source_surface(self.cr, self.surface, 0, 0)
        cairo.cairo_set_source_rgba(self.cr, 255, 0, 0, 0)

        self.client.push_handlers(
                on_focus=self.on_focus,
                on_updated_geom=self.on_updated_geom,
                on_blur=self.on_blur,
                )

        self.client.actor.push_handlers(
                on_configure_notify=self.actor_on_configure_notify,
                on_expose=self.on_expose,
                on_button_press=self.on_button_press,
                )
        self.client.window.push_handlers(
                on_property_notify=self.on_property_notify,
                on_configure_notify=self.window_on_configure_notify,
                on_unmap_notify=self.on_unmap_notify,
                on_map_notify=self.on_map_notify,
                )
        # TODO: dirty. something's wrong with substructure and structure notify.
        self.client.screen.root.push_handlers(
                on_configure_notify=self.screen_on_configure_notify
                )

        self.redraw()

    def on_focus(self, client):
        if (self._active and not self._obsolete):
            self.redraw()

    def on_blur(self, client):
        if (self._active and not self._obsolete):
            self.redraw()

    def on_expose(self, evt):
        if (self._active and not self._obsolete):
            self.redraw()

    def on_unmap_notify(self, evt):
        if not self._obsolete:
            self._active = False
            self.client.actor.unmap()
            self.client.conn.flush()

    def on_updated_geom(self, client):
        """
            Event handler: called when the client's geom
            attribute changed. Resize the surface and
            redraw.
        """
        log.debug('Got on_updated_geom, redrawing')
        cairo.cairo_xcb_surface_set_size(self.surface,
                client.geom.width, client.geom.height)
        self.redraw()

    def screen_on_configure_notify(self, evt):
        if not self._obsolete:
            if evt.window is self.client.window:
                return self.window_on_configure_notify(evt)
            elif evt.window is self.client.actor:
                return self.actor_on_configure_notify(evt)

    def on_map_notify(self, evt):
        if not self._obsolete:
            self._active = True
            self.client.actor.map()
            self.client.conn.flush()

    def on_button_press(self, evt):
        self.plugin.emit_action(self.client, evt)

    def on_property_notify(self, evt):
        """
            if a window changes a watched atom, redraw
            the title bar.
        """
        if (evt.atom in self.plugin.watched_atoms and not self._obsolete):
            self.redraw()

    def redraw(self):
        log.debug('Redrawing, active=%s, obsolete=%s' % (self._active, self._obsolete))

        extents = cairo.cairo_text_extents_t()

        window_title = self.client.get_window_title().encode('utf-8') # <- TODO: is that too expensive?

        if self.client.is_focused():
            bg_color = hex_to_cairo_color(config['cairodeco.color'])
            fg_color = hex_to_cairo_color(config['cairodeco.title.color'])
        else:
            bg_color = hex_to_cairo_color(config.get('cairodeco.inactive_color', config['cairodeco.color']))
            fg_color = hex_to_cairo_color(config.get('cairodeco.title.inactive_color', config['cairodeco.title.color']))

        cairo.cairo_set_source_rgba(self.cr,
                bg_color[0], bg_color[1], bg_color[2], 1)
        cairo.cairo_set_operator(self.cr, cairo.CAIRO_OPERATOR_SOURCE)
        cairo.cairo_paint(self.cr)

        cairo.cairo_set_operator(self.cr, cairo.CAIRO_OPERATOR_OVER)

        cairo.cairo_set_source_rgba(self.cr, fg_color[0], fg_color[1], fg_color[2], 1)

        cairo.cairo_show_text(self.cr, window_title)
        cairo.cairo_text_extents(self.cr, window_title, extents)

        width = self.client.geom.width
        x = 0

        if config['cairodeco.title.position'] == 'left':
            x = 0
        elif config['cairodeco.title.position'] == 'right':
            x = width - extents.x_advance
        elif config['cairodeco.title.position'] == 'center':
            x = (width - extents.x_advance) / 2


        cairo.cairo_move_to(self.cr,
                x,
                config['cairodeco.height'] - (config['cairodeco.height'] - extents.height) / 2.0)
        self.client.conn.flush()

    def actor_on_configure_notify(self, evt):
        """ if the actor is configured, configure the window, too """
        if not self._obsolete:
            geom = Rect(width=evt.width, height=evt.height)
            compute_window_geom(geom)
            self._window_configures += 1
            self.client.window.configure(**geom.to_dict()) # TODO: is that efficient?
            self.client.conn.flush()

    def window_on_configure_notify(self, evt):
        """ if the window is configured, configure the actor, too """
        log.debug('%s got window configure notify event, configure counter=%d' % (self, self._window_configures))
        if self._window_configures == 0:
            geom = Rect.from_object(evt)
            compute_actor_geom(geom)
            self.client.actor.configure(**geom.to_dict())
            self.client.conn.flush()
        else:
            self._window_configures -= 1

    def remove(self):
        """ the end. """
        log.debug('removing deco for %s' % self.client)
        if self.client.window.valid:
            self.client.window.reparent(self.client.screen.root,
                    self.client.geom.x,
                    self.client.geom.y)
            # TODO: don't stick them at (0, 0). geom.x/geom.y seem are 0 - why?
        self.client.actor.destroy()
        self.client.conn.flush()
        self._obsolete = True
        # remove all handlers of everything
        self.client.remove_handlers(self)
        self.client.actor.remove_handlers(
                on_configure_notify=self.actor_on_configure_notify,
                on_expose=self.on_expose,
                on_button_press=self.on_button_press,
                )
        self.client.window.remove_handlers(
                on_property_notify=self.on_property_notify,
                on_configure_notify=self.window_on_configure_notify,
                on_unmap_notify=self.on_unmap_notify,
                on_map_notify=self.on_map_notify,
                )
        self.client.screen.root.remove_handlers(
                on_configure_notify=self.screen_on_configure_notify
                )
        self.plugin.remove_data(self.client)
        del self.client

class SXDeco(Plugin):
    key = 'decoration'

    def __init__(self, app):
        self.app = app
        app.push_handlers(self)
        self.bindings = {}

        self.watched_atoms = [self.app.conn.atoms[name] for name in
                ["WM_NAME", "_NET_WM_NAME", "_NET_WM_VISIBLE_NAME"]
                ]

    def on_load_config(self, config):
        for stroke, action in config.get('decoration.bindings', {}).iteritems():
            self.bindings[parse_buttonstroke(stroke)] = action

    def on_ready(self, app):
        for screen in app.screens:
            screen.push_handlers(self)
            for client in screen.clients:
                self.create_client_data(screen, client)

    def on_new_client(self, screen, client):
        self.create_client_data(screen, client)

    def on_unmanage_client(self, screen, client):
        self.get_data(client).remove()

    def create_client_data(self, screen, client):
        # to have proper transparency, the actor window
        # has to use the same colormap as the foreign window.
        colormap = client.window.get_attributes().reply().colormap
        client.actor = xproto.Window.create(self.app.conn,
                screen.root,
                screen.info.root_depth,
                screen.info.root_visual,
                client.geom.x,
                client.geom.y,
                client.geom.width,
                client.geom.height + config['cairodeco.height'],
                override_redirect=True,
                back_pixel=screen.info.white_pixel,
                colormap=colormap,
                event_mask=
                    xproto.EventMask.Exposure |
                    xproto.EventMask.StructureNotify |
                    # Child.StructureNotify and Parent.SubstructureNotify
                    # seem to block each other. That's not what we want.
                    # I commented this out, and it seems to work.
#                    xproto.EventMask.SubstructureNotify |
                    xproto.EventMask.ButtonPress,
                )
        client.window.reparent(client.actor, 0, config['cairodeco.height'])

        data = ClientData(self, screen, client)
        self.attach_data_to(client, data)
        client.actor.map()
        log.debug('created client actor client=%s actor=%s data=%s', client, client.actor, data)

    def emit_action(self, client, evt):
        stroke = (evt.state, evt.detail)
        if stroke in self.bindings:
            info = ActionInfo(screen = self.app.get_screen_by_root(evt.root),
                    x=evt.event_x,
                    y=evt.event_y,
                    client=client) # TODO: no additional info? :/
            # ... call the action
            self.app.plugins['actions'].emit(self.bindings[stroke], info)

