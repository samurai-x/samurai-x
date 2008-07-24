from pyglet.window.xlib import xlib

from samuraix import keysymdef
from samuraix.testfunc import testfunc
from samuraix.statusbar import StatusBar
from samuraix.userfuncs import *


config = {
    'focus': {
        'model': 'sloppy',
        'new': True,
    },

    'screens': {
        'default': {

            'virtual_desktops': [
                {'name': 'one'},
                {'name': 'two'},
                {'name': 'three'},
            ],

            'widgets': [
                {
                    'name': 'statusbar',
                    'class': StatusBar,
                    'color': (0.7, 0.0, 0.0),
                    'text-color': (1.0, 1.0, 1.0)
                },
            ],

            'keys': {
                (keysymdef.XK_Return, xlib.Mod4Mask): 
                    spawn("xterm"),
                (keysymdef.XK_g, xlib.Mod4Mask):
                    spawn("gimp"),

                (keysymdef.XK_F2, xlib.Mod4Mask):
                    spawn("./samurai-runner"),

                (keysymdef.XK_Page_Up, xlib.Mod4Mask):
                    spawn("amixer -c 0 set Master 2dB+"),
                (keysymdef.XK_Page_Down, xlib.Mod4Mask):
                    spawn("amixer -c 0 set Master 2dB-"),
                (keysymdef.XK_End, xlib.Mod4Mask):
                    spawn("amixer -c 0 set Master 0dB+ toggle"),
                
                (keysymdef.XK_l, xlib.Mod4Mask):
                    spawn("xlock -mode biof"),

                (keysymdef.XK_1, xlib.Mod4Mask): 
                    screenfunc('set_active_desktop_by_index', 0),
                (keysymdef.XK_2, xlib.Mod4Mask):
                    screenfunc('set_active_desktop_by_index', 1),
                (keysymdef.XK_3, xlib.Mod4Mask):
                    screenfunc('set_active_desktop_by_index', 2),
                (keysymdef.XK_4, xlib.Mod4Mask):
                    screenfunc('set_active_desktop_by_index', 3),
                (keysymdef.XK_5, xlib.Mod4Mask):
                    screenfunc('set_active_desktop_by_index', 4),
                (keysymdef.XK_6, xlib.Mod4Mask):
                    screenfunc('set_active_desktop_by_index', 5),
                (keysymdef.XK_7, xlib.Mod4Mask):
                    screenfunc('set_active_desktop_by_index', 6),
                (keysymdef.XK_8, xlib.Mod4Mask):
                    screenfunc('set_active_desktop_by_index', 7),
                (keysymdef.XK_9, xlib.Mod4Mask):
                    screenfunc('set_active_desktop_by_index', 8),

                (keysymdef.XK_Right, xlib.Mod4Mask):
                    screenfunc('next_desktop'),
                (keysymdef.XK_Left, xlib.Mod4Mask):
                    screenfunc('prev_desktop'),

                (keysymdef.XK_m, xlib.Mod4Mask):
                    focusedwindowfunc('toggle_maximise'),               
            },
            'buttons': {
                (3, 0): testfunc,
                (1, 0): testfunc, 
            },
        },
    },

    'client': {
        'buttons': {
            (1, xlib.Mod4Mask): clientfunc('mousemove'),
            (3, xlib.Mod4Mask): clientfunc('mouseresize'), 
        }
    },
        
}

