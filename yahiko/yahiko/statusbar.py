from __future__ import with_statement

import copy
import socket
import SocketServer
from select import select
from datetime import datetime
import time

import ooxcb
from ooxcb.protocol import xproto
from ooxcb.contrib import cairo

from yahiko import ui

import ooxcb.contrib.ewmh
ooxcb.contrib.ewmh.mixin()

from yaydbus.bus import SessionBus
from yaydbus import service

import logging
log = logging.getLogger(__name__)


class SlotInterface(service.Object):
    def __init__(self, slot, path):
        self.slot = slot 
        service.Object.__init__(self, slot.status_bar.app.bus, path)


class Slot(object):
    dbus_class = SlotInterface

    def __init__(self, status_bar, name):
        self.status_bar = status_bar
        self.window = None
        self.name = name

        self.dbus = self.dbus_class(self, '/org/yahiko/status_bar/%s' % name)
        self.status_bar.app.bus.add_object(self.dbus)

    def get_window(self):
        return self.window


class LabelSlotInterface(SlotInterface):
    @service.method('org.yahiko.status_bar.LabelSlotInterface', in_signature='s')
    def set_text(self, text):
        self.slot.text = text

    @service.method('org.yahiko.status_bar.LabelSlotInterface', out_signature='s')
    def get_text(self):
        return self.slot.text
    

class LabelSlot(Slot):
    dbus_class = LabelSlotInterface

    def __init__(self, status_bar, name, text="hello"):
        Slot.__init__(self, status_bar, name)
        self.window = ui.Label(
                text=text,
                style={
                    'text.color': (1.0, 1.0, 1.0),
                },
        )

    def _get_text(self):
        return self.window.text
    def _set_text(self, text):
        self.window.text = text
        self.window.dirty()
    text = property(_get_text, _set_text)


class ActiveClientSlot(LabelSlot):
    def __init__(self, status_bar, name):
        LabelSlot.__init__(self, status_bar, name)

        self.status_bar.screen.root.change_attributes(
            event_mask=
                xproto.EventMask.PropertyChange,
        )
        self.status_bar.screen.root.push_handlers(on_property_notify=self.on_property_notify)
        
    def on_property_notify(self, event):
        if event.atom == self.status_bar.conn.atoms['_NET_ACTIVE_WINDOW']:
            win = self.status_bar.screen.root.get_property('_NET_ACTIVE_WINDOW', 'WINDOW').reply().value.to_windows()[0]
            self.text = win.ewmh_get_window_name()           


class ClockSlot(LabelSlot):
    def __init__(self, status_bar, name):
        LabelSlot.__init__(self, status_bar, name)

        self.status_bar.app.add_timer(1, self.update_label)

    def update_label(self):
        self.text = datetime.now().strftime('%H:%I:%S')


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



class App(object):
    def __init__(self, conn, screen):
        self.conn = conn
        self.status_bar = StatusBar(self, screen)
        self.running = True

        # filehandles used when select'ing 
        self.fds = {'read': {}, 'write': {}, 'error': {}}
        # timeout used when select'ing
        self.select_timeout = 1.0
        self.timers = {}

        fd = self.conn.get_file_descriptor()
        self.add_fd_handler('read', fd, self.do_xcb_events) 
        
        self.bus = SessionBus()
        self.add_fd_handler('read', self.bus, self.process_dbus)
        self.bus.request_name('org.yahiko.status_bar')

        self.status_bar.add_slot(LabelSlot(self.status_bar, 's1', "hello"))
        self.status_bar.add_slot(LabelSlot(self.status_bar, 's2', "to"))
        self.status_bar.add_slot(LabelSlot(self.status_bar, 's3', "you"))
        self.status_bar.add_slot(ActiveClientSlot(self.status_bar, 's4'))
        self.status_bar.add_slot(ClockSlot(self.status_bar, 's5'))

        #HOST=""
        #PORT=9000
        #self.server = SocketServer.TCPServer((HOST, PORT), StatusBarHandler)
        #self.server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def process_dbus(self):
        self.bus.receive_one()

    def add_fd_handler(self, which_list, fd, callback):
        """ 
            add a callback to be called when the main loop detects a
            read/write/error on the file descriptor fd
        """
        assert which_list in ('read', 'write', 'error')
        self.fds[which_list][fd] = callback

    def remove_fd_handler(self, which_list, fd):
        """
            remove a callback to be called when the main loop detects
            a read/write/error on the file descriptor fd
        """
        assert which_list in ('read', 'write', 'error')
        del self.fds[which_list][fd]

    def add_timer(self, seconds, func):
        self.timers[func] = (time.time() + seconds, seconds)   

    def stop(self):
        self.running = False

    def run(self):
        """
            Start the mainloop. It uses `select` to poll the file descriptor
            for events and dispatches them.
            All exceptions are caught and logged, so samurai-x won't crash.
            If `self.running` is False for some reason, samurai-x will
            disconnect and stop.
        """
        self.running = True

        # process any events that are waiting first
        while True:
            try:
                ev = self.conn.poll_for_event()
            except Exception, e:
                log.exception(e)
            else:
                if ev is None:
                    break
                try:
                    ev.dispatch()
                except Exception, e:
                    log.exception(e)

        while self.running:
            #log.debug('selecting...')
            try:
                rready, wready, xready = select(
                        self.fds['read'].keys(),
                        self.fds['write'].keys(),
                        self.fds['error'].keys(),
                        self.select_timeout
                )
            except Exception, e:
                # error 4 is when a signal has been caught
                if e.args[0] == 4:
                    pass
                else:
                    log.exception(str((e, type(e), dir(e), e.args)))
                    raise
            else:
                # should catch errors in these?
                for fd in rready:
                    self.fds['read'][fd]()
                for fd in wready:
                    self.fds['write'][fd]()
                for fd in xready:
                    self.fds['error'][fd]()

            now = time.time()
            for func, (timeout, secs) in self.timers.iteritems():
                if timeout < now:
                    func()
                    self.timers[func] = (now+secs, secs)

        self.conn.disconnect()


    def do_xcb_events(self):
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


