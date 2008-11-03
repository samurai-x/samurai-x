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

from pyglet.window.xlib import xlib 
import samuraix
from samuraix.sxctypes import *

import logging
log = logging.getLogger(__name__)

class SimpleWindow(object):
    
    def __init__(self, screen, geom, border_width=0):
        self.screen = screen
        self.geom = geom 
        if border_width is None:
            border_width = 1
        self.border_width = border_width

        wa = xlib.XSetWindowAttributes()
        wa.event_mask = (xlib.SubstructureRedirectMask |
                         xlib.SubstructureNotifyMask |
                         xlib.EnterWindowMask | 
                         xlib.LeaveWindowMask | 
                         xlib.StructureNotifyMask |
                         xlib.ButtonPressMask | 
                         xlib.KeyPressMask | 
                         xlib.ExposureMask)

        wa.override_redirect = 1
        wa.background_pixmap = xlib.ParentRelative

        root = screen.root_window
        default_depth = screen.default_depth
        self.window = xlib.XCreateWindow(samuraix.display, root, 
                            geom.x, geom.y, geom.width, geom.height,
                            self.border_width,
                            default_depth,
                            xlib.CopyFromParent,
                            screen.default_visual,
                            xlib.CWOverrideRedirect | xlib.CWBackPixmap | xlib.CWEventMask,
                            byref(wa))

        xlib.XSelectInput(samuraix.display, self.window, wa.event_mask)

        self.drawable = xlib.XCreatePixmap(samuraix.display, root, 
                            geom.width, geom.height,
                            default_depth)

    def delete(self):
        xlib.XDestroyWindow(samuraix.display, self.window)
        xlib.XFreePixmap(samuraix.display, self.drawable)
    
    def move(self, x, y):
        self.geom.x = x
        self.geom.y = y
        return xlib.XMoveWindow(samuraix.display, self.window, x, y)

    def resize(self, width, height):
        self.geom.width = width
        self.geom.height = height 
        xlib.XFreePixmap(samuraix.display, self.drawable)
        self.drawable = xlib.XCreatePixmap(samuraix.display, self.screen.root_window, 
                width, height, self.screen.default_depth)
        return xlib.XResizeWindow(samuraix.display, self.window, width, height)

    def refresh_drawable(self):
        #log.debug('refresh drawable %s' % self)
        xlib.XCopyArea(samuraix.display, self.drawable, self.window,
                xlib.XDefaultGC(samuraix.display, self.screen.num), 0, 0,
                self.geom.width, self.geom.height, 0, 0)





