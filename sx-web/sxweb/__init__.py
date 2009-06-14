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
import socket
import wsgiref
from wsgiref import simple_server
import mimetypes

import samuraix
from samuraix.plugin import Plugin
from samuraix.util import DictProxy

from webob import Request, Response
from webob import exc

from mako.template import Template
from mako.lookup import TemplateLookup

import logging
log = logging.getLogger(__name__)

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

template_lookup = TemplateLookup(
        directories=[template_dir], 
        module_directory='/tmp/mako_modules',
)


def render(templatename, **kwargs):
    template = template_lookup.get_template(templatename)
    return template.render(**kwargs)


class WSGIApp(object):
    def __init__(self, app):
        self.app = app 

    def __call__(self, environ, start_response):
        req = Request(environ)
        if req.environ['REMOTE_ADDR'] != '127.0.0.1':
            resp = exc.HTTPBadRequest(str(e))
        try:
            resp = self.process(req)
        except ValueError, e:
            resp = exc.HTTPBadRequest(str(e))
        except exc.HTTPException, e:
            resp = e
        return resp(environ, start_response)

    def process(self, request):
        fn = request.environ['PATH_INFO'][1:]
        if not fn:
            fn = 'index.html'
        if fn.endswith('.html'):
            content_type="text/html"
            body = render(fn, app=self.app)
        else:
            ffn = os.path.join(template_dir, fn)
            content_type = mimetypes.guess_type(ffn)[0]
            body = open(ffn).read()
            
        return Response(
                content_type=content_type, 
                body=body,
        )


class SXWeb(Plugin):
    key = 'web'

    def __init__(self, app):
        self.app = app
        app.push_handlers(self)

    def on_load_config(self, config):
        self.config = DictProxy(config, self.key+'.')
        self.port = self.config.get('port', 8000)

    def on_ready(self, app):
        log.info('serving on port %s', self.port)
        
        wsgiapp = WSGIApp(app)

        try:
            self.httpd = simple_server.make_server('', self.port, wsgiapp)
        except socket.error, e:
            log.error('cannot launch web server: %s', str(e))
            return 

        print dir(self.httpd)

        app.add_fd_handler('read', self.httpd.socket, self.httpd.handle_request)

    def __del__(self):
        log.debug('sxweb going down!')

