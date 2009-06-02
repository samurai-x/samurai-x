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
    Currently, it attempts to load all standard plugins, defines
    two floating desktops, creates some hotkeys and binds the
    left mouse button to the move action, the right mouse button
    to the resize action.
"""

config = {
    'core.plugin_paths': ['~/.samuraix/plugins'],
    'core.plugins': [
        'sxactions',
        'sxdesktops',
        'sxbind',
        'sxcairodeco',
        'sxmoveresize',
        'sxclientbuttons',
        'sxfocus',
        'sxlayoutmgr',
    ],

    'desktops.desktops':
        [('one', {'layout': 'vert'}),
         ('two', {'layout': 'horiz'})]
    ,
    'bind.keys': {
            'Meta+n': 'desktops.cycle offset=1',
            'Meta+p': 'desktops.cycle offset=-1',
            'Meta+c': 'desktops.cycle_clients',
            'Meta+d': 'log message="pressed d"',
            'META+X': 'spawn cmdline="xterm -bg \'#cc0000\'"',
            'META+g': 'spawn cmdline="gimp"',
            'Meta+Q': 'quit',
            'Meta+R': 'restart',
        },
    'decoration.bindings': {
            '1': 'moveresize.move',
            '3': 'moveresize.resize',
        },
    'clientbuttons.bindings': {
            'Meta+1': 'moveresize.move',
            'Meta+3': 'moveresize.resize',
        },
    'cairodeco.height': 15,
    'cairodeco.title.position': "center", # one of "left", "center" or "right"
    'cairodeco.color': '#cc0000',
    'cairodeco.title.color': '#ffffff',
    'cairodeco.title.inactive_color': '#000000',
}

