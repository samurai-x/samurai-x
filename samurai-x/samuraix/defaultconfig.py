from pyglet.window.xlib import xlib

from samuraix import keysymdef
from samuraix.testfunc import testfunc
from samuraix.statusbar import StatusBar
from samuraix.userfuncs import *

default_mod = xlib.Mod4Mask

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
                    'text-color': (1.0, 1.0, 1.0),
                    'clock-format': "%a %d/%m/%y %H:%M",
                    'padding-left': 10,
                    'padding-right': 10,
                    'text-y': 10, 
                    'font': 'snap',
                    'font-size': 10,
                },
            ],

            'background': {
                'color': "000000",
                'image': "/home/dunk/projects/samurai-x/gfx/samuraix.svg",
            },

            'keys': {
                (keysymdef.XK_Return, default_mod): 
                    spawn("xterm"),
                (keysymdef.XK_g, default_mod):
                    spawn("gimp"),

                (keysymdef.XK_F2, default_mod):
                    spawn("./sx-runner"),

                (keysymdef.XK_Page_Up, default_mod):
                    spawn("amixer -c 0 set Master 2dB+"),
                (keysymdef.XK_Page_Down, default_mod):
                    spawn("amixer -c 0 set Master 2dB-"),
                (keysymdef.XK_End, default_mod):
                    spawn("amixer -c 0 set Master 0dB+ toggle"),
                
                (keysymdef.XK_l, default_mod):
                    spawn("xlock -mode biof"),

                (keysymdef.XK_1, default_mod): 
                    screenfunc('set_active_desktop_by_index', 0),
                (keysymdef.XK_2, default_mod):
                    screenfunc('set_active_desktop_by_index', 1),
                (keysymdef.XK_3, default_mod):
                    screenfunc('set_active_desktop_by_index', 2),
                (keysymdef.XK_4, default_mod):
                    screenfunc('set_active_desktop_by_index', 3),
                (keysymdef.XK_5, default_mod):
                    screenfunc('set_active_desktop_by_index', 4),
                (keysymdef.XK_6, default_mod):
                    screenfunc('set_active_desktop_by_index', 5),
                (keysymdef.XK_7, default_mod):
                    screenfunc('set_active_desktop_by_index', 6),
                (keysymdef.XK_8, default_mod):
                    screenfunc('set_active_desktop_by_index', 7),
                (keysymdef.XK_9, default_mod):
                    screenfunc('set_active_desktop_by_index', 8),

                (keysymdef.XK_Right, default_mod):
                    screenfunc('next_desktop'),
                (keysymdef.XK_Left, default_mod):
                    screenfunc('prev_desktop'),

                (keysymdef.XK_m, default_mod):
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
            (1, default_mod): clientfunc('mousemove'),
            (3, default_mod): clientfunc('mouseresize'), 
        }
    },
        
}

