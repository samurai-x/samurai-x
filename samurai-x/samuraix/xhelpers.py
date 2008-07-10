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


def set_window_state(window, state):
    long_2 = c_long * 2
    data = long_2(state, xlib.None_)
    return xlib.XChangeProperty(samuraix.display, window, samuraix.atoms['WM_STATE'],
            samuraix.atoms['WM_STATE'], 32,
            xlib.PropModeReplace, cast(data, c_uchar_p), 2)


def get_text_property(win, atom):
    text_prop = xlib.XTextProperty()
    status = xlib.XGetTextProperty(samuraix.display, win, text_prop, atom)

    list_return = c_char_p_p()
    count_return = c_int()
    xlib.XmbTextPropertyToTextList(samuraix.display, text_prop, byref(list_return), byref(count_return))
    name = None
    if count_return:
        name = string_at(list_return[0])
    xlib.XFreeStringList(list_return)
    return name


