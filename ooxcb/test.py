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

win.configure_checked(width=100).check()

win.map()

conn.flush()

@win.event
def on_button_press(evt):
    print 'Button pressed, exiting'
    conn.disconnect()
    sys.exit()

#foo = win.intern_atom('FOO', False).atom
#win.change_property(xproto.PropMode.Replace, foo, conn.XA_STRING, 8, 'huhu da!') 
conn.flush()
#print win.get_property_request(1, foo, conn.XA_STRING).reply().type.get_name().as_string

print "The window's colormap is %s!" % win.get_attributes().reply().colormap

while True:
    try:
        conn.wait_for_event().dispatch()
    except ooxcb.ProtocolException, error:
        print "Protocol error %s received!" % error.__class__.__name__
        break
    except Exception, error:
        raise
conn.disconnect()
