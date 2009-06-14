# Copyright (c) 2008-2009, samurai-x.org
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
"""
    This module just contains a default example configuration that will be
    used as fallback if there is no user configuration found.
    You can print this file using `sx-wm --default-config`.
"""

import logging
log = logging.getLogger(__name__)

from pkg_resources import resource_filename as resource

config = {
    # The search paths for plugin packages
    'core.plugin_paths': ['~/.samuraix/plugins'],
    # The list of plugins to load. Sometimes, the order is important!
    'core.plugins': [
        'sxactions',
        'sxdesktops',
        'sxlayoutmgr',
        'sxbind',
        'yahiko_decorator',
        'sxmoveresize',
        'sxclientbuttons',
        'sxfocus',
    ],

    # Here we create 10 desktops. You can find more
    # information about this in the sx-desktops documentation:
    # http://docs.samurai-x.org/samurai-x2/plugins/sx-desktops.html#configuration
    'desktops.desktops':
        [
         ('1', {'layout': 'floating'}),
         ('2', {'layout': 'floating'}),
         ('3', {'layout': 'floating'}),
         ('4', {'layout': 'floating'}),
         ('5', {'layout': 'floating'}),
         ('6', {'layout': 'floating'}),
         ('7', {'layout': 'floating'}),
         ('8', {'layout': 'floating'}),
         ('9', {'layout': 'floating'}),
         ('10', {'layout': 'floating'}),
         ]
    ,
    # Here we can bind keystrokes to actions using the sx-bind plugin.
    # More information about actions:
    # http://docs.samurai-x.org/samurai-x2/plugins/sx-actions.html
    # More information about sx-bind:
    # http://docs.samurai-x.org/samurai-x2/plugins/sx-bind.html
    'bind.keys': {
            'Meta+n': 'desktops.cycle offset=1',
            'Meta+p': 'desktops.cycle offset=-1',
            'meta+X': 'spawn cmdline="xterm"',
            'Meta+Q': 'quit',
            # and shortcuts to reach an arbitrary desktop very fast
            'Meta+1': 'desktops.goto index=1',
            'Meta+2': 'desktops.goto index=2',
            'Meta+3': 'desktops.goto index=3',
            'Meta+4': 'desktops.goto index=4',
            'Meta+5': 'desktops.goto index=5',
            'Meta+6': 'desktops.goto index=6',
            'Meta+7': 'desktops.goto index=7',
            'Meta+8': 'desktops.goto index=8',
            'Meta+9': 'desktops.goto index=9',
            'Meta+0': 'desktops.goto index=10',
        },

    # That is the configuration for the sx-clientbuttons plugin.
    # It makes it possible to press the Meta key and the left
    # mouse button inside a window to move it, and
    # Meta + right mouse button to resize it.
    # More information: http://docs.samurai-x.org/samurai-x2/plugins/sx-clientbuttons.html
    'clientbuttons.bindings': {
            'Meta+1': 'moveresize.move',
            'Meta+3': 'moveresize.resize',
        },

    # Configuration for yahiko_decorator follows.
    # If you click and drag the titlebar with the left mouse button,
    # you move the window. If you click and drag with the right mouse
    # button, you resize it.
    'decorator.title.bindings': {
            '1': 'moveresize.move',
            '3': 'moveresize.resize',
    },

    # Here we create a "Close" button on the left side of the titlebar.
    'decorator.buttons.leftside': [
        {
            'width': 20,
            'style': {
                'text.color': (1.0, 1.0, 1.0),
                'background.style': 'image',
                # This will give us the filename of the graphic file.
                'background.image': resource('yahiko', 'gfx/close.png'),
            },
            # if you click with the left mouse button, the "kill" action
            # is emitted.
            'bindings': {
                '1': 'kill',
            }
        }
    ]
}


