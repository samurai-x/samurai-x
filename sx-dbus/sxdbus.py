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
    sx-dbus is a plugin that enables dbus inside samurai-x.

    .. warning::
        
        :ref:`sx-actions` exposes a method that is able to execute
        arbitrary actions, including the "spawn" action. That means you
        can execute arbitrary commands in the context of the `sx-wm`
        process over dbus. Be careful.

    Dependencies
    ------------

    sx-dbus depends on :ref:`sx-gobject`.

"""

import functools

import gobject

try:
    from yaydbus.bus import SessionBus
    from yaydbus import service
    YAYDBUS = True
except Exception, e:
    print e
    import dbus
    from dbus import service
    import dbus.mainloop.glib
    YAYDBUS = False

from samuraix.plugin import Plugin

import logging 
log = logging.getLogger(__name__)


DEFAULT_BUS_NAME = 'org.samuraix'


def sxmethod(interface, **kwargs):
    """ 
        decorator like dbus.service.method() but automatically adds in the sx bus name
    """
    return service.method('%s.%s' % (DEFAULT_BUS_NAME, interface), **kwargs)

def sxsignal(interface, **kwargs):
    """ 
        decorator like dbus.service.signal() but automatically adds in the sx bus name
    """
    return service.signal('%s.%s' % (DEFAULT_BUS_NAME, interface), **kwargs)


class DBusObject(service.Object):
    def __init__(self, app, *args, **kwargs):
        self.app = app 

        service.Object.__init__(self, *args, **kwargs)
        
    @sxmethod("DBusInterface", in_signature='s', out_signature='s')
    def hello(self, name):   
        return "hello %s" % name


class SXDBus(Plugin):
    key = 'dbus'

    def __init__(self, app):
        self.objects = {}
        if YAYDBUS:
            self.session_bus = SessionBus()
            app.add_fd_handler('read', self.session_bus, self.process_dbus)
        else:
            dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

            self.session_bus = dbus.SessionBus()
            self.name = service.BusName(DEFAULT_BUS_NAME, self.session_bus)

        if YAYDBUS:
            self.session_bus.request_name(DEFAULT_BUS_NAME)
            self.session_bus.request_name(DEFAULT_BUS_NAME+'.DBusService')
        self.register('dbus', functools.partial(DBusObject, app))

    def process_dbus(self):
        self.session_bus.receive_one()

    def register(self, name, cls, path=None):
        """ register a new dbus object """
        log.info('registering %s: %s', name, cls)

        if YAYDBUS:
            self.objects[name] = self.session_bus.make_object(path or ("/%s" % name), cls)
        else:
            self.objects[name] = cls(
                    conn=self.session_bus, 
                    object_path=path or ("/%s" % name),
                    bus_name=self.name,
            )


if __name__ == '__main__':
    plugin = SXDBus(None)
    if YAYDBUS:
        from yaydbus.mainloop import Mainloop
        m = Mainloop((plugin.session_bus,))
        m.run()
    else:
        mainloop = gobject.MainLoop()
        mainloop.run()
