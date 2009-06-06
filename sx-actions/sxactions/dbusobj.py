import dbus 
from sxdbus import sxmethod

class ActionsObject(dbus.service.Object):
    def __init__(self, plugin, **kwargs):
        self.plugin = plugin
        dbus.service.Object.__init__(self, **kwargs)

    @sxmethod("ActionsInterface", in_signature='s', out_signature='')
    def action(self, action):
        self.plugin.emit(action, {})
