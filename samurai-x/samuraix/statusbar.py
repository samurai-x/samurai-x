from pyglet.window.xlib import xlib 
from datetime import datetime

import samuraix
from samuraix.rect import Rect
from samuraix.drawcontext import DrawContext
from samuraix.simplewindow import SimpleWindow
from samuraix.widget import Widget
from samuraix.sxctypes import *

from samuraix import cairo


class StatusBarWidget(object):
    def __init__(self, statusbar):
        self.statusbar = statusbar
        self.dirty = True


class ActiveDesktopWidget(StatusBarWidget):
    def __init__(self, statusbar):
        StatusBarWidget.__init__(self, statusbar)
        self.statusbar.push_handlers(self)

    def on_desktop_change(self):
        self.dirty = True

    def draw(self, context, geom):
        self.context.text(self.options['padding-left'], 10, 
                self.screen.active_desktop.name, 
                color=self.options['text-color'],
                font=self.options['font'],
                font_size=self.options['font-size'],
        )


class StatusBar(Widget):
    def __init__(self, screen, name, **options):
        Widget.__init__(self, screen, name, **options)

        sg = screen.geom

        self.window = SimpleWindow(self.screen, Rect(sg.x, sg.y, sg.width, 15))
        self.update_position()
        self.context = DrawContext(screen, 
                                   self.window.geom.width, self.window.geom.height,
                                   self.window.drawable)

        screen.push_handlers(self)

        

        samuraix.timer.schedule_repeated(self.update_time, 60)
        
    def test_window(self, window):
        return self.window.window == window

    def refresh(self):
        self.window.refresh_drawable()

    def update_time(self):
        self.dirty = True

    def draw(self):
        if not self.dirty: 
            return 

        geom = self.window.geom

        self.context.fillrect(0, 0, 
                geom.width, geom.height, 
                self.options['color'])

        self.context.text(self.options['padding-left'], 10, 
                self.screen.active_desktop.name, 
                color=self.options['text-color'],
                font=self.options['font'],
                font_size=self.options['font-size'],
        )

        if self.options['clock-format']:
            self.context.text(geom.width-self.options['padding-right'], 10,
                datetime.now().strftime(self.options['clock-format']),
                color=(1.0, 1.0, 1.0),
                align="right",
                font=self.options['font'],
                font_size=self.options['font-size'],
            )

        #self.context.text(self.window.geom.width - 100, 10, "samurai-x 0.1")
        #self.context.svg('/usr/share/icons/gnome/scalable/status/audio-volume-muted.svg', 
        #    width=15, height=15, x=self.window.geom.width - 20)

        self.window.refresh_drawable()

        self.dirty = False

    def update_position(self):
        xlib.XMapRaised(samuraix.display, self.window.window)

    def on_desktop_change(self):
        self.dirty = True

