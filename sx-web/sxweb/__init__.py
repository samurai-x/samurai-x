from samuraix.plugin import Plugin
import samuraix
import BaseHTTPServer
import cgi, sys
from pprint import pformat

import logging
log = logging.getLogger(__name__)


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path != "/":
            self.send_error(404, "File not found")
            return
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(self.makepage())

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        samuraix.app.plugins['actions'].emit(form['action'].value, {})        
        self.do_GET()

    def makepage(self):
        return """\
<html>
<body>
<h1>Config</h1>
<pre>%(config)s</pre>
<h1>Run Action</h1>
<form method='post'>
    <input type='text' name='action'/>
    <input type='submit' value='run action'/>
</form>
""" % {
        'config': pformat(samuraix.config),
        }


class SXWeb(Plugin):

    def __init__(self, app):
        self.app = app
        app.push_handlers(self)

        PORT = 8000

        self.httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)
    
        app.add_fd_handler('read', self.httpd.socket, self.httpd.handle_request)


