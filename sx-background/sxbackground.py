import sys

from samuraix.plugin import Plugin 
from samuraix.screen import Screen
from ooxcb.contrib import cairo
from ooxcb import xproto
import ooxcb


# ripped from yahiko
def default_func(cr, style, width, height):
    x = 0
    y = 0
    if 'background.style' in style: 
        cairo.cairo_rectangle(cr, x, y, width, height)

        bstyle = style.get('background.style')
        assert bstyle in ('fill', 'gradient', 'image')
        if bstyle == 'fill' and 'background.color' in style:
            cairo.cairo_set_source_rgb(cr, *style['background.color'])
            cairo.cairo_fill(cr)
        elif bstyle == 'gradient' and 'background.fill-line' in style and 'background.fill-stops' in style:
            pat = cairo.cairo_pattern_create_linear(*style['background.fill-line'])
            for stop in style['background.fill-stops']:
                cairo.cairo_pattern_add_color_stop_rgb(pat, *stop)
            cairo.cairo_set_source(cr, pat)
            cairo.cairo_fill(cr)
        elif bstyle == 'image' and 'background.image' in style and style['background.image']:
            image = cairo.cairo_image_surface_create_from_png(style.get('background.image'))
            w = float(cairo.cairo_image_surface_get_width(image))
            h = float(cairo.cairo_image_surface_get_height(image))

            cairo.cairo_scale(cr, width/w, height/h)

            cairo.cairo_set_source_surface(cr, image, x, y)
            cairo.cairo_paint(cr)

    if 'border.color' in style:
        bstyle = style.get('style', 'fill')
        assert bstyle in ('fill', 'gradient')
        if bstyle == 'fill' and 'border.color' in style:
            cairo.cairo_set_source_rgb(cr, *style['border.color'])
        elif bstyle == 'gradient' and 'border.fill-line' in style and 'border.fill-stops' in style:
            pat = cairo.cairo_pattern_create_linear(*style['border.fill-line'])
            for stop in style['border.fill-stops']:
                cairo.cairo_pattern_add_color_stop_rgb(pat, *stop)
            cairo.cairo_set_source(cr, pat)
        cairo.cairo_set_line_width(cr, style.get('width', 1.0))
        cairo.cairo_rectangle(cr, x, y, width, height)
        cairo.cairo_stroke(cr)


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
        func = default_func
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




