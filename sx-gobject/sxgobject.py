# Copyright (c) 2008-2009, samurai-x.org
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

"""
    sx-gobject is a plugin that replaces the default samurai-x loop with a gobject based loop.

"""

import logging
log = logging.getLogger(__name__)

import gobject

from samuraix.plugin import Plugin

def _make_handler(fn):
    def h(source, cb_condition):
        ret = fn()
        if ret is None:
            ret = True
        return ret
    return h

class SXGObject(Plugin):
    key = 'gobject'

    def __init__(self, app):
        self.app = app
        self.app.stop = lambda *args: self.mainloop.quit()
        app.run = self.run

    def run(self):
        app = self.app
        app.running = True

        # process any events that are waiting first
        while True:
            try:
                ev = app.conn.poll_for_event()
            except Exception, e:
                log.exception(e)
            else:
                if ev is None:
                    break
                try:
                    ev.dispatch()
                except Exception, e:
                    log.exception(e)

        #dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        #session_bus = dbus.SessionBus()
        #name = dbus.service.BusName("com.example.SampleService", session_bus)
        #object = SomeObject(session_bus, '/SomeObject')

        mainloop = self.mainloop = gobject.MainLoop()
        for typ, cond in (('read', gobject.IO_IN), ('write', gobject.IO_OUT), ('error', gobject.IO_ERR)):
            for fd in app.fds[typ].keys():
                gobject.io_add_watch(fd, cond, _make_handler(app.fds[typ][fd]))
        mainloop.run()

        app.conn.disconnect()

