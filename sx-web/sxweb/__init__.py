from samuraix.plugin import Plugin
import samuraix
import cgi, sys
from pprint import pformat
import wsgiref
from wsgiref import simple_server

import logging
log = logging.getLogger(__name__)


class SXWeb(Plugin):

    def __init__(self, app):
        self.app = app
        app.push_handlers(self)

        PORT = 8000

        self.httpd = simple_server.make_server('', PORT, simple_server.demo_app)
    
        app.add_fd_handler('read', self.httpd.socket, self.httpd.handle_request)


