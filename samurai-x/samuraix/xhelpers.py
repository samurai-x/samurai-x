import os

from pyglet.window.xlib import xlib 
from samuraix.sxctypes import *

import samuraix
from samuraix import keysymdef

import logging
log = logging.getLogger(__name__)


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


def open_display(displayname=None):
    log.info('opening display...')
    if displayname is None:
        displayname = os.environ.get('DISPLAY', ':0')
    samuraix.displayname = displayname

    log.info("connecting to %s" % displayname)
    samuraix.display = xlib.XOpenDisplay(None)
    if not samuraix.display:
        # not sure what this exception should be really...
        raise RuntimeError("Cant connect to xserver")

    xlib.XSynchronize(samuraix.display, True)


def close_display():
    log.info('closing display..')
    xlib.XSync(samuraix.display, False)
    xlib.XCloseDisplay(samuraix.display)


def check_for_other_wm():
    log.info('checking for other wm...')
    def xerror(display, ev):
        raise "another wm is already running!"
    c_xerror = xlib.XErrorHandler(xerror)

    xlib.XSetErrorHandler(c_xerror)
    for screen in range(xlib.XScreenCount(samuraix.display)):
        xlib.XSelectInput(samuraix.display, 
            xlib.XRootWindow(samuraix.display, screen),
            xlib.SubstructureRedirectMask)
    xlib.XSync(samuraix.display, False)
    xlib.XSetErrorHandler(xlib.XErrorHandler())


def get_numlock_mask():
    log.info('fetching numlock mask...')
    modmap = xlib.XGetModifierMapping(samuraix.display)[0]
    keycode = xlib.XKeysymToKeycode(samuraix.display, keysymdef.XK_Num_Lock)

    mask = 0 

    for i in range(8):
        for j in range(0, modmap.max_keypermod):
            if modmap.modifiermap[i * modmap.max_keypermod + j] == keycode:
                mask = 1 << i

    xlib.XFreeModifiermap(modmap)

    xlib.NumLockMask = mask


def setup_xerror():
    log.info('installing x error handler...')
    def xerror(display, ev):
        log.debug('xerror %s' % ev)
        if (ev.error_code == xlib.BadWindow or
            (ev.error_code == xlib.BadMatch and ev.request_code == xlib.X_SetInputFocus) or
            (ev.error_code == xlib.BadValue and ev.request_code == xlib.X_KillClient) or
            (ev.error_code == xlib.BadMatch and ev.request_code == xlib.X_ConfigureWindow)):
            return 0
        log.warn('fatal error: request_code=%s error_code=%s' % (ev.request_code, ev.error_code))
        return xerrorxlib(display, ev)

    c_xerror = xlib.XErrorHandler(xerror)
    xerrorxlib = xlib.XSetErrorHandler(c_xerror)
    xlib.XSync(samuraix.display, False)
