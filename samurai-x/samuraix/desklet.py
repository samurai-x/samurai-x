import sys
sys.path.append('..')

import time

import samuraix
from samuraix import xhelpers
from samuraix.rect import Rect
from samuraix.simple_window import SimpleWindow
from samuraix.sxctypes import *
from samuraix.drawcontext import DrawContext

from pyglet.window.xlib import xlib

import logging
log = logging.getLogger(__name__)


class SimpleXApp(object):

    def __init__(self, screen, geom, border_width=1):
        self.window = SimpleWindow(screen, geom, border_width)
        xlib.XMapRaised(samuraix.display, self.window.window)

        self.mapped = False

        self.x_event_map = {
            xlib.ButtonPress:       self.on_button_press,
            xlib.ConfigureRequest:  self.on_configure_request,
            xlib.ConfigureNotify:   self.on_configure_notify,
            xlib.DestroyNotify:     self.on_destroy_notify,
            xlib.EnterNotify:       self.on_enter_notify, 
            xlib.Expose:            self.on_expose,
            xlib.KeyPress:          self.on_key_press,
            xlib.MappingNotify:     self.on_mapping_notify,
            xlib.MapRequest:        self.on_map_request,
            xlib.PropertyNotify:    self.on_property_notify,
            xlib.UnmapNotify:       self.on_unmap_notify,
            xlib.ClientMessage:     self.on_client_message,
        }

        self.context = DrawContext(screen,
                        geom.width, geom.height,
                        self.window.drawable)

        self._text = ''

    def run(self):
        self.running = True

        e = xlib.XEvent()

        then = time.time()

        while self.running:
            #if xlib.XCheckWindowEvent(samuraix.display, self.window.window, 
            self.draw()

            while xlib.XPending(samuraix.display):
                xlib.XNextEvent(samuraix.display, byref(e))
                self.handle_event(e)

            now = time.time()
            d = now-then 
            if d < 1.0:
                time.sleep(1.0 - d)

            then = now

    def handle_event(self, e):
        try:
            func = self.x_event_map[e.type]
        except KeyError:
            log.debug('cant map event %s' % e.type)
        else:
            func(e)
        xlib.XSync(samuraix.display, False)

    def on_expose(self, e):
        print "expose"
        self.window.refresh_drawable()

    def draw(self):
        text = time.strftime("%c")
        if text == self._text:
            return 

        self._text = text

        w = self.window.geom.width
        h = self.window.geom.height
        self.context.fillrect(0, 0, w, h, (0.7, 0.5, 0.3))
        self.context.text(10, 10, text)
        self.window.refresh_drawable()

    def on_button_press(self, e):
        self.running = False

    def on_configure_request(self, e):
        print "configure request"
    def on_configure_notify(self, e):
        print "configure_notifuy"
    def on_destroy_notify(self, e):
        print "destroy notify"
    def on_enter_notify(self, e):
        print "enter notify"
    def on_expose(self, e):
        print "expose"
    def on_key_press(self, e):
        print "key ress"
    def on_mapping_notify(self, e):
        print "mapping notify"
    def on_map_request(self, e):
        print "map request"
    def on_property_notify(self, e):
        print "property notfy"
    def on_unmap_notify(self, e):
        print "unmap notify"
    def on_client_message(self, e):
        print "client message"


def run():
    from samuraix.screen import SimpleScreen


    xhelpers.open_display()
    xhelpers.setup_xerror()

    xhelpers.get_numlock_mask()

    simpleapp = SimpleXApp(SimpleScreen(0), Rect(0, 0, 200, 15))
    try:
        simpleapp.run()   
    finally:
        xhelpers.close_display()


if __name__ == '__main__':
    run()

