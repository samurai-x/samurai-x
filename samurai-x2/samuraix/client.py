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

import samuraix.event
import samuraix.drawcontext
import samuraix.xcb
from samuraix.xcb import _xcb
from samuraix import cairo, config

from .rect import Rect
from .utils import hex2cairocolor

import logging
log = logging.getLogger(__name__)


# TODO something like this ...
#class Frame(object):
#    def __init__(self, client):
#        self.client = client 
#        self.window = samuraix.xcb.Window.create(...)
#
#    def on_expose(self, evt):
#        ...
#    def on_configure_notify(self, evt):
#        ...
#    def on_button_press(self, evt):
#        ...


class Client(samuraix.event.EventDispatcher):
    all_clients = []
    window_2_client_map = weakref.WeakValueDictionary()
    
    class ClientHandler(object):
        def __init__(self, client, x, y, cursor=None):
            self.client = client
            self.offset_x, self.offset_y = x, y

            self.gc = samuraix.xcb.graphics.GraphicsContext.create(
                    self.client.screen.connection, 
                    self.client.screen.root,
                    attributes={
                            'function': samuraix.xcb.graphics.GX_XOR, 
                            'foreground': self.client.screen.white_pixel,
                            'subwindow_mode': _xcb.XCB_SUBWINDOW_MODE_INCLUDE_INFERIORS,
                    },
            )

            client.screen.root.grab_pointer(cursor)


        def on_motion_notify(self, evt):
            pass

        def on_button_release(self, evt):
            pass

    class MoveHandler(ClientHandler):
        def __init__(self, client, x, y):
            super(Client.MoveHandler, self).__init__(client, x, y, client.screen.connection.cursors['Move'])
            self._x = None
            self._y = None

        def on_motion_notify(self, evt):
            self.clear_preview()
            x, y = evt.root_x - self.offset_x, evt.root_y - self.offset_y
            self.gc.poly_rectangle(self.client.screen.root,
                                    [samuraix.xcb.graphics.Rectangle(x, y, self.client.frame_geom.width, self.client.frame_geom.height)],
                                    False)
            self._x = evt.root_x
            self._y = evt.root_y
            return True

        def on_button_release(self, evt):
            self.client.screen.root.remove_handlers(self)
            self.client.screen.root.ungrab_pointer()
            self.clear_preview()
            if self._x is not None:
                self.client.frame.configure(x=self._x - self.offset_x, y=self._y - self.offset_y)
                self.client.force_update_geom()
            return True

        def clear_preview(self):
            """ clear old preview if necessary """
            if self._x is not None:
                x, y = self._x - self.offset_x, self._y - self.offset_y
                self.gc.poly_rectangle(self.client.screen.root,
                                        [samuraix.xcb.graphics.Rectangle(x, y, self.client.frame_geom.width, self.client.frame_geom.height)],
                                        False)

    class ResizeHandler(ClientHandler):
        def __init__(self, client, x, y):
            super(Client.ResizeHandler, self).__init__(client, x, y, client.screen.connection.cursors['Resize'])

            geom = self.client.frame_geom
            client.frame.warp_pointer(geom.width, geom.height)

            self._w = None
            self._h = None

        def on_motion_notify(self, evt):
            self.clear_preview()
            geom = self.client.frame_geom
            w = evt.root_x - geom.x
            h = evt.root_y - geom.y
            self.gc.poly_rectangle(self.client.screen.root,
                                    [samuraix.xcb.graphics.Rectangle(geom.x, geom.y, w, h)],
                                    False)
            self._w = w
            self._h = h
            return True

        def on_button_release(self, evt):
            self.clear_preview()

            geom = self.client.frame_geom.copy()
            geom.width, geom.height = self._w, self._h
            if geom.width:
                self.client.resize(geom)
            #configure(width=w, height=h)

            self.client.screen.root.remove_handlers(self)
            self.client.screen.root.ungrab_pointer()
            # put the mouse back where it was 
            self.client.frame.warp_pointer(self.offset_x, self.offset_y)

            return True

        def clear_preview(self):
            """ clear old preview if necessary """
            if self._w:
                self.gc.poly_rectangle(
                        self.client.screen.root,
                        [samuraix.xcb.graphics.Rectangle(
                            self.client.frame_geom.x, self.client.frame_geom.y, 
                            self._w, self._h
                        )],
                        False
                )

    @classmethod
    def get_by_window(cls, window):
        return cls.window_2_client_map.get(window)

    def __init__(self, screen, window, wa, geometry):
        super(Client, self).__init__()

        self.screen = screen
        self.window = window
        
        self.window.attributes = {
                'event_mask': (
                    samuraix.xcb.event.StructureNotifyEvent,
                    samuraix.xcb.event.ConfigureNotifyEvent,
                    samuraix.xcb.event.PropertyChangeEvent,
                    # commented out because there would be strange
                    # errors with frames if the following is commented
                    # in. But WHY?
#                    samuraix.xcb.event.ButtonPressEvent,
#                    samuraix.xcb.event.MotionNotifyEvent,
#                    samuraix.xcb.event.ButtonReleaseEventp,
                    samuraix.xcb.event.SubstructureRedirectEvent,
                    samuraix.xcb.event.SubstructureNotifyEvent,
                    samuraix.xcb.event.UnmapNotifyEvent,
               ),
        }
        self.connection = window.connection

        self.geom = Rect(
                geometry['x'], geometry['y'], 
                geometry['width'], geometry['height']
        )

        # display on all desktops?
        self.sticky = False 
        # full screened?
        self.maximized = False
        # geom backup for unmaximizing
        self.backup_geom = None

        self.all_clients.append(self)
        self.window_2_client_map[self.window] = self

        self.create_frame()
        self.window.map()
        self.grab_buttons()
        self.grab_focus_button()

        self.window.push_handlers(self)

        self.apply_normal_hints()

        self._moving = False
        self._resizing = False

    def on_configure_request(self, evt):
        log.debug('Client received configure request: Window=%s' % evt.window)
        cnf = {}
        mask = evt.value_mask
        # ... copied from screen.py
        # TODO: get rid of that boilerplate code
        if mask & _xcb.XCB_CONFIG_WINDOW_X:
            cnf['x'] = evt.x
        if mask & _xcb.XCB_CONFIG_WINDOW_Y:
            cnf['y'] = evt.y
        if mask & _xcb.XCB_CONFIG_WINDOW_WIDTH:
            cnf['width'] = evt.width
        if mask & _xcb.XCB_CONFIG_WINDOW_HEIGHT:
            cnf['height'] = evt.height
        if mask & _xcb.XCB_CONFIG_WINDOW_BORDER_WIDTH:
            cnf['border_width'] = evt.border_width
        if mask & _xcb.XCB_CONFIG_WINDOW_SIBLING:
            cnf['sibling'] = evt.sibling # does that work?
        if mask & _xcb.XCB_CONFIG_WINDOW_STACK_MODE:
            cnf['stack_mode'] = evt.stack_mode

        if cnf:
            evt.window.configure(**cnf)
        else:
            log.warning('Strange configure request: No attributes set')

    def grab_focus_button(self):
        """ 
            grab the 'focus button'.
            If you click inside a window, 
            it will be focused.

            However, it is necessary to ungrab
            the buttons after focusing; otherwise
            the window won't get any button events :(
        """
        self.window.grab_button(1, 0)

    def ungrab_focus_button(self):
        self.window.ungrab_button(1, 0)

    def grab_buttons(self):
        for (mod, button) in self.screen.buttons.iterkeys():
            self.window.grab_button(button, mod)

    def ungrab_buttons(self):
        for (mod, button) in self.screen.buttons.iterkeys():
            self.window.ungrab_button(button, mod)

    def apply_normal_hints(self, hints=None, geom=None):
        """
            apply the WM_NORMAL_HINTS (TODO: complete)

            :param hints: A `SizeHints` object or None (fetch it)
            :param geom: received geom - will not be modified; if None,
                use a copy of `self.geom`
        """
        apply_style = True
        if hints is None:
            hints = self.window.get_property('WM_NORMAL_HINTS')
        if geom is None:
            geom = self.geom
        geom = geom.copy()
        
        hints.compute(geom)
        self.apply_style(geom)
        
        self.resize(geom)
        self.force_frame_expose(geom.width, geom.height)

    def apply_style(self, geom):
        """
            apply `self.style` on `geom`.

            `geom` will be modified in-place.
        """
        if geom.x == 0:
            geom.x = self.style['border']
        if geom.y == 0:
            geom.y = self.style['title_height'] + self.style['border']

        geom.height += self.style['title_height'] + (self.style['border'] * 2)
        geom.width += self.style['border'] * 2
        geom.x -= self.style['border']
        geom.y -= self.style['title_height'] + self.style['border']

    def resize(self, geom):
        log.warn('resize %s', geom)
        self.frame.resize(
                geom.x,
                geom.y,
                geom.width,
                geom.height
        )

        self.window.resize(
                self.style['border'],
                self.style['title_height']+self.style['border'], 
                geom.width - (2 * self.style['border']), 
                geom.height - self.style['title_height'] - (2 * self.style['border'])
        )

        self.force_update_geom()
        self._recreate_context()

        self.connection.flush()

    def on_button_press(self, evt):
        log.debug('got button press event: button #%d modifiers=%d' % (evt.button, evt.state))
        # first: is it the focus button? (no modifiers, button #1)
        if evt.button == 1 and evt.state == 0:
            self.focus()
            self.connection.allow_events(2)
            self.connection.flush()
        else:
            # no, it is probably a button binding.
            try:
                func = self.screen.buttons[(evt.state, evt.button)]
            except KeyError:
                log.warn('cant find button')
            else:
                func(self.screen, (self, evt.event_x, evt.event_y))

    def on_unmap_notify(self, evt):
        log.debug('Got unmap notify for window %s, i am %s' % (evt.window, self.window))
        if evt.window is self.window:
            # if i am focused, unfocus me 
            if self.screen.focused_client is self:
                self.screen.focused_client = None
            self.frame.unmap()

    def on_configure_notify(self, evt):
        # we need to fit the frame around the window when this happens 
        # im not 100% sure when this happens, but it definatly happens when 
        # resizing some windows ( like gnome-terminal that fits itself to a 
        # whole col/rows )
        log.warn('win CFG %s', str((evt.x, evt.y, evt.width, evt.height)))
        width = evt.width + (2 * self.style['border'])
        height = evt.height + (2 * self.style['border']) + self.style['title_height']
        
        new_geom = self.frame_geom.copy()
        new_geom.width = width
        new_geom.height = height
        self.update_geom(new_geom)

        self.frame.resize(
                self.frame_geom.x,
                self.frame_geom.y,
                width,
                height
        )
        self.connection.flush()

        self._recreate_context()
        self.force_frame_expose(width, height)

    def frame_on_configure_notify(self, evt):
        log.warn('frame CFG %s', str((evt.x, evt.y, evt.width, evt.height)))
        self.force_update_geom() # TODO. ugly

    def on_destroy_notify(self, evt):
        # destroy me :-(
        log.warning('got a destroy notify self=%s event.event=%s event.window=%s' % (self.window, evt.event, evt.window))
        if evt.window is self.window: # only for the window, not for the frame
            self.remove(False)

    def remove(self, destroy=True):
        log.info('Removing me=%s! clients=%s' % (self, self.all_clients))
        try:
            self.all_clients.remove(self)
            del self.window_2_client_map[self.window]
        except (ValueError, KeyError), e:
            log.warning(e)
        if self.screen.focused_client is self:
            self.screen.focused_client = None

        self.connection.grab_server()
        #self.window.ungrab_button(0, 1 << 15) # urgh
        self.ungrab_buttons()
        self.ungrab_focus_button()
        self.connection.flush()

        self.frame.destroy()
        self.frame.delete()
        if destroy:
            self.window.destroy()
        self.connection.flush()
        self.connection.ungrab_server()
        self.dispatch_event('on_removed')

    def create_frame(self):
        self.frame_geom = frame_geom = self.geom.copy()

        self.style = dict(
            title_height=20,
            border=3,
            icon_size=(24, 24),
        )

        self.apply_style(frame_geom)

        frame = samuraix.xcb.window.Window.create(
                self.screen.connection,
                self.screen,
                frame_geom.x,
                frame_geom.y,
                frame_geom.width,
                frame_geom.height,
                1,
                attributes={'event_mask': (samuraix.xcb.event.ExposeEvent,
                                         samuraix.xcb.event.ButtonPressEvent,
                                         samuraix.xcb.event.ButtonReleaseEvent,
                                         samuraix.xcb.event.ConfigureNotifyEvent,

                                         ),
                           'override_redirect': True},
        )

        frame.background_color = hex2cairocolor(config.get('client.frame.background_color', '#cc0000'))
        frame.title_color = hex2cairocolor(config.get('client.frame.title_color', '#ffffff'))
        self.window.reparent(frame, 
                self.style['border'], 
                self.style['border'] + self.style['title_height']
        )

        frame.set_handler('on_button_press', self.frame_on_button_press)
        frame.set_handler('frame_on_configure_notify', self.on_configure_notify)
        frame.set_handler('on_expose', self.frame_on_expose)

        log.debug('frame w %s h %s', frame_geom.width, frame_geom.height)

        frame.gc = samuraix.xcb.graphics.GraphicsContext.create(self.connection, self.screen.root)
            
        self.frame = frame
        frame.map()

        self._recreate_context()
        self.force_frame_expose(frame_geom.width, frame_geom.height)
        self.connection.flush()

    def on_reparent_notify(self, evt):
        # remove. TODO: untested
        if evt.parent is not self.frame:
            self.remove()

    def update_geom(self, geometry):
        if isinstance(geometry, dict):
            geometry = Rect(geometry['x'], geometry['y'], geometry['width'], geometry['height'])
        #self.geom = geometry
        #self.frame_geom = frame_geom = self.geom.copy()
        self.geom = geom = self.geom.copy()
        self.frame_geom = geometry
        geom.height -= self.style['title_height'] + (self.style['border'] * 2)
        geom.width -= self.style['border'] * 2
        geom.x += self.style['border']
        geom.y += self.style['title_height'] + self.style['border']
        #log.warn("%s geom %s", self, geometry)
        #self.frame_on_expose(None)

    def force_frame_expose(self, width, height):
        ev = samuraix.xcb.event.ExposeEvent(self.connection, _dispatch_target=self.frame)
        ev.x = 0
        ev.y = 0
        ev.width = width
        ev.height = height
        self.frame_on_expose(ev)

    def frame_on_button_press(self, evt):
        if evt.detail == 1:
            self.user_move(evt.event_x, evt.event_y)
        if evt.detail == 3:
            self.user_resize(evt.event_x, evt.event_y)

    def user_move(self, x, y):
        self.focus()
        self._moving = True
        self.screen.root.push_handlers(
                self.MoveHandler(self, x, y)
        )


    def user_resize(self, x, y):
        self.focus()
        self._resizing = True
        self.screen.root.push_handlers(
                self.ResizeHandler(self, x, y)
        )

    def force_update_geom(self):
        self.update_geom(self.frame.get_geometry())

    def _recreate_context(self):
        self.frame.pixmap = samuraix.xcb.pixmap.Pixmap.create(self.connection, 
                self.screen.root,
                self.frame_geom.width, self.frame_geom.height,
                depth = self.screen.root_depth
        )
        self.context = samuraix.drawcontext.DrawContext(
                self.screen, 
                self.frame_geom.width+1, self.frame_geom.height+1, 
                self.frame.pixmap,
        )
        self.redraw()

    def redraw(self):
        context = self.context
        cr = context.cr
        
        g = self.frame.get_geometry()

        cairo.cairo_set_antialias(cr, cairo.CAIRO_ANTIALIAS_NONE)
        cairo.cairo_set_line_width(cr, 1)
        cairo.cairo_set_source_rgb(cr, *self.frame.background_color)
        cairo.cairo_rectangle(cr, 0, 0, g['width']-1, g['height']-1)
        cairo.cairo_fill_preserve(cr)
        cairo.cairo_set_source_rgb(cr, 1.0, 1.0, 1.0)
        cairo.cairo_stroke(cr)

        name = self.window.get_property('WM_NAME')
        if not name:
            name = 'untitled'
        else:
            name = name[0]

        context.text(
                self.style['border'] + self.style['icon_size'][0] + 1, 
                self.style['border'] + 1 + context.default_font_size, 
                name,
                self.frame.title_color,
        )
        
        pixels = self.window.get_property('_NET_WM_ICON')
        if pixels:
            try:
                context.netwm_icon(pixels, resize_to=self.style['icon_size'])
            except Exception, e:
                log.exception(e)

    def frame_on_expose(self, evt):
        _xcb.xcb_copy_area(self.connection._connection, 
                self.frame.pixmap._xid, 
                self.frame._xid, 
                self.frame.gc._xid, 
                evt.x, evt.y,
                evt.x, evt.y,
                evt.width, evt.height,
        )

        self.connection.flush()

    def ban(self):
        if self.sticky:
            return # TODO?
        log.debug('banning %s' % self)
        #self.window.unmap()
        # TODO: multiple decoration
        self.frame.unmap()
        # TODO: set window state

    def unban(self):
        if self.sticky:
            return # TODO?
        log.debug('unbanning %s' % self)
        #self.window.map()
        # TODO: multiple decoration
        self.frame.map()
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
        self.ungrab_focus_button()
        self.window.set_input_focus()

        if self.screen.focused_client is not None:
            self.screen.focused_client.blur()

        self.screen.focused_client = self
        self.dispatch_event('on_focus')
        # have to configure `frame` here!
        self.frame.configure(stack_mode=samuraix.xcb.window.STACK_MODE_ABOVE) 
        # TODO: grab buttons etc

    def blur(self):
        """
            Oh no! I am no longer focused!

            Grab the focus button and dispatch 'on_blur'.
        """
        self.grab_focus_button()
        self.dispatch_event('on_blur')

Client.register_event_type('on_focus')
Client.register_event_type('on_blur')
Client.register_event_type('on_removed')
