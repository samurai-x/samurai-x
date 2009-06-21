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
import weakref

from ooxcb import timestamp
from ooxcb.protocol import xproto
from ooxcb.protocol.xproto import EventMask
from ooxcb.list import List
from ooxcb.contrib.sizehints import SizeHints

from .rect import Rect
from .base import SXObject
from .util import ClientMessageHandlers

NET_WM_STATE_REMOVE = 0
NET_WM_STATE_ADD = 1
NET_WM_STATE_TOGGLE = 2

class Client(SXObject):
    """
        A client is managing an X top-level window. samurai-x2 has the concept
        of windows and actors.

        :todo: explain / link to explanation

        .. data:: all_clients

            A list of all available :class:`Client` instances.

        .. data:: window_2_client_map

            A :class:`weakref.WeakValueDictionary` mapping
            :class:`ooxcb.xproto.Window` objects to :class:`Client`
            instances.

        .. attribute:: actor

            The actor window, as explained in the :ref:`client-concept`.

        .. attribute:: window

            The foreign top-level window, as explained in the
            :ref:`client-concept`.

    """
    all_clients = []
    window_2_client_map = weakref.WeakValueDictionary()

    @classmethod
    def get_by_window(cls, window):
        """
            returns the :class:`Client` instance for the given *window*
            or None if there is no client managing *window*.
        """
        return cls.window_2_client_map.get(window)

    def __init__(self, screen, window, geometry):
        """
            :Parameters:
                `screen` : :class:`samuraix.screen.Screen`
                    The samurai-x2 screen the client belongs
                    to
                `window` : :class:`ooxcb.xproto.Window`
                    The foreign top-level window the client
                    will manage
                `geometry`:
                    An object having `x`, `y`, `width` and
                    `height` members describing *window*'s
                    geometry. That's mostly because we don't
                    want to send more X requests out than
                    we have to.
        """
        SXObject.__init__(self)

        self.conn = window.conn
        self.app = screen.app
        self.geom = Rect.from_object(geometry)
        self.client_message_handlers = ClientMessageHandlers()
        self.install_handlers()

        self.state = set() # a set of Atom instances, values for _NET_WM_STATE
        self.protocols = set() # a set of Atom instances, values for WM_PROTOCOLS
        self.wm_hints = None
        self.screen = screen
        self.window = window
        self.window.valid = True

        self.actor = window
        self.window.push_handlers(self)
        log.info('New client: Client=%s Window=%s Actor=%s' % (self, self.window, self.actor))

        self.window.change_attributes(
                event_mask =
                    EventMask.StructureNotify |
                    EventMask.PropertyChange
        )

        self.all_clients.append(self)
        self.window_2_client_map[self.window] = self

        self.update_protocols()
        self.apply_normal_hints()
        self.conn.flush()

    def __repr__(self):
        return '<Client at 0x%x for %s>' % (id(self), repr(self.window))

    def is_focused(self):
        """
            returns True if self is its screen's focused client
        """
        return self.screen.focused_client is self

    def add_net_wm_state(self, name):
        """
            add the atom with the name *name* to the list
            of states for _NET_WM_STATE.
        """
        self.state.add(self.conn.atoms[name])

    def remove_net_wm_state(self, name):
        """
            remove the atom with the name *name* from the list
            of states for _NET_WM_STATE.
            Catch errors.
        """
        try:
            self.state.remove(self.conn.atoms[name])
        except KeyError:
            pass

    def update_protocols(self):
        """
            get the WM_PROTOCOLS property from the window and update
            :attr:`protocols`.
        """
        prop = self.window.get_property('WM_PROTOCOLS', 'ATOM').reply()
        if prop.exists:
            self.protocols = set(prop.value.to_atoms())
        else:
            self.protocols = set()

    def kill(self):
        """
            kill the client. If :attr:`protocols` contains
            `WM_DELETE_WINDOW`, send such a client message, otherwise,
            use :meth:`kill_client <ooxcb.xproto.Window.kill_client>`.
        """
        if self.conn.atoms['WM_DELETE_WINDOW'] in self.protocols:
            # use client message
            log.debug('Killing client %s using WM_DELETE_WINDOW' % self)
            msg = xproto.ClientMessageEvent.create(
                    self.conn,
                    self.conn.atoms['WM_PROTOCOLS'],
                    self.window,
                    32,
                    [
                        self.conn.atoms['WM_DELETE_WINDOW'].get_internal(),
                        xproto.Time.CurrentTime,
                    ]
                    )
            self.window.send_event(0, msg)
        else:
            # use kill_client
            log.debug('Killing client %s using `kill_client`' % self)
            self.conn.core.kill_client(self.window)
        self.conn.flush()

    def _set_input_focus_via_request(self):
        """
            use :meth:`set_input_focus <ooxcb.xproto.Window.set_input_focus>`
            to give the input focus
        """
        log.debug('Setting input focus via request (%s)' % self)
        self.window.set_input_focus()

    def _set_input_focus_via_clientmessage(self):
        """
            use the `WM_TAKE_FOCUS` client message to give the input focus.
        """
        log.debug('Setting input focus via client message (%s)' % self)
        msg = xproto.ClientMessageEvent.create(
                self.conn,
                self.conn.atoms['WM_PROTOCOLS'],
                self.window,
                32,
                [
                    self.conn.atoms['WM_TAKE_FOCUS'].get_internal(),
                    timestamp()
                ]
                )
        self.window.send_event(0, msg)

    def set_input_focus(self):
        """
            grant the input focus. If :attr:`protocols` contains
            `WM_TAKE_FOCUS`, send such a client message, otherwise
            use :meth:`set_input_focus <ooxcb.xproto.Window.set_input_focus>`.
        """
        log.info('setting input focus on %s' % self)
        take_focus = self.conn.atoms['WM_TAKE_FOCUS'] in self.protocols
        hints = self.window.icccm_get_wm_hints() # TODO: cache that?
        if not hints:
            self._set_input_focus_via_request()
        # Check what we do to grant the input focus. Described in
        # the ICCCM, Section 4.1.7.
        elif (not hints.input and not take_focus):
            # Do not give input focus
            pass
        elif not take_focus:
            # Passive / Locally Active
            self._set_input_focus_via_request()
        else:
            # use client message
            self._set_input_focus_via_clientmessage()
        self.conn.flush()

    def init(self):
        """
            Initialize the actor.
            Called internally by :meth:`samuraix.screen.manage`
            after *self.actor* is set.
            That's not so nice.
        """
        self.actor.valid = True
        self.actor.push_handlers(on_configure_notify=self.actor_on_configure_notify)
        # map actor and window.
        if self.actor is not self.window:
            self.window.map()
        # "unban" to get a valid WM_STATE property.
        self.unban()

    def msg_active_window(self, evt):
        """
            Handler for the _NET_ACTIVE_WINDOW client message.

            If the window is banned (WM_STATE is not WMState.Normal),
            it is unbanned.

            If it is called on an unmanaged window, it will not
            be handled - that's what we want.

            :todo: check if it's on the correct desktop
        """
        if self.window.icccm_get_wm_state().state != xproto.WMState.Normal:
            self.user_unban()
        self.screen.focus(self)

    def msg_change_state(self, evt):
        """
            handler for WM_CHANGE_STATE.

            This will iconify(?) me.
        """
        if evt.data.data32[0] == xproto.WMState.Iconic:
            self.iconify()
        else:
            log.warning('Unhandled WM_CHANGE_STATE: data: %s' % str(evt.data.data32))

    def msg_wm_state(self, evt):
        """
            handler for _NET_WM_STATE.

            That updates `self.state` and dispatches
            the 'on_handle_net_wm_state' event at least
            one time (or two, if two atoms were specified)
        """

        data32 = evt.data.data32
        # first bunch of data is the desired action.
        # (one of the constants above)
        action = data32[0]
        # data32[1:2] are the atoms to change. There has to be
        # specified at least one. The second one is optional.
        first, second = None, None
        first = self.conn.atoms.get_by_id(data32[1])
        if data32[2]:
            second = self.conn.atoms.get_by_id(data32[2])
        # data32[3] is the source indication. Ignored for now.
        source_indication = data32[3]
        log.info('Got a _NET_WM_STATE client message.'
                'Action=%d first=%s second=%s source ind.=%d',
                action, first, second, source_indication)
        # so modify self.state as wished.
        if action == NET_WM_STATE_REMOVE:
            self.state.remove(first)
            if second is not None:
                self.state.remove(second)
        elif action == NET_WM_STATE_ADD:
            self.state.add(first)
            if second is not None:
                self.state.add(second)
        elif action == NET_WM_STATE_TOGGLE:
            if first in self.state:
                self.state.remove(first)
            else:
                self.state.add(first)
            if second is not None:
                if second in self.state:
                    self.state.remove(second)
                else:
                    self.state.add(second)
        # TODO: a funny 'else' ...?
        self.update_net_wm_state()
        self.dispatch_event('on_handle_net_wm_state',
                first in self.state, first, source_indication)
        if second is not None:
            self.dispatch_event('on_handle_net_wm_state',
                    second in self.state, second, source_indication)

    def on_map_notify(self, evt):
        """
            window's event handler for map notify events
        """
        state = self.window.icccm_get_wm_state()
        if not state:
            log.warning('got map notify, but window does not have WM_STATE set')
            return
        # Iconic -> Normal
        if state.state == xproto.WMState.Iconic:
            # TODO: what about checking for the correct desktop?
            self.user_unban()
        else:
            log.debug('map notify with unknown transition')

    def on_handle_net_wm_state(self, present, atom, source_indication):
        """
            Default event handler: handles _NET_WM_STATE_HIDDEN!
        """
        if atom == self.conn.atoms['_NET_WM_STATE_HIDDEN']:
            if present:
                self.user_ban()
            else:
                self.user_unban()
        else:
            log.warning('Cannot handle _NET_WM_STATE thingy %s :(',
                    atom.get_name().reply().name.to_string())

    def process_netwm_client_message(self, evt):
        """
            process an EWMH / NETWM client message event.
        """
        return self.client_message_handlers.handle(evt)

    def install_handlers(self):
        """
            Install all client message handlers.

            :note: called internally
        """
        self.client_message_handlers.register_handler(
                self.conn.atoms['_NET_ACTIVE_WINDOW'],
                self.msg_active_window
                )
        self.client_message_handlers.register_handler(
                self.conn.atoms['WM_CHANGE_STATE'],
                self.msg_change_state
                )
        self.client_message_handlers.register_handler(
                self.conn.atoms['_NET_WM_STATE'],
                self.msg_wm_state
                )

    def update_net_wm_state(self):
        """
            ensure that the window's `_NET_WM_STATE` property contains
            the same atoms as *self.state*.
        """
        self.window.change_property('_NET_WM_STATE', 'ATOM', 32,
                List.from_atoms(self.state)
        )
        self.conn.flush()

    def on_property_notify(self, evt):
        """
            Event handler for :class:`ooxcb.xproto.PropertyNotifyEvent`,
            just a debug printout at the moment
        """
        log.debug('Got property notify event: %s changed in %s.' %
                (evt.atom.get_name().reply().name.to_string(), evt.window))

    def on_client_message(self, evt):
        """
            Event handler for :class:`ooxcb.xproto.ClientMessageEvent`.
            prints a debug message to the logs and calls
            :meth:`process_netwm_client_message`.
        """
        log.debug('Got client message event: %s, data32: %s' %
                (evt.type.get_name().reply().name.to_string(), evt.data.data32))
        self.process_netwm_client_message(evt)

    def actor_on_configure_notify(self, evt):
        """
            Event handler for :class:`ooxcb.xproto.ConfigureNotifyEvent`:
            update the geometry
        """
        self.update_geom(Rect.from_object(evt))

    def update_geom(self, geom):
        """
            *geom* is the new geometry of the actor(!) window.
            Dispatches 'on_updated_geom'.
        """
        self.geom = geom
        self.dispatch_event('on_updated_geom', self)

    def apply_normal_hints(self, hints=None, geom=None):
        """
            apply the WM_NORMAL_HINTS (TODO: complete)

            :param hints: A `SizeHints` object or None (fetch it)
            :param geom: received geom - will not be modified; if None,
                use a copy of `self.geom`
        """
        apply_style = True
        if hints is None:
            values = self.window.get_property('WM_NORMAL_HINTS', 'WM_SIZE_HINTS').reply().value
            try:
                hints = SizeHints.from_values(values)
            except KeyError, e:
                # missing value? just ignore it, invalid size hints then.
                log.warning('invalid size hints received: "%s"' % e)
                return
        if geom is None:
            geom = self.geom.copy()

        log.debug('client=%s size hints=%s', self, hints)
        if (hints.valid and geom.width > 1): # that one is a hack. TODO
            hints.compute(geom)
            self.resize(geom)
        else:
            log.warning('Invalid hints received!')

    def resize(self, geom):
        """
            Configure the main window (not the actor)
            to use width and height from *geom*.
        """
        log.debug('Resizing: %s' % geom)
        self.window.configure_checked(width=geom.width, height=geom.height).check()
        self.conn.flush()

    def on_destroy_notify(self, evt):
        """
            Event handler for :class:`ooxcb.xproto.DestroyNotifyEvent`.
            Prints a debug message and calls :meth:`remove` if the top-level
            window was destroyed.
        """
        log.warning('Got destroy notify event, Client=%s Window=%s' % \
                (self, evt.window))
        if evt.window is self.window:
            self.remove()

    def remove(self):
        """
            Called if the client lost its permission to exist. Sets
            *self.window.valid* to False and dispatches the `on_removed`
            event.
        """
        log.info('Removed me=%s! clients=%s' % (self, self.all_clients))
        self.window.valid = False
        self.dispatch_event('on_removed', self)

    def unmanage(self):
        """
            Remove myself ...
            called by the screen
        """
        if self.window.valid:
            # We don't want to receive any further events.
            self.window.change_attributes(event_mask=0)
            self.unban()
        try:
            self.all_clients.remove(self)
            del self.window_2_client_map[self.window]
        except (ValueError, KeyError), e:
            log.warning(e)
        self.window.remove_handlers(self)

    def ban(self, withdrawn=True, hidden=True):
        """
            Unmap the actor window and set WM_STATE.

            :Parameters:
                `withdrawn`: bool
                    If True, the WM_STATE is set to withdrawn
                    If False, it's Iconic.
                `hidden`: bool
                    add `_NET_WM_STATE_HIDDEN` to the net wm state if True
        """
        # TODO: respect sticky?
        log.debug('banning %s' % self)
        self.actor.unmap()
        self.conn.flush()

        state = xproto.WMState.Withdrawn if withdrawn else xproto.WMState.Iconic
        self.window.change_property(
                'WM_STATE',
                'CARDINAL',
                32,
                [state, 0]) # TODO: icon window?
        if hidden:
            self.add_net_wm_state('_NET_WM_STATE_HIDDEN')
            self.update_net_wm_state()
        self.conn.flush()

    def user_ban(self, withdrawn=True):
        """
            That does nothing except call :meth:`ban`.
        """
        self.ban(withdrawn)

    def iconify(self):
        """
            same as `self.ban(False)`
        """
        self.ban(False)

    def unban(self):
        """
            Map the actor window.
        """
        # TODO: respect sticky?
        log.debug('unbanning %s' % self)
        self.actor.map()
        self.window.change_property(
                'WM_STATE',
                'CARDINAL',
                32,
                [xproto.WMState.Normal, 0]) # TODO: icon window?
        self.remove_net_wm_state('_NET_WM_STATE_HIDDEN')
        self.update_net_wm_state()
        self.conn.flush()

    def user_unban(self):
        """
            map the actor window, as requested by the user.
            This will focus the actor.
        """
        self.unban()
        self.screen.focus(self)

    def focus(self, bring_forward=True):
        """
            Focus the client. Do not call that, use
            `Screen.focus` instead.
        """
        # grab the input focus
        self.set_input_focus()
        # set it abvoe
        if bring_forward:
            self.actor.configure(stack_mode=xproto.StackMode.Above)
        self.conn.flush()
        # TODO: grab buttons etc
        self.dispatch_event('on_focus', self)

    def blur(self):
        """
            Blur / Unfocus the client.
            Do not call, use `Screen.focus`.
        """
        self.dispatch_event('on_blur', self)

    def get_window_title(self):
        """
            returns the window title you should use.
            Since it respects the icccm and the netwm standard,
            it will use:

             * _NET_WM_VISIBLE_NAME if available. if not,
             * _NET_WM_NAME if available. if not,
             * WM_NAME

            And WM_NAME is available.

            :note: WM_NAME's encoding is latin-1, _NET_WM_NAME and
                    _NET_WM_VISIBLE_NAME are utf-8-encoded.
        """
        # try _NET_WM_VISIBLE_NAME
        encoding = 'utf-8'
        reply = self.window.get_property(
                '_NET_WM_VISIBLE_NAME', 'UTF8_STRING').reply()
        if not reply.exists:
            # try _NET_WM_NAME
            reply = self.window.get_property(
                    '_NET_WM_NAME', 'UTF8_STRING').reply()
            if not reply.exists:
                # use WM_NAME ( has ... to ... exist! )
                reply = self.window.get_property(
                        'WM_NAME', 'STRING').reply()
                encoding = 'latin-1'
        return reply.value.to_string().decode(encoding)

Client.register_event_type('on_focus')
Client.register_event_type('on_blur')
Client.register_event_type('on_handle_net_wm_state')
Client.register_event_type('on_removed')
Client.register_event_type('on_updated_geom')
