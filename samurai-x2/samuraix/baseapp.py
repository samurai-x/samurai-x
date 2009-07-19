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

import sys
import signal
from time import time 
from select import select

import ooxcb
import ooxcb.contrib.cursors

from samuraix.base import SXObject

import logging
log = logging.getLogger(__name__)


class Timer(object):
    """ 
        timer object used internally - you shouldnt change attributes 
        of this unless you know what your doing!
    """

    __slots__ = ['app', 'func', 'interval', 'call_time', 'repeat']

    def __init__(self, app, func, interval, repeat=False):
        self.app = app
        self.func = func
        self.interval = interval
        self.call_time = time() + interval
        self.repeat = repeat

    def cancel(self):
        self.app.remove_timer(self)


class BaseApp(SXObject):
    def __init__(self, synchronous_check=False):
        """
            __init__ just initializes the application with some placeholder
            members. The real initialization is done in `App.init`.
        """
        SXObject.__init__(self)

        self.conn = None
        self.cursors = None
        self.synchronous_check = synchronous_check

        self.running = False

        # filehandles used when select'ing 
        self.fds = {'read': {}, 'write': {}, 'error': {}}
        # timeout used when select'ing
        self.select_timeout = None

        # timer callbacks
        self.timers = []

        # a list of functions that should be called in the next
        # iteration of the mainloop. That's not nice and should
        # be removed. Currently, it's used to make the Python gc
        # collect client objects.
        self.functions_to_call = []

    def add_fd_handler(self, which_list, fd, callback):
        """ 
            add a callback to be called when the main loop detects a
            read/write/error on the file descriptor fd
        """
        assert which_list in ('read', 'write', 'error')
        self.fds[which_list][fd] = callback

    def remove_fd_handler(self, which_list, fd):
        """
            remove a callback to be called when the main loop detects
            a read/write/error on the file descriptor fd
        """
        assert which_list in ('read', 'write', 'error')
        del self.fds[which_list][fd]

    def add_timer(self, func, interval, repeat=False):
        """ 
            add a callback `func` to be called every `seconds` seconds 
            returns a Timer object
        """
        t = Timer(self, func, interval, repeat=repeat)
        self.timers.append(t)
        self.timers.sort(key=lambda t: t.call_time)
        if self.select_timeout is None:
            self.select_timeout = interval
        else:
            self.select_timeout = min(self.select_timeout, interval)
        log.debug('select_timeout is now %s', self.select_timeout)
        return t

    def remove_timer(self, timer):
        """ 
            remove the timer `timer` from the list of timers. 
            `timer` is the object returned by add_timer 
        """
        self.timers.remove(timer)
        # TODO should this take into account the current time?
        # there might be a timeout in less than this...
        # it might just not matter at all 
        if self.timers:
            self.select_timeout = min(t.interval for t in self.timers)
        else:
            self.select_timeout = None

    def init(self):
        """
            This method establishes a connection to the X server and turns on
            the synchronous checks if self.synchronous_check is True
            (that means that you get X exceptions
            synchronously). The rest:

             * It configures signal handlers for SIGINT, SIGTERM, SIGHUP (all
               these signals will gracefully shut down samurai-x)

        """
        log.info('init')

        self.conn = ooxcb.connect()

        # add the xcb file handles to the list of handles we select 
        fd = self.conn.get_file_descriptor()
        self.add_fd_handler('read', fd, self.do_xcb_events) 

        if self.synchronous_check:
            self.conn.synchronous_check = True

        self.cursors = ooxcb.contrib.cursors.Cursors(self.conn)

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGHUP, self.stop)

    def stop(self, *args):
        """
            Stop samurai-x. Call `unmanage_all` on each screen and
            set `self.running` to False.
            This method takes no arguments. *\*args* is just here that
            we can use `stop` directly as signal handler.
        """
        log.info('stopping')
        self.running = False

    def run(self):
        """
            Start the mainloop. It uses `select` to poll the file descriptor
            for events and dispatches them.
            All exceptions are caught and logged, so samurai-x won't crash.
            If `self.running` is False for some reason, samurai-x will
            disconnect and stop.
        """
        self.running = True

        # process any events that are waiting first
        while True:
            try:
                ev = self.conn.poll_for_event()
            except Exception, e:
                log.exception(e)
            else:
                if ev is None:
                    break
                try:
                    ev.dispatch()
                except Exception, e:
                    log.exception(e)

        while self.running:
            #log.debug('selecting...')
            try:
                rready, wready, xready = select(
                        self.fds['read'].keys(),
                        self.fds['write'].keys(),
                        self.fds['error'].keys(),
                        self.select_timeout
                )
            except Exception, e:
                # error 4 is when a signal has been caught
                if e.args[0] == 4:
                    pass
                else:
                    log.exception(str((e, type(e), dir(e), e.args)))
                    raise
            else:
                # should catch errors in these?
                for fd in rready:
                    self.fds['read'][fd]()
                for fd in wready:
                    self.fds['write'][fd]()
                for fd in xready:
                    self.fds['error'][fd]()

            # run any timers that need to be run 
            if self.timers:
                now = time()
                to_remove = []
                should_sort = False
                for timer in self.timers:
                    if timer.call_time < now:
                        timer.func()
                        if timer.repeat:
                            timer.call_time = now + timer.interval
                            should_sort = True
                        else:
                            to_remove.append(timer)
                    # timers are sorted so we can quit early 
                    else:
                        break
                if to_remove:
                    for timer in to_remove:
                        self.timers.remove(timer)
                    # TODO see the note in remove_timer
                    if self.timers:
                        self.select_timeout = min(t.interval for t in self.timers)
                    else:
                        self.select_timeout = None
                    log.debug('select_timeout is now %s', self.select_timeout)
                if should_sort:
                    self.timers.sort(key=lambda t: t.call_time)

        self.conn.disconnect()

    def add_function_to_call(self, func):
        """
            add a function that should be called in the next
            mainloop iteration.

            .. note:: Don't use that if you can avoid it,
                      it might be removed.

        """
        self.functions_to_call.append(func)

    def do_xcb_events(self):
        # process all "functions to call". That seems to be required
        # to be done outside the loop, otherwise `gc.collect()` (see
        # samuraix.screen.Screen.unmanage) won't work - no idea why.
        if self.functions_to_call:
            for func in self.functions_to_call:
                func()
            self.functions_to_call = []

        # might as well process all events in the queue...
        while True:
            try:
                ev = self.conn.poll_for_event()
            except Exception, e:
                log.exception(e)
            else:
                if ev is None:
                    break
                try:
                    #log.debug('Dispatching %s to %s.' %
                    #        (ev.event_name, ev.event_target))
                    ev.dispatch()
                except Exception, e:
                    log.exception(e)



