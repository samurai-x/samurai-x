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


def xerror(display, e):
    #if e:
    e = e.contents
    if e.error_code == xlib.BadWindow:
        log.debug('BadWindow err')
        return 0

    if True:
        buf = c_buffer(1024)
        xlib.XGetErrorText(display, e.error_code, buf, len(buf))
        log.warn('X11 error: %s', buf.value)
        log.warn('   serial: %s', e.serial)
        log.warn('  request: %s', e.request_code)
        log.warn('    minor: %s', e.minor_code)
        log.warn(' resource: %s', e.resourceid)

        import traceback
        print 'Python stack trace (innermost last):'
        traceback.print_stack()

    return 0

    #if (ev.error_code == xlib.BadWindow or
    #    (ev.error_code == xlib.BadMatch and ev.request_code == xlib.X_SetInputFocus) or
    #    (ev.error_code == xlib.BadValue and ev.request_code == xlib.X_KillClient) or
    #    (ev.error_code == xlib.BadMatch and ev.request_code == xlib.X_ConfigureWindow)):
    #    return 0
    #log.warn('fatal error: request_code=%s error_code=%s' % (ev.request_code, ev.error_code))
    #return xerrorxlib(display, ev)

xerror_ptr = xlib.XErrorHandler(xerror)

def setup_xerror():
    log.info('installing x error handler...')
    xlib.XSetErrorHandler(xerror_ptr)
    xlib.XSync(samuraix.display, False)

