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

from samuraix.client import Client
from samuraix.plugin import Plugin
from samuraix.rect import Rect

class TilingDesktop(object):
    def __init__(self, plugin, desktop):
        self.plugin = plugin
        self.screen = desktop.screen
        self.desktop = desktop
        self.desktop.push_handlers(
                on_rearrange=self.on_rearrange)
        self.geom = self.screen.get_geometry()
        self.scan()
        self.compute_all()

    def scan(self):
        for client in self.desktop.clients:
            client.push_handlers(on_focus=self.on_focus)
            client.window.push_handlers(on_configure_notify=self.on_configure_notify)

    def on_rearrange(self, desktop):
        self.compute_all()

    def compute_all(self):
        if self.desktop.clients:
            if self.screen.focused_client is None:
                # We always need a focused client.
                self.screen.focus(self.desktop.clients.current())
                return
            geom = self.geom
            cnt = 0
            uheight = geom.height // (max(len(self.desktop.clients) - 1, 1)) # one is focused ;)
            for client in self.desktop.clients:
                client.actor.map()
                if client.is_focused():
                    client.actor.configure(x=0,
                            y=0,
                            width=geom.width // 2 - 1,
                            height=geom.height)
                else:
                    client.actor.configure(x=geom.width//2,
                            y=cnt * uheight,
                            width=geom.width // 2,
                            height=uheight - 1)
                    cnt += 1
            self.plugin.app.conn.flush()

class SXTiling(Plugin):
    key = 'tiling'
    # requires a desktops plugin ...

    def __init__(self, app):
        Plugin.__init__(self)

        self.app = app
        self.desktops = []

        self.app.push_handlers(self)

        self.app.plugins['desktops'].register_layouter('tiling', self)

    def on_load_config(self, config):
        self.desktops = []

    def register_desktop(self, desktop, info):
        # no additional information needed ... yet.
        self.desktops.append(TilingDesktop(self, desktop))
