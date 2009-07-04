import sys

from yaydbus.bus import SessionBus
from yaydbus.dbus_types import Array

bus = SessionBus()

obj = bus.get_object('/org/yahiko/status_bar/'+sys.argv[1], 'org.yahiko.status_bar')
proxy = obj.get_bound('org.yahiko.status_bar')

proxy.set_text(sys.argv[2])
