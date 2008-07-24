import sys
sys.path.append('..')

from pyglet.window.xlib import xlib

import samuraix
from samuraix import xhelpers
from samuraix.screen import SimpleScreen
from samuraix.drawcontext import DrawContext



def _run():
    display = xhelpers.open_display()
    screen = SimpleScreen(xlib.XDefaultScreen(display))
    root = screen.root_window

    geom = screen.geom

    drawable = xlib.XCreatePixmap(display, root, geom.width, geom.height, 
                                  screen.default_depth)

    context = DrawContext(screen, geom.width, geom.height, drawable)
    context.fill((0.7, 0.3, 0.2))

    xlib.XSetWindowBackgroundPixmap(display, root, drawable)


def run():
    try:
        _run()
    finally:
        xhelpers.close_display()


if __name__ == '__main__':
    run()

