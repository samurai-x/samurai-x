import os
import sys
import pty
import time
import threading
import select
import copy

from array import array

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
from yahiko import cairo
from yahiko import pango

from ooxcb.protocol import xproto
from ooxcb.eventsys import EventDispatcher

import ooxcb.contrib.ewmh
ooxcb.contrib.ewmh.mixin()

import logging
log = logging.getLogger(__name__)

#sys.path.append('/usr/lib/python2.6/dist-packages')

try:
    import psyco
    psyco.full(1)
except ImportError:
    pass

ASCII_NUL = 0     # Null
ASCII_BK = 7     # Bell
ASCII_BS = 8      # Backspace
ASCII_HT = 9      # Horizontal Tab
ASCII_LF = 10     # Line Feed
ASCII_VT = 11     # Vertical Tab
ASCII_FF = 12     # Form Feed
ASCII_CR = 13     # Carriage Return
ASCII_XON = 17    # Resume Transmission
ASCII_XOFF = 19   # Stop Transmission or Ignore Characters
ASCII_ESC = 27    # Escape
ASCII_SPACE = 32  # Space
ASCII_CSI = 153   # Control Sequence Introducer


clamp = lambda x, xmin, xmax: min(xmax, max(xmin, x))

color_map = {
    0:  '#000',
    1:  '#700',
    2:  '#070',
    3:  '#770',
    4:  '#007',
    5:  '#707',
    6:  '#077',
    7:  '#777',
    8:  '#000',
    9:  '#F00',
    10:  '#0F0',
    11:  '#FF0',
    12:  '#00F',
    13:  '#F0F',
    14:  '#0FF',
    15:  '#FFF',
}


DEFAULT_RENDITION = 0x0f000000

class TermRow(object):
    __slots__ = ['chars', 'rendition', 'dirty', 'layout']

    def __init__(self, cols):
        self.chars = array('c', ' '*cols)
        self.rendition = array('L', [0]*cols)
        self.dirty = False
        self.layout = None


class TermScreen(list):
    def __init__(self, term):
        list.__init__(self)
        self.term = term
        self.cursor_row = 0 
        self.cursor_col = 0
        self.cursor_stack = []
        self.cursor_visible = True
        self.cols = 0
        self.rows = 0 
        self.scroll_top = 0
        self.scroll_bottom = 0
        self.visible_start = 0 
        self.rendition = DEFAULT_RENDITION

    def save_cursor(self):
        self.cursor_stack.append((self.cursor_row, self.cursor_col))

    def restore_cursor(self):
        self.cursor_row, self.cursor_col = self.cursor_stack.pop()

    def resize(self, rows, cols):
        if rows != self.rows or cols != self.cols:
            log.info("resize rows %s cols %s", rows, cols)
            self.rows = rows
            self.cols = cols 
            self.scroll_top = 0
            self.scroll_bottom = rows
            del self[:]
            for row in xrange(self.rows):
                self.append(TermRow(cols))

    def clear(self, top, left, bottom, right):
        top = clamp(top, 0, self.rows-1)
        left = clamp(left, 0, self.cols-1)
        bottom = clamp(bottom, 0, self.rows-1)
        right = clamp(right, 0, self.cols-1)
        
        for crow in xrange(top, bottom+1):
            row = self[crow+self.visible_start]
            row.dirty = True
            for ccol in xrange(left, right+1):
                row.chars[ccol] = ' '
                row.rendition[ccol] = DEFAULT_RENDITION

    def scroll_up(self):
        self.visible_start += 1
        self.insert(self.visible_start+self.scroll_bottom-1, TermRow(self.cols))
        if len(self) > self.term.buffer_size:
            self[:] = self[-self.term.buffer_size:]
            self.visible_start = len(self) - self.rows

    def move_visible_start(self, amt):
        self.visible_start = clamp(self.visible_start + amt, 0, len(self) - self.rows)
        self.term.flush()

    def putch(self, ch):
        self.visible_start = len(self) - self.rows
        if self.cursor_col >= self.cols:
            self.cursor_col = 0
            self.cursor_row += 1
            if self.cursor_row >= self.rows:
                self.scroll_up()
            self.cursor_row -= 1

        try:
            row = self[self.cursor_row+self.visible_start]
        except:
            print self.cursor_row, self.rows, len(self)
            raise

        row.chars[self.cursor_col] = ch
        row.rendition[self.cursor_col] = self.rendition
        row.dirty = True
        self.cursor_col += 1

    def copy(self):
        ret = TermScreen(self.term)
        ret.cols = self.cols
        ret.rows = self.rows
        ret.rendition = self.rendition
        ret.scroll_top = self.scroll_top
        ret.scroll_bottom = self.scroll_bottom
        ret.cursor_row = self.cursor_row
        ret.cursor_col = self.cursor_col
        ret.cursor_stack = self.cursor_stack[:]
        ret.cursor_visible = self.cursor_visible
        for row in self:
            nrow = TermRow(self.cols)
            nrow.chars = row.chars[:]
            nrow.rendition = row.rendition[:]
            ret.dirty = True
            ret.append(nrow)
        return ret


class ReadMore(Exception):
    pass


class Term(EventDispatcher):
    def __init__(self):
        EventDispatcher.__init__(self)

        self.char_handlers = {
            ASCII_NUL  : self.on_char_ignore,
            ASCII_BK  : self.on_char_ignore,
            ASCII_BS   : self.on_char_BS,
            ASCII_HT   : self.on_char_HT,
            ASCII_VT   : self.on_char_LF,
            ASCII_FF   : self.on_char_LF,
            ASCII_CR   : self.on_char_CR,
            ASCII_LF   : self.on_char_LF,
            ASCII_XON  : self.on_char_ignore,
            ASCII_XOFF : self.on_char_ignore,
            ASCII_ESC  : self.on_char_ESC,
            ASCII_CSI  : self.on_char_ESC,
        }

        self.escape_seq_handlers = {
            'A' : self.on_esc_seq_A,
            'B' : self.on_esc_seq_B,
            'C' : self.on_esc_seq_C,
            'D' : self.on_esc_seq_D,
            'G' : self.on_esc_seq_G,
            'H' : self.on_esc_seq_H,
            'J' : self.on_esc_seq_J,
            'K' : self.on_esc_seq_K,
            'd' : self.on_esc_seq_d,
            'm' : self.on_esc_seq_m,
            'h' : self.on_esc_seq_h,
            'l' : self.on_esc_seq_l,
            'c' : self.on_esc_seq_c,
            'r' : self.on_esc_seq_r,
            'f' : self.on_esc_seq_f,
        }

        self.esc_seq_hl_handlers = {
            # Lock keyboard (set); Unlock keyboard (reset)
            #'2': self.on_esc_seq_hl_2, 
            # Insert mode (set); Replace mode (reset)
            #'4': self.on_esc_seq_hl_4, 
            # Echo on (set); Echo off (reset)
            #'12': self.on_esc_seq_hl_12, 
            # Return = CR+LF (set); Return = CR (reset)
            #'20': self.on_esc_seq_hl_20, 
            # Cursorkeys application (set); Cursorkeys normal (reset)
            #'?1': self.on_esc_seq_hl_q1, 
            # Ansi (set); VT52 (reset)
            #'?2': self.on_esc_seq_hl_q2, 
            # 132 char/row (set); 80 char/row (reset)
            #'?3': self.on_esc_seq_hl_q3, 
            # Jump scroll (set); Smooth scroll (reset)
            #'?4': self.on_esc_seq_hl_q4, 
            # Reverse screen (set); Normal screen (reset)
            #'?5': self.on_esc_seq_hl_q5, 
            # Sets relative coordinates (set); Sets absolute coordinates (reset)
            #'?6': self.on_esc_seq_hl_q6, 
            # Auto wrap (set); Auto wrap off (reset)
            #'?7': self.on_esc_seq_hl_q7, 
            # Auto repeat on (set); Auto repeat off (reset)
            #'?8': self.on_esc_seq_hl_q8, 
            # Send FF to printer after print screen (set); No char after PS (reset)
            #'?18': self.on_esc_seq_hl_q18, 
            # Print screen prints full screen (set); PS prints scroll region (reset)
            #'?19': self.on_esc_seq_hl_q19, 
            # Cursor on (set); Cursor off (reset) 
            '?25': self.on_esc_seq_hl_q25, 
            # ?47 save/restore screen
            '?47': self.on_esq_seq_hl_q47,
        }

        # used to save partial data in .write()
        self._saved_data = None

        # size of the scrollback buffer
        self.buffer_size = 1000

        # stack of saved screens
        self.saved_screens = []
        
        # the screen object 
        self.screen = TermScreen(self)

    def flush(self):
        self.dispatch_event('on_flush')
        
    def write(self, data):
        idx = 0
        if self._saved_data:
            data = self._saved_data + data
        data_len = len(data)
        try:
            while idx < data_len:   
                ch = data[idx]
                och = ord(ch)
                try:
                    f = self.char_handlers[och]
                except KeyError:
                    if och >= 32 and och <= 126:
                        self.screen.putch(ch)
                    idx += 1
                else:
                    try:
                        idx = f(ch, data, idx)
                    except ReadMore:
                        self._saved_data = data[idx:]
                        break
            self.flush()

        except:
            crashlog = open('crash.log', 'w')
            for i, c in enumerate(data):
                if i == idx:
                    print >>crashlog, '**', 
                print >>crashlog, '%s:"%s"' % (ord(c), c),
            raise
        self._saved_data = None

    def on_char_ignore(self, ch, data, idx):    
        return idx + 1

    def on_char_BS(self, ch, data, idx):
        self.screen.cursor_col -= 1
        if self.screen.cursor_col <= 0:
            self.screen.cursor_col = 0
        return idx + 1

    def on_char_HT(self, ch, data, idx):
        self.screen.cursor_col += self.screen.cursor_col % 8
        return idx + 1

    def on_char_LF(self, ch, data, idx):
        self.screen.cursor_row += 1
        if self.screen.cursor_row >= self.screen.rows:
            self.screen.scroll_up()
            self.screen.cursor_row -= 1
        self.screen.cursor_col = 0 
        return idx + 1

    def on_char_CR(self, ch, data, idx):
        self.screen.cursor_col = 0 
        return idx + 1

    def _parse_escape_seq(self, data, idx):
        seq = ''
        while True:
            ch = data[idx]
            och = ord(ch)
            if och >= 32 and och <= 63:
                seq += ch
            elif och >= 4 and och < 126:
                return idx + 1, seq, ch
            else:
                raise "oops"
            idx += 1
        raise "oops2"

    def on_char_ESC(self, ch, data, idx):
        idx += 1
        try:
            ch = data[idx]
        except IndexError:
            raise ReadMore()

        if ch == '[':
            idx += 1
            idx, seq, ch = self._parse_escape_seq(data, idx)
            try:
                func = self.escape_seq_handlers[ch]
            except KeyError:
                log.warn('unknown esc seq %s', ch)
            else:
                try:
                    func(seq)
                except:
                    raise
        elif ch == ']':
            idx += 2
            title = ''
            while True:
                idx += 1
                ch = data[idx]
                och = ord(ch)
                if och == ASCII_BK:
                    break   
                title += ch
            idx += 1
            self.dispatch_event('on_title_change', title)
        elif ch == '7':
            self.screen.save_cursor()
            idx += 1
        elif ch == '8':
            idx += 1
            self.screen.restore_cursor()
        else:
            log.warn('unkown escape %s, "%s"', ch, map(ord, data[idx: idx+5]))
        return idx 

    def on_esc_seq_ignore(self, data):
        return 

    def on_esc_seq_A(self, data):
        # n A: Moves the cursor up n(default 1) times.
        if data:
            self.screen.cursor_row -= int(data)
        else:
            self.screen.cursor_row -= 1
        if self.screen.cursor_row < 0:
            self.screen.cursor_row = 0

    def on_esc_seq_B(self, data):
        # n B: Moves the cursor down n(default 1) times.
        if data:
            self.screen.cursor_row += int(data)
        else:
            self.screen.cursor_row += 1
        if self.screen.cursor_row >= self.screen.rows:
            self.screen.cursor_row = self.screen.rows - 1

    def on_esc_seq_C(self, data):
        # n C: Moves the cursor forward n(default 1) times.
        if data:
            self.screen.cursor_col += int(data)
        else:
            self.screen.cursor_col += 1
        if self.screen.cursor_col >= self.screen.cols:
            self.screen.cursor_col = self.screen.cols - 1

    def on_esc_seq_D(self, data):
        # n D: Moves the cursor backward n(default 1) times.
        if data:
            self.screen.cursor_col -= int(data)
        else:
            self.screen.cursor_col -= 1
        if self.screen.cursor_col < 0:
            self.screen.cursor_col = 0

    def on_esc_seq_G(self, data):
        # n G: Cursor horizontal absolute position. 'n' denotes
        # the column no(1 based index). Should retain the line 
        # position.
        self.screen.cursor_col = int(data)
        if self.screen.cursor_col < 0:
            self.screen.cursor_col = 0 
        elif self.screen.cursor_col >= self.screen.cols:
            self.screen.cursor_col = self.screen.cols - 1

    def on_esc_seq_H(self, data):
        # n ; m H: Moves the cursor to row n, column m.
        # The values are 1-based, and default to 1 (top left
        # corner). 
        if data == '' or data == ';':
            self.screen.cursor_row = 0
            self.screen.cursor_col = 0
        else:
            row, col = data.split(';')
            self.screen.cursor_row = clamp(int(row)-1, 0, self.screen.rows-1)
            self.screen.cursor_col = clamp(int(col)-1, 0, self.screen.cols-1)

    def on_esc_seq_J(self, data):
        # n J: Clears part of the screen. If n is zero 
        # (or missing), clear from cursor to end of screen. 
        # If n is one, clear from cursor to beginning of the 
        # screen. If n is two, clear entire screen.
        if data:
            n = int(data)
        else:
            n = 0
        if n == 0:
            self.screen.clear(self.screen.cursor_row, self.screen.cursor_col, self.screen.rows-1, self.screen.cols-1)
        elif n == 1:
            self.screen.clear(0, 0, self.screen.cursor_row, self.screen.cursor_col)
        elif n == 2:
            self.screen.clear(0, 0, self.screen.rows-1, self.screen.cols-1)
        else:
            raise "oops"

    def on_esc_seq_K(self, data):
        # n K: Erases part of the line. If n is zero 
        # (or missing), clear from cursor to the end of the
        # line. If n is one, clear from cursor to beginning of 
        # the line. If n is two, clear entire line. Cursor 
        # position does not change.
        if data:
            n = int(data)
        else:
            n = 0
        if n == 0:
            self.screen.clear(self.screen.cursor_row, self.screen.cursor_col, self.screen.cursor_row, self.screen.cols-1)
        elif n == 1:
            self.screen.clear(self.screen.cursor_row, 0, self.screen.cursor_row, self.screen.cursor_col)
        elif n == 2:
            self.screen.clear(self.screen.cursor_row, 0, self.screen.cursor_row, self.screen.cols-1)
        else:
            raise "oops K"

    def on_esc_seq_d(self, data):
        # n d: Cursor vertical absolute position. 'n' denotes
        # the line no(1 based index). Should retain the column 
        # position.
        self.screen.cursor_row = int(data) - 1

        if self.screen.cursor_row < 0:
            self.screen.cursor_row = 0 
        elif self.screen.cursor_row >= self.screen.rows:
            self.screen.cursor_row = self.screen.rows - 1

    def on_esc_seq_h(self, data):
        # sets some option
        try:
            func = self.esc_seq_hl_handlers[data]
        except KeyError:
            log.warn('unknown h %s', data)
        else:
            func(True)

    def on_esc_seq_l(self, data):
        # resets some option
        try:
            func = self.esc_seq_hl_handlers[data]
        except KeyError:
            log.warn('unknown l %s', data)
        else:
            func(False)

    def on_esc_seq_c(self, data):
        log.warn('term type not implemented')

    def on_esc_seq_f(self, data):
        # absolute move of cursor 
        if data:
            row, col = data.split(';')
            self.screen.cursor_row = clamp(self.scrolling_top + int(row)-1, 0, self.screen.rows-1)
            self.screen.cursor_col = clamp(int(col)-1, 0, self.screen.cols-1)
        else:
            self.screen.cursor_col = self.scrolling_top
            self.screen.cursor_row = 0 

    def on_esc_seq_r(self, data):
        if data:
            scroll_top, scroll_bottom = data.split(';')
            log.info('setting scrolling to %s,%s', scroll_top, scroll_bottom)
            self.scroll_top = int(scroll_top) - 1
            self.scroll_bottom = int(scroll_bottom) - 1
        else:
            log.info('resetting scrolling')
            self.scroll_top = 0
            self.scroll_bottom = self.screen.rows 

    def on_esc_seq_m(self, data):
        if data:
            renditions = data.split(';')
            for r in renditions:
                r = int(r)
                if r == 0:
                    self.screen.rendition = DEFAULT_RENDITION
                elif r == 1:
                    # alt intensity on
                    self.screen.rendition |= 1 << 0
                elif r == 2:
                    # 
                    self.screen.rendition |= 1 << 1
                elif r == 4:
                    # underline on
                    self.screen.rendition |= 1 << 2
                elif r == 5:
                    # blink on 
                    self.screen.rendition |= 1 << 3
                elif r == 7:
                    # inverse on 
                    self.screen.rendition |= 1 << 4
                elif r == 8:
                    # 
                    self.screen.rendition |= 1 << 5
                elif r == 24:
                    # underline off 
                    self.screen.rendition &= ~ (1 << 2)
                elif r == 25:
                    # blink off
                    self.screen.rendition &= ~ (1 << 3)
                elif r == 27:
                    # inverse off 
                    self.screen.rendition &= ~ (1 << 4)
                elif r >= 30 and r < 38:
                    # foreground 1-7
                    self.screen.rendition = (self.screen.rendition & 0x00ffffff) | ((r - 30) << 24)
                elif r >= 90 and r < 98:
                    # foreground 8-15
                    self.screen.rendition = (self.screen.rendition & 0x00ffffff) | ((r - 82) << 24)
                elif r >= 40 and r < 48:
                    # background 1-7
                    self.screen.rendition = (self.screen.rendition & 0xff00ffff) | ((r - 40) << 16)
                elif r >= 100 and r < 108:
                    # background 8-15
                    self.screen.rendition = (self.screen.rendition & 0xff00ffff) | ((r - 92) << 16)
                elif r == 39:
                    # reset foreground
                    self.screen.rendition = (self.screen.rendition & 0x00ffffff) | DEFAULT_RENDITION
                elif r == 49:
                    # reset background
                    self.screen.rendition = (self.screen.rendition & 0xff00ffff) | DEFAULT_RENDITION
                
                else:
                    log.warn('unknown m rendition %s', r)
                #print "r", "%08x" % self.screen.rendition
        else:
            self.screen.rendition = DEFAULT_RENDITION

    def on_esc_seq_hl_q25(self, set):
        if set:
            self.screen.cursor_visible = True
        else:
            self.screen.cursor_visible = False

    def on_esq_seq_hl_q47(self, set):
        if set:
            log.debug('saving screen')
            self.saved_screens.append(self.screen.copy())
        else:
            log.debug('restoring screen')
            self.screen = self.saved_screens.pop()
            self.on_esc_seq_r(None)
            self.flush()

Term.register_event_type("on_flush")
Term.register_event_type("on_title_change")
                

class TermWindow(ui.Window):
    def __init__(self, app, **kwargs):
        self.app = app
        self.term = app.term
        ui.Window.__init__(self, **kwargs)

    def set_render_coords(self, x, y, width, height):
        ui.Window.set_render_coords(self, x, y, width, height)

        cr = self.app.ui.cr
        context = pango.cairo_create_context(cr)
        font_map = pango.cairo_font_map_get_default()
        desc = pango.FontDescription.from_string('Bitstream Vera Sans Mono 8')
        font = pango.font_map_load_font(font_map, context._internal, desc._internal)
        metrics = pango.font_get_metrics(font, None)[0]
        self.char_width = pango.pango_units_to_double(pango.font_metrics_get_approximate_char_width(metrics))
        self.char_height = (
            pango.pango_units_to_double(pango.font_metrics_get_ascent(metrics)) + 
            pango.pango_units_to_double(pango.font_metrics_get_descent(metrics))
        )

        self.chars_width = int(self.rwidth / self.char_width)
        self.chars_height = int(self.rheight / self.char_height)

        self.app.term.screen.resize(self.chars_height, self.chars_width)
        fcntl.ioctl(self.app.process_io, termios.TIOCSWINSZ,
                struct.pack("hhhh", self.chars_height, self.chars_width, 0, 0))

    def _render(self, cr):
        desc = pango.FontDescription.from_string('Bitstream Vera Sans Mono 8')
        y = self.ry + self.char_height
        for row in self.term.screen[self.term.screen.visible_start:self.term.screen.visible_start+self.term.screen.rows]:
            if row.dirty:
                curr = row.rendition[0]
                #print "curr %08x" % curr, curr >> 24, (curr & 0x00ff0000) >> 16
                markup = ('<span foreground="%s" background="%s">' % (
                        color_map[curr >> 24], 
                        color_map[(curr & 0x00ff0000) >> 16],
                        )) + row.chars[0]
                for c in xrange(1, self.chars_width):
                    ch = row.chars[c]
                    r = row.rendition[c]
                    if curr != r:
                        curr = r
                        markup += ('</span><span foreground="%s" background="%s">' % (
                                color_map[curr >> 24], 
                                color_map[(curr & 0x00ff0000) >> 16],
                                ))
                    if ch == '>':
                        markup += '&gt;'
                    elif ch == '<':
                        markup += '&lt;'
                    else:
                        markup += ch
                markup += '</span>'
                row.layout = pango.cairo_create_layout(cr)
                row.layout.font_description = desc
                row.layout.set_markup(markup, -1)
                row.dirty = False
            if row.layout:
                cr.move_to(self.rx, y-pango.pango_units_to_double(row.layout.get_baseline()))
                pango.cairo_update_layout(cr, row.layout)
                pango.cairo_show_layout(cr, row.layout)

            y += self.char_height
        desc.free()

        cr.rectangle(
            self.rx+(self.term.screen.cursor_col*self.char_width),
            2+self.ry+(self.term.screen.cursor_row*self.char_height),
            self.char_width,
            self.char_height)
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.5)
        cr.fill()


class YahikoTerm(object):
    def __init__(self, app, screen, double_buf=False):
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
                    | xproto.EventMask.StructureNotify
                ),
        )

        self.win.ewmh_set_window_name('yahiko-term')
        self.win.map()

        self.win.push_handlers(
                on_key_press=self.win_on_key_press,
        )
        
        if not double_buf:
            log.info('not using double buffering')
            top_lev_class = ui.TopLevelContainer
        else:
            log.info('using double buffering')
            top_lev_class = ui.DoubleBufTopLevelContainer

        self.ui = top_lev_class(
                self.win,
                visualtype,
                style={
                    'background.style': 'fill',
                    'background.color': (0.0, 0.0, 0.0),
                },
                layouter=ui.HorizontalLayouter,
        )

        self.term = Term()
        self.term.push_handlers(
                on_flush=self.term_on_flush,
                on_title_change=self.term_on_title_change,
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

        self.process_pid, self.process_io = pty.fork()
        if self.process_pid == 0:
            #os.system('python test.py')
            os.system('bash')

        self.ui.recreate_surface()
        self.ui.layout()
        self.ui.dirty()
        
        log.info("Child process pid %s", self.process_pid)

        self.app.add_fd_handler('read', self.process_io, self.process_io_read)
        self.app.add_fd_handler('error', self.process_io, self.process_io_error)

    def term_on_title_change(self, title):
        self.win.ewmh_set_window_name(title)

    def term_on_flush(self):
        text = ''
        for line in self.term.screen:
            text += line.chars.tostring() + "\n"
        self.output.text = text
        self.output.cursor_row = self.term.screen.cursor_row
        self.output.cursor_col = self.term.screen.cursor_col
        self.output.dirty()

    def win_on_key_press(self, event):
        if event.detail == 0:
            return 
        # up
        elif event.detail == 111:
            os.write(self.process_io, 'OA')
        # down
        elif event.detail == 116:
            os.write(self.process_io, 'OB')
        # right
        elif event.detail == 114:
            os.write(self.process_io, 'OC')
        # left
        elif event.detail == 113:
            os.write(self.process_io, 'OD')
        # shift + pageup
        elif event.detail == 112 and event.state & xproto.ModMask.Shift:
            self.term.screen.move_visible_start(-1)
        # shift + pagedown
        elif event.detail == 117 and event.state & xproto.ModMask.Shift:
            self.term.screen.move_visible_start(1)
        else:
            shift = int((event.state & xproto.ModMask.Shift) 
                     or (event.state & xproto.ModMask.Lock))
            control = int(event.state & xproto.ModMask.Control)
            k = (event.conn.keysyms.get_keysym(event.detail, shift)) & 255

            # dodgey control hack 
            if control:
                k -= 96
            # remove other keys
            if k > 225:
                return 
            log.debug('sending %s', k)

            os.write(self.process_io, chr(k))
        
    def process_io_error(self):
        print "process error"
        self.app.stop()

    def process_io_read(self):
        output = ""
        while True:
            try:
                data = os.read(self.process_io, 512)
            except OSError:
                print "OSError"
                self.app.stop()
                return 
            data_len = len(data)
            output += data

            if data_len < 512:
                break
        self.term.write(output)


class App(BaseApp):
    def __init__(self, double_buf=False, **kwargs):
        BaseApp.__init__(self, **kwargs)
        self.double_buf = double_buf

    def init(self):
        BaseApp.init(self)

        screen = self.conn.setup.roots[self.conn.pref_screen]
        self.term = YahikoTerm(self, screen, double_buf=self.double_buf)

    def run(self):
        self.start_time = time.time()
        BaseApp.run(self)

    def stop(self, **args):
        self.stop_time = time.time()
        print "exec time", self.stop_time - self.start_time
        BaseApp.stop(self)
    

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

    parser.add_option('', '--prof', dest='profile',
            action='store_true', 
            default=False, 
            help='profile the application',
    )

    parser.add_option('-b', '--double-buf', dest='double_buf',
            default=False,
            action='store_true',
            help='use double buffering',
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
            double_buf=options.double_buf,
            #config_path=options.configpath,
        )

    if options.profile:
        import cProfile as profile
        profile.runctx('sxmain.run_app(create_app)', globals(), locals())
    else:
        sxmain.run_app(create_app)


if __name__ == '__main__':
    run()

