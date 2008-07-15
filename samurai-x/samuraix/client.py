import pyglet
from pyglet.window.xlib import xlib 

import weakref

from samuraix.sxctypes import *
from samuraix.rect import Rect
from samuraix import xhelpers
import samuraix

from samuraix.xconstants import BUTTONMASK, MOUSEMASK, CLEANMASK

import logging
log = logging.getLogger(__name__)

class Client(pyglet.event.EventDispatcher):

    class ClientFunc(object):
        def __init__(self, funcname, *args):
            self.funcname = funcname
            self.args = args

        def __call__(self, client):
            func = getattr(client, self.funcname)
            func(*self.args)

    all_clients = []
    window_2_client_map = weakref.WeakValueDictionary()

    default_config = {
        'buttons': {
            (1, xlib.Mod4Mask): ClientFunc('mousemove'),
            (3, xlib.Mod4Mask): ClientFunc('mouseresize'), 
        },
    }

    @classmethod 
    def get_by_window(cls, window):
        return cls.window_2_client_map.get(window)

    def __init__(self, screen, window, wa):
        self.screen = screen
        self.window = window
        self.geom = Rect(wa.x, wa.y, wa.width, wa.height)
        self.float_geom = self.geom.copy()       
        self.maxed_geom = self.geom.copy()
        self.old_border = wa.border_width
        self.desktop = None

        self.config = self.default_config.copy()
        
        self.configure_window()
        self.update_title()
        self.update_size_hints()
        self.update_wm_hints()
        self.check_ewmh()

        xlib.XSelectInput(samuraix.display, window, 
                xlib.StructureNotifyMask | 
                xlib.PropertyChangeMask | 
                xlib.EnterWindowMask)

        log.info("new client with %s %s" % (self.window, self.geom))

        self.all_clients.append(self)
        self.window_2_client_map[self.window] = self

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

    def check_ewmh(self):
        format = c_int()
        real = xlib.Atom()
        data = c_uchar_p()
        n = c_ulong()
        extra = c_ulong()

        #if (xlib.XGetWindowProperty(samuraix.display, self.window, samuraix.atoms['_NET_WM_STATE'],
        #    0, LONG_NAN, False, xatom.XA_ATOM, byref(real), byref(format), byref(n),
        #    byref(extra), byref(data)) == xlib.Success):
        #    state = cast(data, xlib.Atom_p)       

    def update_title(self):
        self.title = xhelpers.get_text_property(self.window, samuraix.atoms['_NET_WM_NAME'])
        if not self.title:
            self.title = xhelpers.get_text_property(self.window, samuraix.atoms['WM_NAME'])
        log.debug("title of %s is now %s" % (self, self.title))
    
    def update_size_hints(self):
        msize = c_long()
        size = xlib.XSizeHints()

        if not xlib.XGetWMNormalHints(samuraix.display, self.window, byref(size), byref(msize)):
            return 0

        if size.flags & xlib.PBaseSize:
            self.base_width = size.base_width
            self.base_height = size.base_height
        elif size.flags & xlib.PMinSize:
            self.base_width = size.min_width
            self.base_height = size.min_height
        else:
            self.base_width = 0 
            self.base_height = 0 

        if size.flags & xlib.PResizeInc:
            self.inc_width = size.width_inc
            self.inc_height = size.height_inc
        else:
            self.inc_width = 0
            self.inc_height = 0 

        if size.flags & xlib.PMaxSize:
            self.max_width = size.max_width
            self.max_height = size.max_height
        else:
            self.max_width = 0 
            self.max_height = 0

        if size.flags & xlib.PMinSize:
            self.min_width = size.min_width
            self.min_height = size.min_height
        elif size.flags & xlib.PBaseSize:
            self.min_width = size.base_width
            self.min_height = size.base_height
        else:
            self.min_width = 0 
            self.min_height = 0

        if size.flags & xlib.PAspect:
            self.min_aspect_x = size.min_aspect.x
            self.min_aspect_y = size.min_aspect.y
            self.max_aspect_x = size.max_aspect.x
            self.max_aspect_y = size.max_aspect.y
        else:
            self.min_aspect_x = 0
            self.min_aspect_y = 0
            self.max_aspect_x = 0
            self.max_aspect_y = 0

        return size.flags

    def update_wm_hints(self):
        wmhp = xlib.XGetWMHints(samuraix.display, self.window)
        wmh = wmhp[0]
        if wmh:
            self.urgent = wmh.flags & xlib.XUrgencyHint
            if self.urgent: # and its not the focused window...
                pass
                # meant to invalidate that cache and draw titlebar
            if wmh.flags & xlib.StateHint and wmh.initial_state == xlib.WithdrawnState:
                self.border_width = 0
                self.skip = True
            xlib.XFree(wmhp)
        
    def process_ewmh_state_atom(self, client, state, set):
        if state == samuraix.atoms['_NET_WM_STATE_STICKY']:
            pass

    def resize(self, geometry, hints=False):
        if geometry.width <= 0 or geometry.height <= 0:
            log.debug('not resizing - too small')
            return False

        if (geometry.x != self.geom.x or
            geometry.y != self.geom.y or
            geometry.width != self.geom.width or
            geometry.height != self.geom.height):

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
        log.debug('focusing %s' % self)
        xlib.XSetInputFocus(samuraix.display, self.window, xlib.RevertToPointerRoot, 
            xlib.CurrentTime)
        self.stack()
        self.grab_buttons()

    def stack(self):
        log.debug('stacking %s' % self)
        xlib.XRaiseWindow(samuraix.display, self.window)

    def remove(self):
        log.debug('removing %s' % self)
        wc = xlib.XWindowChanges()

        wc.border_width = self.old_border
        
        #xlib.XGrabServer(samuraix.display)
        #xlib.XConfigureWindow(samuraix.display, self.window, xlib.CWBorderWidth, byref(wc))

        #xlib.XUngrabButton(samuraix.display, xlib.AnyButton, xlib.AnyModifier, self.window)
        #xhelpers.set_window_state(self.window, xlib.WithdrawnState)
        #xlib.XSync(samuraix.display, False)
        #xlib.XUngrabServer(samuraix.display)

        try:
            self.all_clients.remove(self)
        except ValueError:
            log.warn('remove bug')
        
    def on_button_press(self, ev):
        modifiers = CLEANMASK(ev.state)
        log.debug("client %s button_press %s %s" % (self, ev.button, modifiers))
        try:
            func = self.config['buttons'][(ev.button, modifiers)]
        except KeyError:
            log.debug("no callback found for event")
        else:
            func(self)

    def grab_buttons(self):
        log.debug("grab_buttons %s %s" % (self, self.window))

        print samuraix.display, bool(samuraix.display), self.window, bool(self.window)
        xlib.XGrabButton(samuraix.display, xlib.Button1, 
            xlib.NoSymbol,
            self.window, False, BUTTONMASK, xlib.GrabModeSync, xlib.GrabModeAsync, 
            xlib.None_, xlib.None_)
        print 1
        xlib.XGrabButton(samuraix.display, xlib.Button1, 
            xlib.NoSymbol | xlib.LockMask,
            self.window, False, BUTTONMASK, xlib.GrabModeSync, xlib.GrabModeAsync, 
            xlib.None_, xlib.None_)
        print 1
        xlib.XGrabButton(samuraix.display, xlib.Button1, 
            xlib.NoSymbol | xlib.NumLockMask,
            self.window, False, BUTTONMASK, xlib.GrabModeSync, xlib.GrabModeAsync, 
            xlib.None_, xlib.None_)
        print 1
        xlib.XGrabButton(samuraix.display, xlib.Button1, 
            xlib.NoSymbol | xlib.NumLockMask | xlib.LockMask,
            self.window, False, BUTTONMASK, xlib.GrabModeSync, xlib.GrabModeAsync, 
            xlib.None_, xlib.None_)
        
        print 1
        for button, modifiers in self.config['buttons'].iterkeys():
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
                xlib.XUngrabPointer(samuraix.display, xlib.CurrentTime)
                return
            elif ev.type == xlib.MotionNotify:
                geom.x = ox + (ev.xmotion.x - x)
                geom.y = oy + (ev.xmotion.y - y)
                self.resize(geom)
            else:
                samuraix.app.handle_event(ev)

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
        log.debug("enter %s" % self)
        self.grab_buttons()

    def ban(self):
        log.debug('banning %s' % self)
        xlib.XUnmapWindow(samuraix.display, self.window)
        xhelpers.set_window_state(self.window, xlib.IconicState)
        # title bar unmap here

    def unban(self):
        log.debug('unbanning %s' % self)
        xlib.XMapWindow(samuraix.display, self.window)
        xhelpers.set_window_state(self.window, xlib.NormalState)
        # titlebar remap here
                
    def move_to_desktop(self, desktop):
        log.debug('move to desktop %s %s' % (self, desktop))
        self.desktop.remove_client(self)
        desktop.add_client(self)
        

Client.register_event_type('on_button_press')
Client.register_event_type('on_enter')


