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

import logging
log = logging.getLogger(__name__)
import sys
import signal
from select import select

import ooxcb

from .screen import Screen
from .pluginsys import PluginLoader

class App(object):
    def __init__(self):
        self.screens = []

    def init(self):
        self.conn = ooxcb.connect()

        self.conn.push_handlers(self)
        self.running = False
        self.plugins = PluginLoader(self)
        self.plugins.setup()

        setup = self.conn.get_setup()

        log.debug("found %d screens" % setup.roots_len)

        for i in range(setup.roots_len):
            scr = Screen(self, i)
            try:
                scr.scan()
            except Exception, e:
                log.exception(e)
            self.screens.append(scr)

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGHUP, self.stop)

    def stop(self, *args):
        log.info('stopping')
        self.running = False

    def run(self):
        self.running = True

        fd = self.conn.get_file_descriptor()

        # process any events that are waiting first 
        while True:
            try:
                ev = self.conn.poll_for_event()
            except Exception, e:
                log.exception(e)
            else:
                if ev is None:
                    break
                try:
                    ev.dispatch()
                except Exception, e:
                    log.exception(e)

        while self.running:
            log.debug('selecting...')
            try:
                select([fd], [], [fd], 1.0)
            except Exception, e:
                # error 4 is when a signal has been caught
                if e.args[0] == 4:
                    pass
                else:
                    log.exception(str((e, type(e), dir(e), e.args)))
                    raise 

            # might as well process all events in the queue...
            while True:
                try:
                    ev = self.conn.poll_for_event()
                except Exception, e:
                    log.exception(e)
                else:
                    if ev is None:
                        break
                    try:
                        ev.dispatch()
                    except Exception, e:
                        log.exception(e)

    def on_property_notify(self, ev):
        log.info('Got a property notify event ... %s' % ''.join(map(chr, ev.atom.get_name().reply().name)))
