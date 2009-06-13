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
    sx-autoclient is a plugin that runs a series of commands every time a new client 
    is created. It is usefull for putting certain windows on certain desktops or 
    positioning clients automatically. 

    Configuration
    -------------

    .. attribute:: autoclient.rules

        List of functions to call when a new client is created. 
        For example::
        
            def test_rule(screen, client):
                log.info('test rule!')
                client.actor.configure(x=100, y=100)

            config = {
                # ...
                'autoclient.rules': [test_rule],
            }

"""

from samuraix.plugin import Plugin 

import logging
log = logging.getLogger(__name__)

class SXAutoClient(Plugin):
    def __init__(self, app):
        self.app = app
        app.push_handlers(self)

    def on_load_config(self, config):
        self.config = config 

    def on_ready(self, app):
        for screen in app.screens:
            self.on_add_screen(app, screen)

    def on_add_screen(self, app, screen):
        screen.push_handlers(on_new_client=self.screen_on_new_client)

    def screen_on_new_client(self, screen, client):
        rules = self.config.get('autoclient.rules', [])
        for rule in rules:
            if rule(screen, client):
                return 
        
