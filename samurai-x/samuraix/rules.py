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

from samuraix.rect import Rect

import logging 
log = logging.getLogger(__name__)

class Rule(object):
    def match(self, client):
        return False


class TitleRule(object):
    def __init__(self, title):
        self.title = title
    def match(self, client):
        log.debug('titlematch %s %s' % (client.title, self.title))
        return client.title == self.title 


def move_to_desktop_two(client):
    client.move_to_desktop(client.screen.desktops['two'])

def move_to_100_100(client):
    geom = Rect(100, 100, 100, 100)
    client.resize(geom)


class Rules(object):
    def __init__(self, screen):
        self.screen = screen 
        screen.push_handlers(self)

        self.rules = [
            (TitleRule("Terminal"), move_to_100_100),
        ]

    def on_client_add(self, client):
        for rule, cb in self.rules:
            if rule.match(client):
                cb(client)
