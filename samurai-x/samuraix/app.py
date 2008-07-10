import pyglet
import samuraix

from pyglet.window.xlib import xlib 
#from pyglet.window.xlib import cursorfont
from ctypes import *

import keydefs 

from samuraix.xhelpers import get_window_state
from samuraix.client import Client
from samuraix.screen import Screen

from samuraix.testfunc import testfunc
from samuraix.xconstants import CLEANMASK

class App(pyglet.event.EventDispatcher):

    x_event_map = {
        xlib.ButtonPress:       'on_button_press',
        xlib.ConfigureRequest:  'on_configure_request',
        xlib.ConfigureNotify:   'on_configure_notify',
        xlib.DestroyNotify:     'on_destroy_notify',
        xlib.EnterNotify:       'on_enter_notify', 
        xlib.Expose:            'on_expose',
        xlib.KeyPress:          'on_key_press',
        xlib.MappingNotify:     'on_mapping_notify',
        xlib.MapRequest:        'on_map_request',
        xlib.PropertyNotify:    'on_property_notify',
        xlib.UnmapNotify:       'on_unmap_notify',
        xlib.ClientMessage:     'on_client_message',
    }

    client_class = Client

    @classmethod
    def register_x_event_handlers(cls):
        for event in cls.x_event_map.itervalues():
            cls.register_event_type(event)

    def __init__(self):
        self.default_root_buttons = [
            (3, 0, testfunc),
            (1, 0, testfunc),
        ]

        self.create_screens()

        self.clients = []
        self.scan()

        self.running = False

    def run(self):
        xlib.XSync(samuraix.display, False)
        self.running = True

        try:
            self._run()
        finally:
            xlib.XSync(samuraix.display, False)
            xlib.XCloseDisplay(samuraix.display)

    def _run(self):
        ev = xlib.XEvent()

        while self.running:
            while xlib.XPending(samuraix.display):
                print "loop middle"
                while xlib.XPending(samuraix.display):
                    print "loop inner"
                    xlib.XNextEvent(samuraix.display, byref(ev))
                    self.handle_event(ev)
                xlib.XSync(samuraix.display, False)

    def handle_event(self, ev):
        try:
            evname = self.x_event_map[ev.type]
        except KeyError:
            print "not doing", ev.type
            return 
        self.dispatch_event(evname, ev)
        xlib.XSync(samuraix.display, False)

    def create_screens(self):
        num_screens = xlib.XScreenCount(samuraix.display)

        self.screens = []

        for i in range(num_screens):
            self.screens.append(Screen(i, buttons=self.default_root_buttons))
        
        wa = xlib.XSetWindowAttributes()
        wa.event_mask = ( xlib.SubstructureRedirectMask |      
                          xlib.SubstructureNotifyMask | 
                          xlib.EnterWindowMask | 
                          xlib.LeaveWindowMask | 
                          xlib.StructureNotifyMask )
        wa.cursor = samuraix.cursors['normal']

        #just do the following for real screens
        # ( whateva the fsck that means ... )
        for screen in self.screens:
            root = screen.root_window

            xlib.XChangeWindowAttributes(samuraix.display, 
                root, 
                xlib.CWEventMask | xlib.CWCursor,
                byref(wa))

            xlib.XSelectInput(samuraix.display,
                root, 
                wa.event_mask)

            screen.grab_buttons()

    def scan(self):
        wa = xlib.XWindowAttributes()

        wins = xlib.Window_p()
        wins.contains = None
        d1 = xlib.Window()
        d2 = xlib.Window()
        num = c_uint()

        for screen in self.screens:
            root = xlib.XRootWindow(samuraix.display, screen.num)
            print "root is", root
            if xlib.XQueryTree(samuraix.display, root, byref(d1), byref(d2), byref(wins), byref(num)):
                print "wins contents", wins.contents
                print "found %s windows" % num
                for i in range(num.value):
                    print "found win", wins[i]
                    if wins[i] == root:
                        print "we found root!"
                    if (xlib.XGetWindowAttributes(samuraix.display, wins[i], byref(wa)) and 
                            not wa.override_redirect and 
                            (wa.map_state == xlib.IsViewable or 
                             get_window_state(wins[i]) == xlib.IconicState)):
                        self.manage(wins[i], wa, screen)
            if wins:
                xlib.XFree(wins)


    def manage(self, window, wa, screen):
        print "managing", window, wa, screen
        client = self.client_class(screen, window, wa)
        self.clients.append(client)

    def get_client_by_window(self, win):
        for client in self.clients:
            print client.window, win, type(client.window), type(win)
            if client.window == win:
                return client
        return None

    def on_button_press(self, e):
        ev = e.xbutton

        wdummy = xlib.Window()
        udummy = c_uint()
        i = c_int()
        x = c_int()
        y = c_int()

        print "press", ev.window, type(ev.window), e.xany.window, type(e.xany.window)
        client = self.get_client_by_window(ev.window)
        print "found client", client
        if client is not None:
            if CLEANMASK(ev.state) == xlib.NoSymbol and ev.button == xlib.Button1:
                xlib.XAllowEvents(samuraix.display, xlib.ReplayPointer, xlib.CurrentTime)
                client.grab_buttons()
            else:
                client.dispatch_event('on_button_press', ev)
        else:
            for screen in self.screens:
                if (screen.root_window == ev.window and
                        xlib.XQueryPointer(e.xany.display, ev.window, byref(wdummy),
                        byref(wdummy), byref(x), byref(y), byref(i), byref(i), byref(udummy))):
                    screen.dispatch_event('on_button_press', ev)

    def on_configure_request(self, e):
        ev = e.xconfigurerequest

        client = self.get_client_by_window(ev.window)
        if client is not None:
            geom = client.geom.copy()
            
            if ev.value_mask & xlib.CWX:
                geom.x = ev.x
            if ev.value_mask & xlib.CWY:
                geom.y = ev.y
            if ev.value_mask & xlib.CWWidth:
                geom.width = ev.width
            if ev.value_mask & xlib.CWHeight:
                geom.height = ev.height

            if (geom.x != client.geom.x or 
                geom.y != client.geom.y or
                geom.width != client.geom.width or
                geom.height != client.geom.height):
                client.resize(geom)
            else:
                client.configure_window()               
        else:
            wc = xlib.XWindowChanges()
            wc.x = ev.x
            wc.y = ev.y
            wc.width = ev.width
            wc.height = ev.height
            wc.border_width = ev.border_width
            wc.sibling = ev.above
            wc.stack_mode = ev.detail
            xlib.XConfigureWindow(e.xany.display, ev.window, ev.value_mask, byref(wc))

    def on_configure_notify(self, ev):
        pass

    def on_destroy_notify(self, e):
        ev = e.xdestroywindow
        client = self.get_client_by_window(ev.window)
        if client is not None:
            client.remove()

    def on_enter_notify(self, e):
        ev = e.xcrossing
        client = self.get_client_by_window(ev.window)
        if client:
            client.dispatch_event('on_enter')
        else:
            for screen in self.screens:
                if ev.window == screen.root_window:
                    screen.grab_buttons()
                    return 

    def on_expose(self, ev):
        pass

    def on_key_press(self, ev):
        pass

    def on_mapping_notify(self, ev):
        pass

    def on_map_request(self, e):
        ev = e.xmaprequest
        wa = xlib.XWindowAttributes()
        
        if not xlib.XGetWindowAttributes(e.xany.display, ev.window, byref(wa)):
            return 

        if wa.override_redirect:
            return 

        client = self.get_client_by_window(ev.window)
        if client is None:
            screen = self.screens[0]
            for s in self.screens:
                if wa.screen == s.num:
                    screen = s
                    break
            
            self.manage(ev.window, wa, screens)

    def on_property_notify(self, ev):
        pass

    def on_unmap_notify(self, e):
        ev = e.xunmap
        client = self.get_client_by_window(ev.window)
        if (client is not None and 
            ev.event == xlib.XRootWindow(e.xany.display, client.screen.num) and 
            ev.send_event and 
            window_getstate(client.window) == xlib.NormalState):
            client.remove()

    def on_client_message(self, ev):
        pass



