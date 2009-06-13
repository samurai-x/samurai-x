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
    sx-actions is a plugin that:

     * provides a simple notation to describe actions that should be emitted when
       a certain event occurs
     * provides an interface for other plugins to register action handlers or
       emit actions.

    Its plugin key is "actions", sx-actions is not configurable.

    Concept
    -------

    An action handler is just a callable that takes one argument::

        def handler(info)

    *info* is a dictionary (i.e. a :class:`ActionInfo` instance)
    containing information about the situation in which the
    action is emitted. It can also contain information the user provided in the
    so-called action line. We call that *info* dictionary the "parameter dictionary".
    It contains parameters.

    If the handler tries to access items that do not exist in the *info*, a
    warning is printed to the log.

    For example, let's say you want to spawn a firefox instance pointing
    to http://www.python.org when the user presses Meta+F.
    You would have an entry like the following in your samurai-x configuration file::

        config = {
            'bind.keys': {
                'Meta+F': 'spawn cmdline="firefox http://www.python.org"'
            }
        }

    The :ref:`sx-bind` plugin has the responsibility to emit the action line
    `spawn cmdline="firefox http://www.python.org"` when the user presses the
    key combination Meta+F. Then, the sx-actions plugin will see if there is a
    Python callable registered as handler for the "spawn" action. This callable
    will get a dictionary as its first arguments, containing the parameters
    the user specified in the action line plus, if given, some additional
    parameters provided by the plugin that emitted the action (the
    :ref:`sx-cairodeco` and :ref:`sx-simpledeco` do that, for example).
    In this case, the *info* dict will look like this::

        {
            'cmdline': "firefox http://www.python.org"
        }

    So, not every action can be emitted from every plugin (because some
    action handlers need some special additional parameters that not provided by
    every plugin). But don't worry, you will find the required parameters
    in the descriptions of every action.

    Predefined actions
    ------------------

    There are some predefined actions:

    .. function:: spawn(cmdline)
        :module:

        spawns an application.

        :Parameters:
            `cmdline`
                the command line of the application to launch

    .. function:: quit()
        :module:

        quits samurai-x2 gracefully.

    .. function:: log(message)
        :module:

        logs the message *message* into the log (debug level)

        :Parameters:
            `message`: str

    .. function:: restart()
        :module:

        restarts samurai-x2 gracefully. This will use the same process.

    .. function:: kill()
        :module:

        kills (quits) the currently focused or a specified (i.e. specified
        by the calling plugin) client.

        :Parameters:
            `screen`: :class:`Screen <samuraix.screen.Screen>`
                The screen the event was dispatched on
            `client`: :class:`Client <samuraix.client.Client>`
                The client to kill. Optional, uses the currently focused
                client as default.

    How to use it in your plugin
    ----------------------------

    Registering an action handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    If you want to provide an action handler, you have to think of
    a nice name for your action first. It would be nice if you'd
    choose a dotted name, with the key of your plugin as the first
    element. For example, if your plugin is `sx-webbrowser`, and
    you want to register an action that opens a webbrowser,
    a nice name for it would be `webbrowser.open`.

    After that, you need a Python callable that takes one argument.
    That will most likely be a function or a method::

        def open_webbrowser_action(info)

    *info* is a dictionary containing the parameters the user provided
    in his action emission line and, maybe, some additional information
    provided by the emitting plugin.

    Let's say your `webbrowser.open` action takes one parameter that
    the user has to specify in his emission line: *url*, the address
    to point to. The *info* dictionary contains it.

    Now you can write your handler function (note that we import the
    :mod:`webbrowser` module from the Python standard library)::

        import webbrowser

        def open_webbrowser_action(info):
            webbrowser.open(info['url'])

    Fine. Now you just have to register your handler function (you need
    a reference to the samurai-x2 :class:`samuraix.appl.App`)::

        app.plugins['actions'].register('webbrowser.open', open_webbrowser_action)

    Now, the user is able to emit your action!

    Emitting actions
    ~~~~~~~~~~~~~~~~

    If you have a plugin that deals with events and you want to make it possible
    to connect these events to actions, you can just use sx-actions this way::

        # ...
        info = {"parameter": some_value, "some_other_parameter": some_other_value}
        app.plugins['actions'].emit(action_line, info)

    The connection of events to action lines (and the storing of action lines) is
    the responsibility of your plugin.

    D-Bus interface
    ---------------

    If a plugin providing the *dbus* key is available, sx-actions registers the
    following D-Bus methods:

    .. method:: org.samuraix.ActionsInterface.action(action_line)

        Emit the action *action_line*.

"""

import logging
log = logging.getLogger(__name__)

import subprocess

import samuraix.main
from samuraix.plugin import Plugin

class ActionInfo(dict):
    """
        a dictionary that prints an error to the log if someone
        tries to access an item that does not exist.
        You can use that for your own action parameters dictionary,
        but you don't have to do necessarily, :meth:`SXActions.emit`
        will create an :class:`ActionInfo` instance lazily.
    """
    def __missing__(self, key):
        log.error(
                'The action emitter does not provide the parameter "%s"; ' % key + \
                'either the emitter and the action handler are not compatible, or ' + \
                'you don\'t provide a required information in your action emission line.')

def parse_emission(line):
    """
        parse an action emission line::

            parse_emission("foo.bar a=4 slurp='bla\tbla'")
            # => ('foo.bar', {'a':4, 'slurp': 'bla\tbla'})

    """
    gen = iter(line)

    def push_blank():
        char = gen.next()
        while char in ' \t':
            char = gen_next()
        return char

    def p_string(char):
        start_char = char
        s = ''
        while True:
            char = gen.next()
            if char == '\\':
                # escaped character follows ...
                char = (char + gen.next()).decode('string-escape')
            if char == start_char:
                break
            s += char
        return s

    def p_ident(char=''):
        py = char
        while True:
            try:
                char = gen.next()
            except StopIteration:
                break
            if char in ' \t:=':
                break
            py += char
        try:
            py = int(py)
        except ValueError:
            pass

        return py

    def p_value(c):
        py = c
        char = gen.next()
        if char in '"\'':
            py = p_string(char)
        else:
            py = p_ident(char)
        return py

    def p_kwargs():
        py = {}
        while True:
            try:
                c = push_blank()
                name = p_ident(c)
            except StopIteration:
                break
            else:
                try:
                    value = p_value(c)
                except StopIteration:
                    raise Exception('Incomplete arguments list')
                except AssertionError:
                    raise Exception('= expected')
                py[name] = value
        return py

    # first, parse the name
    name = p_ident()
    # parse the kwargs
    kwargs = p_kwargs()
    return name, kwargs

class SXActions(Plugin):
    """
        A plugin implementing the 'actions' key.

        Such a class should provide the following methods:

         * :meth:`emit`
         * :meth:`register`

    """
    key = 'actions'

    def __init__(self, app):
        self.app = app
        self.actions = {
                'spawn': self.action_spawn,
                'quit': self.action_quit,
                'log': self.action_log,
                'restart': self.action_restart,
                'kill': self.action_kill,
                'mark': self.action_mark,
                } # TODO: dotted names?

        app.push_handlers(on_ready=self.on_ready)

    def on_ready(self, app):
        if 'dbus' in app.plugins:
            import sxactions.dbusobj
            import functools
            app.plugins['dbus'].register(
                    'actions', 
                    functools.partial(sxactions.dbusobj.ActionsObject, self),
            )

    def action_mark(self, info):
        log.info('MARK --------------------------------------------')

    def action_spawn(self, info):
        """
            spawn an application.

            Parameters:
                `cmdline`: str

        """
        cmdline = info['cmdline']
        subprocess.Popen(cmdline, shell=True)

    def action_quit(self, info):
        """
            quit samurai-x.
        """
        self.app.stop()

    def action_restart(self, info):
        """
            restart samurai-x.
        """
        samuraix.main.restart()

    def action_kill(self, info):
        """
            kill a client. If specified, use the `client` parameter,
            if not, use the focused client on the `screen` parameter.
            Therefore, the `screen` parameter is absolutely required.
        """
        screen = info['screen']
        client = info.get('client', screen.focused_client)
        if client is None:
            log.warning('No focused client on screen %s' % screen)
        else:
            client.kill()

    def action_log(self, info):
        """
            print something to the log

            Parameters:
                `message`: str

        """
        log.debug(info['message'])

    def register(self, ident, action):
        """
            add an action an user can connect to. *ident* is a,
            preferable dotted, name to identify the action.
            *action* is a callable taking one argument:

            ::

                def handler(info)

            `info` is an :class:`ActionInfo` instance. If you try
            to access a non-existing item (so the action and the
            emitter do not fit), it will print an error message to
            the log.
        """
        self.actions[ident] = action

    def emit(self, line, info):
        """
            emit the action specified by the emission line `line`.
            `info` will be updated with the information from the
            emission line.
            If *info* is not already an instance of :class:`ActionInfo`,
            such an instance with the contents if *info* will be created.
        """
        if not isinstance(info, ActionInfo):
            info = ActionInfo(**info)
        ident, kwargs = parse_emission(line)
        info.update(kwargs)
        return self.actions[ident](info)

