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

import TermEmulator

from ooxcb.protocol import xproto
from ooxcb.eventsys import EventDispatcher

import ooxcb.contrib.ewmh
ooxcb.contrib.ewmh.mixin()

import logging
log = logging.getLogger(__name__)

sys.path.append('/usr/lib/python2.6/dist-packages')
import psyco
psyco.full()

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


# n A: Moves the cursor up n(default 1) times.
ESC_SEQ_A = 'A'  
# n B: Moves the cursor down n(default 1) times.
ESC_SEQ_B = 'B'  
# n C: Moves the cursor forward n(default 1) times.
ESC_SEQ_c = 'C'  
# n D: Moves the cursor backward n(default 1) times.
ESC_SEQ_D = 'D'  

# n G: Cursor horizontal absolute position. 'n' denotes
# the column no(1 based index). Should retain the line 
# position.
ESC_SEQ_G = 'G'  

# n ; m H: Moves the cursor to row n, column m.
# The values are 1-based, and default to 1 (top left
# corner). 
ESC_SEQ_H = 'H'  

# n J: Clears part of the screen. If n is zero 
# (or missing), clear from cursor to end of screen. 
# If n is one, clear from cursor to beginning of the 
# screen. If n is two, clear entire screen.
ESC_SEQ_J = 'J'   

# n K: Erases part of the line. If n is zero 
# (or missing), clear from cursor to the end of the
# line. If n is one, clear from cursor to beginning of 
# the line. If n is two, clear entire line. Cursor 
# position does not change.
ESC_SEQ_K = 'K'   

# n d: Cursor vertical absolute position. 'n' denotes
# the line no(1 based index). Should retain the column 
# position.
ESC_SEQ_d = 'd'  

# n [;k] m: Sets SGR (Select Graphic Rendition) 
# parameters. After CSI can be zero or more parameters
# separated with ;. With no parameters, CSI m is treated
# as CSI 0 m (reset / normal), which is typical of most
# of the ANSI codes.
ESC_SEQ_SGR = 'm'  

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
color_map2 = {
    0:  (0, 0, 0), #'#000',
    1:  (127, 0, 0), #'#700',
    2:  (0, 127, 0), #'#070',
    3:  (127, 127, 0), #'#770',
    4:  (0, 0, 127), #'#007',
    5:  (127, 0, 127), #'#707',
    6:  (0, 127, 127), #'#077',
    7:  (127, 127, 127), #'#777',
    8:  (0, 0, 0), #'#000',
    9:  (65535, 0, 0), #'#700',
   10:  (0, 65535, 0), #'#070',
   11:  (65535, 65535, 0), #'#770',
   12:  (0, 0, 65535), #'#007',
   13:  (65535, 0, 65535), #'#707',
   14:  (0, 65535, 65535), #'#077',
   15:  (65535, 65535, 65535), #'#777',
}


"""
class TermRendition(object):
    #__slots__ = ['style', 'background', 'foreground']

    bright      = 0x00000001
    dim         = 0x00000010
    underline   = 0x00000100
    blink       = 0x00001000
    reverse     = 0x00010000
    hidden      = 0x00100000

    def __init__(self):
        self.reset()

    def reset(self):
        self.style = 0
        self.foreground = 7
        self.background = 0

    def copy_to(self, other):
        other.style = self.style
        other.foreground = self.foreground
        other.background = self.background
    

class TermChar(TermRendition):
    #__slots__ = ['ch']
    def __init__(self):
        TermRendition.__init__(self)
        self.ch = ' '

    def __str__(self):
        return self.ch




from mako.filters import html_escape

class TermRow(list):
    #__slots__ = ['dirty', '_cached_pango']
    def __init__(self, cols):
        self.dirty = False
        self._cached_pango = None
        for c in xrange(cols):
            self.append(TermChar())

    def __str__(self):
        return "".join(c.ch for c in self)

    def pango_str(self):
        if not self.dirty and self._cached_pango:
            return self._cached_pango

        cstyle = 0 
        cfg = 0
        cbg = 0
        set_one = False
        ret = ''
        for c in self:
            if c.style != cstyle or cfg != c.foreground or cbg != c.background:
                if set_one:
                    ret += ('</span>')
                try:
                    hfg = color_map[c.foreground]
                except KeyError:
                    log.warn('color %s nt found', c.foreground)
                    hfg = '#f00'
                try:
                    hbg = color_map[c.background]
                except KeyError:
                    log.warn('color %s not found', c.background)
                    hbg = '#700'

                extra = ''
                if c.style & TermRendition.underline:
                    extra += ('underline="single"')
                if c.style & TermRendition.bright:
                    extra += ('font-weight="bold"')
                if c.style & TermRendition.reverse:
                    hfg, hbg = hbg, hfg
                ret += ('<span foreground="%s" background="%s" %s>' % (hfg, hbg, extra))
                set_one = True
                cstyle = c.style
                cfg = c.foreground
                cbg = c.background
            if c.ch == '<': ret += '&lt;'
            elif c.ch == '>': ret += '&gt;'
            else: ret += c.ch
        if set_one:
            ret += ('</span>')
        self._cached_pango = ret
        self.dirty = False
        return self._cached_pango

    def pango_str(self):
        if not self.dirty and self._cached_pango:
            return self._cached_pango

        cstyle = 0 
        cfg = 0
        cbg = 0
        set_one = False
        ret = []
        for c in self:
            if c.style != cstyle or cfg != c.foreground or cbg != c.background:
                if set_one:
                    ret.append('</span>')
                try:
                    hfg = color_map[c.foreground]
                except KeyError:
                    log.warn('color %s nt found', c.foreground)
                    hfg = '#f00'
                try:
                    hbg = color_map[c.background]
                except KeyError:
                    log.warn('color %s not found', c.background)
                    hbg = '#700'

                extra = []
                if c.style & TermRendition.underline:
                    extra.append('underline="single"')
                if c.style & TermRendition.bright:
                    extra.append('font-weight="bold"')
                if c.style & TermRendition.reverse:
                    hfg, hbg = hbg, hfg
                ret.append('<span foreground="%s" background="%s" %s>' % (hfg, hbg, " ".join(extra)))
                set_one = True
                cstyle = c.style
                cfg = c.foreground
                cbg = c.background
            ret.append(html_escape(c.ch))
        if set_one:
            ret.append('</span>')
        self._cached_pango = "".join(ret)
        self.dirty = False
        return self._cached_pango

"""

DEFAULT_RENDITION = 0x0f000000

class TermRow(object):
    __slots__ = ['chars', 'rendition', 'dirty', 'layout']

    def __init__(self, cols):
        self.chars = array('c', ' '*cols)
        self.rendition = array('L', [0]*cols)
        self.dirty = False
        self.layout = None

    #def pango_str(self):
    #    return "<span fgcolor='#fff'>"+self.chars.tostring()+"</span>"


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
            #'?25': self.on_esc_seq_hl_q25, 
            # ?47 save/restore screen
            '?47': self.on_esq_seq_hl_q47,
        }

        self.cursor_row = 0
        self.cursor_col = 0 
        self.cols = 0
        self.rows = 0
        self.scroll_top = 0
        self.scroll_bottom = 0
        self.rendition = DEFAULT_RENDITION

        self._saved_idx = 0
        self._saved_data = None

        self.saved_screens = []
        self.screen = None

    def resize(self, rows, cols):
        log.info("resize rows %s cols %s", rows, cols)
        self.rows = rows
        self.cols = cols 
        self.scroll_top = 0
        self.scroll_bottom = rows
        self.screen = []
        for row in xrange(self.rows):
            self.screen.append(TermRow(cols))

    def clear(self, top, left, bottom, right):
        print "clear!"
        top = clamp(top, 0, self.rows-1)
        left = clamp(left, 0, self.cols-1)
        bottom = clamp(bottom, 0, self.rows-1)
        right = clamp(right, 0, self.cols-1)
        
        for crow in xrange(top, bottom+1):
            row = self.screen[crow]
            row.dirty = True
            for ccol in xrange(left, right+1):
                row.chars[ccol] = ' '
                row.rendition[ccol] = DEFAULT_RENDITION

    def scroll_up(self):
        self.screen.pop(self.scroll_top)
        self.screen.insert(self.scroll_bottom-1, TermRow(self.cols))

    def putch(self, ch):
        if self.cursor_col >= self.cols:
            self.cursor_col = 0
            self.cursor_row += 1
            if self.cursor_row >= self.rows:
                self.scroll_up()
            self.cursor_row -= 1

        row = self.screen[self.cursor_row]
        row.chars[self.cursor_col] = ch
        row.rendition[self.cursor_col] = self.rendition
        row.dirty = True
        self.cursor_col += 1

    def flush(self):
        self.dispatch_event('on_flush')
        
    def write(self, data):
        idx = self._saved_idx
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
                        self.putch(ch)
                    idx += 1
                else:
                    try:
                        idx = f(ch, data, idx)
                    except ReadMore:
                        self._saved_idx = idx
                        self._saved_data = data
                        break
            self.flush()

        except:
            crashlog = open('crash.log', 'w')
            for i, c in enumerate(data):
                if i == idx:
                    print >>crashlog, '**', 
                print >>crashlog, '%s:"%s"' % (ord(c), c),
            raise
        self._saved_idx = 0
        self._saved_data = None

    def on_char_ignore(self, ch, data, idx):    
        return idx + 1

    def on_char_BS(self, ch, data, idx):
        self.cursor_col -= 1
        if self.cursor_col <= 0:
            self.cursor_col = 0
        return idx + 1

    def on_char_HT(self, ch, data, idx):
        self.cursor_col += self.cursor_col % 8
        return idx + 1

    def on_char_LF(self, ch, data, idx):
        self.cursor_row += 1
        if self.cursor_row >= self.rows:
            self.scroll_up()
            self.cursor_row -= 1
        self.cursor_col = 0 
        return idx + 1

    def on_char_CR(self, ch, data, idx):
        self.cursor_col = 0 
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
        return idx 

    def on_esc_seq_ignore(self, data):
        return 

    def on_esc_seq_A(self, data):
        # n A: Moves the cursor up n(default 1) times.
        if data:
            self.cursor_row -= int(data)
        else:
            self.cursor_row -= 1
        if self.cursor_row < 0:
            self.cursor_row = 0

    def on_esc_seq_B(self, data):
        # n B: Moves the cursor down n(default 1) times.
        if data:
            self.cursor_row += int(data)
        else:
            self.cursor_row += 1
        if self.cursor_row >= self.rows:
            self.cursor_row = self.rows - 1

    def on_esc_seq_C(self, data):
        # n C: Moves the cursor forward n(default 1) times.
        if data:
            self.cursor_col += int(data)
        else:
            self.cursor_col += 1
        if self.cursor_col >= self.cols:
            self.cursor_col = self.cols - 1

    def on_esc_seq_D(self, data):
        # n D: Moves the cursor backward n(default 1) times.
        if data:
            self.cursor_col -= int(data)
        else:
            self.cursor_col -= 1
        if self.cursor_col < 0:
            self.cursor_col = 0

    def on_esc_seq_G(self, data):
        # n G: Cursor horizontal absolute position. 'n' denotes
        # the column no(1 based index). Should retain the line 
        # position.
        self.cursor_col = int(data)
        if self.cursor_col < 0:
            self.cursor_col = 0 
        elif self.cursor_col >= self.cols:
            self.cursor_col = self.cols - 1

    def on_esc_seq_H(self, data):
        # n ; m H: Moves the cursor to row n, column m.
        # The values are 1-based, and default to 1 (top left
        # corner). 
        if data == '' or data == ';':
            self.cursor_row = 0
            self.cursor_col = 0
        else:
            row, col = data.split(';')
            self.cursor_row = clamp(int(row)-1, 0, self.rows-1)
            self.cursor_col = clamp(int(col)-1, 0, self.cols-1)

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
            self.clear(self.cursor_row, self.cursor_col, self.rows-1, self.cols-1)
        elif n == 1:
            self.clear(0, 0, self.cursor_row, self.cursor_col)
        elif n == 2:
            self.clear(0, 0, self.rows-1, self.cols-1)
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
            self.clear(self.cursor_row, self.cursor_col, self.cursor_row, self.cols-1)
        elif n == 1:
            self.clear(self.cursor_row, 0, self.cursor_row, self.cursor_col)
        elif n == 2:
            self.clear(self.cursor_row, 0, self.cursor_row, self.cols-1)
        else:
            raise "oops K"

    def on_esc_seq_d(self, data):
        # n d: Cursor vertical absolute position. 'n' denotes
        # the line no(1 based index). Should retain the column 
        # position.
        self.cursor_row = int(data) - 1

        if self.cursor_row < 0:
            self.cursor_row = 0 
        elif self.cursor_row >= self.rows:
            self.cursor_row = self.rows - 1

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
            self.cursor_row = clamp(self.scrolling_top + int(row)-1, 0, self.rows-1)
            self.cursor_col = clamp(int(col)-1, 0, self.cols-1)
        else:
            self.cursor_col = self.scrolling_top
            self.cursor_row = 0 

    def on_esc_seq_r(self, data):
        if data:
            scroll_top, scroll_bottom = data.split(';')
            log.info('setting scrolling to %s,%s', scroll_top, scroll_bottom)
            self.scroll_top = int(scroll_top) - 1
            self.scroll_bottom = int(scroll_bottom) - 1
        else:
            log.info('resetting scrolling')
            self.scroll_top = 0
            self.scroll_bottom = self.rows 

    def on_esc_seq_m(self, data):
        if data:
            renditions = data.split(';')
            for r in renditions:
                r = int(r)
                if r == 0:
                    self.rendition = DEFAULT_RENDITION
                elif r == 1:
                    self.rendition |= 1 << 0
                elif r == 2:
                    self.rendition |= 1 << 1
                elif r == 4:
                    self.rendition |= 1 << 2
                elif r == 5:
                    self.rendition |= 1 << 3
                elif r == 7:
                    self.rendition |= 1 << 4
                elif r == 8:
                    self.rendition |= 1 << 5
                elif r >= 30 and r < 38:
                    self.rendition |= (r - 30) << 24
                elif r >= 90 and r < 98:
                    self.rendition |= (r - 82) << 24
                elif r >= 40 and r < 48:
                    self.rendition |= (r - 40) << 16
                elif r >= 100 and r < 108:
                    self.rendition |= (r - 92) << 16
                #elif r == 39:
                #    self.rendition.foreground = 7
                #elif r == 49:
                #    self.rendition.background = 0
                else:
                    log.warn('unknown m rendition %s', r)
                #print "r", "%08x" % r
        else:
            print "mclear"
            self.rendition = DEFAULT_RENDITION

    def on_esq_seq_hl_q47(self, set):
        if set:
            log.debug('saving screen')
            self.saved_screens.append((copy.deepcopy(self.screen), self.cursor_row, self.cursor_col))
        else:
            log.debug('restoring screen')
            self.screen, self.cursor_row, self.cursor_col = self.saved_screens.pop()
            self.on_esc_seq_r(None)
            self.flush()

Term.register_event_type("on_flush")
Term.register_event_type("on_title_change")
                

class TermWindow(ui.Window):
    def __init__(self, app, **kwargs):
        self.app = app
        self.term = app.term
        self.cursor_col = 0 
        self.cursor_row = 0 
        ui.Window.__init__(self, **kwargs)

    def set_render_coords(self, x, y, width, height):
        ui.Window.set_render_coords(self, x, y, width, height)

        #text = DictProxy(self.style, 'text.')
        #family = text.get('family', 'sans-serif')
        #weight = getattr(
        #        cairo, 
        #        'CAIRO_FONT_WEIGHT_' + text.get('weight', 'normal').upper(), 
        #        cairo.CAIRO_FONT_WEIGHT_NORMAL,
        #)
        #slant = getattr(
        #        cairo,
        #        'CAIRO_FONT_SLANT_' + text.get('slant', 'normal').upper(),
        #        cairo.CAIRO_FONT_SLANT_NORMAL,
        #)
        #cr = self.app.ui.cr
        #cr.select_font_face(family, weight, slant)
        #extents = cairo.font_extents_t()
        #cr.font_extents(byref(extents))
        #self.char_height = extents.height
        #self.char_width = extents.max_x_advance

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

        self.app.term.resize(self.chars_height, self.chars_width)
        fcntl.ioctl(self.app.process_io, termios.TIOCSWINSZ,
                struct.pack("hhhh", self.chars_height, self.chars_width, 0, 0))

    def _render(self, cr):
        desc = pango.FontDescription.from_string('Bitstream Vera Sans Mono 8')
        y = self.ry
        for row in self.term.screen:
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
                cr.move_to(self.rx, y)
                pango.cairo_update_layout(cr, row.layout)
                pango.cairo_show_layout(cr, row.layout)

            y += self.char_height
        desc.free()

        #cr.rectangle(
        ##    self.rx+(self.cursor_col*self.char_width),
        #    2+self.ry+(self.cursor_row*self.char_height),
        #    self.char_width,
        #    self.char_height)
        #cr.set_source_rgba(1.0, 1.0, 1.0, 0.5)
        #cr.fill()


class YahikoTerm(object):
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
                    | xproto.EventMask.StructureNotify
                ),
        )

        self.win.ewmh_set_window_name('yahiko-term')
        self.win.map()

        self.win.push_handlers(
                on_key_press=self.win_on_key_press,
        )
        
        self.ui = ui.TopLevelContainer(
                self.win,
                visualtype,
                style={
                    'background.style': 'fill',
                    'background.color': (0.0, 0.0, 0.0),
                    #'border.style': 'fill',
                    #'border.color': (0.5, 0.0, 0.0),
                    #'border.width': 1.0,
                    #'layout.padding': 1,
                },
                layouter=ui.HorizontalLayouter,
        )

        #self.term = TermEmulator.V102Terminal(40, 80)
        #self.term.SetCallback(
        #        self.term.CALLBACK_UPDATE_LINES,
        #        self.term_on_update_lines,
        #)

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

        #fcntl.ioctl(process_io, termios.TIOCSWINSZ,
        #        struct.pack("hhhh", self.term.rows, self.term.cols, 0, 0))
        
        #tcattrib = termios.tcgetattr(process_io)
        #tcattrib[3] = tcattrib[3] & ~termios.ICANON
        #termios.tcsetattr(process_io, termios.TCSAFLUSH, tcattrib)
        
        # Sets raw mode
        #tty.setraw(process_io)
        
        # Sets the terminal window size
        #fcntl.ioctl(process_io, termios.TIOCSWINSZ,
        #            struct.pack("hhhh", self.chars_height, self.chars_width, 0, 0))
        
        #tcattrib = termios.tcgetattr(process_io)
        #tcattrib[3] = tcattrib[3] & ~termios.ICANON
        #termios.tcsetattr(process_io, termios.TCSAFLUSH, tcattrib)

        self.app.add_fd_handler('read', self.process_io, self.process_io_read)
        self.app.add_fd_handler('error', self.process_io, self.process_io_error)

    def term_on_title_change(self, title):
        self.win.ewmh_set_window_name(title)

    def term_on_flush(self):
        text = ''
        for line in self.term.screen:
            text += line.chars.tostring() + "\n"
        self.output.text = text
        self.output.cursor_row = self.term.cursor_row
        self.output.cursor_col = self.term.cursor_col
        self.output.dirty()

    def win_on_key_press(self, event):
        if event.detail == 0:
            return 

        # up
        if event.detail == 111:
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
        else:
            shift = int((event.state & xproto.ModMask.Shift) or (event.state & xproto.ModMask.Lock))
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
        self.output.text = self.output.text.replace('\t', '        ')
        self.output.dirty()


class App(BaseApp):
    def init(self):
        BaseApp.init(self)

        screen = self.conn.setup.roots[self.conn.pref_screen]
        self.term = YahikoTerm(self, screen)

    def run(self):
        self.start_time = time.time()
        BaseApp.run(self)

    def stop(self):
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

    if options.profile:
        import cProfile as profile
        profile.runctx('sxmain.run_app(create_app)', globals(), locals())
    else:
        sxmain.run_app(create_app)


if __name__ == '__main__':
    run()

