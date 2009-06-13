import sys

from samuraix.plugin import Plugin 
from samuraix.screen import Screen
from ooxcb.contrib import cairo
from ooxcb import xproto
import ooxcb


def set_root(conn, screen_info, color):
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
    cairo.cairo_rectangle(cr, 0, 0, geom.width, geom.height)
    cairo.cairo_set_source_rgb(cr, *color)
    cairo.cairo_fill(cr)
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
        set_root(screen.conn, screen.info, (1.0, 0.0, 0.0))


class FakeApp(object):
    def __init__(self, conn):
        self.conn = conn


def run():
    conn = ooxcb.connect()

    setup = conn.get_setup()

    try:
        for i in xrange(setup.roots_len):
            screen_info = conn.get_setup().roots[i]
            set_root(conn, screen_info, (float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])))
    finally:
        conn.disconnect()




