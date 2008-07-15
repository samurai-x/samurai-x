from samuraix.rect import Rect

import logging 
log = logging.getLogger(__name__)

class Rule(object):
    def match(self, client):
        return False


class TitleRule(object):
    def __init__(self, title):
        self.title = title
    def match(self, client):
        log.debug('titlematch %s %s' % (client.title, self.title))
        return client.title == self.title 


def move_to_desktop_two(client):
    client.move_to_desktop(client.screen.desktops['two'])

def move_to_100_100(client):
    geom = Rect(100, 100, 100, 100)
    client.resize(geom)


class Rules(object):
    def __init__(self, screen):
        self.screen = screen 
        screen.push_handlers(self)

        self.rules = [
            (TitleRule("Terminal"), move_to_100_100),
        ]

    def on_client_add(self, client):
        for rule, cb in self.rules:
            if rule.match(client):
                cb(client)
