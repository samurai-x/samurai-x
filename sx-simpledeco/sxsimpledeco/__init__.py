import logging
log = logging.getLogger(__name__)

from samuraix.plugin import Plugin
from ooxcb import xproto

BAR_HEIGHT = 20

class ClientData(object):
    def __init__(self, screen, client):
        self.client = client
        
        self.gc = xproto.GContext.create(self.client.conn,
                self.client.actor,
                foreground=screen.info.black_pixel,
                background=screen.info.white_pixel
                )

        self.client.actor.push_handlers(self)

    def on_expose(self, evt):
        self.client.actor.clear_area(0, 0, self.client.geom.width, self.client.geom.height)
        self.gc.image_text8(self.client.actor, 1, BAR_HEIGHT - 4, "Hello World!")
        self.client.conn.flush()

class SXDeco(Plugin):
    key = 'decoration'

    def __init__(self, app):
        self.app = app
        app.push_handlers(self)

    def on_ready(self, app):
        for screen in app.screens:
            screen.push_handlers(self)
            for client in screen.clients:
                self.create_client_data(screen, client)
        
    def on_new_client(self, screen, client):
        self.create_client_data(screen, client)

    def create_client_data(self, screen, client):
        client.actor = xproto.Window.create(self.app.conn, 
                screen.root,
                screen.info.root_depth,
                screen.info.root_visual,
                client.geom.x,
                client.geom.y,
                client.geom.width,
                client.geom.height,
                override_redirect=True,
                back_pixel=screen.info.white_pixel,
                event_mask=xproto.EventMask.Exposure,
                )
        client.window.reparent(client.actor, 0, BAR_HEIGHT)

        self.attach_data_to(client, ClientData(screen, client))
        client.actor.map()
        log.debug('created client actor %s', client)

