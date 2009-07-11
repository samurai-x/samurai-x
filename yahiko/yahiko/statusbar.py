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
from samuraix.baseapp import BaseApp

import logging
log = logging.getLogger(__name__)


DEFAULT_LOGFILE = os.path.join(gettempdir(), 'yahiko-statusbar.lastrun.log')


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

    def __init__(self, status_bar, name, **kwargs):
        Slot.__init__(self, status_bar, name)
        self.window = ui.Label(
                style={
                    'text.color': (1.0, 1.0, 1.0),
                    'text.align': 'centre',
                    #'border.style': 'fill',
                    #'border.width': 1,
                    #'border.color': (0.5, 0.5, 0.5),
                },
                **kwargs
        )

    def _get_text(self):
        return self.window.text
    def _set_text(self, text):
        self.window.text = text
        self.window.dirty()
    text = property(_get_text, _set_text)


class ActiveClientSlot(LabelSlot):
    def __init__(self, status_bar, name, **kwargs):
        LabelSlot.__init__(self, status_bar, name)

        self.status_bar.screen.root.change_attributes(
            event_mask=
                xproto.EventMask.PropertyChange,
        )
        self.status_bar.screen.root.push_handlers(
                on_property_notify=self.on_property_notify,
        )

        self.update_active_window()
        
    def on_property_notify(self, event):
        if event.atom == self.status_bar.conn.atoms['_NET_ACTIVE_WINDOW']:
            self.update_active_window()

    def update_active_window(self):
        win = self.status_bar.screen.root.get_property('_NET_ACTIVE_WINDOW', 'WINDOW').reply().value.to_windows()[0]
        self.text = win.ewmh_get_window_name()           


class ActiveDesktopSlot(LabelSlot):
    def __init__(self, status_bar, name, **kwargs):
        LabelSlot.__init__(self, status_bar, name)

        self.status_bar.screen.root.change_attributes(
            event_mask=
                xproto.EventMask.PropertyChange,
        )

        self.desktop_names = self.status_bar.screen.root.get_property('_NET_DESKTOP_NAMES', 'UTF8_STRING').reply().value.to_utf8().split('\0')

        self.status_bar.screen.root.push_handlers(
                on_property_notify=self.on_property_notify,
        )

        self.update_active_desktop()
        
    def on_property_notify(self, event):
        if event.atom == self.status_bar.conn.atoms['_NET_CURRENT_DESKTOP']:
            self.update_active_desktop()

    def update_active_desktop(self):
        desktop_idx = self.status_bar.screen.root.get_property('_NET_CURRENT_DESKTOP', 'CARDINAL').reply().value[0]
        self.text = self.desktop_names[desktop_idx]


class ClockSlot(LabelSlot):
    def __init__(self, status_bar, name, **kwargs):
        LabelSlot.__init__(self, status_bar, name, **kwargs)

        self.status_bar.app.add_timer(60, self.update_clock)

        self.update_clock()

    def update_clock(self):
        self.text = datetime.now().strftime('%H:%M')


class StatusBar(object):

    default_config = {
        'x': "50%",
        'width': "90%",
        'height': 15,
        'slots': [
            {
                'class': ActiveClientSlot,
                'name': 'active_client',
            },
            {
                'class': ActiveDesktopSlot, 
                'name': 'active_desktop',
                'kwargs': {'width': 50},
            },
            {
                'class': ClockSlot, 
                'name': 'clock',
                'kwargs': {'width': 50},
            },
        ],
        'style': {
            'background.style': 'fill',
            'background.color': (0.2, 0.2, 0.2),
            'border.style': 'fill',
            'border.color': (0.5, 0.0, 0.0),
            'border.width': 1.0,
            'layout.padding': 1,
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
            slot_cls = slot['class']
            slot_name = slot['name']
            slot_args = slot.get('args', ())
            slot_kwargs = slot.get('kwargs', {})
            style = slot.get('style')
            s = slot_cls(self, slot_name, *slot_args, **slot_kwargs)
            if style:
                s.get_window().style.update(style)
            self.add_slot(s)

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


class App(BaseApp):
    def __init__(self, config_path=None, **kwargs):
        BaseApp.__init__(self, **kwargs)
        if config_path:
            self.user_config = sxmain.load_user_config(config_path)
        else:
            self.user_config = None

    def init(self):
        BaseApp.init(self)

        self.bus = SessionBus()
        self.add_fd_handler('read', self.bus, self.process_dbus)
        self.bus.request_name('org.yahiko.status_bar')
        screen = self.conn.setup.roots[self.conn.pref_screen]
        self.status_bar = StatusBar(self, screen, self.user_config)

    def run(self):
        self.status_bar.ui.recreate_surface()
        self.status_bar.ui.layout()
        self.status_bar.ui.dirty()
    
        BaseApp.run(self)

    def process_dbus(self):
        self.bus.receive_one()

        BaseApp.run(self)


def parse_options():
    """
        Parse the command line options and return them. The command-line
        arguments are ignored, since we aren't accepting any.
    """
    parser = sxmain.create_default_option_parser(
            config_path='~/.samuraix/apps/yahiko_statusbar/',
    )

    parser.add_option('', '--default-config', dest='print_default_config',
            help='print the default configuration to stdout',
            action='store_true',
            default=False,
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

    def create_app():
        return App( 
            synchronous_check=options.synchronous_check,
            config_path=options.configpath,
        )
    sxmain.run_app(create_app)

if __name__ == '__main__':
    run()


