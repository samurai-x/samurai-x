try:
    from yaydbus.service import Object
    YAYDBUS = True
except ImportError:
    from dbus.service import Object
    YAYDBUS = False
from sxdbus import sxmethod

class ActionsObject(Object):
    def __init__(self, plugin, *args, **kwargs):
        self.plugin = plugin
        Object.__init__(self, *args, **kwargs)

    @sxmethod("ActionsInterface", in_signature='s', out_signature='')
    def action(self, action):
        self.plugin.emit(action, {})
