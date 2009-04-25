# a simple xtest extension test.
from __future__ import with_statement

import sys
sys.path.append('..')

import ooxcb
import ooxcb.xproto
import ooxcb.xtest
from ooxcb.constant import KeyPress, KeyRelease
from ooxcb.keysymdef import XK_B

conn = ooxcb.connect()

# fetch the keycode of the 'b' key
keycode = conn.keysyms.get_keycode(XK_B)

with conn.bunch():
    # simulate a 'b' key press
    conn.xtest.fake_input(KeyPress, keycode)
    # simulate a 'b' key release (necessary)
    conn.xtest.fake_input(KeyRelease, keycode)

