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
    sx-web is a plugin that runs a wsgi http server inside samurai-x.
    Currently, it only displays some information about the installed plugins.

    Dependencies
    ------------

    sx-web depends on `webob`_ and `mako`_.

    .. _webob: http://pythonpaste.org/webob/
    .. _mako: http://www.makotemplates.org/

    Configuration
    -------------

    .. attribute:: web.port
    
        Port number to run the web server on (defaults to 8000)

"""

import os
import sys
import socket
import wsgiref
from wsgiref import simple_server
import mimetypes
import code
import json
from StringIO import StringIO

import samuraix
from samuraix.plugin import Plugin
from samuraix.util import DictProxy

from webob import Request, Response
from webob import exc

from mako.template import Template
from mako.lookup import TemplateLookup
from mako.filters import html_escape

import logging
log = logging.getLogger(__name__)

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
static_dir = os.path.join(os.path.dirname(__file__), 'static')

template_lookup = TemplateLookup(
        directories=[template_dir], 
        module_directory='/tmp/mako_modules',
)


def render(templatename, **kwargs):
    template = template_lookup.get_template(templatename)
    return template.render(**kwargs)


class WSGIApp(object):
    def __init__(self, plugin):
        self.plugin = plugin 

    def __call__(self, environ, start_response):
        req = Request(environ)
        if req.environ['REMOTE_ADDR'] != '127.0.0.1':
            resp = exc.HTTPBadRequest(str(e))
        else:
            resp = self.process(req)
            #try:
            #    resp = self.process(req)
            #except ValueError, e:
            #    resp = exc.HTTPBadRequest(str(e))
            #except exc.HTTPException, e:
            #    resp = e
        return resp(environ, start_response)

    def process(self, request):
        if request.path_info == '/':
            content_type="text/html"
            body = render('index.html',     
                    app=self.plugin.app, 
                    plugin=self.plugin,
                    all_tabs=Tab.all_tabs,
            )
        else:
            url_parts = request.path_info[1:].split('/', 1)
            tab_name = url_parts[0]
            if len(url_parts) > 1:
                rest = url_parts[1]
            else:
                rest = ''
            if tab_name == 'static':
                ffn = os.path.join(static_dir, rest)
                content_type = mimetypes.guess_type(ffn)[0]
                body = open(ffn).read()
            else:
                tab = Tab.all_tabs[tab_name]
                request.script_name = '/' + tab_name
                request.path_info = '/' + rest
                return tab(request)
        return Response(
                content_type=content_type,
                body=body,
        )
            

class Tab(object):
    all_tabs = {}

    def __init__(self, plugin, name, htmlname=None):
        self.plugin = plugin 
        self.name = name 
        self.htmlname = htmlname or name.lower().replace(' ', '_')
        self.all_tabs[self.htmlname] = self

    def __call__(self, request):
        return Response(
            body=request.path_info)          


class PluginsTab(Tab):
    def html(self):
        return render("/tabs/plugins/index.html", app=self.plugin.app)

class YahikoDecoratorTab(Tab):
    def html(self):
        return render("/tabs/yahiko/index.html", app=self.plugin.app)


class WebConsole(code.InteractiveConsole):
    def start_buffer(self):
        self.wbuf = StringIO()

    def write(self, data):
        self.wbuf.write(data)
    
    def get_buffer(self):
        return self.wbuf.getvalue()


class InteractiveTab(Tab):
    def __init__(self, plugin, name, htmlname=None):
        Tab.__init__(self, plugin, name, htmlname=htmlname)
        self.console = WebConsole({'app':self.plugin.app})

    def html(self):
        return render("/tabs/interactive/index.html")

    def __call__(self, request):
        if request.path_info == '/':
            return Response(
                    body=render("/tabs/interactive/index.html"),
            )
        elif request.path_info == '/input':
            self.console.start_buffer()
            sys.stdout = StringIO()
            more = self.console.push(request.params['input'])
            if more:
                prompt = '... '
            else:
                prompt = '>>> '
            out = html_escape(sys.stdout.getvalue()).splitlines()
            sys.stdout = sys.__stdout__
            err = html_escape(self.console.get_buffer()).splitlines()
            return Response(
                content_type="text/javascript",
                body=json.dumps({'stderr': err, 'stdout': out, 'prompt': html_escape(prompt)}),
            )


class SXWeb(Plugin):
    key = 'web'

    def __init__(self, app):
        self.app = app
        app.push_handlers(self)

        PluginsTab(self, 'Plugins')
        #Tab(self, 'Config')
        InteractiveTab(self, 'interactive')

    def on_load_config(self, config):
        self.config = DictProxy(config, self.key+'.')
        self.port = self.config.get('port', 8000)

    def on_ready(self, app):
        log.info('serving on port %s', self.port)
        
        wsgiapp = WSGIApp(self)

        try:
            self.httpd = simple_server.make_server('', self.port, wsgiapp)
        except socket.error, e:
            log.error('cannot launch web server: %s', str(e))
            return 

        app.add_fd_handler('read', self.httpd.socket, self.httpd.handle_request)

    def __del__(self):
        log.debug('sxweb going down!')

