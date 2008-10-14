'''
Input monitoring for key events and mouse (press/release) events. 
Mouse movements are not captured.
'''
import sys
import time

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
old_time = int(time.time())
def check_timer():
    cur_time = int(time.time())
    if (cur_time - old_time) > 10:
        print '10 seconds exceeded, exiting...'
        return False
    return True

@w.event
def on_expose(evt):
    print 'on_expose %s'%(evt)

def on_button_event(evt):
    print '%(event)s, serial %(type)s, window 0x%(window)X,'% \
        ({'event':evt, 'type':evt.event_type, 'window':evt.event._xid})
    print 'root 0x%(root)X, time %(time)d, (%(win_x)d,%(win_y)d), root:(%(root_x)d,%(root_y)d),'% \
        ({'root':evt.root._xid,'time':evt._event.time,'win_x':evt.event_x, 'win_y':evt.event_y, 'root_x':evt.root_x, 'root_y':evt.root_y})
    print 'state 0x%(state)X, button %(button)d, '% \
        ({'state':evt.state, 'button':evt.button})

def on_expose_event(evt):
    print '%(event)s, serial %(type)s, window 0x%(window)X,'% \
        ({'event':evt, 'type':evt.event_type, 'window':evt.event._xid})

def on_key_event(evt):
    from samuraix.xcb.keysymbols import KeySymbols
    from samuraix.xcb.keylookup import  keysym_to_str
    keysymbols = KeySymbols(c)
    keysym = keysymbols.get_keysym(evt.keycode)
    keystring = keysym_to_str(keysym)
    print '%(event)s, serial %(type)s, window 0x%(window)X,'% \
        ({'event':evt, 'type':evt.event_type, 'window':evt.event._xid})
    print 'root 0x%(root)X, time %(time)d, (%(win_x)d,%(win_y)d), root:(%(root_x)d,%(root_y)d),'% \
        ({'root':evt.root._xid,'time':evt._event.time,'win_x':evt.event_x, 'win_y':evt.event_y, 'root_x':evt.root_x, 'root_y':evt.root_y})
    print 'state 0x%(state)X, keycode %(keycode)d (keysym 0x%(keysymbol)X, "%(keystring)s")), '% \
        ({'state':evt.state, 'keycode':evt.keycode, 'keysymbol':keysym, 'keystring':keystring})


event_map = {xcb.event.KeyPressEvent.event_type: on_key_event,             \
            xcb.event.KeyReleaseEvent.event_type: on_key_event,            \
            #xcb.event.ExposeEvent.event_type: on_expose_event,             \
            xcb.event.ButtonPressEvent.event_type: on_button_event,        \
            xcb.event.ButtonReleaseEvent.event_type: on_button_event,      \
            }
while check_timer():
    evt = c.poll_for_event()
    if evt:
        if evt.event_type in event_map:
            old_time = int(time.time())
            event_map[evt.event_type](evt)
            print ''
