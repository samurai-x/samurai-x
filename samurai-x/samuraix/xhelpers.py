from pyglet.window.xlib import xlib 
from samuraix.sxctypes import *

import samuraix

def get_window_state(window):
    format = c_int()
    p = c_uchar_p()
    n = c_ulong()
    extra = c_ulong()
    real = xlib.Atom()

    if (xlib.XGetWindowProperty(samuraix.display, window, samuraix.atoms['WM_STATE'],
            0, 2, False, samuraix.atoms['WM_STATE'], 
            byref(real), byref(format), byref(n), byref(extra), byref(p)) != xlib.Success):
        return -1
    if n.value != 0:
        return p
    return -1


