# Copyright (c) 2008, samurai-x.org
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the samurai-x.org nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SAMURAI-X.ORG ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL SAMURAI-X.ORG  BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import os

import pyglet
pyglet.options['shadow_window'] = False

from pyglet.window.xlib import cursorfont

import samuraix
from samuraix import xhelpers
from samuraix import userfuncs
from samuraix.procutil import set_process_name
from samuraix.timer import Timer

import logging
log = logging.getLogger(__name__)


def init_atoms():
    log.debug('creating atoms instance...')
    from samuraix.atoms import Atoms
    samuraix.atoms = Atoms()


def init_cursors():
    log.debug('creating cursors instance...')
    from samuraix.cursors import Cursors
    samuraix.cursors = Cursors()
    samuraix.cursors['normal'] = samuraix.cursors[cursorfont.XC_left_ptr]
    samuraix.cursors['resize'] = samuraix.cursors[cursorfont.XC_sizing]
    samuraix.cursors['move'] = samuraix.cursors[cursorfont.XC_fleur]


def init_timer():
    log.debug('creating timer...')
    from samuraix.timer import Timer
    samuraix.timer = Timer()


def configure_logging(file_level=logging.DEBUG, console_level=logging.INFO):
    #logging.basicConfig(level=logging.DEBUG,
    #            format='%(asctime)s %(name)s %(levelname)s %(message)s')

    from samuraix.logformatter import FDFormatter

    console = logging.StreamHandler()
    console.setLevel(console_level)
    # set this to True for color console output
    if True:
        formatter_class = FDFormatter
    else:
        formatter_class = logging.Formatter
    formatter = formatter_class('[%(asctime)s %(levelname)s %(name)s] %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logfile = 'lastrun.log'

    log.info('logging everything to %s' % logfile)

    lastlog = logging.FileHandler(logfile, 'w')
    lastlog.setLevel(file_level)
    formatter = logging.Formatter('[%(asctime)s %(levelname)s %(name)s %(lineno)d] %(message)s')
    lastlog.setFormatter(formatter)
    logging.getLogger('').addHandler(lastlog)

    logging.root.setLevel(logging.DEBUG)


def load_config(config=None):
    log.info('loading config...')
    if config is None:
        from samuraix.defaultconfig import config

    if callable(config):
        config = config()
    samuraix.config = config


def load_user_config(configfile=None):
    if configfile is None:
        configfile = '~/.samuraix'
    configfile = os.path.normpath(os.path.expanduser(configfile))
    log.info('reading config from %s...' % configfile)
    locals = {}
    try:
        execfile(configfile, {}, locals)
    except IOError, e:
        log.warn('failed reading config file: %s' % e)
        return None
    return locals['config']


def parse_options(args=None):
    log.debug('parsing options...')

    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="print debug messages to stdout")
    parser.add_option('-c', "--config",
                      dest='configfile', default=None,
                      help="config file to use")
    parser.add_option('', '--dumpconfig', dest='dumpconfig', default=False,
                      help="dump the default config to stdout and quit")

    return parser.parse_args(args=args)
    

def handle_options(options, args):
    log.debug('handling options... %s %s' % (options, args))
    if options.debug:
        handler = logging.getLogger('').handlers[0]
        handler.setLevel(logging.DEBUG)

    #if options.dumpconfig:

def run_app():
    log.info('... and with (almost) god like speed ...')
    try:
        samuraix.app.run()
    except Exception, e:
        log.exception("exception in main loop!")
        import traceback
        log.warn(traceback.format_exc())
    finally:
        xhelpers.close_display()


def run(app_func=None, config=None, args=None):
    configure_logging()

    options, args = parse_options(args)
    if options or args: 
        handle_options(options, args)    

    if config is None:
        config = load_user_config(options.configfile)
    load_config(config=config)

    set_process_name('samurai-x')

    xhelpers.open_display()
    xhelpers.check_for_other_wm()
    xhelpers.setup_xerror()

    init_atoms()
    xhelpers.get_numlock_mask()
    init_cursors()
    init_timer()

    if app_func is None:
        from samuraix.appl import App
        app_func = App

    log.info('creating app instance...')
    samuraix.app = app_func()
    samuraix.app.init()
    run_app()
    log.info('done')


if __name__ == '__main__':    
    run()


