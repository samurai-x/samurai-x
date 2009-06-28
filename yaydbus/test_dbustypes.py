from yaydbus.dbus_types import *

print marshal_bunch(
        ('Hallo!', Array(Struct(int, UInt32))([(44, 55), (66, 77)]),)
        )
