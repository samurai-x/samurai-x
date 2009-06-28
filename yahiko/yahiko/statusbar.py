from __future__ import with_statement

import copy
import socket
import SocketServer

import ooxcb
from ooxcb.protocol import xproto
from ooxcb.contrib import cairo

from yahiko import ui

import ooxcb.contrib.ewmh
ooxcb.contrib.ewmh.mixin()

import gobject

import dbus
import dbus.service
import dbus.mainloop.glib


DEFAULT_BUS_NAME = 'org.yahiko.statusbar'



class DBusObject(dbus.service.Object):
    def __init__(self, app, conn=None, object_path=None, bus_name=None):
        self.app = app 

        dbus.service.Object.__init__(self, 
                conn=conn, 
                object_path=object_path, 
                bus_name=bus_name,
        )
        
    @sxmethod("DBusInterface", in_signature='s', out_signature='s')
    def hello(self, name):   
        return "hello %s" % name

class Slot(object):
    def __init__(self, status_bar):
        self.status_bar = status_bar
        self.window = None

    def get_window(self):
        return self.window


class HelloWorldSlot(Slot):
    def __init__(self, status_bar, text="hello"):
        Slot.__init__(self, status_bar)
        self.window = ui.Label(
                text=text,
                style={
                    'text.color': (1.0, 1.0, 1.0),
                },
        )


class ActiveClientSlot(Slot):
    def __init__(self, status_bar):
        Slot.__init__(self, status_bar)
        self.window = ui.Label(
                text="",
                style={
                    'text.color': (1.0, 1.0, 1.0),
                },
        )

        self.status_bar.screen.root.change_attributes(
            event_mask=
                xproto.EventMask.PropertyChange,
        )
        self.status_bar.screen.root.push_handlers(on_property_notify=self.on_property_notify)
        
    def on_property_notify(self, event):
        if event.atom == self.status_bar.conn.atoms['_NET_ACTIVE_WINDOW']:
            win = self.status_bar.screen.root.get_property('_NET_ACTIVE_WINDOW', 'WINDOW').reply().value.to_windows()[0]
            self.window.text = win.ewmh_get_window_name()           
            self.window.dirty()


def sbmethod(interface, **kwargs):
    """ 
        decorator like dbus.service.method() but automatically adds in the sx bus name
    """
    return dbus.service.method('%s.%s' % (DEFAULT_BUS_NAME, interface), **kwargs)

def sbsignal(interface, **kwargs):
    """ 
        decorator like dbus.service.signal() but automatically adds in the sx bus name
    """
    return dbus.service.signal('%s.%s' % (DEFAULT_BUS_NAME, interface), **kwargs)


class DBusObject(dbus.service.Object):
    def __init__(self, status_bar, conn=None, object_path=None, bus_name=None):
        self.status_bar = status_bar
        dbus.service.Object.__init__(self, 
                conn=conn,
                object_path=object_path, 
                bus_name=bus_name,
        )

    @sbmethod("DBusInterface", in_signature="s,s", out_signature="")
    def update(self, name


class StatusBar(object):
    def __init__(self, app, screen):
        self.app = app
        self.conn = app.conn
        self.screen = screen

        visualtype = screen.get_root_visual_type()
        width = 300
        height = 25
        self.win = xproto.Window.create_toplevel_on_screen(self.conn, screen,
                width=width, height=height,
                back_pixel=screen.white_pixel,
                event_mask=(0
                    | xproto.EventMask.Exposure
                    | xproto.EventMask.ButtonPress
                    | xproto.EventMask.PointerMotion
                    | xproto.EventMask.KeyPress
                    | xproto.EventMask.PropertyChange
                    | xproto.EventMask.StructureNotify
                )
        )
        self.win.map()

        @self.win.event
        def on_key_press(event):
            if event.detail == 9:
                self.app.stop()
        
        self.ui = ui.TopLevelContainer(
                self.win,
                visualtype,
                style={
                    'background.style': 'fill',
                    'background.color': (0.2, 0.2, 0.2),
                    'border.color': (255, 255, 255),
                    'border.width': 1.0,
                    'layout.padding': 5,
                },
                layouter=ui.HorizontalLayouter,
        )

        self.slots = []

    def add_slot(self, item):
        self.slots.append(item)
        self.ui.add_child(item.get_window())
        self.ui.layout()
        self.ui.dirty()


class StatusBarHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print "%s wrote:" % self.client_address[0]
        print self.data
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data.upper())


class App(object):
    def __init__(self, conn, screen):
        self.conn = conn
        self.status_bar = StatusBar(self, screen)
        self.status_bar.add_slot(HelloWorldSlot(self.status_bar, "hello"))
        self.status_bar.add_slot(HelloWorldSlot(self.status_bar, "to"))
        self.status_bar.add_slot(HelloWorldSlot(self.status_bar, "you"))
        self.status_bar.add_slot(ActiveClientSlot(self.status_bar))
        self.running = True

        HOST=""
        PORT=9000
        self.server = SocketServer.TCPServer((HOST, PORT), StatusBarHandler)
        self.server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def stop(self):
        self.running = False

    def run(self):
        mainloop = self.mainloop = gobject.MainLoop()
        fd = self.conn.get_file_descriptor()
        gobject.io_add_watch(fd, gobject.IO_IN, self.do_xcb_events)
        gobject.io_add_watch(self.server.socket.fileno(), gobject.IO_IN, self.server.handle_request)
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        self.session_bus = dbus.SessionBus()
        self.name = dbus.service.BusName(DEFAULT_BUS_NAME, self.session_bus)

        mainloop.run()

    def do_xcb_events(self, source, condition):
        # might as well process all events in the queue...
        while True:
            try:
                ev = self.conn.poll_for_event()
            except Exception, e:
                log.exception(e)
            else:
                if ev is None:
                    break
                try:
                    #log.debug('Dispatching %s to %s.' %
                    #        (ev.event_name, ev.event_target))
                    ev.dispatch()
                except Exception, e:
                    log.exception(e)
        return True


def run():
    conn = ooxcb.connect()
    try:
        screen = conn.setup.roots[conn.pref_screen]
        app = App(conn, screen)
        app.run()
    finally:
        conn.disconnect()

if __name__ == '__main__':
    run()


