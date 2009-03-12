import sys

import ooxcb
from ooxcb.xproto import *

conn = ooxcb.connect()

setup = conn.get_setup()
root = setup.roots[0].root
depth = setup.roots[0].root_depth
visual = setup.roots[0].root_visual

win = Window.create(conn, root, depth, visual, back_pixel=setup.roots[0].white_pixel,
        event_mask=EventMask.Exposure | EventMask.ButtonPress)
win.configure(width=100)
win.map()
conn.flush()

@win.event
def on_button_press(evt):
    print 'Button pressed, exiting'
    conn.disconnect()
    sys.exit()

while True:
    try:
        conn.wait_for_event().dispatch()
    except ooxcb.ProtocolException, error:
        print "Protocol error %s received!" % error.__class__.__name__
        break
    except Exception, error:
        raise
conn.disconnect()
