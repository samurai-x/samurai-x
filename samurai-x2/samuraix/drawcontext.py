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

from __future__ import division
import ctypes

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

        self.default_font = "a_font_that_does_not_exist" # TODO
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
        #self.connection.flush()

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

        #self.connection.flush()

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
        #self.connection.flush()

    def fill(self, color=(0.0, 0.0, 0.0)):
        cairo.cairo_set_source_rgb(self.cr, *color)
        cairo.cairo_paint(self.cr)
        #self.connection.flush()

    def png(self, filename, x=0, y=0, w=None, h=None):
        """
            paint a png file.
            :todo: `w` and `h` currently unused
        """
        # TODO: width, height
        cairo.cairo_save(self.cr)

        surf = cairo.cairo_image_surface_create_from_png(filename)
        cairo.cairo_set_source_surface(self.cr, surf, x, y)
        cairo.cairo_paint(self.cr)

        cairo.cairo_surface_finish(surf)

        cairo.cairo_restore(self.cr)

    def netwm_icon(self, inp, x=0, y=0, resize_to=(24, 24)):
        """
            Draw the netwm icon, specified in _NET_WM_ICON property.

            It's a list of cardinals (ints).

            :Parameters:
                `inp` : list
                    A list of integers, as described in the netwm standard
                `x` : int
                    x offset
                `y` : int
                    y offset
                `resize_to` : tuple or None
                    if `resize_to` is not None, resize the icon to the
                    specified width and height.

            :note: As described in `a bug report`_, _NET_WM_ICON could contain
            several icon sizes. At the moment, only the first listed is used.
            TODO : That should be fixed.
            
            .. _a bug report: http://bugs.kde.org/show_bug.cgi?id=131590 
        """
        cairo.cairo_save(self.cr)
       
        width = inp[0]
        height = inp[1]
        stride = cairo.cairo_format_stride_for_width(cairo.CAIRO_FORMAT_ARGB32, width) 

        data = (ctypes.c_uint * (width * height))(*inp[2:2 + width*height])

        surface = cairo.cairo_image_surface_create_for_data(
                ctypes.cast(data, ctypes.POINTER(ctypes.c_ubyte)),
                cairo.CAIRO_FORMAT_ARGB32,
                width,
                height,
                stride)

        ic = cairo.cairo_create(self.surface)
        cairo.cairo_set_operator(ic, cairo.CAIRO_OPERATOR_OVER)

        # Resize
        if resize_to:
            new_width, new_height = resize_to
            scale_x = new_width / width
            scale_y = new_height / height
            cairo.cairo_scale(ic, scale_x, scale_y)

        cairo.cairo_set_source_surface(ic, surface, x, y)
        cairo.cairo_paint(ic)

        cairo.cairo_surface_finish(surface)
        cairo.cairo_destroy(ic)
        # Restore. We're finished.
        cairo.cairo_restore(self.cr)

