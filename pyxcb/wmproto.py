import xcb

c = xcb.connection.Connection()
screen = c.screens[0]
root = screen.root

root.attributes = {'event_mask': (xcb.event.MapRequestEvent, xcb.event.SubstructureRedirectEvent, xcb.event.SubstructureNotifyEvent,
    xcb.event.StructureNotifyEvent)}

while 1:
    e = c.poll_for_event()
    if e:
        print 'Received event:', e

c.disconnect()
