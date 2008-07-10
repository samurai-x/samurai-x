
import os

import pyglet
pyglet.options['shadow_window'] = False

from pyglet.window.xlib import xlib 
from pyglet.window.xlib import cursorfont

import samuraix
from samuraix.sxctypes import *
from samuraix import keydefs

import logging
log = logging.getLogger(__name__)


def open_display(displayname=None):
    if displayname is None:
        displayname = os.environ.get('DISPLAY', ':0')
    samuraix.displayname = displayname

    log.debug("connecting to %s" % displayname)
    samuraix.display = xlib.XOpenDisplay(None)
    if not samuraix.display:
        # not sure what this exception should be really...
        raise RuntimeError("Cant connect to xserver")

    xlib.XSynchronize(samuraix.display, True)


def get_numlock_mask():
    modmap = xlib.XGetModifierMapping(samuraix.display)[0]
    keycode = xlib.XKeysymToKeycode(samuraix.display, keydefs.XK_Num_Lock)

    mask = 0 

    for i in range(8):
        for j in range(0, modmap.max_keypermod):
            if modmap.modifiermap[i * modmap.max_keypermod + j] == keycode:
                mask = 1 << i

    xlib.XFreeModifiermap(modmap)

    xlib.NumLockMask = mask


def init_atoms():
    from samuraix.atoms import Atoms
    samuraix.atoms = Atoms()

def init_cursors():
    from samuraix.cursors import Cursors
    samuraix.cursors = Cursors()
    samuraix.cursors['normal'] = samuraix.cursors[cursorfont.XC_left_ptr]
    samuraix.cursors['resize'] = samuraix.cursors[cursorfont.XC_sizing]
    samuraix.cursors['move'] = samuraix.cursors[cursorfont.XC_fleur]

def configure_logging():
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)s %(levelname)s %(message)s')


def load_config():
    samuraix.config = {
        'screens': {
            '0': {
                'virtual_desktops': [
                    {'name': 'one'},
                    {'name': 'two'},
                    {'name': 'three'},        
                ],
            },
        },
    }


def run(app):
    configure_logging()

    load_config()

    open_display()
    init_atoms()
    get_numlock_mask()
    init_cursors()

    app.register_x_event_handlers()
    samuraix.app = app()
    samuraix.app.run()

if __name__ == '__main__':    
    from samuraix.app import App
    run(App)


