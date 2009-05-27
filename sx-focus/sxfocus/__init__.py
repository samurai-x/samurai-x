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

import logging
log = logging.getLogger(__name__)

from samuraix import config
from samuraix.plugin import Plugin

from ooxcb.xproto import EventMask
from ooxcb import xproto

from sxactions import ActionInfo

class FocusStyle(object):
    def __init__(self, plugin, client):
        self.plugin = plugin
        self.client = client


class ClickToFocus(FocusStyle):
    def __init__(self, plugin, client):
        FocusStyle.__init__(self, plugin, client)
        client.push_handlers(self)
        client.window.push_handlers(self)

    def bind_focus(self):
        self.client.window.grab_button(EventMask.ButtonPress,
            xproto.ButtonIndex._1,
            0,
            False,
            xproto.GrabMode.Sync,
            xproto.GrabMode.Sync
        )

    def unbind_focus(self):
        self.client.window.ungrab_button(xproto.ButtonIndex._1, 0)

    def on_button_press(self, evt):
        # make sure the state is 0 to not interfere with the client-buttons 
        # plugin
        if evt.state == 0 and not self.client.is_focused():
            # That is the most important line. Here we remove the active
            # grab that has been activated, and resend the button press
            # event. So, if the user clicks inside a window, this click
            # doesn't get "lost", but is handled by the window, after
            # it got focused. That is what most users would expect.
            # TODO: should we do that configurable?
            self.client.conn.core.allow_events(xproto.Allow.ReplayPointer)
            self.client.screen.focus(self.client)

    def on_focus(self, c):
        self.unbind_focus()     

    def on_blur(self, c):
        self.bind_focus()


class SloppyFocus(ClickToFocus):
    def __init__(self, plugin, client):
        ClickToFocus.__init__(self, plugin, client)
        client.actor.change_attributes(
                event_mask=client.actor.get_attributes().reply().your_event_mask | EventMask.EnterWindow | EventMask.LeaveWindow)

        client.actor.push_handlers(self)
    
    def on_enter_notify(self, evt):
        self.client.focus(bring_forward=False)
        # do we need this? im not sure...
        #self.client.conn.core.allow_events(xproto.Allow.ReplayPointer)


class SloppyFocusWithAutoRaise(SloppyFocus):
    def on_enter_notify(self, evt):
        self.client.focus(bring_forward=True)
        # do we need this? im not sure...
        #self.client.conn.core.allow_events(xproto.Allow.ReplayPointer)


class SXFocus(Plugin):
    """ Plugin for various styles of mouse focusing """

    key = 'focus'

    styles = {
        'click': ClickToFocus,
        'sloppy': SloppyFocus, 
        'sloppy-autoraise': SloppyFocusWithAutoRaise, 
    }

    def __init__(self, app):
        self.app = app
        app.push_handlers(self)

    def on_load_config(self, config):
        self.focus_method = self.styles[config.get('focus.style', 'click')]

    def on_ready(self, app):
        for screen in app.screens:
            screen.push_handlers(self)

            for client in screen.clients:
                self.on_new_client(screen, client)

    def on_new_client(self, screen, client):
        style = self.focus_method(self, client)

    def on_unmanage_client(self, screen, client):
        # TODO.. tidy up properly
        pass

        
