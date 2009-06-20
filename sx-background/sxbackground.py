import sys

from samuraix.plugin import Plugin 
from samuraix.screen import Screen
from ooxcb.contrib import cairo
from ooxcb.protocol import xproto
import ooxcb

from yahiko.ui import Window


def yahiko_render(cr, style, width, height):
    win = Window(style=style)
    win.set_render_coords(0, 0, width, height)
    win.render(cr)


def set_root(conn, screen_info, style, func=None):
    root = screen_info.root
    geom = root.get_geometry().reply()
    pixmap = xproto.Pixmap.create(
            conn, 
            root, 
            geom.width, geom.height, 
            screen_info.root_depth
    )

    surface = cairo.cairo_xcb_surface_create(
        conn,
        pixmap,
        screen_info.get_root_visual_type(),
        geom.width, geom.height,
    )
    root.change_attributes(back_pixmap=pixmap)
    cr = cairo.cairo_create(surface)
    if func is None:
        func = yahiko_render
    func(cr, style, geom.width, geom.height)

    root.clear_area(0, 0, geom.width, geom.height)
    conn.flush()


class SXBackground(Plugin):
    def __init__(self, app):
        self.app = app
        app.push_handlers(self)

    def on_load_config(self, config):
        self.config = config

    def on_ready(self, app):
        for screen in self.app.screens:
            self.on_add_screen(app, screen)

    def on_add_screen(self, app, screen):
        style = self.config.get('background.style')
        if style:
            set_root(screen.conn, screen.info, style)


def run():
    conn = ooxcb.connect()

    setup = conn.get_setup()

    import simplejson
    style = simplejson.loads(sys.argv[1])

    try:
        for i in xrange(setup.roots_len):
            screen_info = conn.get_setup().roots[i]
            set_root(conn, screen_info, style)
    finally:
        conn.disconnect()




