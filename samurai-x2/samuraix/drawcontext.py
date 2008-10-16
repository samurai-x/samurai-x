import samuraix
from samuraix import (rsvg, cairo)
from samuraix.sxctypes import byref

import logging
log = logging.getLogger(__name__)


class DrawContext(object):
    svg_handles = {}

    def __init__(self, screen, width, height, drawable):
        self.connection = screen.connection
        self.screen = screen
        self.width = width
        self.height = height
        self.drawable = drawable
        self.visual = screen.root_visual_type
        self.surface = cairo.cairo_xcb_surface_create(
                byref(self.connection._connection), drawable._xid,
                byref(self.visual._visualtype),
                width, height
        )
        self.cr = cairo.cairo_create(self.surface)
        cairo.cairo_set_operator(self.cr, cairo.CAIRO_OPERATOR_SOURCE)
        cairo.cairo_set_source_surface(self.cr, self.surface, 0, 0)
        cairo.cairo_set_source_rgba(self.cr, 255, 0, 0, 0)

        self.default_font = "snap"
        self.default_font_size = 10

        log.debug('created drawcontext %s' % self)

    def __del__(self):
        self.delete()

    def delete(self):
        log.debug('destroying drawcontext %s' %self)
        cairo.cairo_surface_destroy(self.surface)
        cairo.cairo_destroy(self.cr)

    def fillrect(self, x, y, width, height, color):
        if False:
            pat = cairo.cairo_pattern_create_linear (0.0, 0.0, width, 0.0)
            cairo.cairo_pattern_add_color_stop_rgba (pat, 0.0, 1.0, 0.0, 0.0, 1.0)
            cairo.cairo_pattern_add_color_stop_rgba (pat, width/3, 0.1, 0.0, 0.0, 1.0)
            cairo.cairo_pattern_add_color_stop_rgba (pat, width, 0.0, 0.0, 0.0, 1.0)
            cairo.cairo_rectangle(self.cr, x, y, width, height)
            cairo.cairo_set_source(self.cr, pat)
            cairo.cairo_fill(self.cr)
            cairo.cairo_pattern_destroy(pat)
        else:
            cairo.cairo_set_source_rgb(self.cr, color[0], color[1], color[2])
            cairo.cairo_rectangle(self.cr, x, y, width, height)
            cairo.cairo_fill(self.cr)
        self.connection.flush()

    def text(self, x, y, string, color=(0.0, 0.0, 0.0), 
            font=None, bold=False, align=None, font_size=None):
        cairo.cairo_set_source_rgb(self.cr, color[0], color[1], color[2])

        if font is None:
            font = self.default_font
        if font_size is None:
            font_size = self.default_font_size

        if bold:
            weight = cairo.CAIRO_FONT_WEIGHT_BOLD
        else:
            weight = cairo.CAIRO_FONT_WEIGHT_NORMAL

        cairo.cairo_select_font_face(self.cr, font, cairo.CAIRO_FONT_SLANT_NORMAL,
                               weight)
        cairo.cairo_set_font_size(self.cr, font_size)

        if align and align != 'left':
            #typedef struct {
            #    double x_bearing;
            #    double y_bearing;
            #    double width;
            #    double height;
            #    double x_advance;
            #    double y_advance;
            #} cairo.cairo_text_extents_t;

            extents = cairo.cairo_text_extents_t()

            cairo.cairo_text_extents(self.cr, string, byref(extents))

            if align == "right":
                x -= extents.x_advance  

        cairo.cairo_move_to(self.cr, x, y)
        cairo.cairo_show_text(self.cr, string)

        self.connection.flush()

    def svg(self, filename, x=0, y=0, width=None, height=None):
        try:
            handle = self.svg_handles[filename]
        except KeyError:
            handle = self.svg_handles[filename] = rsvg.rsvg_handle_new_from_file(filename)

        cairo.cairo_save(self.cr)

        cairo.cairo_translate(self.cr, x, y)
 
        if width is not None or height is not None:
            dim = rsvg.RsvgDimensionData()
            rsvg.rsvg_handle_get_dimensions(handle, byref(dim))
            if width is not None:
                scale_x = float(width) / dim.width
            else:
                scale_x = 1.0
            if height is not None:
                scale_y = float(height) / dim.height
            else:
                scale_y = 1.0
            cairo.cairo_scale(self.cr, scale_x, scale_y)

        rsvg.rsvg_handle_render_cairo(handle, self.cr)

        cairo.cairo_restore(self.cr)
        self.connection.flush()

    def fill(self, color=(0.0, 0.0, 0.0)):
        cairo.cairo_set_source_rgb(self.cr, *color)
        cairo.cairo_paint(self.cr)
        self.connection.flush()
