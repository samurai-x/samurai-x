import string

import ooxcb
from ooxcb.eventsys import EventDispatcher
from ooxcb.contrib import cairo
from ooxcb import xproto

from ctypes import byref

from samuraix.rect import Rect
from samuraix.util import DictProxy

from yahiko import rsvg

import logging
log = logging.getLogger(__name__)


class Window(EventDispatcher):

    def __init__(self, width=None, height=None, style=None, **kwargs):
        self.rx = None
        self.ry = None
        self.rwidth = None
        self.rheight = None
        
        self.width = width
        self.height = height 

        self.style = style or {}

        self.parent = None

        self.push_handlers(**kwargs)

    def set_size(self, width, height):
        self.width = width
        self.height = height 

    def set_render_coords(self, x, y, width, height):
        self.rx = x
        self.ry = y
        self.rwidth = width
        self.rheight = height 

    def setup_clip(self, cr):
        cairo.cairo_rectangle(cr, self.rx, self.ry, self.rwidth, self.rheight)
        cairo.cairo_clip(cr)

    def render(self, cr):
        assert None not in (self.rx, self.ry, self.rwidth, self.rheight), self

        style = self.style

        if not style:
            return 

        if 'background.style' in style: 
            cairo.cairo_rectangle(cr, self.rx, self.ry, self.rwidth, self.rheight)

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
                fn = style.get('background.image')
                ext = fn.rsplit('.', 1)[1]
                if ext == 'png':
                    image = cairo.cairo_image_surface_create_from_png(fn)
                    w = float(cairo.cairo_image_surface_get_width(image))
                    h = float(cairo.cairo_image_surface_get_height(image))

                    print w, h, self.rwidth, self.rheight, self.rx, self.ry

                    cairo.cairo_scale(cr, self.rwidth/w, self.rheight/h)
                    cairo.cairo_set_source_surface(cr, image, self.rx, self.ry)
                    cairo.cairo_paint(cr)
                elif ext == 'svg':
                    handle = rsvg.rsvg_handle_new_from_file(fn, None)
                    dim = rsvg.RsvgDimensionData()
                    rsvg.rsvg_handle_get_dimensions(handle, byref(dim))
                    cairo.cairo_scale(cr, self.rwidth/dim.width, self.rheight/dim.height)
                    cairo.cairo_save(cr)
                    cairo.cairo_translate(cr, self.rx, self.ry)
                    rsvg.rsvg_handle_render_cairo(handle, cr)

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
            cairo.cairo_rectangle(cr, self.rx, self.ry, self.rwidth, self.rheight)
            cairo.cairo_stroke(cr)

    def hit(self, x, y):
        return (x > self.rx and 
                y > self.ry and 
                x < self.rx + self.rwidth and 
                y < self.ry + self.rheight)

    def grab_input(self, control=None):
        self.parent.grab_input(control or self)

    def dirty(self, control=None):
        self.parent.dirty(control or self)


Window.register_event_type('on_button_press')
Window.register_event_type('on_key_press')


class Layouter(object):
    def __init__(self, container):
        self.container = container

    def layout(self): 
        raise NotImplementedError

    def fit(self):
        raise NotImplementedError


class VerticalLayouter(Layouter):
    def layout(self):
        padding = self.container.style.get('layout.padding', 0)
        h = self.container.rheight - (2 * padding)
        w = self.container.rwidth - (2 * padding)

        used_height = 0 
        without_height = len(self.container.children)

        for child in self.container.children:
            if child.height:
                used_height += child.height
                without_height -= 1

        if without_height:
            hplus = (h - used_height) / without_height
        else:
            hplus = 0

        y = padding
        for child in self.container.children:
            if child.style:
                margin = child.style.get('layout.margin', 0)
            else:
                margin = 0 

            child.set_render_coords(
                    padding + margin,
                    y + margin,
                    w - (2 * margin),
                    (child.height or hplus) - (2 * margin),
            )
            y += (child.height or hplus)

            if hasattr(child, 'layout'):
                child.layout()

    def fit(self):
        width = 0
        height = 0

        for child in self.container.children:
            child_layout_style = DictProxy(child.style, 'layout.')
            margin = child_layout_style.get('margin', 0)
            if child.width:
                width = max(width, child.width + (2 * margin))

            if child.height:
                height += child.height + (2 * margin)

        layout_style = DictProxy(self.container.style, 'layout.')
        padding = layout_style.get('padding', 0)
        width += padding * 2
        height += padding * 2

        self.container.set_size(width, height)

        if self.container.parent and hasattr(self.container.parent, 'layout'):
            self.container.parent.fit()


class HorizontalLayouter(Layouter):
    def layout(self):
        layout_style = self.container.style.get('layout', {})
        if layout_style:
            padding = layout_style.get('padding', 0)
        else:
            padding = 0

        h = self.container.rheight - (2 * padding)
        w = self.container.rwidth - (2 * padding)

        used_width = 0 
        with_width = 0 

        for child in self.container.children:
            if child.width:
                used_width += child.width
                with_width += 1

        wplus = (w - used_width) / (len(self.container.children) - with_width)
        x = padding
        for child in self.container.children:
            margin = 0
            if child.style:
                child_layout_style = child.style.get('layout')
                if child_layout_style:
                    margin = child_layout_style.get('margin', 0)

            child.set_render_coords(
                    x + margin,
                    padding + margin,
                    (child.width or wplus) - (2 * margin),
                    h - (2 * margin),
            )
            x += (child.width or wplus)

            if hasattr(child, 'layout'):
                child.layout()


class Container(Window):
    def __init__(self, layouter=None, **kwargs):
        Window.__init__(self, **kwargs)
        if layouter:
            self.layouter = layouter(self)
        else:
            self.layouter = None
        self.children = []

    def layout(self):
        if self.layouter:
            self.layouter.layout()

    def fit(self):
        self.layouter.fit()

    def render(self, cr):
        Window.render(self, cr)

        if self.children:
            cairo.cairo_translate(cr, self.rx, self.ry)

            for child in self.children:
                #cairo.cairo_save(cr)
                #child.setup_clip(cr)
                child.render(cr)
                #cairo.cairo_restore(cr)

    def add_child(self, child):
        assert child.parent is None
        child.parent = self
        self.children.append(child)

    def add_children(self, children):
        [self.add_child(child) for child in children]

    def on_button_press(self, event):
        local_x, local_y = event.event_x - self.rx, event.event_y - self.ry

        for child in self.children:
            if child.hit(local_x, local_y):
                return child.dispatch_event('on_button_press', event)


class TopLevelContainer(Container):
    def __init__(self, window, visual_type, **kwargs):
        Container.__init__(self, **kwargs)
        self.window = window
        self.visual_type = visual_type

        geom = window.get_geometry().reply()
        self.width = geom.width
        self.height = geom.height

        self.focused_control = None

        self.surface = None
        self.cr = None

        window.push_handlers(
                on_property_notify=self.on_window_property_notify,
                on_configure_notify=self.on_window_configure_notify,
                on_button_press=self.on_button_press,
                on_key_press=self.on_window_key_press,
                on_expose=self.on_window_expose,
        )

        #self.recreate_surface()
    def remove_handlers(self):
            self.window.remove_handlers(
                on_property_notify=self.on_window_property_notify,
                on_configure_notify=self.on_window_configure_notify,
                on_button_press=self.on_button_press,
                on_key_press=self.on_window_key_press,
                on_expose=self.on_window_expose,
            )

    def set_size(self, width, height):
        if self.width != width or self.height != height:
            self.window.configure(width=width, height=height)

    def recreate_surface(self):
        self.surface = cairo.cairo_xcb_surface_create(
                self.window.conn, 
                self.window,
                self.visual_type,
                self.width, self.height)
        
        self.cr = cairo.cairo_create(self.surface)

    def on_window_expose(self, event):
        if event.count == 0:
            self.render()

    def on_window_property_notify(self, event):
        pass

    def on_window_key_press(self, event):
        if self.focused_control is not None:
            self.focused_control.dispatch_event('on_key_press', event)

    def on_window_configure_notify(self, event):
        rect = Rect.from_object(event)
        if rect.width != self.width or rect.height != self.height:
            self.width = rect.width
            self.height = rect.height 
            self.recreate_surface()
            self.layout()
            self.render()

    def layout(self):
        self.rx = 0
        self.ry = 0
        self.rwidth = self.width
        self.rheight = self.height
        Container.layout(self)

    def render(self, control=None):
        if self.cr is None:
            return 
        cairo.cairo_save(self.cr)
        if control is None:
            Container.render(self, self.cr)
        else:
            #control.setup_clip(self.cr)
            control.render(self.cr)
        cairo.cairo_restore(self.cr)
        self.window.conn.flush()

    def grab_input(self, control=None):
        if control is None:
            control = self
        self.focused_control = control

    def dirty(self, control=None):
        self.render(control)


class Label(Window):
    def __init__(self, text=None, **kwargs):
        self.text = text
        Window.__init__(self, **kwargs)

    def render(self, cr):
        Window.render(self, cr)
        
        text = DictProxy(self.style, 'text.')
        if (not self.style
            or not self.text
            or not text
            or not 'color' in text
            and text['color']):
            return 

        extents = cairo.cairo_text_extents_t()
        cairo.cairo_text_extents(cr, self.text, byref(extents))

        cairo.cairo_set_source_rgb(cr, *text['color'])

        align = text.get('align', 'centre')
        assert align in ('left', 'centre', 'right')
        if align == 'centre':
            cairo.cairo_move_to(cr, 
                    self.rx+(self.rwidth/2)-(extents.width/2), 
                    self.ry+(self.rheight/2)+(extents.height/2)
            )
        elif align == 'left':
            cairo.cairo_move_to(cr,
                    self.rx,
                    self.ry+(self.rheight/2)+(extents.height/2)
            )
        elif align == 'right':
            cairo.cairo_move_to(cr,
                    self.rx+self.rwidth - extents.width,
                    self.ry+(self.rheight/2)+(extents.height/2)
            )
        cairo.cairo_show_text(cr, self.text)


class Input(Label):
    def on_key_press(self, event):
        if event.detail == 0:
            return 
        shift = int((event.state & xproto.ModMask.Shift) or (event.state & xproto.ModMask.Lock))
        k = ooxcb.keysyms.keysym_to_str(event.conn.keysyms.get_keysym(event.detail, shift))
        
        if k == 'Return':
            self.dispatch_event('on_return', self)    
        elif k in string.printable:
            self.text += k
            self.dirty()

    def on_button_press(self, event):
        self.grab_input()
        
Input.register_event_type('on_return')
