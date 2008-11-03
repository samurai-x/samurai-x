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

from time import time as timenow
from select import select

import logging
log = logging.getLogger(__name__)


class ScheduledFunc(object):
    def __init__(self, funcs, when, delay=None):
        self.funcs = funcs
        self.when = when
        self.delay = delay

    def __str__(self):
        return "<ScheduledFunc %s %s %s>" % (self.func, self.when, self.delay)


class Timer(object):
    def __init__(self):
        self.scheduled_funcs = []
        self.select_timeout = 0.5

    def schedule(self, func, when):
        sf = ScheduledFunc(func, when)
        self.scheduled_funcs.append(sf)

    def schedule_repeated(self, func, delay):
        # TODO: check for sf's with same delay and attach func to it
        # instead of creating a new item

        sf = ScheduledFunc([func], timenow()+delay, delay)
        self.scheduled_funcs.append(sf)

    def update(self, fd):
        now = timenow()

        to_remove = []
        for sf in self.scheduled_funcs:
            if now > sf.when:
                for func in sf.funcs:
                    func()
                if sf.delay is not None:
                    sf.when += sf.delay
                else:
                    to_remove.append(sf)

        for sf in to_remove:
            self.scheduled_funcs.remove(sf)

        select([fd], [], [fd], self.select_timeout)

