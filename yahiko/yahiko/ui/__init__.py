from ooxcb.eventsys import EventDispatcher

from ooxcb.contrib import cairo

import ooxcb

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

    def render(self, surface):
        assert None not in (self.rx, self.ry, self.rwidth, self.rheight)

        if 'background' in self.style and self.style['background'] is not None:
            cairo.cairo_set_source_rgb(surface, *self.style['background'])
            cairo.cairo_rectangle(surface, self.rx, self.ry, self.rwidth, self.rheight)
            cairo.cairo_fill(surface)

        if ('border' in self.style and self.style['border'] != None
            and 'color' in self.style['border'] and self.style['border']['color'] != None
            ):
            cairo.cairo_set_source_rgb(surface, *self.style['border']['color'])
            cairo.cairo_rectangle(surface, self.rx, self.ry, self.rwidth, self.rheight)
            cairo.cairo_stroke(surface)

    def hit(self, x, y):
        return (x > self.rx and 
                y > self.ry and 
                x < self.rx + self.rwidth and 
                y < self.ry + self.rheight)

    def grab_input(self, control=None):
        self.parent.grab_input(control or self)


Window.register_event_type('on_button_press')
Window.register_event_type('on_key_press')


class Layouter(object):
    def __init__(self, container):
        self.container = container

    def layout(self): 
        pass


class VerticalLayouter(Layouter):
    def layout(self):
        hplus = self.container.rheight / len(self.container.children)
        y = 0
        for child in self.container.children:
            child.rx = 0
            child.ry = y
            child.rwidth = self.container.width
            child.rheight = hplus
            y += hplus


class HorizontalLayouter(Layouter):
    def layout(self):
        wplus = self.container.rwidth / len(self.container.children)
        x = 0
        for child in self.container.children:
            child.rx = x
            child.ry = 0
            child.rwidth = wplus
            child.rheight = self.container.height
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
            #matrix = cairo.cairo_matrix_t() 
            #cairo.cairo_get_matrix(cr, byref(matrix))    
            cairo.cairo_translate(cr, self.rx, self.ry)

            for child in self.children:
                cairo.cairo_save(cr)
                child.render(cr)
                cairo.cairo_restore(cr)

            #cairo.cairo_set_matrix(cr, byref(matrix))

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

    def on_window_property_notify(self, event):
        print event 

    def on_window_key_press(self, event):
        print self, "key press", event
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

    def render(self):
        cairo.cairo_save(self.cr)
        Container.render(self, self.cr)
        cairo.cairo_restore(self.cr)

    def grab_input(self, control=None):
        if control is None:
            control = self
        print self, "focused_control", control
        self.focused_control = control


class Label(Window):
    def __init__(self, text=None, **kwargs):
        self.text = text
        Window.__init__(self, **kwargs)

    def render(self, cr):
        Window.render(self, cr)

        extents = cairo.cairo_text_extents_t()
        cairo.cairo_text_extents(cr, self.text, byref(extents))

        cairo.cairo_move_to(cr, 
                self.rx+(self.rwidth/2)-(extents.width/2), 
                self.ry+(self.rheight/2)+(extents.height/2)
        )
        cairo.cairo_show_text(cr, self.text)


class Input(Label):
    def on_key_press(self, event):
        if event.detail == 0:
            return 
        shift = int((event.state & xproto.ModMask.Shift) or (event.state & xproto.ModMask.Lock))
        print self, event.detail, event.state, event.conn, shift
        k = ooxcb.keysyms.keysym_to_str(event.conn.keysyms.get_keysym(event.detail, shift))
        print k

    def on_button_press(self, event):
        print self, "button_press"
        self.grab_input()
        
