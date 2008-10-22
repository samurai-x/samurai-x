import weakref

import samuraix.event
import samuraix.drawcontext
import samuraix.xcb, samuraix.xcb._xcb
from samuraix import cairo

from .rect import Rect

import logging
log = logging.getLogger(__name__)

class Client(samuraix.event.EventDispatcher):
    all_clients = []
    window_2_client_map = weakref.WeakValueDictionary()
    
    class ClientHandler(object):
        def __init__(self, client, x, y):
            self.client = client
            self.offset_x, self.offset_y = x, y

        def on_motion_notify(self, evt):
            pass

        def on_button_release(self, evt):
            pass

    class MoveHandler(ClientHandler):
        def __init__(self, client, x, y):
            super(Client.MoveHandler, self).__init__(client, x, y)
            self.gc = samuraix.xcb.graphics.GraphicsContext.create(self.client.screen.connection, self.client.screen.root,
                    attributes={'function':samuraix.xcb.graphics.GX_XOR, 'foreground':self.client.screen.white_pixel})
            client.screen.root.grab_pointer()
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
            super(Client.ResizeHandler, self).__init__(client, x, y)
            self.gc = samuraix.xcb.graphics.GraphicsContext.create(
                    self.client.screen.connection, 
                    self.client.screen.root,
                    attributes={
                        'function':samuraix.xcb.graphics.GX_XOR, 
                        'foreground':self.client.screen.white_pixel,
                    }
            )

            client.screen.root.grab_pointer()
            geom = self.client.frame_geom
            client.frame.warp_pointer(geom.width, geom.height)

            self._w = None
            self._h = None

        def on_motion_notify(self, evt):
            self.clear_preview()
            geom = self.client.frame_geom
            print self.client.frame_geom
            w = evt.root_x - geom.x + self.client.style['border'] * 2
            h = evt.root_y - geom.y + self.client.style['title_height']+(self.client.style['border']*2)
            self.gc.poly_rectangle(self.client.screen.root,
                                    [samuraix.xcb.graphics.Rectangle(geom.x, geom.y, w, h)],
                                    False)
            self._w = w
            self._h = h
            return True

        def on_button_release(self, evt):
            self.clear_preview()

            geom = self.client.frame_geom
            w, h = self._w, self._h
            if w:
                self.client.window.resize(geom.x, geom.y, w, h)

                self.client.frame.resize(
                        geom.x-self.client.style['border'],
                        geom.y-(self.client.style['title_height']+self.client.style['border']),
                        w+self.client.style['border']*2,
                        h+self.client.style['title_height']+(self.client.style['border']*2)
                )

                self.client.window.reparent(
                        self.client.frame, 
                        self.client.style['border'], 
                        self.client.style['border'] + self.client.style['title_height']
                )

            #configure(width=w, height=h)

            self.client.screen.root.remove_handlers(self)
            self.client.screen.root.ungrab_pointer()
            self.client.force_update_geom()
            self.client._recreate_context()
            self.client.frame_on_expose(None)
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
                'event_mask': (samuraix.xcb.event.StructureNotifyEvent,),
        }

        self.geom = Rect(
                geometry['x'], geometry['y'], 
                geometry['width'], geometry['height']
        )

        # display on all desktops?
        self.sticky = False 

        self.all_clients.append(self)
        self.window_2_client_map[self.window] = self

        self.create_frame()
        self.window.map()

        self.window.push_handlers(self)

        self._moving = False
        self._resizing = False

    def on_configure_notify(self, evt):
        print 'CFG', evt.x, evt.y, evt.width, evt.height
        self.force_update_geom() # TODO. ugly

    def on_destroy_notify(self, evt):
        # destroy me :-(
        self.remove()

    def remove(self):
        self.all_clients.remove(self)
        del self.window_2_client_map[self.window]
        self.frame.destroy()
        self.window.destroy()
        self.dispatch_event('on_removed')

    def create_frame(self):
        self.frame_geom = frame_geom = self.geom.copy()

        self.style = dict(
            title_height=20,
            border=3,
        )

        frame_geom.height += self.style['title_height'] + (self.style['border'] * 2)
        frame_geom.width += self.style['border'] * 2
        frame_geom.x -= self.style['border']
        frame_geom.y -= self.style['title_height'] + self.style['border']
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
                                         samuraix.xcb.event.ConfigureNotifyEvent,),
                           'override_redirect': True},
        )

        self.window.reparent(frame, 
                self.style['border'], 
                self.style['border'] + self.style['title_height']
        )

        frame.map()
        frame.set_handler('on_button_press', self.frame_on_button_press)
        frame.set_handler('on_configure_notify', self.on_configure_notify)
        frame.set_handler('on_expose', self.frame_on_expose)

        self.frame = frame

        self._recreate_context()

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
        print "%s geom %s" % (self, geometry)
        self.frame_on_expose(None)

    def frame_on_button_press(self, evt):
        self.focus()
        if evt.detail == 1:
            self._moving = True
            self.screen.root.push_handlers(
                    self.MoveHandler(self, evt.event_x, evt.event_y)
            )

        if evt.detail == 3:
            self._resizing = True
            self.screen.root.push_handlers(
                    self.ResizeHandler(self, evt.event_x, evt.event_y)
            )

    def force_update_geom(self):
        self.update_geom(self.frame.get_geometry())

    def _recreate_context(self):
        self.context = samuraix.drawcontext.DrawContext(
                self.screen, 
                self.frame_geom.width+1, self.frame_geom.height+1, 
                self.frame
        )

    def frame_on_expose(self, evt):
        context = self.context
        cr = context.cr
        
        if False:
            context.fill((255, 0, 255))
            context.text(0, 10, self.window.get_property('WM_NAME')[0], (255, 255, 255))
            # fred: why do I have to set y=10?
            # dunk: because its specifying the baseline of the text not the top 
        else:
            g = self.frame.get_geometry()
            if evt and not evt.x == 0: # TODO!!!11: too much flickering :-(
                log.warn('ignoring frame expose event %s' % evt)
                return
            cairo.cairo_set_antialias(cr, cairo.CAIRO_ANTIALIAS_NONE)
            cairo.cairo_set_line_width(cr, 1)
            cairo.cairo_set_source_rgb(cr, 0.8, 0.0, 0.0)
            cairo.cairo_rectangle(cr, 0, 0, g['width']-1, g['height']-1)
            cairo.cairo_fill_preserve(cr)
            cairo.cairo_set_source_rgb(cr, 1.0, 1.0, 1.0)
            cairo.cairo_stroke(cr)

            name = self.window.get_property('WM_NAME')
            if not name:
                name = 'untitled'
            else:
                name = name[0]

            log.debug('drawing window name "%s"', name)

            context.text(
                    self.style['border'] + 1, 
                    self.style['border'] + 1 + context.default_font_size, 
                    name,
                    (255, 255, 255)
            )

            # TODO should the client know its own connection?
            self.window.connection.flush()

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

    def focus(self):
        self.window.set_input_focus()
        self.screen.focused_client = self
        self.dispatch_event('on_focus')
        self.frame.configure(stack_mode=samuraix.xcb.window.STACK_MODE_ABOVE) # have to configure `frame` here!
        # TODO: grab buttons etc

Client.register_event_type('on_focus')
Client.register_event_type('on_removed')
