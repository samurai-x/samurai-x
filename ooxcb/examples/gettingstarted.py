import sys
sys.path.append('..')

import ooxcb
import ooxcb.xproto

conn = ooxcb.connect()
setup = conn.setup

screen = conn.setup.roots[conn.pref_screen]
window = ooxcb.xproto.Window.create_toplevel_on_screen(conn, screen,
                back_pixel=screen.white_pixel,
                event_mask=ooxcb.xproto.EventMask.Exposure | ooxcb.xproto.EventMask.ButtonPress
                )

gc = ooxcb.xproto.GContext.create(conn, window)

with conn.bunch():
    window.map()

@window.event
def on_expose(evt):
    #gc.poly_line(window, [(0, 0), (640, 480)])
    gc.poly_line(window, [(10, 10), (600, 400), (10, 400), (10, 10)])
    conn.flush()

@window.event
def on_button_press(evt):
    conn.disconnect()
    sys.exit()
    
# Our mainloop.
while 1:
    conn.wait_for_event().dispatch()

conn.disconnect()
