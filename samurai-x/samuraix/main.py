import pyglet
pyglet.options['shadow_window'] = False

from pyglet.window.xlib import xlib 
from pyglet.window.xlib import cursorfont

import samuraix
from samuraix.sxctypes import *
from samuraix import xhelpers

import logging
log = logging.getLogger(__name__)


def init_atoms():
    log.info('creating atoms instance...')
    from samuraix.atoms import Atoms
    samuraix.atoms = Atoms()


def init_cursors():
    log.info('creating cursors instance...')
    from samuraix.cursors import Cursors
    samuraix.cursors = Cursors()
    samuraix.cursors['normal'] = samuraix.cursors[cursorfont.XC_left_ptr]
    samuraix.cursors['resize'] = samuraix.cursors[cursorfont.XC_sizing]
    samuraix.cursors['move'] = samuraix.cursors[cursorfont.XC_fleur]

def configure_logging():
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)s %(levelname)s %(message)s')


def load_config():
    log.info('loading config...')
    samuraix.config = {
        'screens': {
            0: {
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

    xhelpers.open_display()
    xhelpers.check_for_other_wm()
    #xhelpers.setup_xerror()

    load_config()

    init_atoms()
    xhelpers.get_numlock_mask()
    init_cursors()

    log.info('creating app instance...')
    samuraix.app = app()
    samuraix.app.init()
    log.info('let battle commence...')
    try:
        samuraix.app.run()
    finally:
        xhelpers.close_display()
    log.info('done')


if __name__ == '__main__':    
    from samuraix.appl import App
    run(App)


