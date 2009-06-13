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
    sx-help is a plugin that creates the 'help' action. 

    Actions
    -------
    
    .. function:: help
        :module:
        
        Show help

"""

import os

import logging
log = logging.getLogger(__name__)

from samuraix import config
from samuraix.plugin import Plugin

from sxactions import ActionInfo


class SXHelp(Plugin):
    """ Plugin to show "first time help" and create and action to reshow that help """

    key = 'help'

    def __init__(self, app):
        self.app = app
        app.push_handlers(self)

        app.plugins['actions'].register('help', self.show_help)

    def on_ready(self, app):
        firsttimefile = config.get('help.first_time_file', 
                os.path.expanduser('~/.samuraix/firsttime')
        )
    
        if os.path.exists(firsttimefile) or config.get('help.no_first_time', False):
            return 
        else: 
            filedir = os.path.dirname(firsttimefile)
            if not os.path.exists(filedir):
                os.makedirs(filedir)
            open(firsttimefile, 'w').write('hello')
            self.show_help()

    def show_help(self):
        url = config.get('help.url', 'http://samurai-x.org/wiki/UserManual')
        self.app.plugins['actions'].emit('spawn', 
            ActionInfo(cmdline='firefox %s' % url)
        )
        
    
