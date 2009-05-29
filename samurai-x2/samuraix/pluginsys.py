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
    This module is responsible for loading plugins.
"""

import logging
log = logging.getLogger(__name__)

import os.path

import pkg_resources

from samuraix import config

class PluginError(Exception):
    """
        raised by :meth:`PluginLoader.require_key` if a
        required plugin key couldn't be found.
    """
    pass

class PluginLoader(dict):
    """
        A class loading all available plugins using setuptools entrypoints.
        First, all paths in the 'core.plugin_paths' configuration option
        are checked and all found setuptools distributions are added to the
        working set. These distributions usually are Python eggs - so, it is
        very easy to remove a plugin - you can just remove the egg from the
        plugin path.
        The plugin loader object is a dictionary subclass. You can access
        plugins by their keys, for example:

        ::

            print self.app.plugins['desktops']

        However, there is usually just one :class:`PluginLoader` per
        samurai-x instance, and it's loaded by the application. Internally.
    """
    def __init__(self, app):
        """
            :type app: :class:`samuraix.appl.App`
        """
        self.app = app

    def setup(self):
        """
            add the available distributions to the pkg_resources working set
            and load all plugins. That is called internally by the application.
        """
        self.add_entries()
        self.load_all()

    def add_entries(self):
        """
            iterate the plugin paths (the 'core.plugin_paths' option)
            and add all found distributions to the working set.
        """
        for path in map(os.path.expanduser,
                config.get('core.plugin_paths', [])):
            map(pkg_resources.working_set.add,
                    pkg_resources.find_distributions(path, False))

    def require_key(self, key):
        """
            Call this to check if there is a plugin providing with the
            key *key*. If there is none, an :class:`PluginError` is raised.
        """
        if not key in self:
            raise PluginError('You have to install a plugin '
                              'implementing the "%s" key!' % key)

    def load_all(self):
        """
            load all plugins, warn if a plugin couldn't be loaded.
        """
        # get the names of all required plugins
        names = config.get('core.plugins', [])
        # get all available entrypoints and create a dictionary mapping
        # an entrypoint's name to an entrypoint.
        entrypoints = list(pkg_resources.iter_entry_points('samuraix.plugin'))
        dct = dict((ep.name, ep) for ep in entrypoints)

        for name in names:
            try:
                ep = dct[name]
            except KeyError:
                log.error("The plugin '%s' couldn't be found!" % name)
            else:
                log.info("Loading plugin '%s'...", name)
                cls = ep.load()
                self[cls.key] = cls(self.app)

