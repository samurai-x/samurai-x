import logging
log = logging.getLogger(__name__)

from samuraix.client import Client
from samuraix.plugin import Plugin
from samuraix.rect import Rect

class TilingDesktop(object):
    def __init__(self, plugin, desktop):
        self.plugin = plugin
        self.screen = desktop.screen
        self.screen.root.push_handlers(
                on_configure_request=self.on_configure_request,
        )

        self.desktop = desktop
        self.desktop.push_handlers(
                on_new_client=self.on_new_client,
                on_unmanage_client=self.on_unmanage_client,
        )
        self.geom = self.screen.get_geometry()
        self.scan()
        self.compute_all()

    def scan(self):
        for client in self.desktop.clients:
            client.push_handlers(on_focus=self.on_focus)
            client.window.push_handlers(on_configure_notify=self.on_configure_notify)
            
    def on_new_client(self, screen, client):
        client.push_handlers(on_focus=self.on_focus)
        self.compute_all()

    def on_unmanage_client(self, desktop, client):
        self.compute_all()

    def compute_all(self):
        if self.desktop.clients:
            geom = self.geom
            cnt = 0
            uheight = geom.height // (max(len(self.desktop.clients) - 1, 1)) # one is focused ;)
            for client in self.desktop.clients:
                client.actor.map()
                if client.is_focused():
                    client.actor.configure(x=0,
                            y=0,
                            width=geom.width // 2 - 1,
                            height=geom.height)
                else:
                    client.actor.configure(x=geom.width//2,
                            y=cnt * uheight,
                            width=geom.width // 2,
                            height=uheight - 1)
                    cnt += 1
            self.plugin.app.conn.flush()

    def on_focus(self, client):
        self.compute_all()

    def on_configure_request(self, evt):
        if Client.get_by_window(evt.window) in self.desktop.clients:
            self.compute_all()
            return True

    def on_configure_notify(self, evt):
        if Client.get_by_window(evt.window) in self.desktop.clients:
            self.compute_all()
            return True

class SXTiling(Plugin):
    key = 'tiling'
    # requires a desktops plugin ...

    def __init__(self, app):
        Plugin.__init__(self)

        self.app = app
        self.desktops = []

        self.app.push_handlers(self)

        self.app.plugins['desktops'].register_layouter('tiling', self)

    def on_load_config(self, config):
        self.desktops = []

    def register_desktop(self, desktop, info):
        # no additional information needed ... yet.
        self.desktops.append(TilingDesktop(self, desktop))
