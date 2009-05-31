from ooxcb.eventsys import EventDispatcher

from ooxcb.contrib import cairo

from ctypes import byref


class Window(EventDispatcher):
    def __init__(self, width=None, height=None, style=None, **kwargs):
        self.rx = None
        self.ry = None
        self.rwidth = None
        self.rheight = None
        
        self.width = width
        self.height = height 

        self.style = style

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


Window.register_event_type('on_button_press')


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

    def on_button_press(self, event):
        local_x, local_y = event.event_x - self.rx, event.event_y - self.ry

        for child in self.children:
            if child.hit(local_x, local_y):
                child.dispatch_event('on_button_press', event)


class TopLevelContainer(Container):
    def __init__(self, x=None, y=None, **kwargs):
        Container.__init__(self, **kwargs)
        self.x = x
        self.y = y        

        assert None not in (self.x, self.y, self.width, self.height)

    def layout(self):
        self.rx = self.x
        self.ry = self.y
        self.rwidth = self.width
        self.rheight = self.height
        Container.layout(self)

    def render(self, cr):
        cairo.cairo_save(cr)
        Container.render(self, cr)
        cairo.cairo_restore(cr)


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
    pass
