from __future__ import with_statement

import os
from optparse import OptionParser
import copy
import socket
import SocketServer
from select import select
from datetime import datetime
import time
from tempfile import gettempdir

import ooxcb
from ooxcb.protocol import xproto
from ooxcb.contrib import cairo
from ooxcb.list import List

from yahiko import ui

import ooxcb.contrib.ewmh
ooxcb.contrib.ewmh.mixin()

from yaydbus.bus import SessionBus
from yaydbus import service

import samuraix.main as sxmain

import logging
log = logging.getLogger(__name__)

DEFAULT_LOGFILE = os.path.join(gettempdir(), 'sx.lastrun.log')

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

    default_config = {
        'x': "50%",
        'width': "90%",
        'height': 15,
        'slots': [
            (ActiveClientSlot, 'active_client'),
            (ClockSlot, 'clock'),
        ],
        'style': {
            'background.style': 'fill',
            'background.color': (0.2, 0.2, 0.2),
            'border.color': (255, 255, 255),
            'border.width': 1.0,
            'layout.padding': 5,
        }
    }

    def __init__(self, app, screen, config):
        self.app = app
        self.conn = app.conn
        self.screen = screen
        self.config = self.default_config.copy()
        if config:
            self.config.update(config)

        self.massage_config()

        visualtype = screen.get_root_visual_type()
        self.win = xproto.Window.create_toplevel_on_screen(self.conn, screen,
                y=self.config['height'],
                width=self.config['width'], height=self.config['height'],
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

        self.win.ewmh_set_window_name('yahiko-statusbar')
        self.win.change_property('WM_CLASS', 'STRING', 8, List.from_string('yahiko-statusbar'))
        self.win.change_property('_NET_WM_DESKTOP', 'CARDINAL', 32, [0xffffffffL])

        self.win.change_property('_NET_WM_WINDOW_TYPE', 'ATOM', 32,
                List.from_atoms([
                    self.conn.atoms['_NET_WM_WINDOW_TYPE_DOCK'],
                ]),
        )
        self.win.change_property('_NET_WM_STATE', 'ATOM', 32,
                List.from_atoms([
                    self.conn.atoms['_NET_WM_STATE_SKIP_PAGER'],
                    self.conn.atoms['_NET_WM_STATE_SKIP_TASKBAR'],
                    self.conn.atoms['_NET_WM_STATE_STICKY'],
                ]),
        )
        self.win.change_property('_NET_WM_STRUT', 'CARDINAL', 32,
                [0, 0, 0, self.config['height']],
        )
        self.win.map()
        root_geom = self.screen.root.get_geometry().reply()
        self.win.configure(
                x=self.config['x']-(self.config['width']/2), 
                y=root_geom.height - self.config['height'],
        )

        @self.win.event
        def on_key_press(event):
            if event.detail == 9:
                self.app.stop()
        
        self.ui = ui.TopLevelContainer(
                self.win,
                visualtype,
                style=self.config['style'],
                layouter=ui.HorizontalLayouter,
        )

        self.slots = []

        for slot in self.config['slots']:
            slot_cls = slot[0]
            slot_name = slot[1]
            slot_args = slot[2:]
            self.add_slot(slot_cls(self, slot_name, *slot_args))

    def massage_config(self):
        root_geom = self.screen.root.get_geometry().reply()
        def parse_number(s, max):
            if type(s) is str:
                s = s.strip()
                if s.endswith('%'):
                    s = (max / 100) * float(s[:-1])
                elif not s.isdigit():
                    log.error('unknown format %s' % s)

            return int(s)

        self.config['width'] = parse_number(
                self.config['width'], root_geom.width)
        self.config['height'] = parse_number(
                self.config['height'], root_geom.height)
        self.config['x'] = parse_number(
                self.config['x'], root_geom.width)

    def add_slot(self, item):
        self.slots.append(item)
        self.ui.add_child(item.get_window())
        self.ui.layout()
        self.ui.dirty()


class App(object):
    def __init__(self, conn, screen, config_path=None):
        self.conn = conn

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

        if config_path:
            user_config = sxmain.load_user_config(config_path)
        else:
            user_config = None
        self.status_bar = StatusBar(self, screen, user_config)

        #self.status_bar.add_slot(LabelSlot(self.status_bar, 's1', "hello"))
        #self.status_bar.add_slot(LabelSlot(self.status_bar, 's2', "to"))
        #self.status_bar.add_slot(LabelSlot(self.status_bar, 's3', "you"))
        #self.status_bar.add_slot(ActiveClientSlot(self.status_bar, 's4'))
        #self.status_bar.add_slot(ClockSlot(self.status_bar, 's5'))

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

        self.status_bar.ui.recreate_surface()
        self.status_bar.ui.layout()
        self.status_bar.ui.dirty()

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

    def process_dbus(self):
        self.bus.receive_one()

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


def configure_logging(options, file_level=logging.DEBUG, console_level=logging.DEBUG):
    """
        Set up the logging for the client.

        :param file_level: level of logging for files
        :param console_level: level of logging for the console
    """
    console = logging.StreamHandler()
    console.setLevel(console_level)
    formatter = FDFormatter('[%(asctime)s %(levelname)s %(name)s] %(message)s')
    console.setFormatter(formatter)
    # reset the handlers incase its a restart
    logging.getLogger('').handlers = []
    logging.getLogger('').addHandler(console)
    logging.root.setLevel(logging.DEBUG)
    lastlog = logging.FileHandler(options.logfile, 'w')
    lastlog.setLevel(file_level)
    formatter = logging.Formatter(
            '[%(asctime)s %(levelname)s %(name)s %(lineno)d] %(message)s')
    lastlog.setFormatter(formatter)
    logging.getLogger('').addHandler(lastlog)

    # parse logging levels string, format is:
    #   <logger_name>:<level_name>[,<logger_name2>:<level_name2>[,...]]
    # where logger_name is the name of a logger eg samuraix.main
    # and level_name is a name as described in the logging module
    # such as DEBUG/INFO/ERROR
    for setting in getattr(options, 'logging_levels', '').split(','):
        setting = setting.strip()
        if not setting:
            continue
        name, level = setting.split(':')
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level))

    log.info('logging everything to %s' % options.logfile)


def parse_options():
    """
        Parse the command line options and return them. The command-line
        arguments are ignored, since we aren't accepting any.
    """
    parser = OptionParser()
    parser.add_option('-c', '--config', dest='configpath',
            help='use samurai-x2 configuration from PATH (default: %default)', metavar='FILE',
            default='~/.samuraix/apps/yahiko_statusbar/')

    parser.add_option('-f', '--logfile', dest='logfile',
            help='save the samurai-x2 log file to FILE', metavar='FILE',
            default=DEFAULT_LOGFILE)

    parser.add_option('', '--default-config', dest='print_default_config',
            help='print the default configuration to stdout',
            action='store_true',
            default=False)

    parser.add_option('-s', '--synchronous-check', dest='synchronous_check',
            help='turn on synchronous checks (useful for debugging)',
            action='store_true',
            default=False)

    parser.add_option('-l', '--logging', dest='logging_levels',
            help='set a logging handler to a specific debug level',
            default='',
    )

    options, args = parser.parse_args()
    return options


def run():
    options = parse_options()
    if options.print_default_config:
        from pprint import pprint
        pprint(StatusBar.default_config)
        return 
    sxmain.configure_logging(options)
    conn = ooxcb.connect()
    try:
        screen = conn.setup.roots[conn.pref_screen]
        app = App(conn, screen, config_path=options.configpath)
        app.run()
    finally:
        conn.disconnect()

if __name__ == '__main__':
    run()


