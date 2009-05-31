from __future__ import with_statement

import sys
sys.path.append('../ooxcb')

import ooxcb
from ooxcb import xproto
from ooxcb.contrib import cairo

from yahiko import ui

conn = ooxcb.connect()
screen = conn.setup.roots[conn.pref_screen]
visualtype = screen.get_root_visual_type()
width = 640
height = 480
running = True

with conn.bunch():
    win = xproto.Window.create_toplevel_on_screen(conn, screen,
            width=width, height=height,
            back_pixel=screen.white_pixel,
            event_mask=(0
                | xproto.EventMask.Exposure
                | xproto.EventMask.ButtonPress
                | xproto.EventMask.PointerMotion
                | xproto.EventMask.KeyPress
            )
    )
    win.map()

    # create a surface for this window
    surface = cairo.cairo_xcb_surface_create(conn, win,
            visualtype,
            width, height)
    
    # and a cairo context
    cr = cairo.cairo_create(surface)
    #cairo.cairo_set_operator(cr, cairo.CAIRO_OPERATOR_SOURCE)
    #cairo.cairo_set_source_surface(cr, surface, 0, 0)
    #cairo.cairo_set_source_rgba(cr, 255, 0, 0, 0)


def debug_func(x):
    def f(event):
        print x
    return f


widget = ui.TopLevelContainer(
        x=20, y=20,
        width=420, height=20, 
        style={
            'background': (0.2, 0.2, 0.2),
            'border': {
                'color': (255, 255, 255),
                'width': 1.0,
            },
        },
        layouter=ui.HorizontalLayouter,
)

label_style = {
    'border': {
        'color': (0.8, 0.8, 0.8),
        'width': 0.5, 
    }
}

widget.children.extend([
    ui.Label(text="but 1", style=label_style, on_button_press=debug_func(90)),
    ui.Label(text="but 2", style=label_style, on_button_press=debug_func(91)),
    ui.Label(text="but 3", style=label_style, on_button_press=debug_func(92)),
])
widget.layout()


widget2 = ui.TopLevelContainer(
        x=100, y=100,
        width=60, height=220, 
        style={
            'background': (0.2, 0.2, 0.2),
            'border': {
                'color': (255, 255, 255),
                'width': 1.0,
            },
        },
        layouter=ui.VerticalLayouter,
)

label_style = {
    'border': {
        'color': (0.4, 0.4, 0.8),
        'width': 0.5, 
    }
}


widget2.children.extend([
    ui.Label(text="but 1", style=label_style, on_button_press=debug_func(10)),
    ui.Label(text="but 2", style=label_style, on_button_press=debug_func(11)),
    ui.Label(text="but 3", style=label_style, on_button_press=debug_func(12)),
])
widget2.layout()


@win.event
def on_expose(event):
    widget.render(cr)
    widget2.render(cr)

    conn.flush()

@win.event
def on_button_press(event):
    if widget.hit(event.event_x, event.event_y):
        widget.dispatch_event('on_button_press', event)
    if widget2.hit(event.event_x, event.event_y):
        widget2.dispatch_event('on_button_press', event)

@win.event
def on_key_press(event):
    global running 
    running = False

#@win.event
#def on_motion_notify(event):
#    #print event.event_x, event.event_y

while 1:
    conn.wait_for_event().dispatch()
    if not running:
        break

conn.disconnect()
