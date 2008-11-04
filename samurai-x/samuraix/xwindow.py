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


class XWindow(object):

    all_windows = {}

    def __init__(self, window):
        self.window = window
        self.all_windows[window] = self

    #def __del__(self):
    #    try:
    #        self.delete()
    #    except KeyError:
    #        pass

    def delete(self):
        del self.all_windows[self.window]
        xlib.XDestroyWindow(samuraix.display, self.window)

    @classmethod 
    def create(cls, screen, geom, border_width, event_mask=None, 
                override_redirect=1, background_pixmap=xlib.ParentRelative):
        wa = xlib.XSetWindowAttributes()
        if event_mask is None:
            wa.event_mask = (
                         xlib.SubstructureRedirectMask |
                         xlib.SubstructureNotifyMask |
                         xlib.EnterWindowMask | 
                         xlib.LeaveWindowMask | 
                         xlib.StructureNotifyMask |
                         xlib.ButtonPressMask | 
                         xlib.KeyPressMask | 
                         xlib.ExposureMask
            )
        else:
            wa.event_mask = event_mask

        wa.override_redirect = override_redirect
        wa.background_pixmap = background_pixmap

        win = xlib.XCreateWindow(samuraix.display, screen.root_window, 
                    geom.x, geom.y, geom.width, geom.height,
                    border_width,
                    screen.default_depth,
                    xlib.CopyFromParent,
                    screen.default_visual,
                    xlib.CWOverrideRedirect | xlib.CWBackPixmap | xlib.CWEventMask,
                    byref(wa))
    
        return cls(win)

    def move(self, x, y):
        xlib.XMoveWindow(samuraix.display, self.window, x, y)

    def resize(self, width, height):
        xlib.XResizeWindow(samuraix.display, self.window, width, height)
        
