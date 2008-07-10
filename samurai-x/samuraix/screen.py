import pyglet
from pyglet.window.xlib import xlib 

import samuraix
from samuraix.rect import Rect
from samuraix.xconstants import BUTTONMASK, CLEANMASK
from samuraix.desktop import Desktop
from samuraix import keydefs
from samuraix.testfunc import testfunc

import logging
log = logging.getLogger(__name__)

class Screen(pyglet.event.EventDispatcher):
    _default_conf = {
        'virtual_desktops': [
            {'name':'one'},
        ],
    }

    def __init__(self, num, buttons=None):
        self.num = num
        self.geom = Rect(0, 0, 
                    xlib.XDisplayWidth(samuraix.display, num),
                    xlib.XDisplayHeight(samuraix.display, num))

        self.buttons = () if buttons is None else buttons
        self.keys = [
            (keydefs.XK_Return, xlib.Mod4Mask, testfunc),
        ]
        
        self.desktops = []

        try:
            conf = samuraix.config['screens'][self.num]
        except KeyError:
            conf = self._default_conf

        for conf_desktop in conf['virtual_desktops']:
            desktop = Desktop(self, conf_desktop['name'])
            self.desktops.append(desktop)

        self.active_desktop = self.desktops[0]

    def __str__(self):
        return "<Screen num=%s>" % self.num

    def _get_root_window(self):
        return xlib.XRootWindow(samuraix.display, self.num)
    root_window = property(_get_root_window)

    def set_active_desktop(self, name):
        for desktop in self.desktops:
            if desktop.name == name:
                self.active_desktop = self.desktops[name]
                return
        raise ValueError(name)

    def on_button_press(self, ev):
        for button, modifiers, func in self.buttons:
            if ev.button == button and  ev.state == modifiers:
                func()

    def on_key_press(self, ev):
        keysym = xlib.XKeycodeToKeysym(samuraix.display, ev.keycode, 0)
        for ks, modifiers, func in self.keys:
            if ks == keysym and CLEANMASK(modifiers) == CLEANMASK(ev.state):
                func()

    def grab_buttons(self):
        log.debug("grab_buttons %s" % self)
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
        log.debug("ungrab_buttons %s" % self)
        xlib.XUngrabButton(samuraix.display, xlib.AnyButton, xlib.AnyModifier, 
            self.root_window)

    def grab_keys(self):
        log.debug("gab_keys %s" % self)

        root = self.root_window

        xlib.XUngrabKey(samuraix.display, xlib.AnyKey, xlib.AnyModifier, root) 
        for keysym, modifiers, func in self.keys:
            kc = xlib.XKeysymToKeycode(samuraix.display, keysym)
            
            xlib.XGrabKey(samuraix.display, kc, 
                modifiers,
                root, True, xlib.GrabModeAsync, xlib.GrabModeAsync)
            xlib.XGrabKey(samuraix.display, kc, 
                modifiers | xlib.LockMask, 
                root, True, xlib.GrabModeAsync, xlib.GrabModeAsync)
            xlib.XGrabKey(samuraix.display, kc, 
                modifiers | xlib.NumLockMask, 
                root, True, xlib.GrabModeAsync, xlib.GrabModeAsync)
            xlib.XGrabKey(samuraix.display, kc, 
                modifiers | xlib.NumLockMask | xlib.LockMask, 
                root, True, xlib.GrabModeAsync, xlib.GrabModeAsync)


Screen.register_event_type('on_button_press')
Screen.register_event_type('on_key_press')


