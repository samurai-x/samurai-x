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
log = logging.getLogger(__name__)

import os.path

import pkg_resources

from samuraix import config

class PluginLoader(dict):
    def __init__(self, app):
        self.app = app

    def setup(self):
        self.add_entries()
        self.load_all()

    def add_entries(self):
        """
            add the plugin paths to the working set
        """
        for path in map(os.path.expanduser, config.get('core.plugin_paths', [])):
            map(pkg_resources.working_set.add,
                    pkg_resources.find_distributions(path, False))
   
    def require_key(self, key):
        assert key in self, 'You have to install a plugin implementing the "%s" key!' % key
        
    def load_all(self):
        """
            load all plugins, warn if a plugin couldn't be loaded.
        """
        names = set(config.get('core.plugins', []))
        for ep in pkg_resources.iter_entry_points('samuraix.plugin'):
            if ep.name in names:
                cls = ep.load()
                self[cls.key] = cls(self.app)
                names.remove(ep.name)

        if names:
            log.error("The following plugins couldn't be loaded: %s" % ', '.join(names))
