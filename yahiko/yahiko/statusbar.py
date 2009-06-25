from __future__ import with_statement

import copy

import ooxcb
from ooxcb.protocol import xproto
from ooxcb.contrib import cairo

from yahiko import ui


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

        self.status_bar.screen.root.push_handlers(on_client_message=self.on_client_message)
        
    def on_client_message(self, event):
        print event 
        


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
        self.status_bar.add_slot(HelloWorldSlot(self.status_bar, "hello"))
        self.status_bar.add_slot(HelloWorldSlot(self.status_bar, "to"))
        self.status_bar.add_slot(HelloWorldSlot(self.status_bar, "you"))
        self.status_bar.add_slot(ActiveClientSlot(self.status_bar))
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            self.conn.wait_for_event().dispatch()


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


