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

import logging
import weakref
from subprocess import Popen

class Action(object):
    def __init__(self):
        pass

    def __call__(self, screen):
        pass

class Spawn(Action):
    def __init__(self, cmd):
        self.cmd = cmd

    def __call__(self, screen):
        pid = Popen(self.cmd, shell=True).pid

class Quit(Action):
    def __call__(self, screen):
        screen.app.stop()

class NextDesktop(Action):
    def __init__(self):
        pass

    def __call__(self, screen):
        screen.next_desktop()

class PreviousDesktop(Action):
    def __init__(self):
        pass

    def __call__(self, screen):
        screen.previous_desktop()

class MaximizeClient(Action):
    def __init__(self, subject):
        self.subject = subject

    def __call__(self, screen):
        self.subject(screen).toggle_maximize()

class NextClient(Action):
    def __call__(self, screen):
        desktop = screen.active_desktop
        focused = screen.focused_client
        idx = 0
        if focused is not None:
            idx = (desktop.clients.index(weakref.ref(focused)) + 1) % len(desktop.clients)
        desktop.focus_client(desktop.clients[idx]())

class DebugOutput(Action):
    def __init__(self, msg):
        self.msg = msg

    def __call__(self, screen):
        logging.debug(self.msg)

# -- subjects

class Subject(object):
    def __init__(self):
        pass

    def __call__(self, screen):
        raise NotImplementedError()

class FocusedClient(Subject):
    """
        This subject returns the current focused client
        or None if no client is focused.
    """
    def __call__(self, screen):
        return screen.focused_client
