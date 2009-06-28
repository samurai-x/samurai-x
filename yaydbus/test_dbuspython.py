import dbus
import os

bus = dbus.SessionBus()
e = bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus/fob')
print e.A()
