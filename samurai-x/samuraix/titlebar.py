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
from samuraix.simplewindow import SimpleWindow
from samuraix.rect import Rect
from samuraix.drawcontext import DrawContext
from samuraix import xhelpers


class TitleBar(object):
    def __init__(self, client):
        self.client = client 

        height = 15
        width = client.geom.width
        self.window = SimpleWindow(client.screen, 
                Rect(0, 0, width, height), 0)

        xlib.XMapWindow(samuraix.display, self.window.window)

        self.update_geometry()

        client.push_handlers(on_title_changed=self.on_client_title_changed)

    def on_client_title_changed(self):
        self.draw()

    def draw(self):
        self.context.fillrect(0, 0, 
                self.window.geom.width, self.window.geom.height, 
                (0.1, 0.1, 0.7))
        
        self.context.text(10, 10, 
                self.client.title, 
                color=(1.0, 1.0, 1.0))

        self.window.refresh_drawable()

    def refresh(self):
        self.window.refresh_drawable()

    def update_geometry(self):
        cg = self.client.geom
        wg = self.window.geom
        bw = self.client.border_width
        self.window.resize(cg.width+(2*bw), wg.height)
        self.window.move(cg.x - bw, cg.y - wg.height)
        self.context = DrawContext(self.client.screen,
                            wg.width, wg.height, self.window.drawable)
        self.draw()

    def remove(self):
        self.window.delete()

    def ban(self):
        xlib.XUnmapWindow(samuraix.display, self.window.window)
        xhelpers.set_window_state(self.window.window, xlib.IconicState)

    def unban(self):
        xlib.XMapWindow(samuraix.display, self.window.window)
        xhelpers.set_window_state(self.window.window, xlib.NormalState)
        self.draw()

    def bring_to_front(self):
        xlib.XRaiseWindow(samuraix.display, self.window.window)

