import functools

import gobject

import dbus
import dbus.service
import dbus.mainloop.glib

from samuraix.plugin import Plugin

import logging 
log = logging.getLogger(__name__)


DEFAULT_BUS_NAME = 'org.samuraix'


def sxmethod(interface, **kwargs):
    return dbus.service.method('%s.%s' % (DEFAULT_BUS_NAME, interface), **kwargs)

def sxsignal(interface, **kwargs):
    return dbus.service.signal('%s.%s' % (DEFAULT_BUS_NAME, interface), **kwargs)


class DBusObject(dbus.service.Object):
    def __init__(self, app, conn=None, object_path=None, bus_name=None):
        self.app = app 

        dbus.service.Object.__init__(self, 
                conn=conn, 
                object_path=object_path, 
                bus_name=bus_name,
        )
        
    @sxmethod("DBusInterface", in_signature='s', out_signature='s')
    def hello(self, name):   
        return "hello %s" % name


class SXDBus(Plugin):
    key = 'dbus'

    def __init__(self, app):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        self.session_bus = dbus.SessionBus()
        self.name = dbus.service.BusName(DEFAULT_BUS_NAME, self.session_bus)

        self.objects = {}

        self.register('dbus', functools.partial(DBusObject, app))

    def register(self, name, cls, path=None):
        self.objects[name] = cls(
                conn=self.session_bus, 
                object_path=path or ("/%s" % name),
                bus_name=self.name,
        )


if __name__ == '__main__':
    plugin = SXDBus(None)
    mainloop = gobject.MainLoop()
    mainloop.run()
