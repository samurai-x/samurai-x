from ctypes import CDLL

import logging
log = logging.getLogger(__name__)

def set_process_name(name):
    log.debug('setting process name to %s' % name)
    libc = CDLL('libc.so.6')
    libc.prctl(15, name, 0, 0, 0)


