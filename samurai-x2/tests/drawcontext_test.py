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
    c.flush()
#    context.svg('../gfx/samuraix.svg', width=480)

while 1:
    c.wait_for_event_dispatch()

c.disconnect()
