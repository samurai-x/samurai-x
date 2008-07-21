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



