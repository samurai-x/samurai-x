import gobject

import dbus
import dbus.service
import dbus.mainloop.glib

from samuraix.plugin import Plugin

import logging 
log = logging.getLogger(__name__)


class ControlObject(dbus.service.Object):
    def __init__(self, app, conn=None, object_path=None, bus_name=None):
        self.app = app 

        dbus.service.Object.__init__(self, 
                conn=conn, 
                object_path=object_path, 
                bus_name=bus_name,
        )
        
    @dbus.service.method("org.samuraix.ControlInterface", 
                         in_signature='s', out_signature='')
    def action(self, action):   
        self.app.plugins['actions'].emit(action, {})


class SXDBus(Plugin):
    key = 'dbus'

    def __init__(self, app):
        log.info('DBUS ----------------------------')

        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        self.session_bus = dbus.SessionBus()
        self.name = dbus.service.BusName("org.samuraix.ControlService", self.session_bus)
        self.object = ControlObject(app, 
                conn=self.session_bus, 
                object_path='/ControlObject',
        )


if __name__ == '__main__':
    plugin = SXDBus(None)
    mainloop = gobject.MainLoop()
    mainloop.run()
