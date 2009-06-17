#!/usr/bin/env python
"""
    simple script for building a samurai-x development environment.

    It uses setuptools egg links to create a development environment,
    so you can modify the existing packages and won't have to re-install
    everything after an edit.
    
    See http://peak.telecommunity.com/DevCenter/setuptools#development-mode

    USAGE:
        
        ./create-environment.py ./dev/

        where `./dev/` is the path to install the console scripts and
        setuptools links to.

        This script has to be called from the git repository root.

        To run sx-wm, just cd into your development environment, create
        a new shell with an adjusted environment with `./setenv` and
        run `./sx-wm`.
"""

from __future__ import with_statement

import sys
import os
import stat
from glob import iglob
from subprocess import Popen

PYTHON = sys.executable

def has_colors(stream):
    """ from http://code.activestate.com/recipes/475186/ - thanks """
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs

    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False

HAS_COLORS = has_colors(sys.stdout)
MESSAGE_COLOR_TEMPLATE = '\033[0;32m%s\033[0m'

def message(msg):
    if HAS_COLORS:
        print MESSAGE_COLOR_TEMPLATE % msg
    else:
        print msg

def develop_package(path, dev):
    message('running `python setup.py develop` for %s ...' % path)
    code = Popen([PYTHON, 'setup.py', 'develop', '-d', dev], 
            env={'PYTHONPATH': dev}, 
            cwd=path
            ).wait()
    if code != 0:
        message('ERROR: something went wrong!')
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print __doc__
        return 1
    else:
        dev_path = os.path.abspath(sys.argv[1])
        if not os.path.isdir(dev_path):
            os.makedirs(dev_path)

        for package_name in ('ooxcb', 'samurai-x2', 'yahiko'):
            develop_package(os.path.abspath(package_name), dev_path)

        setenv_path = os.path.join(dev_path, 'setenv')
        with open(setenv_path, 'w') as setenv:
            setenv.write('#!/bin/sh\n')
            setenv.write('export PYTHONPATH=$PYTHONPATH:%s\n' % dev_path)

        # should *we* make it executable?
        message('Making it executable ...')
        os.chmod(setenv_path, stat.S_IRWXU)

        # install all plugins (packages in directories named `sx-*`)
        message('Installing plugins ...')
        plugins_dir = os.path.expanduser('~/.samuraix/plugins')
        if not os.path.isdir(plugins_dir):
            os.makedirs(plugins_dir)
        for plugin_dir in iglob('./sx-*'):
            if plugin_dir != './sx-allplugins':
                develop_package(plugin_dir, plugins_dir)
        message('Done!')

if __name__ == '__main__':
    sys.exit(main())

