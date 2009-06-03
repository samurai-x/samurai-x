import string

import ooxcb
from ooxcb.eventsys import EventDispatcher
from ooxcb.contrib import cairo
from ooxcb import xproto

from ctypes import byref

from samuraix.rect import Rect


class Window(EventDispatcher):

    def __init__(self, width=None, height=None, style=None, **kwargs):
        self.rx = None
        self.ry = None
        self.rwidth = None
        self.rheight = None
        
        self.width = width
        self.height = height 

        self.style = style

        self.parent = None

        self.push_handlers(**kwargs)

    def setup_clip(self, cr):
        cairo.cairo_rectangle(cr, self.rx, self.ry, self.rwidth, self.rheight)
        cairo.cairo_clip(cr)

    def render(self, cr):
        assert None not in (self.rx, self.ry, self.rwidth, self.rheight)

        if 'background' in self.style and self.style['background'] is not None:
            cairo.cairo_set_source_rgb(cr, *self.style['background']['color'])
            cairo.cairo_rectangle(cr, self.rx, self.ry, self.rwidth, self.rheight)
            cairo.cairo_fill(cr)

        if ('border' in self.style and self.style['border'] != None
            and 'color' in self.style['border'] and self.style['border']['color'] != None
            ):
            cairo.cairo_set_source_rgb(cr, *self.style['border']['color'])
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
        pass


class VerticalLayouter(Layouter):
    def layout(self):
        layout_style = self.container.get('layout')
        if layout_style:
            padding = layout_style.get('padding', 0)
        else:
            padding = 0
        h = self.container.rheight - (2 * padding)
        w = self.container.rwidth - (2 * padding)

        hplus = w / len(self.container.children)
        y = padding
        for child in self.container.children:
            child.rx = padding
            child.ry = y
            child.rwidth = w
            child.rheight = hplus
            y += hplus


class HorizontalLayouter(Layouter):
    def layout(self):
        layout_style = self.container.style.get('layout')
        if layout_style:
            padding = layout_style.get('padding', 0)
        else:
            padding = 0

        h = self.container.rheight - (2 * padding)
        w = self.container.rwidth - (2 * padding)

        wplus = w / len(self.container.children)
        x = padding
        for child in self.container.children:
            child_layout_style = child.style.get('layout')
            if child_layout_style:
                margin = child_layout_style.get('margin', 0)
            else:
                margin = 0
            child.rx = x + margin
            child.ry = padding + margin
            child.rwidth = wplus - (2 * margin)
            child.rheight = h - (2 * margin)
            x += wplus


class Container(Window):
    def __init__(self, layouter=None, **kwargs):
        Window.__init__(self, **kwargs)
        self.layouter = layouter(self)
        self.children = []

    def layout(self):
        self.layouter.layout()

    def render(self, cr):
        Window.render(self, cr)

        if self.children:
            cairo.cairo_translate(cr, self.rx, self.ry)

            for child in self.children:
                cairo.cairo_save(cr)
                child.setup_clip(cr)
                child.render(cr)
                cairo.cairo_restore(cr)

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
                child.dispatch_event('on_button_press', event)


class TopLevelContainer(Container):
    def __init__(self, window, visual_type, **kwargs):
        Container.__init__(self, **kwargs)
        self.window = window
        self.visual_type = visual_type

        geom = window.get_geometry().reply()
        self.width = geom.width
        self.height = geom.height

        self.focused_control = None

        window.push_handlers(
                on_property_notify=self.on_window_property_notify,
                on_configure_notify=self.on_window_configure_notify,
                on_button_press=self.on_button_press,
                on_key_press=self.on_window_key_press,
                on_expose=self.on_window_expose,
        )

    def recreate_surface(self):
        # create a surface for this window
        self.surface = cairo.cairo_xcb_surface_create(
                self.window.conn, 
                self.window,
                self.visual_type,
                self.width, self.height)
        
        # and a cairo context
        self.cr = cairo.cairo_create(self.surface)

    def on_window_expose(self, event):
        self.render()

    def on_window_property_notify(self, event):
        pass

    def on_window_key_press(self, event):
        if self.focused_control is not None:
            self.focused_control.dispatch_event('on_key_press', event)

    def on_window_configure_notify(self, event):
        rect = Rect.from_object(event)
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
        cairo.cairo_save(self.cr)
        if control is None:
            Container.render(self, self.cr)
        else:
            control.setup_clip(self.cr)
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

        if not self.text or not 'color' in self.style['text'] and self.style['text']['color']:
            return 

        extents = cairo.cairo_text_extents_t()
        cairo.cairo_text_extents(cr, self.text, byref(extents))

        cairo.cairo_set_source_rgb(cr, *self.style['text']['color'])

        align = self.style['text'].get('align', 'centre')
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
        
        print k

        if k == 'Return':
            self.dispatch_event('on_return', self)    
        elif k in string.printable:
            self.text += k
            self.dirty()

    def on_button_press(self, event):
        self.grab_input()
        
Input.register_event_type('on_return')
