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

import sys
import signal
from select import select

import ooxcb
import ooxcb.cursors

from .screen import Screen
from .pluginsys import PluginLoader
from .base import SXObject

class App(SXObject):
    """
        The samurai-x application object is the central point of the
        window manager. There is only one instance of `App` in one
        samurai-x process and it handles the connection to the X server,
        the event loop and the plugin loading process.

        Every builtin samurai-x object should have an `app` member you
        can access.
    """
    def __init__(self):
        """
            __init__ just initializes the application with some placeholder
            members. The real initialization is done in `App.init`.
        """
        SXObject.__init__(self)

        self.conn = None
        self.cursors = None
        self.running = False
        self.screens = []
        self.plugins = None

    def init(self):
        """
            This method establishes a connection to the X server and turns on
            the synchronous checks (that means that you get X exceptions
            synchronously). The rest:

             * It loads all plugins and checks if there is a plugin providing
               the required 'desktop' key.
             * It gets all screens, creates `Screen` instances and dispatches
               the 'on_new_screen' on self.
             * It configures signal handlers for SIGINT, SIGTERM, SIGHUP (all
               these signals will gracefully shut down samurai-x)
             * It calls `self.reload_config()` that initially loads the config
               and dispatches 'on_load_config'
             * It dispatches 'on_ready'
             * It calls `scan` on each Screen to make it scan for children.

            :todo: turn out the synchronous check (that slows down everything a
                   bit)
            :todo: allow the user to specify the X connection string. Maybe he
                   wants to connect to a foreign display without changing the
                   DISPLAY environment variable?

        """
        self.conn = ooxcb.connect()
        self.conn.synchronous_check = True # HAR HAR HAR, SO EVIL
        self.cursors = ooxcb.cursors.Cursors(self.conn)

        self.conn.push_handlers(self)
        self.running = False
        self.plugins = PluginLoader(self)
        self.plugins.setup()
        self.plugins.require_key('desktops') # we need a desktop manager plugin

        setup = self.conn.get_setup()

        log.debug("found %d screens" % setup.roots_len)

        for i in range(setup.roots_len):
            scr = Screen(self, i)
            self.dispatch_event('on_new_screen', self, scr)
            self.screens.append(scr)

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGHUP, self.stop)

        self.reload_config()
        self.dispatch_event('on_ready', self)

        # scan the screens after everything is done.
        # plugin's event handlers will be called then.
        # I hope that has no side effects for existing plugins :)
        for screen in self.screens:
            screen.scan()

    def reload_config(self):
        """
            (Re)load the config and dispatch the 'on_load_config' event with
            the new configuration as the first argument. All plugins should
            reload their configuration variables when receiving that,
            although we have to think a bit about the way we want to
            realize that :)

            :todo: `config` is not really re-loaded yet. That should really be
                    fixed.
        """
        from samuraix import config # TODO?
        self.dispatch_event('on_load_config', config)

    def stop(self, *args):
        """
            Stop samurai-x. Call `unmanage_all` on each screen and
            set `self.running` to False.
            This method takes no arguments. *\*args* is just here that
            we can use `stop` directly as signal handler.
        """
        log.info('Unmanaging all remaining clients ...')
        for screen in self.screens:
            screen.unmanage_all()
        self.conn.flush()
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

        fd = self.conn.get_file_descriptor()

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
            log.debug('selecting...')
            try:
                select([fd], [], [fd], 1.0)
            except Exception, e:
                # error 4 is when a signal has been caught
                if e.args[0] == 4:
                    pass
                else:
                    log.exception(str((e, type(e), dir(e), e.args)))
                    raise

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
                        log.debug('Dispatching %s to %s.' %
                                (ev.event_name, ev.event_target))
                        ev.dispatch()
                    except Exception, e:
                        log.exception(e)

        self.conn.disconnect()

    def get_screen_by_root(self, root):
        """
            return the `Screen` instance for the given
            root window *root* or None if there is no screen found.
        """
        for screen in self.screens:
            # windows are cached, so we can use identity comparison
            if screen.root is root:
                return screen
        return None

    def on_property_notify(self, ev):
        """
            Event handler for the property notify event.
            That just writes a message to the log for now.
        """
        log.info('Got a property notify event ... %s' % \
                ev.atom.get_name().reply().name.to_string())

App.register_event_type('on_load_config')
App.register_event_type('on_new_screen')
App.register_event_type('on_ready')
