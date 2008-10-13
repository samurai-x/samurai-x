'''
Input monitoring for key events and mouse (press/release) events. 
Mouse movements are not captured.
'''
import samuraix.xcb as xcb

# get connection to the xcb
c = xcb.connection.Connection()
screen = c.screens[0]
root = screen.root

w = xcb.window.Window.create(c, screen, 10, 10, 200, 200, 10,        \
                    attributes={'back_pixel':screen.white_pixel,     \
                                'event_mask': set([                  \
                                    xcb.event.ExposeEvent,           \
                                    xcb.event.KeyPressEvent,         \
                                    xcb.event.KeyReleaseEvent,       \
                                    xcb.event.ButtonPressEvent,      \
                                    xcb.event.ButtonReleaseEvent,    \
                                    xcb.event.EnterNotifyEvent,      \
                                    xcb.event.KeymapNotifyEvent,     \
                                    xcb.event.VisibilityNotifyEvent, \
                                    xcb.event.MotionNotifyEvent,     \
                                    ])
                                })
w.map()
gc = xcb.graphics.GraphicsContext.create(c, w, {'foreground':screen.black_pixel})

@w.event
def on_expose(evt):
    print 'on_expose %s'%(evt)

def on_key_event(evt):
    print '%(event)s, serial %(keycode)s, window %(window)s' %({'event':evt, 'keycode':evt.keycode, 'window':evt.event._xid})

event_map = {xcb.event.KeyPressEvent.event_type: on_key_event, \
            xcb.event.KeyReleaseEvent.event_type: on_key_event, \
            }

while 1:
    evt = c.wait_for_event()
    if evt.event_type in event_map:
        event_map[evt.event_type](evt)
