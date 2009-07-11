import os
import sys
import pty
import threading
import select

import fcntl
import termios
import struct
import tty

import string

from ctypes import byref

from samuraix.baseapp import BaseApp
from samuraix import main as sxmain 
from samuraix.util import DictProxy

from yahiko import ui

import TermEmulator

from ooxcb.protocol import xproto
from ooxcb.contrib import cairo

import ooxcb.contrib.ewmh
ooxcb.contrib.ewmh.mixin()


class TermWindow(ui.Label):
    def __init__(self, app, **kwargs):
        self.app = app
        ui.Label.__init__(self, **kwargs)


class Term(object):
    def __init__(self, app, screen):
        self.app = app
        self.screen = screen
        self.conn = app.conn

        self.config = {
            'width': 640,
            'height': 480,
        }

        visualtype = screen.get_root_visual_type()
        self.win = xproto.Window.create_toplevel_on_screen(self.conn, screen,
                y=self.config['height'],
                width=self.config['width'], height=self.config['height'],
                back_pixel=screen.white_pixel,
                event_mask=(0
                    | xproto.EventMask.Exposure
                    | xproto.EventMask.KeyPress
                )
        )

        self.win.ewmh_set_window_name('yahiko-term')
        self.win.map()

        self.win.push_handlers(on_key_press=self.on_key_press)

        
        self.ui = ui.TopLevelContainer(
                self.win,
                visualtype,
                style={
                    'background.style': 'fill',
                    'background.color': (0.2, 0.2, 0.2),
                    'border.style': 'fill',
                    'border.color': (0.5, 0.0, 0.0),
                    'border.width': 1.0,
                    'layout.padding': 1,
                },
                layouter=ui.HorizontalLayouter,
        )

        self.output = TermWindow(
            self,
            style={
                'text.color': (1.0, 1.0, 1.0),
                'text.size': 10,
                'text.align': 'left',
                'text.family': 'monospace',
                'text.vertical-align': 'top', 
            },
        )
        self.ui.add_child(self.output)

        self.ui.recreate_surface()
        self.ui.layout()
        self.ui.dirty()

        text = DictProxy(self.output.style, 'text.')
        family = text.get('family', 'sans-serif')
        weight = getattr(
                cairo, 
                'CAIRO_FONT_WEIGHT_' + text.get('weight', 'normal').upper(), 
                cairo.CAIRO_FONT_WEIGHT_NORMAL,
        )
        slant = getattr(
                cairo,
                'CAIRO_FONT_SLANT_' + text.get('slant', 'normal').upper(),
                cairo.CAIRO_FONT_SLANT_NORMAL,
        )
        cr = self.ui.cr
        cairo.cairo_select_font_face(cr, family, weight, slant)
        extents = cairo.cairo_font_extents_t()
        cairo.cairo_font_extents(cr, byref(extents))
        self.char_height = extents.height
        self.char_width = extents.max_x_advance

        self.chars_width = int(self.output.rwidth / self.char_width)
        self.chars_height = int(self.output.rheight / self.char_height)

        self.term = TermEmulator.V102Terminal(self.chars_height, self.chars_width)
        self.term.SetCallback(
                self.term.CALLBACK_UPDATE_LINES,
                self.term_on_update_lines,
        )
        
        processPid, processIO = pty.fork()
        if processPid == 0: # child process
            os.system('/bin/bash')
        
        print "Child process pid", processPid
        
        # Sets raw mode
        #tty.setraw(processIO)
        
        # Sets the terminal window size
        #fcntl.ioctl(processIO, termios.TIOCSWINSZ,
        #            struct.pack("hhhh", self.chars_height, self.chars_width, 0, 0))
        
        tcattrib = termios.tcgetattr(processIO)
        tcattrib[3] = tcattrib[3] & ~termios.ICANON
        termios.tcsetattr(processIO, termios.TCSAFLUSH, tcattrib)
                    
        self.processPid = processPid
        self.processIO = processIO

        self.app.add_fd_handler('read', processIO, self.process_io_read)
        self.app.add_fd_handler('error', processIO, self.process_io_error)

    def on_key_press(self, event):
        if event.detail == 0:
            return 

        shift = int((event.state & xproto.ModMask.Shift) or (event.state & xproto.ModMask.Lock))
        k = (event.conn.keysyms.get_keysym(event.detail, shift)) & 255

        os.write(self.processIO, chr(k))
        
    def process_io_error(self):
        self.app.stop()

    def process_io_read(self):
        output = ""
        while True:
            try:
                data = os.read(self.processIO, 512)
            except OSError:
                self.app.stop()
                return 
            data_len = len(data)
            output += data

            if data_len < 512:
                break
        self.term.ProcessInput(output)

    def term_on_update_lines(self):
        screen = self.term.GetRawScreen()
        #rows = self.term.GetRows()
        #cols = self.term.GetCols()
        #dirty_lines = self.term.GetDirtyLines()
        #print "screen", screen
        #print "rows", rows
        #print "cols", cols
        #print "dirty", dirty_lines
        self.output.text = "\n".join(l.tostring() for l in screen)
        self.output.dirty()


class App(BaseApp):
    def init(self):
        BaseApp.init(self)

        screen = self.conn.setup.roots[self.conn.pref_screen]
        self.term = Term(self, screen)
    

def parse_options():
    """
        Parse the command line options and return them. The command-line
        arguments are ignored, since we aren't accepting any.
    """
    parser = sxmain.create_default_option_parser(
            config_path='~/.samuraix/apps/yahiko_term/',
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
            #config_path=options.configpath,
        )
    sxmain.run_app(create_app)


if __name__ == '__main__':
    run()
