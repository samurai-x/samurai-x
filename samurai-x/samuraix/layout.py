from samuraix.rect import Rect

class Layout(object):
    def __init__(self, desktop):
        self.desktop = desktop
        desktop.push_handlers(self)

    def on_client_add(self, client):
        self.layout([client])

    def layout(self, new=None):
        pass


class MaxLayout(object):
    def layout(self, new=None):
        for client in new:
            geom = Rect(0, 15, client.screen.width, client.screen.height-15)
            client.resize(geom)


