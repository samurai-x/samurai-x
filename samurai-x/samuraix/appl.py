import pyglet
from pyglet.window.xlib import xlib 

import signal
import functools

#import Pyro.core

import samuraix
from samuraix.xhelpers import get_window_state
from samuraix.screen import Screen
from samuraix.client import Client
from samuraix.sxctypes import *
from samuraix import xatom

from samuraix.testfunc import testfunc
from samuraix.xconstants import CLEANMASK

import logging
log = logging.getLogger(__name__)


#class PyroHandler(Pyro.core.ObjBase):
#    def __init__(self):
#        Pyro.core.ObjBase.__init__(self)
#    def app(self):
#        return samuraix.app
    

class App(pyglet.event.EventDispatcher):

    def __init__(self):
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

        self.pointer_x = 0
        self.pointer_y = 0

    def init(self):
        log.info('app %s initialising...' % self)

        log.info('registering signal handlers...')
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGHUP, self.stop)

        self.create_screens()

        self.scan()

        self.running = False

        #self.init_pyro()

    def init_pyro(self):
        Pyro.core.initServer()
        self.pyro_daemon = Pyro.core.Daemon()
        self.pyro_uri = self.pyro_daemon.connect(PyroHandler(), "samuraix")

        log.info("The daemon runs on port: %s", self.pyro_daemon.port)
        log.info("The object's uri is: %s", self.pyro_uri)

    def run(self):
        log.info('app %s now running...' % self)

        xlib.XSync(samuraix.display, False)
        self.running = True

        ev = xlib.XEvent()

        while self.running:
            # for non blocking use this ..
            #while xlib.XPending(samuraix.display):

            # pyro stuff...
            #def check():
            #    return not xlib.XPending(samuraix.display)

            #self.pyro_daemon.requestLoop(condition=check, timeout=0.1)

            xlib.XNextEvent(samuraix.display, byref(ev))
            self.handle_event(ev)
            xlib.XSync(samuraix.display, False)

            for screen in self.screens:
                for widget in screen.widgets:
                    if widget.dirty:
                        widget.draw()

        for screen in self.screens:
            screen.remove()

        for client in Client.all_clients:
            client.unban()

    def stop(self, *args, **kwargs):
        log.info(' app %s stop' % self)
        self.running = False

    def handle_event(self, ev):
        try:
            func = self.x_event_map[ev.type]
        except KeyError:
            log.debug('cant map event %s' % ev.type)
        else:
            func(ev)
        xlib.XSync(samuraix.display, False)

    def create_screens(self):
        log.info('creating screens...')
        num_screens = xlib.XScreenCount(samuraix.display)

        self.screens = []

        for i in range(num_screens):
            scr = Screen(i)
            self.screens.append(scr)
            self.dispatch_event('on_screen_add', scr)
            scr.push_handlers(
                on_client_add=functools.partial(self.dispatch_event, 'on_client_add', scr),
            )

    def on_client_add(self, screen, client):
        log.debug('app client add %s %s' % (screen, client))
        
    def scan(self):
        log.info('scanning screens for existing windows...')
        for screen in self.screens:
            screen.scan()

    def on_button_press(self, e):
        ev = e.xbutton

        wdummy = xlib.Window()
        udummy = c_uint()
        i = c_int()
        x = c_int()
        y = c_int()

        client = Client.get_by_window(ev.window)
        if client is not None:
            client.desktop.focus_client(client)
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

        client = Client.get_by_window(ev.window)
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
        log.debug('on_configure_notify %s' % ev)

    def on_destroy_notify(self, e):
        ev = e.xdestroywindow
        client = Client.get_by_window(ev.window)
        log.debug('on_destory_notify %s %s' % (ev.window, client))
        if client is not None:
            client.remove()

    def on_enter_notify(self, e):
        ev = e.xcrossing

        log.debug(str((ev.mode, ev.x_root, ev.y_root, self.pointer_x, self.pointer_y, ev.x, ev.y)))
        if (ev.mode != xlib.NotifyNormal or 
            (ev.x_root == self.pointer_x and ev.y_root == self.pointer_y)):
            log.debug('skipping on_enter_notify event')
            return

        client = Client.get_by_window(ev.window)
        log.debug('on_enter_notify %s %s' % (ev.window, client))
        if client:
            self.pointer_x = ev.x_root
            self.pointer_y = ev.y_root

            client.dispatch_event('on_enter')
        else:
            for screen in self.screens:
                if ev.window == screen.root_window:
                    screen.grab_buttons()
                    return 

    def on_expose(self, e):
        ev = e.xexpose
        log.debug('expose %s' % ev.window)
        if not ev.count:
            for screen in self.screens:
                for widget in screen.widgets:
                    if widget.test_window(ev.window):
                        widget.refresh()
                        return

    def on_key_press(self, e):
        x = c_int()
        y = c_int()
        d = c_int()
        dummy = xlib.Window()
        m = c_uint()

        for scr in self.screens:
            if (xlib.XQueryPointer(e.xany.display, scr.root_window, byref(dummy), byref(dummy),
                byref(x), byref(y), byref(d), byref(d), byref(m))):
                scr.dispatch_event('on_key_press', e.xkey)
                return 
        log.warn('got a key press for a screen we dont know!')

    def on_mapping_notify(self, e):
        ev = e.xmapping
        xlib.XRefreshKeyboardMapping(ev)
        if ev.request == xlib.MappingKeyboard:
            for screen in self.screens:
                screen.grab_keys()

    def on_map_request(self, e):
        ev = e.xmaprequest
        wa = xlib.XWindowAttributes()

        log.debug('on_map_request %s' % ev.window)

        if not xlib.XGetWindowAttributes(e.xany.display, ev.window, byref(wa)):
            log.debug('couldnt get XGetWindowAttributes')
            return 

        if wa.override_redirect:
            return 

        client = Client.get_by_window(ev.window)
        if client is None:
            for screen in self.screens:
                if (addressof(wa.screen.contents) == 
                        addressof(xlib.XScreenOfDisplay(e.xany.display, screen.num).contents)):
                    screen.manage(ev.window, wa)
                    return 
            assert screen is not None, "looking for screen %s(%s) failed" %(wa.screen, type(wa.screen))

    def on_property_notify(self, e):
        ev = e.xproperty
        log.debug('on_property_notify %s' % ev.atom)

        if ev.state == xlib.PropertyDelete:
            return
        client = Client.get_by_window(ev.window)
        if client:
            log.debug('prop change for client %s' % client)
            if ev.atom == xatom.XA_WM_TRANSIENT_FOR:
                trans = xlib.Window()
                xlib.XGetTransientForHint(e.xany.display, client.window, byref(trans))
                # needs rearrange
            elif ev.atom == xatom.XA_WM_NORMAL_HINTS:
                client.update_size_hints()
            elif ev.atom == xatom.XA_WM_HINTS:
                client.update_wm_hints()
            elif ev.atom == xatom.XA_WM_NAME or ev.atom == samuraix.atoms['_NET_WM_NAME']:
                client.update_title()

    def on_unmap_notify(self, e):
        ev = e.xunmap
        client = Client.get_by_window(ev.window)
        log.debug('on_unmap_notify %s %s' % (ev.window, client))
        if (client is not None and 
            ev.event == client.screen.root_window and 
            ev.send_event and 
            get_window_state(client.window) == xlib.NormalState):
            client.remove()

    def on_client_message(self, e):
        ev = e.xclient
        self.process_ewmh_message(ev)

    def process_ewmh_message(self, ev):
        log.debug('ewmh message %s' % ev.message_type)
        if ev.message_type == samuraix.atoms['_NET_CURRENT_DESKTOP']:
            log.debug('_NET_CURRENT_DESKTOP')
            pass
            # change the desktop
        elif ev.message_type == samuraix.atoms['_NET_CLOSE_WINDOW']:
            client = Client.get_by_window(ev.window)
            log.debug('_NET_CLOSE_WINDOW %s' % client)
            if client:
                client.kill()
        elif ev.message_type == samuraix.atoms['_NET_WM_STATE']:
            client = Client.get_by_window(ev.window)
            log.debug('_NET_WM_STATE %s' % client)
            if client:
                client.process_ewmh_state_atom(ev.data.l[1], ev.data.l[0])
                if ev.data.l[2]:
                    client.process_ewmh_state_atom(ev.data.l[2], ev.data.l[0])
                    

App.register_event_type('on_screen_add')
App.register_event_type('on_client_add')
