import logging
log = logging.getLogger(__name__)

import gobject

from samuraix.plugin import Plugin

class SXGObject(Plugin):
    def __init__(self, app):
        self.app = app
        self.app.stop = lambda *args: self.mainloop.quit()
        app.run = self.run
        # exchange the handler
        fd = app.conn.get_file_descriptor()
        app.remove_fd_handler('read', fd)
        app.add_fd_handler('read', fd, self.do_xcb_events)

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
                gobject.io_add_watch(fd, cond, app.fds[typ][fd])

        mainloop.run()

        app.conn.disconnect()

    def do_xcb_events(self, source, cb_condition):
        self.app.do_xcb_events()
        return True

