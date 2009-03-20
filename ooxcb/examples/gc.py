# coding: utf-8
import sys
sys.path.append('..')

import ooxcb
from ooxcb.xproto import *

conn = ooxcb.connect()

def main():
    screen = conn.setup.roots[conn.pref_screen]

    pixel = screen.default_colormap.alloc_hex_color('#00dd00').reply().pixel

    win = Window.create_toplevel_on_screen(conn, screen,
            back_pixel=pixel,
            event_mask=EventMask.Exposure | EventMask.ButtonPress
    )
    win.map()
    conn.flush()

    gc = GContext.create(conn, win,
            foreground=screen.black_pixel,
            background=pixel
    )

    @win.event
    def on_button_press(evt):
        sys.exit()

    @win.event
    def on_expose(evt):
        with conn.bunch():
            # Some utf-8 text ...
            gc.image_text16(win, 50, 50, u"Öh neün! Öß sünð ßo viele Üµläut¢!")
            # A rectangle!
            gc.poly_rectangle(win, [Rectangle.create(conn, 30, 30, 200, 130)])
            # Points!
            gc.poly_point(win, [(10, 10), (30, 30), (150, 150)])
            # Lines! well, actually a triangle.
            gc.poly_line(win, [(300, 300), (200, 300), (400, 350), (300, 300)])
            # Segments!
            gc.poly_segment(win, [(400, 10, 400, 400), (600, 400, 600, 200)])
            # An arc!
            # The xcb manual says:
            # Note: the angles are expressed in units of 1/64 of a degree, so
            # to have an angle of 90 degrees, starting at 0, angle1 = 0 and
            # angle2 = 90 << 6.
            # Positive angles indicate counterclockwise motion,
            # while negative angles indicate clockwise motion.
            gc.poly_arc(win,
                    [Arc.create(conn, 200, 200, 300, 300, 0, 90 << 6)])

    while 1:
        conn.wait_for_event().dispatch()

if __name__ == '__main__':
    try:
        main()
    finally:
        conn.disconnect()
