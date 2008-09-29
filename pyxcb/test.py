import xcb

c = xcb.connection.Connection()
screen = c.screens[0]
root = screen.root

w = xcb.window.Window.create(c, screen, 0, 0, 320, 480, 10, attributes={'back_pixel':screen.white_pixel,
                                                                        'event_mask': set([
                                                                                       xcb.event.ExposureEvent,
                                                                                       xcb.event.KeyReleaseEvent,
                                                                                       xcb.event.KeyPressEvent
                                                                                       ])
                                                                        })
w.map()
c.flush()

while 1:
    e = c.wait_for_event()
    print 'Received event:', e

c.disconnect()
