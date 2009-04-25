# a simple xtest extension test.
from __future__ import with_statement

import sys
sys.path.append('..')

import ooxcb
import ooxcb.xproto
import ooxcb.xtest
from ooxcb.constant import KeyPress, KeyRelease, MotionNotify
from ooxcb.keysymdef import XK_B

conn = ooxcb.connect()

# fetch the keycode of the 'b' key
keycode = conn.keysyms.get_keycode(XK_B)

with conn.bunch():
    # simulate a 'b' key press
    conn.xtest.fake_input(KeyPress, detail=keycode)
    # simulate a 'b' key release (necessary)
    conn.xtest.fake_input(KeyRelease, detail=keycode)

# and now move the cursor to the center of the screen
screen = conn.setup.roots[conn.pref_screen]
center = (screen.width_in_pixels // 2, screen.height_in_pixels // 2)

with conn.bunch():
    conn.xtest.fake_input(MotionNotify, rootX=center[0], rootY=center[1])

