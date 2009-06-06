from __future__ import with_statement

import copy

import sys
sys.path.append('../ooxcb')

import ooxcb
from ooxcb import xproto
from ooxcb.contrib import cairo

from yahiko import ui

conn = ooxcb.connect()
screen = conn.setup.roots[conn.pref_screen]
visualtype = screen.get_root_visual_type()
width = 300
height = 25
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
                | xproto.EventMask.PropertyChange
                | xproto.EventMask.StructureNotify
            )
    )
    win.map()

    ## create a surface for this window
    #surface = cairo.cairo_xcb_surface_create(conn, win,
    #        visualtype,
    #        width, height)
    
    ## and a cairo context
    #cr = cairo.cairo_create(surface)
    #cairo.cairo_set_operator(cr, cairo.CAIRO_OPERATOR_SOURCE)
    #cairo.cairo_set_source_surface(cr, surface, 0, 0)
    #cairo.cairo_set_source_rgba(cr, 255, 0, 0, 0)

@win.event
def on_key_press(event):
    if event.detail == 9:
        global running 
        running = False
        print event.detail, event.state

def debug_func(x):
    def f(event):
        print x
    return f


widget = ui.TopLevelContainer(
        win,
        visualtype,
        style={
            'background': {
                'color': (0.2, 0.2, 0.2),
            },
            'border': {
                'color': (255, 255, 255),
                'width': 1.0,
            },
            'layout': {
                'padding': 5,
            },
        },
        layouter=ui.HorizontalLayouter,
)

def prompt_return(sender):
    print sender.text
    global running 
    running = False

    import dbus

    bus = dbus.SessionBus()

    remote_object = bus.get_object("org.samuraix.ControlService",
                                   "/ControlObject")
    iface = dbus.Interface(remote_object, "org.samuraix.ControlInterface")
    iface.action('spawn cmdline="%s"' % sender.text)


prompt = ui.Input(
        text="", 
        on_button_press=debug_func('but3'),
        style={
            #'border': {
            #    'color': (0.8, 0.8, 0.8),
            #    'width': 0.5, 
            #},
            'background': {
                'color': (0.7, 0.6, 0.6),
            },
            'text': {
                'color': (0.6, 0, 0),
                'size': 12,
                'align': 'left',
            },
        },
        on_return=prompt_return,
)

widget.add_child(prompt)
widget.layout()

prompt.grab_input()



while 1:
    conn.wait_for_event().dispatch()
    if not running:
        break

conn.disconnect()
