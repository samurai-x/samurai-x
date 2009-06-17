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
    With sx-bind, you can bind keystrokes to actions.
    Its plugin key is "bind".

    Dependencies
    ------------

    sx-bind depends on :ref:`sx-actions`.

    Provided Parameters
    -------------------

    There is just one parameter that sx-bind provides in its parameter dictionary:
    'screen' is the :class:`samuraix.screen.Screen` object the keystroke was pressed
    on.

    Configuration
    -------------

    .. attribute:: bind.keys

        A dictionary connecting :ref:`keystrokes` to action lines.

        Example::

            'bind.keys': {
                    'Meta+n': 'desktops.cycle offset=1',
                    'Meta+p': 'desktops.cycle offset=-1',
                    'Meta+c': 'desktops.cycle_clients',
                    'Meta+d': 'log message="pressed d"',
                    'Meta+Q': 'quit',
                    'Ctrl+R': 'restart',
                    'Meta+L': 'layoutmgr.cycle',
            }

    .. _keystrokes:

    Keystrokes
    ----------

    A keystroke describes a combination of modifier keys and one normal key pressed.
    They are joined together by a "+" char. The modifiers are case-insensitive,
    the key is not.

    Valid modifier names are: 'alt', 'numlock', 'meta', 'altgr', 'shift', 'lock',
    'ctrl', 'control', 'mod1', 'mod2', 'mod3', 'mod4', 'mod5'. 

    The valid key values are listed in the :mod:`ooxcb documentation <ooxcb.keysymdef>`.

    Examples::

        # the following three keystrokes are equal
        Meta+n
        META+n
        mEtA+n
        # some more examples
        SHIFT+metA+0
        Ctrl+alt+Delete

"""

from __future__ import with_statement

import logging
log = logging.getLogger(__name__)

from samuraix.util import MODIFIERS
from samuraix.plugin import Plugin

from ooxcb import keysymdef, xproto

def parse_keystroke(s):
    """
        Return (modifiers, keysym), extracted from the string `s`.

        It has to contain several modifiers and keysym names,
        joined together with a '+'::

            CTRL+A
            MOD4+q

    """
    modmask, keysym = 0, 0

    parts = s.split('+')
    modifiers = parts[:-1]
    key = parts[-1]
    # create modmask
    for mod in modifiers:
        try:
            modmask |= MODIFIERS[mod.lower()]
        except KeyError:
            log.error('Unknown modifier: "%s"' % mod)
    # get keysym
    try:
        keysym = keysymdef.keysyms[key]
    except KeyError:
        log.error('Unknown key: "%s"' % key)
    return modmask, keysym


class SXBind(Plugin):
    key = 'bind'

    def __init__(self, app):
        self.app = app
        self.bindings = {} # (modifier, keycode): 'action line'

        app.push_handlers(self)

    def on_ready(self, app):
        """
            Event handler: everything's ready, setup the event handlers.
        """
        self.setup_handlers()

        with self.app.conn.bunch():
            # first, ungrab all existing key bindings. That is
            # necessary for a proper configuration reloading.
            for modifiers, keycode in self.bindings.iterkeys():
                for screen in self.app.screens:
                    try:
                        screen.root.ungrab_key_checked(keycode, modifiers).check()
                    except xproto.BadAccess:
                        log.warning("Couldn't ungrab modifiers %d keycode %d" % (modifiers, keycode))
            # Then, bind the keys.
            self.bindings = {}
            for keystroke, action in self.config.iteritems():
                self.bind_keystroke(keystroke, action)

    def on_load_config(self, config):
        """
            Event handler: (re-)load the configuration.
        """
        self.config = config.get('bind.keys', {})

    def setup_handlers(self):
        """
            setup the `on_key_press` handlers for the root window.
        """
        for screen in self.app.screens:
            screen.root.push_handlers(on_key_press=self.on_key_press)

    def on_key_press(self, event):
        """
            Event handler: if it is a bound key, emit the corresponding
            action line. If it is not, print a warning to the log.
        """
        key = (event.state, event.detail)
        if key in self.bindings:
            info = {'screen': self.app.get_screen_by_root(event.root)} # TODO: no additional info? :/
            # ... call the action
            self.app.plugins['actions'].emit(self.bindings[key], info)
        else:
            log.warning('received an invalid key press event: %s' % key)

    def bind_key_to_action(self, modifiers, keycode, line):
        """
            if the modifiers in the mask *modifiers* are pressed down,
            and the key with the keycode *keycode* is pressed down,
            emit the action line *line*.
        """
        for screen in self.app.screens:
            screen.root.grab_key_checked(keycode, modifiers).check()
        self.bindings[(modifiers, keycode)] = line

    def bind_keystroke(self, keystroke, line):
        """
            bind the keystroke *keystroke* to the action line *line*.
            *keystroke* has to be in the format that is described
            under :func:`parse_keystroke`.
        """
        modifiers, keysym = parse_keystroke(keystroke)
        keycode = self.app.conn.keysyms.get_keycode(keysym)
        try:
            self.bind_key_to_action(modifiers, keycode, line)
        except xproto.BadAccess:
            log.warning("Couldn't grab key combination '%s'" % keystroke)
