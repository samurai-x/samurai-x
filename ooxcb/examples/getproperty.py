import sys
sys.path.append('..')

import ooxcb
from ooxcb import xproto

conn = ooxcb.connect()

screen = conn.setup.roots[conn.pref_screen]
active = screen.get_active_window()
reply = active.get_property('_NET_WM_NAME', 'UTF8_STRING').reply()
if reply.exists:
    print 'The property exists.'
else:
    print 'The property does not exist.'
print 'Value: %s' % repr(reply.value.to_utf8())

