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
    sx-clientbuttons is a plugin that enables you to bind mouse button 
    and modifier key combinations to an action.

    Configuration
    -------------

    .. attribute:: clientbuttons.bindings

        Dictionary of button/modifier : action. 
        For example::
    
            'clientbuttons.bindings': {
                'Meta+1': 'moveresize.move',
                'Meta+3': 'moveresize.resize',
            }

"""

import logging
log = logging.getLogger(__name__)

from samuraix import config
from samuraix.plugin import Plugin
from samuraix.util import parse_buttonstroke

from ooxcb.xproto import EventMask
from ooxcb import xproto

from sxactions import ActionInfo


class SXClientButtons(Plugin):
    """ Plugin to allow binding mouse actions to actions """

    key = 'clientbuttons'

    def __init__(self, app):
        self.app = app
        app.push_handlers(self)
        self.bindings = {}

    def on_load_config(self, config):
        for stroke, action in config.get('clientbuttons.bindings', {}).iteritems():
            buttonstroke = parse_buttonstroke(stroke)
            self.bindings[buttonstroke] = action

    def on_ready(self, app):
        for screen in app.screens:
            screen.push_handlers(self)

            for client in screen.clients:
                self.on_new_client(screen, client)

    def on_new_client(self, screen, client):
        def on_button_press(evt):
            stroke = (evt.state, evt.detail)
            if stroke in self.bindings:
                info = ActionInfo(screen=self.app.get_screen_by_root(evt.root),
                    x=evt.event_x, y=evt.event_y,
                    client=client)
                self.app.plugins['actions'].emit(self.bindings[stroke], info)

        # grab the specific button and modifier to allow the app to keep working!
        for modifier, button in self.bindings.iterkeys():
            client.actor.grab_button(EventMask.ButtonPress,
                button,
                modifier,
                False,
                xproto.GrabMode.Sync,
                xproto.GrabMode.Sync
            )

        client.actor.push_handlers(on_button_press=on_button_press)

    def on_unmanage_client(self, screen, client):
        # tidy up properly, but only if the actor exists
        if client.actor.valid:
            for modifier, button in self.bindings.iterkeys():
                client.actor.ungrab_button(button, modifier)


