from pyglet.window.xlib import xlib 

import samuraix
from samuraix.cairo import *


class DrawContext(object):
    def __init__(self, screen, width, height, drawable):
        self.screen = screen
        self.width = width
        self.height = height 
        self.drawable = drawable
        self.depth = xlib.XDefaultDepth(samuraix.display, screen.num)
        self.visual = xlib.XDefaultVisual(samuraix.display, screen.num)
        self.surface = cairo_xlib_surface_create(samuraix.display, drawable, self.visual,   
                            width, height)
        self.cr = cairo_create(self.surface)

    def delete(self):
        cairo_surface_destroy(self.surface)
        cairo_destroy(self.cr)

    def fillrect(self, x, y, width, height, color):
        cairo_set_source_rgb(self.cr, color[0], color[1], color[2])
        cairo_rectangle(self.cr, x, y, width, height)
        cairo_fill(self.cr)

    def text(self, x, y, string, color=(0.0, 0.0, 0.0)):
        cairo_set_source_rgb(self.cr, color[0], color[1], color[2])

        cairo_select_font_face(self.cr, "snap", CAIRO_FONT_SLANT_NORMAL,
                               CAIRO_FONT_WEIGHT_NORMAL)
        cairo_set_font_size(self.cr, 10)

        cairo_move_to(self.cr, x, y)
        cairo_show_text(self.cr, string)

 



