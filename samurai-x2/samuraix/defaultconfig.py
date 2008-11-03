import samuraix.xcb.modifiers as mods
import samuraix.xcb.keysymdef as keys
from samuraix.actions import * # EVIL!!

config = {
        'manager.keybindings':
            {
                (mods.MOD_MASK_4, keys.XK_x): Spawn('xterm'),
                (mods.MOD_MASK_4, keys.XK_q): Quit(),
                (mods.MOD_MASK_4, keys.XK_n): NextDesktop(),
                (mods.MOD_MASK_4, keys.XK_p): PreviousDesktop(),
                (mods.MOD_MASK_4, keys.XK_m): MaximiseClient(),
            },
        'manager.desktops':
            ['some', 'more', 'desktops']
        }
