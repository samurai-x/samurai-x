import samuraix.xcb as xcb

c = xcb.connection.Connection()
screen = c.screens[0]
root = screen.root

w = xcb.window.Window.create(c, screen, 0, 0, 480, 480, 10, attributes={'back_pixel':screen.white_pixel,
                                                                        'event_mask': set([
                                                                                       xcb.event.ExposeEvent,
                                                                                       xcb.event.KeyPressEvent,
                                                                                       xcb.event.KeyReleaseEvent,
                                                                                       xcb.event.ButtonPressEvent,
                                                                                       xcb.event.ButtonReleaseEvent,
                                                                                       xcb.event.EnterNotifyEvent,
                                                                                       xcb.event.LeaveNotifyEvent,
                                                                                       xcb.event.MotionNotifyEvent,
                                                                                       xcb.event.KeymapNotifyEvent,
                                                                                       xcb.event.VisibilityNotifyEvent
                                                                                       ])
                                                                        })
w.map()

gc = xcb.graphics.GraphicsContext.create(c, w, {'foreground':screen.black_pixel})

@w.event
def on_expose(evt):
    gc.poly_line(w, [(0, 450), (320, 450)])
    gc.poly_arc(w, [xcb.graphics.Arc(20, 20, 100, 20, 0, 90 << 6)])
    gc.poly_segment(w, [((200, 200), (100, 100)), ((250, 250), (200, 400))])
    gc.poly_rectangle(w, [xcb.graphics.Rectangle(0, 0, 20, 20)], fill=True)
    gc.fill_poly(w, [(300, 300), (340, 340), (0, 480), (300, 300)], xcb.graphics.POLY_SHAPE_NONCONVEX)

while 1:
    c.wait_for_event_dispatch()

c.disconnect()
