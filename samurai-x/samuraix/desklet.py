import sys
sys.path.append('.')

import os
import time
import functools
import string

import samuraix
from samuraix import xhelpers
from samuraix.rect import Rect
from samuraix.simple_window import SimpleWindow
from samuraix.sxctypes import *
from samuraix.drawcontext import DrawContext
from samuraix.screen import SimpleScreen
from samuraix import keysymdef

from pyglet.window.xlib import xlib

import logging
log = logging.getLogger(__name__)


class SimpleXApp(object):

    def __init__(self, screen, geom, border_width=None):
        self.screen = screen
        self.window = SimpleWindow(screen, geom, border_width)

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

        xlib.XMapRaised(samuraix.display, self.window.window)

    def run(self):
        self.running = True

        e = xlib.XEvent()

        then = time.time()

        self.draw()

        while self.running:
            #if xlib.XCheckWindowEvent(samuraix.display, self.window.window, 
            xlib.XNextEvent(samuraix.display, byref(e))
            self.handle_event(e)

    def stop(self, *args):
        self.running = False

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
        raise NotImplemented()

    def on_button_press(self, e):
        print "button press"
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


class TimedXApp(SimpleXApp):

    sleep_time = 1.0

    def run(self):
        self.running = True

        e = xlib.XEvent()

        then = time.time()

        while self.running:
            self.draw()

            while xlib.XPending(samuraix.display):
                xlib.XNextEvent(samuraix.display, byref(e))
                self.handle_event(e)

            now = time.time()
            d = self.sleep_time - (now-then)
            if d > 0:
                time.sleep(d)

            then = now


class ClockApp(TimedXApp):

    def __init__(self, screen, geom, border_width=None):
        TimedXApp.__init__(self, screen, geom, border_width=border_width)
        self._text = ''

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


class RunnerApp(SimpleXApp):

    def __init__(self, screen, geom, border_width=None):
        self.text = ''

        SimpleXApp.__init__(self, screen, geom, border_width=border_width)       

        self.grab_keyboard()

    def grab_keyboard(self):
        for x in range(1000):
            if (xlib.XGrabKeyboard(samuraix.display, self.screen.root_window, True, 
                    xlib.GrabModeAsync, xlib.GrabModeAsync, xlib.CurrentTime) == xlib.GrabSuccess):
                return
            time.sleep(0.001)
        raise "cant grab keyboard!"

    def on_key_press(self, e):
        ev = e.xkey
        keysym = xlib.KeySym()
        buf = c_buffer(32)
        num = xlib.XLookupString(ev, buf, 32, byref(keysym), None)

        keysym = keysym.value
        
        if keysym == keysymdef.XK_Escape:
            self.stop()
        elif keysym == keysymdef.XK_Return:
            self.execute()
        elif keysym == keysymdef.XK_BackSpace:
            self.text = self.text[:-1]
            self.draw()
        elif buf[0] in string.printable:
            self.text += buf[0]
            self.draw()

    def draw(self):
        w = self.window.geom.width
        h = self.window.geom.height
        self.context.fillrect(0, 0, w, h, (0.7, 0.5, 0.3))
        self.context.text(10, 10, self.text)
        self.window.refresh_drawable()
        
    def execute(self):
        shell = "/bin/sh"
        os.execl(shell, shell, "-c", self.text)


def run(app_func, nice_inc=15, name=None):
    from samuraix.main import set_process_name

    xhelpers.open_display()
    xhelpers.setup_xerror()

    xhelpers.get_numlock_mask()

    os.nice(nice_inc)
        
    simpleapp = app_func() #ClockApp(SimpleScreen(0), Rect(0, 0, 200, 15))

    if name is None:
        name = 'sx.%s' % simpleapp.__class__.__name__
    set_process_name(name)

    try:
        simpleapp.run()   
    finally:
        xhelpers.close_display()


if __name__ == '__main__':
    run(functools.partial(RunnerApp, SimpleScreen(0), Rect(0, 0, 200, 15)))

