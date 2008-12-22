# Copyright (c) 2008, samurai-x.org
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the samurai-x.org nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SAMURAI-X.ORG ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL SAMURAI-X.ORG  BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Currently, the samurai-x configuration takes place in a python script.
# You have full access to all python modules in your configuration file,
# so be careful what you do here.

# When samurai-x is loaded, it will look for a file .samuraix in your
# home directory. If there is no such file, samurai-x will use the
# default configuration file which you read currently.

# We need some modules:
import samuraix.xcb.modifiers as mods
# samuraix.xcb.modifiers has some modifier constants you can use:
# MOD_MASK_1 to MOD_MASK_5, MOD_MASK_SHIFT, MOD_MASK_LOCK, MOD_MASK_CONTROL
# The `xmodmap` tool is always helpful.
import samuraix.xcb.keysymdef as keys
# You will most likely only use the XK_a to XK_z constants. 
from samuraix.actions import *

# The `config` variable has to be either a dictionary or
# a callable object that returns a dictionary.
config = {
    # Here we map modifiers + keys to an action.
    # If the modifier and the key are pressed,
    # the action is executed.
    #
    # All actions are defined in samuraix/actions.py.
    'manager.keybindings': {
        # This `Spawn` action executes xterm if
        # Meta-x is pressed.
        (mods.MOD_MASK_4, keys.XK_x): Spawn('xterm'),
        # Meta-q quits samurai-x
        (mods.MOD_MASK_4, keys.XK_q): Quit(),
        # Meta-n switches to the next desktop
        (mods.MOD_MASK_4, keys.XK_n): NextDesktop(),
        # Meta-p switches to the previous desktop
        (mods.MOD_MASK_4, keys.XK_p): PreviousDesktop(),
        # This action takes a so-called `Subject` as first argument
        # which specifies the target of the action.
        # However, currently only the `FocusedClient` subject is
        # available.
        # So: Meta-m maximizes (or minimizes) the currently 
        # focused client.
        (mods.MOD_MASK_4, keys.XK_m): MaximizeClient(FocusedClient()),
        # Meta-Tab cycles the clients of the current desktop.
        (mods.MOD_MASK_4, keys.XK_Tab): NextClient(),
    },

    # Here we map a modifier and a button to an action.
    # This action will occur if the user clicks into a
    # window having the modifiers and the mouse button
    # pressed.
    # There are some actions you can use only for button
    # bindings, but you can use all actions which are suitable
    # for key bindings also for button bindings.
    'manager.client.buttonbindings': {
        # Meta and 1st mouse button lets the user move
        # the window he clicked into.
        (mods.MOD_MASK_4, 1): Move(),
        # Meta and 3rd mouse button lets the user resize
        # the window he clicked into.
        (mods.MOD_MASK_4, 3): Resize(),
        # Another example:
        # Meta and 2nd mouse button spawns xterm
        #(mods.MOD_MASK_4, 2): Spawn('xterm'),
    },
    
    # You can specify an image file (currently .svg and .png
    # supported) for the root window background.
    #'manager.root_background_image': '/path/to/image/file',

    # You can also specify a color for the root background.
    # Default color is #000000
    #'manager.root_background_color': '#ffffff',

    # Sets the color of the frame background (in hexadecimal
    # rgb notation). Default: #cc0000
    #'manager.client.frame.background_color': '#0000ff',

    # Sets the font color of the frame title (the
    # window title). Default: #ffffff
    #'manager.client.frame.title_color': '#000000',

    # Finally, 'manager.desktops' holds a list
    # of desktop names. Here we define three desktops.
    'manager.desktops': [
        'some', 
        'more', 
        'desktops',
    ],

}
