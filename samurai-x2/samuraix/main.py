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
import traceback
import logging
import pkg_resources
from optparse import OptionParser

SXWM_USAGE = '''sx-wm [options] '''

class SamuraiLogger(logging.Logger):
    def exception(self, exc):
        """
            Improved exception logger.
            
            :param exc: An Exception instance
        """
        type_, value, tb = sys.exc_info()
        formatted = '\n'.join(traceback.format_exception(type_, value, tb))
        self._log(logging.ERROR, formatted, (), {})

logging.setLoggerClass(SamuraiLogger)

log = logging.getLogger(__name__)

import samuraix

from .logformatter import FDFormatter


def configure_logging(file_level=logging.DEBUG, console_level=logging.DEBUG):
    '''Set up the logging for the client.

    @param file_level: level of logging for files, defaults to logging.DEBUG
    @param console_level: level of logging for the console, defaults to DEBUG
    '''

    console = logging.StreamHandler()
    console.setLevel(console_level)
    formatter_class = FDFormatter
    formatter = formatter_class('[%(asctime)s %(levelname)s %(name)s] %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.root.setLevel(logging.DEBUG)
    logfile = 'lastrun.log'
    lastlog = logging.FileHandler(logfile, 'w')
    lastlog.setLevel(file_level)
    formatter = logging.Formatter('[%(asctime)s %(levelname)s %(name)s %(lineno)d] %(message)s')
    lastlog.setFormatter(formatter)
    logging.getLogger('').addHandler(lastlog)

    log.info('logging everything to %s' % logfile)

def load_config(config=None):
    if config is None:
        from samuraix.defaultconfig import config
    if callable(config):
        config = config()
    samuraix.config = config

def load_user_config(configfile):
    configfile = os.path.normpath(os.path.expanduser(configfile))
    log.info('reading config from %s...' % configfile)
    locals = {}
    try:
        execfile(configfile, {}, locals)
    except IOError, e:
        log.warn('failed reading config file: %s - using defaultconfig' % e)
        return None
    return locals['config']

def parse_options():
    parser = OptionParser(SXWM_USAGE)
    parser.add_option('-c', '--config', dest='configfile', 
            help='use samuraix configuration from FILE (default: %default)', metavar='FILE',
            default='~/.samuraix/config')

    parser.add_option('', '--default-config', dest='print_default_config', 
            help='print the default configuration to stdout',
            action='store_true',
            default=False)

    options, args = parser.parse_args()
    return options

def run(app_func=None):
    options = parse_options()
    if options.print_default_config: # just print samuraix.defaultconfig and quit.
        print pkg_resources.resource_string('samuraix', 'defaultconfig.py')
        return

    configure_logging()

    cfg = load_user_config(options.configfile)
    load_config(cfg)

    if app_func is None:
        from samuraix.appl import App
        app_func = App

    samuraix.app = app = app_func()

    try:
        app.init()
        app.run()
    except Exception:
        import traceback
        log.error(traceback.format_exc())


