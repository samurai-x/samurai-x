# coding: utf-8
import sys
sys.path.append('..')

import ooxcb
from ooxcb.xproto import *

conn = ooxcb.connect()

def main():
    setup = conn.get_setup()
    screen = setup.roots[0]
    root = setup.roots[0].root
    depth = setup.roots[0].root_depth
    visual = setup.roots[0].root_visual

    win = Window.create(conn, root, depth, visual, 
            back_pixel=setup.roots[0].white_pixel,
            event_mask=EventMask.Exposure | EventMask.ButtonPress)
    win.map()
    conn.flush()

    gc = GContext.create(conn, win,
            foreground=screen.black_pixel,
            background=screen.white_pixel
    )

    while 1:
        if isinstance(conn.wait_for_event(), ButtonPressEvent):
            break
        else: # expose event
            gc.image_text16(win, 100, 100, u"Smörebröd ißt spaßö¢!")
            conn.flush()

if __name__ == '__main__':
    try:
        main()
    finally:
        conn.disconnect()
