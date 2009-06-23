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
import ooxcb.contrib.cursors

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
        self.synchronous_check = False

        self.replace_existing_wm = False
        self.running = False
        self.cursors = None
        self.screens = []
        self.plugins = None
        # filehandles used when select'ing 
        self.fds = {'read': {}, 'write': {}, 'error': {}}
        # timeout used when select'ing
        self.select_timeout = 1.0
       
        # this is really set in self.init()
        self.supported_hints = None


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

    def init(self):
        """
            This method establishes a connection to the X server and turns on
            the synchronous checks if self.synchronous_check is True
            (that means that you get X exceptions
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

            :todo: allow the user to specify the X connection string. Maybe he
                   wants to connect to a foreign display without changing the
                   DISPLAY environment variable?

        """
        log.info('init')

        self.conn = ooxcb.connect()

        # set of hints we support - plugins can add to this set 
        # if they add support for other hints 
        # hints will only be set by the app when a screen is added
        # so if you alter this after the screens have been set 
        # you will need to call 
        atoms = self.conn.atoms
        self.supported_hints = set([
            atoms['_NET_SUPPORTED'],
            atoms['_NET_CLIENT_LIST'],
            atoms['_NET_ACTIVE_WINDOW'], # client.py
            atoms['_NET_SUPPORTING_WM_CHECK'], # screen.py
            #atoms['_NET_CLOSE_WINDOW'],

            atoms['_NET_WM_NAME'],
            atoms['_NET_WM_VISIBLE_NAME'],
            atoms['_NET_WM_ICON_NAME'],
            atoms['_NET_WM_DESKTOP'],
            atoms['_NET_WM_WINDOW_TYPE'],
            atoms['_NET_WM_WINDOW_TYPE_NORMAL'],
            atoms['_NET_WM_WINDOW_TYPE_DOCK'],
            atoms['_NET_WM_WINDOW_TYPE_SPLASH'],
            atoms['_NET_WM_WINDOW_TYPE_DIALOG'],
            atoms['_NET_WM_STATE'],
            atoms['_NET_WM_STATE_STICKY'],
            atoms['_NET_WM_STATE_SKIP_TASKBAR'],
            atoms['_NET_WM_STATE_FULLSCREEN'],

            atoms['UTF8_STRING'],

            # We are not using the reparenting-to-a-fakeroot technique
            # described in the netwm standard,
            # so we don't need to set _NET_VIRTUAL_ROOTS.
            # TODO: ... do we need to set _NET_DESKTOP_LAYOUT? Are we a pager?
        ])

        # add the xcb file handles to the list of handles we select 
        fd = self.conn.get_file_descriptor()
        self.add_fd_handler('read', fd, self.do_xcb_events) 

        if self.synchronous_check:
            self.conn.synchronous_check = True

        self.cursors = ooxcb.contrib.cursors.Cursors(self.conn)

        self.conn.push_handlers(self)
        self.running = False
        self.plugins = PluginLoader(self)
        self.plugins.setup()
        self.plugins.require_key('desktops') # we need a desktop manager plugin

        self.reload_config()

        setup = self.conn.get_setup()

        log.debug("found %d screens" % setup.roots_len)

        for i in range(setup.roots_len):
            scr = Screen(self, i)
            # add to the list of screens 
            self.screens.append(scr)
            self.dispatch_event('on_new_screen', scr)

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGHUP, self.stop)

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

        self.conn.disconnect()

    def do_xcb_events(self):
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
                ev.atom.get_name().reply().name)

    def on_screen_new(self, screen):
        # set the supported hints 
        screen.set_supported_hints(self.supported_hints)

App.register_event_type('on_load_config')
App.register_event_type('on_new_screen')
App.register_event_type('on_ready')
