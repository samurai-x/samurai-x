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

import subprocess

from samuraix.plugin import Plugin

class ActionInfo(dict):
    """
        a dictionary that prints an error to the log if someone
        tries to access an item that does not exist.
        Use that for your own action parameters dictionary!
    """
    def __missing__(self, key):
        log.error(
                'The action emitter does not provide the parameter "%s"; ' % key + \
                'either the emitter and the action handler are not compatible, or' + \
                'you don\'t provide a necessary information in your action emission line.')

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
                } # TODO: dotted names?

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
        """
        ident, kwargs = parse_emission(line)
        info.update(kwargs)
        return self.actions[ident](info)

