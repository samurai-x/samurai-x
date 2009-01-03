# Copyright (c) 2008, samurai-x.org
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the samurai-x.org nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SAMURAI-X.ORG ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL SAMURAI-X.ORG  BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''
Input monitoring for key events and mouse (press/release) events. 

'''
import sys
import time

import pyxcb as xcb

def run():
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
    w.set_property('WM_NAME', ['samurai-x events',], 8, 'STRING')
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

    def on_enter_event(evt):
        '''
        EnterNotify event, serial 28, synthetic NO, window 0x2800001,
        root 0x1a6, subw 0x0, time 40773788, (14,811), root:(735,831),
        mode NotifyNormal, detail NotifyNonlinear, same_screen YES,
        focus YES, state 0
        '''
        print '%(event)s, serial %(type)s, window 0x%(window)X,'% \
            ({'event':evt, 'type':evt.event_type, 'window':evt.event._xid})
        print 'root 0x%(root)X, time %(time)d, (%(win_x)d,%(win_y)d), root:(%(root_x)d,%(root_y)d),'% \
            ({'root':evt.root._xid,'time':evt._event.time,'win_x':evt.event_x, 'win_y':evt.event_y, 'root_x':evt.root_x, 'root_y':evt.root_y})

    def on_button_event(evt):
        print '%(event)s, serial %(type)s, window 0x%(window)X,'% \
            ({'event':evt, 'type':evt.event_type, 'window':evt.event._xid})
        print 'root 0x%(root)X, time %(time)d, (%(win_x)d,%(win_y)d), root:(%(root_x)d,%(root_y)d),'% \
            ({'root':evt.root._xid,'time':evt._event.time,'win_x':evt.event_x, 'win_y':evt.event_y, 'root_x':evt.root_x, 'root_y':evt.root_y})
        print 'state 0x%(state)X, button %(button)d, '% \
            ({'state':evt.state, 'button':evt.button})

    def on_expose_event(evt):
        print '%(event)s, serial %(type)s, window 0x%(window)X,'% \
            ({'event':evt, 'type':evt.event_type, 'window':evt.drawable._xid})
        print '(%(x)s,%(y)s), width %(width)s, height %(height)s, count 0'% \
            ({'x':evt.x,'y':evt.y, 'width':evt.width, 'height':evt.height})

    def on_key_event(evt):
        from pyxcb.keysymbols import KeySymbols
        from pyxcb.keylookup import  keysym_to_str
        keysymbols = KeySymbols(c)
        keysym = keysymbols.get_keysym(evt.keycode)
        keystring = keysym_to_str(keysym)
        print '%(event)s, serial %(type)s, window 0x%(window)X,'% \
            ({'event':evt, 'type':evt.event_type, 'window':evt.event._xid})
        print 'root 0x%(root)X, time %(time)d, (%(win_x)d,%(win_y)d), root:(%(root_x)d,%(root_y)d),'% \
            ({'root':evt.root._xid,'time':evt._event.time,'win_x':evt.event_x, 'win_y':evt.event_y, 'root_x':evt.root_x, 'root_y':evt.root_y})
        print 'state 0x%(state)X, keycode %(keycode)d (keysym 0x%(keysymbol)X, "%(keystring)s")), '% \
            ({'state':evt.state, 'keycode':evt.keycode, 'keysymbol':keysym, 'keystring':keystring})

    def on_visi_event(evt):
        print '%(event)s, serial %(type)s, window 0x%(window)X,'% \
            ({'event':evt, 'type':evt.event_type, 'window':evt.window._xid})
        # TODO state translation
        print 'state (%s)'%evt.visibility_notify_states[evt.state]

    def on_motion_event(evt):
        #TODO: need to finish this, need more info...
        print '%(event)s, serial %(type)s, window 0x%(window)X,'% \
            ({'event':evt, 'type':evt.event_type, 'window':evt.event._xid})
        print 'root 0x%(root)X, time %(time)d, (%(win_x)d,%(win_y)d), root:(%(root_x)d,%(root_y)d),'% \
            ({'root':evt.root._xid,'time':evt._event.time,'win_x':evt.event_x, 'win_y':evt.event_y, 'root_x':evt.root_x, 'root_y':evt.root_y})
        print 'state 0x%(state)X, '% \
            ({'state':evt.state, })


    event_map = {xcb.event.KeyPressEvent.event_type: on_key_event,             \
                xcb.event.KeyReleaseEvent.event_type: on_key_event,            \
                xcb.event.ExposeEvent.event_type: on_expose_event,             \
                xcb.event.ButtonPressEvent.event_type: on_button_event,        \
                xcb.event.ButtonReleaseEvent.event_type: on_button_event,      \
                xcb.event.EnterNotifyEvent.event_type: on_enter_event,         \
                xcb.event.VisibilityNotifyEvent.event_type: on_visi_event,     \
                xcb.event.MotionNotifyEvent.event_type: on_motion_event,       \
                }
    while check_timer():
        evt = c.poll_for_event()
        if evt:
            if evt.event_type in event_map:
                old_time = int(time.time())
                event_map[evt.event_type](evt)
                print ''
    w.destroy()
    sys.exit(0)


if __name__ == '__main__':
    run()
