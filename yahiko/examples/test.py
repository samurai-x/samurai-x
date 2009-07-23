from __future__ import with_statement

import copy

import sys
sys.path.append('../ooxcb')

import ooxcb
from ooxcb.protocol import xproto
from ooxcb.contrib import cairo

from yahiko import ui

import samuraix.main as sxmain
from samuraix.baseapp import BaseApp

class TestWindow(object):
    def __init__(self, app):
        self.app = app 
        self.conn = app.conn
        self.config = {'width':640, 'height': 480}

        screen = self.conn.setup.roots[self.conn.pref_screen]
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
        self.win.map()

        self.ui = ui.TopLevelContainer(
                self.win,
                visualtype,
                style={
                    'background.style': 'fill',
                    'background.color': (0.2, 0.2, 0.2),
                    'border.color': (0.5, 0.0, 0.0),
                    'border.width': 1.0,
                    'border.style': 'fill',
                    'layout.padding': 5,
                },
                layouter=ui.HorizontalLayouter,
        )

        label_style = {
            'border.color': (0.8, 0.8, 0.8),
            'border.width': 0.5, 
            'border.style': 'fill',
            'background.color': (0.7, 0.6, 0.6),
            'background.style': 'fill',
            'text.color': (0.6, 0, 0),
            'text.size': 12,
        }
        ls1 = label_style.copy()
        ls1['text.align'] = 'left'
        ls2 = label_style.copy()
        ls2['text.vertical-align'] = 'middle'
        ls3 = label_style.copy()
        ls3['text.vertical-align'] = 'bottom'
        ls3['text.align'] = 'right'

        def debug_func(msg):
            def f(*args):
                print args, msg
            return f

        self.ui.add_children([
            ui.Label(text="but 1", style=ls1, on_button_press=debug_func('but1')),
            ui.Label(text="but 2", style=ls2, on_button_press=debug_func('but2')),
            ui.Input(text="but 3", style=ls3, on_button_press=debug_func('but3')),
            ui.PangoLabel(text="but 1", style=ls1, on_button_press=debug_func('pbut1')),
            ui.PangoLabel(text="but 2", style=ls2, on_button_press=debug_func('pbut2')),
        ])


class App(BaseApp):
    def init(self):
        BaseApp.init(self)

        self.window = TestWindow(self)

    def run(self):
        self.window.ui.recreate_surface()
        self.window.ui.layout()
        self.window.ui.dirty()
        BaseApp.run(self)


"""
label_style = {
    'border': {
        'color': (0.8, 0.8, 0.8),
        'width': 0.5, 
    },
    'background': {
        'color': (0.7, 0.6, 0.6),
    },
    'text': {
        'color': (0.6, 0, 0),
        'size': 12,
    },
}

ls1 = copy.deepcopy(label_style)
ls2 = copy.deepcopy(label_style)
ls3 = copy.deepcopy(label_style)
ls1['text']['align'] = 'left'
ls1['layout'] = {'margin': 10}
ls2['text']['align'] = 'centre'
ls2['layout'] = {'margin': 20}
ls3['text']['align'] = 'right'
ls3['layout'] = {'margin': 30}

widget.add_children([
    ui.Label(text="but 1", style=ls1, on_button_press=debug_func('but1')),
    ui.Label(text="but 2", style=ls2, on_button_press=debug_func('but2')),
    ui.Input(text="but 3", style=ls3, on_button_press=debug_func('but3')),
])
widget.layout()
"""

def parse_options():
    """
        Parse the command line options and return them. The command-line
        arguments are ignored, since we aren't accepting any.
    """
    parser = sxmain.create_default_option_parser(
            #config_path='~/.samuraix/apps/yahiko_statusbar/',
    )

    options, args = parser.parse_args()
    return options

def run():
    options = parse_options()
    sxmain.configure_logging(options)

    def create_app():
        return App( 
            synchronous_check=options.synchronous_check,
        )
    sxmain.run_app(create_app)

if __name__ == '__main__':
    run()

