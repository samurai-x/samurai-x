from pyglet.window.xlib import xlib 

import samuraix
from samuraix.rect import Rect
from samuraix.drawcontext import DrawContext
from samuraix.simple_window import SimpleWindow
from samuraix.widget import Widget


class Statusbar(Widget):
    def __init__(self, screen):
        Widget.__init__(self, screen)

        self.window = SimpleWindow(self.screen, 
                                   Rect(screen.geom.x, screen.geom.y, 
                                        screen.geom.width, 15))
        self.update_position()
        self.context = DrawContext(screen, 
                                   self.window.geom.width, self.window.geom.height,
                                   self.window.drawable)

        screen.push_handlers(self)

    def test_window(self, window):
        return self.window.window == window

    def refresh(self):
        self.window.refresh_drawable()

    def draw(self):
        if not self.dirty: 
            return 

        self.context.fillrect(0, 0, self.window.geom.width, self.window.geom.height, 
                (0.7, 0.0, 0.0))

        self.context.text(10, 10, self.screen.active_desktop.name)
        self.context.text(self.window.geom.width - 100, 10, "samurai-x 0.1")

        self.window.refresh_drawable()

        self.dirty = False

    def update_position(self):
        xlib.XMapRaised(samuraix.display, self.window.window)

    def on_desktop_change(self):
        self.dirty = True



