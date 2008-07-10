import pyglet
from pyglet.window.xlib import xlib 
from samuraix.rect import Rect
import samuraix

from samuraix.xconstants import BUTTONMASK

class Screen(pyglet.event.EventDispatcher):
    def __init__(self, num, buttons=None):
        self.num = num
        self.geom = Rect(0, 0, 
                    xlib.XDisplayWidth(samuraix.display, num),
                    xlib.XDisplayHeight(samuraix.display, num))

        self.buttons = () if buttons is None else buttons

    def __str__(self):
        return "<Screen num=%s>" % self.num

    def on_button_press(self, ev):
        for button, modifiers, func in self.buttons:
            if ev.button == button and  ev.state == modifiers:
                func()

    def _get_root_window(self):
        return xlib.XRootWindow(samuraix.display, self.num)
    root_window = property(_get_root_window)

    def grab_buttons(self):
        print "grabbing buttons for", self
        root = self.root_window
        for button, mod, cb in self.buttons:
            xlib.XGrabButton(samuraix.display, button, 0, 
                root, False, BUTTONMASK,
                xlib.GrabModeAsync, xlib.GrabModeSync, xlib.None_, xlib.None_)
            xlib.XGrabButton(samuraix.display, button, mod | xlib.LockMask, 
                root, False, BUTTONMASK,
                xlib.GrabModeAsync, xlib.GrabModeSync, xlib.None_, xlib.None_)
            xlib.XGrabButton(samuraix.display, button, mod | xlib.NumLockMask, 
                root, False, BUTTONMASK,
                xlib.GrabModeAsync, xlib.GrabModeSync, xlib.None_, xlib.None_)
            xlib.XGrabButton(samuraix.display, button, mod | xlib.NumLockMask | xlib.LockMask, 
                root, False, BUTTONMASK,
                xlib.GrabModeAsync, xlib.GrabModeSync, xlib.None_, xlib.None_)

    def ungrab_buttons(self):
        print "ungrab_buttons", self
        xlib.XUngrabButton(samuraix.display, xlib.AnyButton, xlib.AnyModifier, 
            self.root_window)


Screen.register_event_type('on_button_press')


