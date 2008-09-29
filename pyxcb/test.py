import xcb
import ctypes

#c = xcb.connection.Connection()
#
#cookie = xcb._xcb.xcb_get_property(c._connection, False, 0x36001f4, a._atom, xcb._xcb.XCB_GET_PROPERTY_TYPE_ANY, 0, 200)
#print cookie
#s = xcb._xcb.xcb_get_property_reply(c._connection, cookie, None).contents
#x = ctypes.cast(xcb._xcb.xcb_get_property_value(s), ctypes.c_char_p)
#print ord(x.value[-1])
#print x.value[:xcb._xcb.xcb_get_property_value_length(s)]

c = xcb.connection.Connection()
#a = xcb.cookie.AtomRequest(c, 'WM_NAME').value
screen = c.screens[0]
root = screen.root
#print root.get_property('_NET_ACTIVE_WINDOW')[0].get_property('WM_CLASS')

e = xcb.event.ClientMessageEvent(c)
e.window = root
e.type = c.get_atom_by_name('_NET_CURRENT_DESKTOP')
e.format = 32
e.data = [1, 0]
root.send_event(e)

#print c.wait_for_event()
#w = xcb.window.Window.create(c, screen, 0, 0, 320, 480, attributes={'back_pixel':screen.white_pixel})
#w.map()

#while 1:
#    c.wait_for_event()

#xcb._xcb.xcb_send_event(c, 0, root._xid, 

#root.send_event(e)
#p = xcb.window.Window(c, 0x3a00018)
#atom = c.get_atom_by_name('_NET_ACTIVE_WINDOW')
#print c.xize_property(root, atom, [0x3000260])
#root.set_property('_NET_ACTIVE_WINDOW', [0x3000260])
#root.set_property('_NET_CURRENT_DESKTOP', [1])

c.disconnect()
