import string

import ooxcb
from ooxcb.eventsys import EventDispatcher
#from ooxcb.contrib import cairo
from ooxcb.protocol import xproto

from ctypes import byref, POINTER

from samuraix.rect import Rect
from samuraix.util import DictProxy

from yahiko import rsvg
from yahiko import cairo
from yahiko import pango

import logging 
log = logging.getLogger(__name__)


class Window(EventDispatcher):
    """
        The base class of all widgets in yahiko.ui. Window simply defines
        a rectangle area on the screen.

        Parameters for ``__init__``:
        
        :param width: The desired width of the window. This may or may 
                      not actually be used when laying out the window.

                      The actual render coordinates of a window are stored in
                      window.rx, window.ry, window.rwidth, window.rheight.

        :param height: The desired height of the window. This may or 
                       may not actually be used when laying out the window.

        :param style: A dictionary describing the style of this window.
                      This resembles CSS and knowledge of CSS wil certainly help 
                      understanding this. Styles currently supported are:

                        * background.style: must be one of:
                            * fill: fill the background with a solid color 
                            * gradient: fill the background with a gradient
                            * image: fill the background with an image 
                        * background.color: used with background.style "fill", a tuple
                            like (r, g, b) representing color
                        * background.fill-line: used with background.style "gradient", 
                            a tuple like (x1, y1, x2, y2) describing the path of a 
                            gradient 
                        * background.fill-stops: used with background.style "gradient", 
                            a list of tuples like [(offset, r, g, b), ...] where 
                            offset is between 0 and 1.0.
                        * background.image: used with background.style "image", a
                            filename of an image ( either PNG or SVG ) 

                        * border.style: must be one of:
                            * fill: fill the border with a solid color 
                            * gradient: fill the border with a gradient 
                        * border.color: used with border.style "fill", a tuple
                            like (r, g, b) representing color
                        * border.fill-line: used with border.style "gradient", 
                            a tuple like (x1, y1, x2, y2) describing the path of a 
                            gradient 
                        * border.fill-stops: used with border.style "gradient", 
                            a list of tuples like [(offset, r, g, b), ...] where 
                            offset is between 0 and 1.0.
                                        
    """
    def __init__(self, style=None, **kwargs):
        self.rx = None
        self.ry = None
        self.rwidth = None
        self.rheight = None
        
        self.style = style or {}
        self.parent = None

        self.push_handlers(**kwargs)

    def set_size(self, width, height):
        self.style['width'] = width
        self.style['height'] = height 

    def set_render_coords(self, x, y, width, height):
        self.rx = x
        self.ry = y
        self.rwidth = width
        self.rheight = height 

    def render(self, cr):
        assert None not in (self.rx, self.ry, self.rwidth, self.rheight), self

        style = self.style

        if not style:
            return 

        needs_restore = False

        if 'clip' in style and style['clip']:
            cr.save()
            needs_restore = True
            cr.rectangle(self.rx, self.ry, self.rwidth, self.rheight)
            cr.clip()

        self._render(cr)

        if needs_restore:
            cr.restore()

    def _render(self, cr):
        style = self.style
        if 'background.style' in style: 
            cr.rectangle(self.rx, self.ry, self.rwidth, self.rheight)

            bstyle = style.get('background.style')
            assert bstyle in ('fill', 'gradient', 'image')
            if bstyle == 'fill' and 'background.color' in style:
                cr.set_source_rgb(*style['background.color'])
                cr.fill()
            elif bstyle == 'gradient' and 'background.fill-line' in style and 'background.fill-stops' in style:
                pat = cairo.Pattern.create_linear(*style['background.fill-line'])
                for stop in style['background.fill-stops']:
                    pat.add_color_stop_rgb(*stop)
                cr.set_source(pat)
                cr.fill()
            elif bstyle == 'image' and 'background.image' in style and style['background.image']:
                fn = style.get('background.image')
                ext = fn.rsplit('.', 1)[1]
                if ext == 'png':
                    image = cairo.ImageSurface.create_from_png(fn)
                    w = float(image.get_width())
                    h = float(image.get_height())
                    cr.scale(self.rwidth/w, self.rheight/h)
                    cr.set_source_surface(image, self.rx, self.ry)
                    cr.paint()
                elif ext == 'svg':
                    handle = rsvg.rsvg_handle_new_from_file(fn, None)
                    dim = rsvg.RsvgDimensionData()
                    rsvg.rsvg_handle_get_dimensions(handle, byref(dim))
                    cairo.cairo_scale(cr, self.rwidth/dim.width, self.rheight/dim.height)
                    cairo.cairo_save(cr)
                    cairo.cairo_translate(cr, self.rx, self.ry)
                    rsvg.rsvg_handle_render_cairo(handle, cr)

        if 'border.style' in style:
            bstyle = style.get('border.style', 'fill')
            assert bstyle in ('fill', 'gradient')
            if bstyle == 'fill' and 'border.color' in style:
                cr.set_source_rgb(*style['border.color'])
            elif bstyle == 'gradient' and 'border.fill-line' in style and 'border.fill-stops' in style:
                pat = cairo.Pattern.create_linear(*style['border.fill-line'])
                for stop in style['border.fill-stops']:
                    pat.add_color_stop_rgb(*stop)
                cr.set_source(pat)
            cr.set_line_width(style.get('border.width', 1.0))
            cr.rectangle(self.rx, self.ry, self.rwidth, self.rheight)
            cr.stroke()


    def hit(self, x, y):
        return (x > self.rx and 
                y > self.ry and 
                x < self.rx + self.rwidth and 
                y < self.ry + self.rheight)

    def grab_input(self, control=None):
        self.parent.grab_input(control or self)

    def dirty(self, control=None):
        if self.parent is not None:
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
            if 'height' in child.style and child.style['height']:
                used_height += child.style['height']
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
                    (child.style.get('height') or hplus) - (2 * margin),
            )
            y += (child.style.get('height') or hplus)

            if hasattr(child, 'layout'):
                child.layout()

    def fit(self):
        width = 0
        height = 0

        for child in self.container.children:
            child_layout_style = DictProxy(child.style, 'layout.')
            margin = child_layout_style.get('margin', 0)
            if 'width' in child.style and child.style['width']:
                width = max(width, child.style['width'] + (2 * margin))

            if 'height' in child.style and child.style['height']:
                height += child.style['height'] + (2 * margin)

        layout_style = DictProxy(self.container.style, 'layout.')
        padding = layout_style.get('padding', 0)
        width += padding * 2
        height += padding * 2

        self.container.set_size(width, height)

        if self.container.parent and hasattr(self.container.parent, 'layout'):
            self.container.parent.fit()


class HorizontalLayouter(Layouter):
    def layout(self):
        padding = self.container.style.get('layout.padding', 0)
        h = self.container.rheight - (2 * padding)
        w = self.container.rwidth - (2 * padding)

        used_width = 0 
        without_width = len(self.container.children)

        for child in self.container.children:
            if 'width' in child.style and child.style['width']:
                used_width += child.style['width']
                without_width -= 1

        if without_width:
            wplus = (w - used_width) / without_width
        else:
            wplus = 0

        x = padding
        for child in self.container.children:
            if child.style:
                margin = child.style.get('layout.margin', 0)
            else:
                margin = 0

            child.set_render_coords(
                    x + margin,
                    padding + margin,
                    (child.style.get('width') or wplus) - (2 * margin),
                    h - (2 * margin),
            )
            x += (child.style.get('width') or wplus)

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
            cr.translate(self.rx, self.ry)

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



class Label(Window):
    def __init__(self, text=None, **kwargs):
        self.text = text
        Window.__init__(self, **kwargs)

    def _render(self, cr):
        Window._render(self, cr)
        
        text = DictProxy(self.style, 'text.')
        if (not self.style
            or not self.text
            or not text
            or not 'color' in text
            and text['color']):
            return 
    
        family = text.get('family', 'sans-serif')
        weight = getattr(
                cairo, 
                'FONT_WEIGHT_' + text.get('weight', 'normal').upper(), 
                cairo.FONT_WEIGHT_NORMAL,
        )
        slant = getattr(
                cairo,
                'FONT_SLANT_' + text.get('slant', 'normal').upper(),
                cairo.FONT_SLANT_NORMAL,
        )
        cr.select_font_face(family, weight, slant)

        lines = self.text.split('\n')

        valign = text.get('vertical-align', 'top')
        assert valign in ('top', 'middle', 'bottom')

        extents = cairo.font_extents_t()
        cr.font_extents(byref(extents))
        line_height = extents.height
        total_height = len(lines) * line_height
        y = self.ry

        if valign == 'top':
            y = self.ry + line_height
        elif valign == 'middle':
            y = self.ry + (self.rheight / 2) - (total_height / 2)
        elif valign == 'bottom':
            y = self.ry + self.rheight - total_height

        extents = cairo.text_extents_t()

        cr.set_source_rgb(*text['color'])

        for line in lines:
            cr.text_extents(line, byref(extents))

            align = text.get('align', 'centre')
            assert align in ('left', 'centre', 'right')
            if align == 'centre':
                cr.move_to(self.rx+(self.rwidth/2)-(extents.width/2), y)
            elif align == 'left':
                cr.move_to(self.rx, y)
            elif align == 'right':
                cr.move_to(self.rx+self.rwidth - extents.width, y)

            cr.show_text(line)
            y += line_height


class PangoLabel(Label):
    pango_alignments = {
        'left': pango.ALIGN_LEFT,
        'centre': pango.ALIGN_CENTER,
        'right': pango.ALIGN_RIGHT,
    }

    def _render(self, cr):
        Window._render(self, cr)
        if not self.text:
            return 
        style = self.style
        layout = pango.cairo_create_layout(cr)
        layout.set_markup(self.text, -1)
        layout.set_width(pango.units_from_double(self.rwidth))
        layout.set_height(pango.units_from_double(self.rheight))
        layout.set_alignment(self.pango_alignments[style.get('text.align', 'centre')])
        font_desc = style.get('text.font-description', 'Bitstream Vera Sans Mono 8')
        desc = pango.FontDescription.from_string(font_desc)
        layout.font_description = desc
        desc.free()

        valign = style.get('text.vertical-align', 'top')
        assert valign in ('top', 'middle', 'bottom')
        if valign == 'top':
            y = self.ry
        else:
            extents = pango.PangoRectangle()
            layout.get_extents(None, byref(extents))
            eheight = pango.units_to_double(extents.height)
            if valign == 'middle':
                y = self.ry + (self.rheight / 2) - (eheight / 2)
            elif valign == 'bottom':
                y = self.ry + self.rheight - eheight

        cr.set_source_rgb(*style['text.color'])
        cr.move_to(self.rx, y)
        pango.cairo_update_layout(cr, layout)
        pango.cairo_show_layout(cr, layout)



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


class TopLevelContainer(Container):
    def __init__(self, window, visual_type, **kwargs):
        Container.__init__(self, **kwargs)
        self.window = window
        self.visual_type = visual_type

        geom = window.get_geometry().reply()
        self.style['width'] = geom.width
        self.style['height'] = geom.height

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
        if self.style['width'] != width or self.style['height'] != height:
            self.window.configure(width=width, height=height)

    def recreate_surface(self):
        self.surface = cairo.XcbSurface.create(
                self.window.conn, 
                self.window,
                self.visual_type,
                self.style['width'], self.style['height'])
        
        self.cr = cairo.Context.create(self.surface)

    def on_window_expose(self, event):
        if event.count == 0:
            self.render()
            self.window.conn.flush()

    def on_window_property_notify(self, event):
        pass

    def on_window_key_press(self, event):
        if self.focused_control is not None:
            self.focused_control.dispatch_event('on_key_press', event)

    def on_window_configure_notify(self, event):
        rect = Rect.from_object(event)
        if rect.width != self.style['width'] or rect.height != self.style['height']:
            self.style['width'] = rect.width
            self.style['height'] = rect.height 
            self.recreate_surface()
            self.layout()
            self.render()

    def layout(self):
        self.rx = 0
        self.ry = 0
        self.rwidth = self.style['width']
        self.rheight = self.style['height']
        Container.layout(self)

    def render(self, control=None):
        if self.cr is None:
            log.warn('cr is None!')
            return 
        self.cr.save()
        if control is None:
            Container.render(self, self.cr)
        else:
            #control.setup_clip(self.cr)
            control.render(self.cr)
        self.cr.restore()
        self.window.conn.flush()

    def grab_input(self, control=None):
        if control is None:
            control = self
        self.focused_control = control

    def dirty(self, control=None):
        # FIXME somehow we need to render a control that fills the 
        # background
        self.render() #control)


class DoubleBufTopLevelContainer(TopLevelContainer):
    def recreate_surface(self):
        try:
            self.buf_surface = cairo.XcbSurface.create(
                    self.window.conn, 
                    self.window,
                    self.visual_type,
                    self.style['width'], self.style['height'])
            
            self.cr_buf = cairo.Context.create(self.buf_surface)
            self.surface = cairo.ImageSurface.create(
                    cairo.FORMAT_RGB24,
                    self.style['width'], self.style['height'])
            self.cr = cairo.Context.create(self.surface)
        except Exception, e:
            print e

    def on_window_expose(self, event):
        if event is None or event.count == 0:
            try:
                self.cr_buf.set_source_surface(self.surface, 0, 0)
                self.cr_buf.paint()
                self.window.conn.flush()
            except Exception, e:
                print e
            
    def dirty(self, control=None):
        self.render()
        #self.window.clear_area(0, 0, self.style['width'], self.style['height'])
        self.on_window_expose(None)


