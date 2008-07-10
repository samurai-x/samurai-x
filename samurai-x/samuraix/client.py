import pyglet
from pyglet.window.xlib import xlib 
from ctypes import *

from samuraix.rect import Rect
import samuraix

from samuraix.xconstants import BUTTONMASK, MOUSEMASK


class Client(pyglet.event.EventDispatcher):
    def __init__(self, screen, window, wa):
        self.screen = screen
        self.window = window
        self.geom = Rect(wa.x, wa.y, wa.width, wa.height)
        self.float_geom = self.geom.copy()       
        self.maxed_geom = self.geom.copy()
        self.old_border = wa.border_width

        self.configure_window()
        self.update_title()
        self.update_size_hints()

        xlib.XSelectInput(samuraix.display, window, 
                xlib.StructureNotifyMask | 
                xlib.PropertyChangeMask | 
                xlib.EnterWindowMask)

        print "new client with ", self.window, self.geom

        self.buttons = [
            (1, xlib.Mod4Mask, self.mousemove),
            (3, xlib.Mod4Mask, self.mouseresize),
        ]

    def __str__(self):
        return "<Client window=%s geom=%s>" % (self.window, self.geom)

    def configure_window(self):
        ce = xlib.XConfigureEvent()
        ce.type = xlib.ConfigureNotify
        ce.display = samuraix.display
        ce.event = self.window
        ce.window = self.window
        ce.x = self.geom.x
        ce.y = self.geom.y
        ce.width = self.geom.width
        ce.height = self.geom.height
        ce.border_width = 1
        ce.above = xlib.None_
        ce.override_redirect = False
        return xlib.XSendEvent(samuraix.display, self.window, False, 
                xlib.StructureNotifyMask, cast(byref(ce), POINTER(xlib.XEvent)))

    def update_title(self):
        print "TODO upadte_title"
    
    def update_size_hints(self):
        print "TODO update_size_hints"

    def resize(self, geometry, hints=False):
        if geometry.width <= 0 or geometry.height <= 0:
            print "too small!"
            return False

        if (geometry.x != self.geom.x or
            geometry.y != self.geom.y or
            geometry.width != self.geom.width or
            geometry.height != self.geom.height):
            print "doing resize"
            wc = xlib.XWindowChanges()
            self.geom.x = wc.x = geometry.x
            self.geom.y = wc.y = geometry.y
            self.geom.width = wc.width = geometry.width
            self.geom.height = wc.height = geometry.height
            wc.border_width = 1 #self.border_width

            xlib.XConfigureWindow(samuraix.display, self.window,
                xlib.CWX | xlib.CWY | xlib.CWWidth | xlib.CWHeight | xlib.CWBorderWidth,
                byref(wc))
            self.configure_window()

    def focus(self):
        pass

    def remove(self):
        samuraix.app.clients.remove(self)
        
        wc = xlib.XWindowChanges()

        wc.border_width = self.old_border
        
        xlib.XGrabServer(samuraix.display)
        xlib.XConfigureWindow(samuraix.display, self.window, xlib.CWBorderWidth, byref(wc))

        xlib.XUngrabButton(samuraix.display, xlib.AnyButton, xlib.AnyModifier, self.window)
        # TODO: window_setstate(c->win, WithdrawnState);
        xlib.XSync(samuraix.display, False)
        xlib.XUngrabServer(samuraix.display)
        
    def on_button_press(self, ev):
        print "client button_press", ev
        for button, modifiers, func in self.buttons:
            if ev.button == button and ev.state == modifiers:
                print "doing", func
                func()
                return
        print "no callback found"

    def grab_buttons(self):
        print "grab_buttons", self

        xlib.XGrabButton(samuraix.display, xlib.Button1, 
            xlib.NoSymbol,
            self.window, False, BUTTONMASK, xlib.GrabModeSync, xlib.GrabModeAsync, 
            xlib.None_, xlib.None_)
        xlib.XGrabButton(samuraix.display, xlib.Button1, 
            xlib.NoSymbol | xlib.LockMask,
            self.window, False, BUTTONMASK, xlib.GrabModeSync, xlib.GrabModeAsync, 
            xlib.None_, xlib.None_)
        xlib.XGrabButton(samuraix.display, xlib.Button1, 
            xlib.NoSymbol | xlib.NumLockMask,
            self.window, False, BUTTONMASK, xlib.GrabModeSync, xlib.GrabModeAsync, 
            xlib.None_, xlib.None_)
        xlib.XGrabButton(samuraix.display, xlib.Button1, 
            xlib.NoSymbol | xlib.NumLockMask | xlib.LockMask,
            self.window, False, BUTTONMASK, xlib.GrabModeSync, xlib.GrabModeAsync, 
            xlib.None_, xlib.None_)
        
        for button, modifiers, func in self.buttons:
            xlib.XGrabButton(samuraix.display, button, 
                modifiers, 
                self.window, False, BUTTONMASK, xlib.GrabModeAsync, xlib.GrabModeSync,
                xlib.None_, xlib.None_)
            xlib.XGrabButton(samuraix.display, button, 
                modifiers | xlib.LockMask, 
                self.window, False, BUTTONMASK, xlib.GrabModeAsync, xlib.GrabModeSync,
                xlib.None_, xlib.None_)
            xlib.XGrabButton(samuraix.display, button, 
                modifiers | xlib.NumLockMask, 
                self.window, False, BUTTONMASK, xlib.GrabModeAsync, xlib.GrabModeSync,
                xlib.None_, xlib.None_)
            xlib.XGrabButton(samuraix.display, button, 
                modifiers | xlib.NumLockMask | xlib.LockMask, 
                self.window, False, BUTTONMASK, xlib.GrabModeAsync, xlib.GrabModeSync,
                xlib.None_, xlib.None_)
                
        self.screen.ungrab_buttons()

    def mousemove(self):
        root = self.screen.root_window
        if (xlib.XGrabPointer(samuraix.display, 
                root, 
                False, MOUSEMASK, xlib.GrabModeAsync, xlib.GrabModeAsync,
                root,
                samuraix.cursors['move'], xlib.CurrentTime) != xlib.GrabSuccess):
            return 

        dummy = xlib.Window()
        x = c_int()
        y = c_int()
        di = c_int()
        dui = c_uint()

        xlib.XQueryPointer(samuraix.display, root, byref(dummy), byref(dummy),
            byref(x), byref(y), byref(di), byref(di), byref(dui))

        x = x.value
        y = y.value

        ev = xlib.XEvent()

        ox = self.geom.x
        oy = self.geom.y

        geom = self.geom.copy()

        while True:
            
            xlib.XMaskEvent(samuraix.display, 
                MOUSEMASK | 
                xlib.ExposureMask | 
                xlib.SubstructureRedirectMask, byref(ev))

            if ev.type == xlib.ButtonRelease:
                print "release"
                xlib.XUngrabPointer(samuraix.display, xlib.CurrentTime)
                return
            elif ev.type == xlib.MotionNotify:
                geom.x = ox + (ev.xmotion.x - x)
                geom.y = oy + (ev.xmotion.y - y)
                print "motion", geom
                self.resize(geom)
            else:
                samuraix.app.handle_event(ev)

            #elif ev.type == xlib.ConfigureRequest:
            #    print "configure"
            #    samuraix.app.handle_event(ev)
            #elif ev.type == xlib.Expose:
            #    print "expose"
            #    samuraix.app.handle_event(ev)

    def mouseresize(self):
        ocx = self.geom.x
        ocy = self.geom.y

        root = xlib.XRootWindow(samuraix.display, self.screen.num)

        if (xlib.XGrabPointer(samuraix.display, 
                root,
                False, MOUSEMASK, xlib.GrabModeAsync, xlib.GrabModeAsync,
                root,
                samuraix.cursors['resize'], xlib.CurrentTime) != xlib.GrabSuccess):
            return 

        xlib.XWarpPointer(samuraix.display, xlib.None_, self.window, 0, 0, 0, 0,
            self.geom.width + 1 - 1, self.geom.height + 1 - 1)   

        ev = xlib.XEvent()

        geom = self.geom.copy()

        while True:
            xlib.XMaskEvent(samuraix.display, 
                MOUSEMASK | xlib.ExposureMask | xlib.SubstructureRedirectMask,
                byref(ev))

            if ev.type == xlib.ButtonRelease:
                xlib.XUngrabPointer(samuraix.display, xlib.CurrentTime)
                return 
            elif ev.type == xlib.MotionNotify:
                geom.width = max(0, ev.xmotion.x - ocx - 2 * 1 + 1)
                geom.height = max(0, ev.xmotion.y - ocy - 2 * 1 + 1)
                self.resize(geom)
            else:
                samuraix.app.handle_event(ev)
                

    def on_enter(self):
        print "enter", self
        self.grab_buttons()
                

Client.register_event_type('on_button_press')
Client.register_event_type('on_enter')


