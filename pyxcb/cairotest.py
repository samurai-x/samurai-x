import xcb
import xcb._cairo
import ctypes
import rsvg

c = xcb.connection.Connection()
screen = c.screens[0]
root = screen.root

class DrawContext(object):
    svg_handles = {}

    def __init__(self, win_surf, im_surf):
        #self.im_surf = im_surf
        self.win_surf = win_surf
        #self.cr = xcb._cairo.cairo_create(self.im_surf)
        self.cr = xcb._cairo.cairo_create(self.win_surf)

        self.default_font = "snap"
        self.default_font_size = 10
        xcb._cairo.cairo_set_operator(self.cr, xcb._cairo.CAIRO_OPERATOR_SOURCE)
        xcb._cairo.cairo_set_source_surface(self.cr, self.win_surf, 0, 0)
        xcb._cairo.cairo_set_source_rgba(self.cr, 255, 0, 0, 0)


    def __del__(self):
        self.delete()

    def delete(self):
        xcb._cairo.cairo_surface_destroy(self.surface)
        xcb._cairo.cairo_destroy(self.cr)

    def fillrect(self, x, y, width, height, color):
        if False:
            pat = xcb._cairo.cairo_pattern_create_linear (0.0, 0.0, width, 0.0)
            xcb._cairo.cairo_pattern_add_color_stop_rgba (pat, 0.0, 1.0, 0.0, 0.0, 1.0)
            xcb._cairo.cairo_pattern_add_color_stop_rgba (pat, width/3, 0.1, 0.0, 0.0, 1.0)
            xcb._cairo.cairo_pattern_add_color_stop_rgba (pat, width, 0.0, 0.0, 0.0, 1.0)
            xcb._cairo.cairo_rectangle(self.cr, x, y, width, height)
            xcb._cairo.cairo_set_source(self.cr, pat)
            xcb._cairo.cairo_fill(self.cr)
            xcb._cairo.cairo_pattern_destroy(pat)
        else:
            xcb._cairo.cairo_set_source_rgb(self.cr, color[0], color[1], color[2])
            xcb._cairo.cairo_rectangle(self.cr, x, y, width, height)
            xcb._cairo.cairo_fill(self.cr)

    def text(self, x, y, string, color=(0.0, 0.0, 0.0), 
            font=None, bold=False, align=None, font_size=None):
        xcb._cairo.cairo_set_source_rgb(self.cr, color[0], color[1], color[2])

        if font is None:
            font = self.default_font
        if font_size is None:
            font_size = self.default_font_size

        if bold:
            weight = xcb._cairo.CAIRO_FONT_WEIGHT_BOLD
        else:
            weight = xcb._cairo.CAIRO_FONT_WEIGHT_NORMAL

        xcb._cairo.cairo_select_font_face(self.cr, font, xcb._cairo.CAIRO_FONT_SLANT_NORMAL,
                               weight)
        xcb._cairo.cairo_set_font_size(self.cr, font_size)

        if align and align != 'left':
            #typedef struct {
            #    double x_bearing;
            #    double y_bearing;
            #    double width;
            #    double height;
            #    double x_advance;
            #    double y_advance;
            #} xcb._cairo.cairo_text_extents_t;

            extents = xcb._cairo.cairo_text_extents_t()

            xcb._cairo.cairo_text_extents(self.cr, string, ctypes.byref(extents))

            if align == "right":
                x -= extents.x_advance  

        xcb._cairo.cairo_move_to(self.cr, x, y)
        xcb._cairo.cairo_show_text(self.cr, string)
        
        c.flush()

    def svg(self, filename, x=0, y=0, width=None, height=None):
        try:
            handle = self.svg_handles[filename]
        except KeyError:
            handle = self.svg_handles[filename] = rsvg.rsvg_handle_new_from_file(filename)

        xcb._cairo.cairo_save(self.cr)

        xcb._cairo.cairo_translate(self.cr, x, y)
 
        if width is not None or height is not None:
            dim = rsvg.RsvgDimensionData()
            rsvg.rsvg_handle_get_dimensions(handle, ctypes.byref(dim))
            if width is not None:
                scale_x = float(width) / dim.width
            else:
                scale_x = 1.0
            if height is not None:
                scale_y = float(height) / dim.height
            else:
                scale_y = 1.0
            xcb._cairo.cairo_scale(self.cr, scale_x, scale_y)

        rsvg.rsvg_handle_render_cairo(handle, self.cr)

        xcb._cairo.cairo_restore(self.cr)


    def fill(self, color=(0.0, 0.0, 0.0)):
        xcb._cairo.cairo_set_source_rgb(self.cr, *color)
        xcb._cairo.cairo_paint(self.cr)

def get_root_visual_type(screen):
    depth_iter = xcb._xcb.xcb_screen_allowed_depths_iterator(screen._screen)
    while depth_iter.rem:

        visual_iter = xcb._xcb.xcb_depth_visuals_iterator(depth_iter.data)
        while visual_iter.rem:
            if screen._screen.root_visual == visual_iter.data.contents.visual_id:
                return visual_iter.data.contents
            xcb._xcb.xcb_visualtype_next(visual_iter.contents)
        xcb._xcb.xcb_depth_next(depth_iter)

w = xcb.window.Window.create(c, screen, 0, 0, 480, 480, 10, attributes={'back_pixel':screen.white_pixel,
                                                                        'event_mask': set([
                                                                                       xcb.event.ExposeEvent,
                                                                                       xcb.event.KeyPressEvent,
                                                                                       xcb.event.KeyReleaseEvent,
                                                                                       xcb.event.ButtonPressEvent,
                                                                                       xcb.event.ButtonReleaseEvent,
                                                                                       xcb.event.EnterNotifyEvent,
                                                                                       xcb.event.LeaveNotifyEvent,
                                                                                       xcb.event.MotionNotifyEvent,
                                                                                       xcb.event.KeymapNotifyEvent,
                                                                                       xcb.event.VisibilityNotifyEvent
                                                                                       ])
                                                                        })


win_surf = xcb._cairo.cairo_xcb_surface_create(ctypes.pointer(c._connection),
        w._xid,
        ctypes.pointer(get_root_visual_type(screen)), 480, 480)

img_surf = xcb._cairo.cairo_image_surface_create(xcb._cairo.CAIRO_FORMAT_RGB24, 480, 480)

dc = DrawContext(win_surf, img_surf)
w.map()
while 1:
    e = c.wait_for_event()
    print 'Received event:', e
    if isinstance(e, xcb.event.ExposeEvent):
        dc.text(100, 100, 'This text is pink.', (255, 0, 255))
        dc.fill((0, 0, 0))
        
c.disconnect()
