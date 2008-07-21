import pyglet
from pyglet.window.xlib import xlib 

import weakref
import functools

import samuraix
from samuraix.rect import Rect
from samuraix.xconstants import BUTTONMASK, CLEANMASK
from samuraix.desktop import Desktop
from samuraix.sxctypes import *
from samuraix import xatom
from samuraix.xhelpers import get_window_state
from samuraix.client import Client
from samuraix.rules import Rules

from samuraix.userfuncs import *

import logging
log = logging.getLogger(__name__)


class SimpleScreen(object):
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return "<Screen num=%s>" % self.num

    def _get_root_window(self):
        return xlib.XRootWindow(samuraix.display, self.num)
    root_window = property(_get_root_window)

    def get_geom(self):
        try:
            return self.geom
        except AttributeError:
            self.geom = Rect(0, 0, 
                            xlib.XDisplayWidth(samuraix.display, self.num),
                            xlib.XDisplayHeight(samuraix.display, self.num))
            return self.geom


class Screen(SimpleScreen, pyglet.event.EventDispatcher):

    client_class = Client
    desktop_class = Desktop

    def __init__(self, num):
        SimpleScreen.__init__(self, num)

        self.desktops = []
        self.active_desktop = None

        self.clients = []
        self.focused_client = None

        self.config = {}

        try:
        
            self.config.update(samuraix.config['screens']['default'])
        except KeyError:
            log.debug('cant find default screen config')

        try:
            self.config.update(samuraix.config['screens'][self.num])
        except KeyError:
            log.debug('cant find config for screen %s' % self.num)

        for conf_desktop in self.config['virtual_desktops']:
            desktop = self.desktop_class(self, conf_desktop['name'])
            self.desktops.append(desktop)
            self.dispatch_event('on_desktop_add', desktop)

        self.load_widgets()
        self.calculate_workspace()

        #if self.config['status_bar']['position'] is not None:
        #    self.widgets.append(Statusbar(self))

        self.set_active_desktop(self.desktops[0])

        wa = xlib.XSetWindowAttributes()
        wa.event_mask = ( xlib.SubstructureRedirectMask |      
                          xlib.SubstructureNotifyMask | 
                          xlib.EnterWindowMask | 
                          xlib.LeaveWindowMask | 
                          xlib.StructureNotifyMask )
        wa.cursor = samuraix.cursors['normal']

        root = self.root_window

        xlib.XChangeWindowAttributes(samuraix.display, 
            root, 
            xlib.CWEventMask | xlib.CWCursor,
            byref(wa))

        xlib.XSelectInput(samuraix.display,
            root, 
            wa.event_mask)

        self.set_supported_hints()

        self.rules = Rules(self)

        self.grab_buttons()
        self.grab_keys()

    def load_widgets(self):
        self.widgets = []
        for widget in self.config['widgets']:
            cls = widget.pop('class')
            name = widget.pop('name')
            self.widgets.append(cls(self, name, **widget))

    def calculate_workspace(self):
        g = self.workspace_geom = self.geom.copy()
        g.y = 15
        g.height -= 15

    def set_supported_hints(self):
        atoms = [
            samuraix.atoms['_NET_SUPPORTED'], 
            samuraix.atoms['_NET_CLIENT_LIST'], 
            samuraix.atoms['_NET_NUMBER_OF_DESKTOPS'], 
            samuraix.atoms['_NET_CURRENT_DESKTOP'], 
            samuraix.atoms['_NET_DESKTOP_NAMES'],
            samuraix.atoms['_NET_ACTIVE_WINDOW'],
            samuraix.atoms['_NET_CLOSE_WINDOW'],

            samuraix.atoms['_NET_WM_NAME'],
            samuraix.atoms['_NET_WM_ICON_NAME'],
            samuraix.atoms['_NET_WM_WINDOW_TYPE'],
            samuraix.atoms['_NET_WM_WINDOW_TYPE_NORMAL'],
            samuraix.atoms['_NET_WM_WINDOW_TYPE_DOCK'],
            samuraix.atoms['_NET_WM_WINDOW_TYPE_SPLASH'],
            samuraix.atoms['_NET_WM_WINDOW_TYPE_DIALOG'],
            samuraix.atoms['_NET_WM_STATE'],
            samuraix.atoms['_NET_WM_STATE_STICKY'],
            samuraix.atoms['_NET_WM_STATE_SKIP_TASKBAR'],
            samuraix.atoms['_NET_WM_STATE_FULLSCREEN'],

            samuraix.atoms['UTF8_STRING'],
        ]
        n = len(atoms)
        atoms_arr_type = xlib.Atom * n
        atoms_arr = atoms_arr_type(*atoms)

        xlib.XChangeProperty(samuraix.display, self.root_window,
            samuraix.atoms['_NET_SUPPORTED'], xatom.XA_ATOM, 32, 
            xlib.PropModeReplace, cast(atoms_arr, c_uchar_p), n)

    def scan(self):
        wa = xlib.XWindowAttributes()

        wins = xlib.Window_p()
        wins.contains = None
        d1 = xlib.Window()
        d2 = xlib.Window()
        num = c_uint()

        root = self.root_window
        log.debug('root is %s' % root)
        if xlib.XQueryTree(samuraix.display, root, byref(d1), byref(d2), byref(wins), byref(num)):
            log.debug('found %s windows' % num)
            for i in range(num.value):
                log.debug('found window %s' % wins[i])
                if (xlib.XGetWindowAttributes(samuraix.display, wins[i], byref(wa)) and 
                        not wa.override_redirect and 
                        (wa.map_state == xlib.IsViewable or 
                         get_window_state(wins[i]) == xlib.IconicState)):
                    self.manage(wins[i], wa)
                    
        if wins:
            xlib.XFree(wins)

    def remove(self):
        self.ungrab_buttons()
        self.ungrab_keys()

    def manage(self, window, wa):
        client = self.client_class(self, window, wa)
        log.info('screen %s managing %s' % (self, client))
        self.clients.append(weakref.ref(client))

        self.dispatch_event('on_client_add', client)
    
    def on_client_add(self, client):
        log.debug('on_client_add %s %s' % (self, client))
        if client.desktop is None:
            self.active_desktop.add_client(client)

    def set_active_desktop_by_index(self, index):
        try:
            desktop = self.desktops[index]
        except IndexError:
            log.debug('cant switch to desktop %s' % index)
            return 
        self.set_active_desktop(desktop)

    def set_active_desktop_by_name(self, name):
        log.debug('set_active_desktop_by_name %s %s' % (self, name))
        for desktop in self.desktops:
            if desktop.name == name:
                self.set_active_desktop(desktop)
                return
        raise ValueError(name)

    def next_desktop(self):
        log.debug('next_desktp %s' % self)
        idx = self.desktops.index(self.active_desktop) + 1
        if idx >= len(self.desktops):
            idx = 0 
        self.set_active_desktop(self.desktops[idx])

    def prev_desktop(self):
        log.debug('prev_desktop %s' % self)
        idx = self.desktops.index(self.active_desktop) - 1
        if idx < 0:
            idx = len(self.desktops) - 1
        self.set_active_desktop(self.desktops[idx])

    def set_active_desktop(self, desktop):
        assert desktop in self.desktops
        if desktop == self.active_desktop:
            return 

        if self.active_desktop is not None:
            log.debug('hiding desktop %s' % self.active_desktop)
            self.active_desktop.dispatch_event('on_hide')

        self.active_desktop = desktop
        log.debug('showing desktop %s' % desktop)
        desktop.dispatch_event('on_show')
        self.dispatch_event('on_desktop_change')

    def on_button_press(self, ev):
        modifiers = CLEANMASK(ev.state)
        log.debug('on_button_press %s %s %s' % (self, ev.button, modifiers))
        try:
            func = self.config['buttons'][(ev.button, modifiers)]
        except KeyError:
            log.debug('no button func found for %s %s' % (ev.button, modifiers))
        else:
            func(self)

    def on_key_press(self, ev):
        keysym = xlib.XKeycodeToKeysym(samuraix.display, ev.keycode, 0)
        modifiers = CLEANMASK(ev.state)
        log.debug('on_key_press %s %s %s' % (self, keysym, modifiers))
        try:
            func = self.config['keys'][(keysym, modifiers)]
        except KeyError:
            log.debug('no key func found for %s %s' % (keysym, modifiers))
        else:
            func(self)

    def grab_buttons(self):
        log.debug("grab_buttons %s" % self)
        root = self.root_window
        self.ungrab_buttons()
        for button, mod in self.config['buttons'].iterkeys():
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
        log.debug("grab_keys %s" % self)

        root = self.root_window

        self.ungrab_keys()
        for keysym, modifiers in self.config['keys'].iterkeys():
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

    def ungrab_keys(self):
        xlib.XUngrabKey(samuraix.display, xlib.AnyKey, xlib.AnyModifier, self.root_window) 


Screen.register_event_type('on_button_press')
Screen.register_event_type('on_key_press')
Screen.register_event_type('on_desktop_add')
Screen.register_event_type('on_desktop_change')
Screen.register_event_type('on_client_add')


