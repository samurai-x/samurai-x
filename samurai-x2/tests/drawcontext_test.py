import samuraix.xcb as xcb
import samuraix.drawcontext

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

context = samuraix.drawcontext.DrawContext(screen, 480, 480, w)
@w.event
def on_expose(evt):
    context.text(100, 100, '*test* Don\'t panic! *test*', (0, 0, 0))
#    context.svg('../gfx/samuraix.svg', width=480)

while 1:
    c.wait_for_event_dispatch()

c.disconnect()
