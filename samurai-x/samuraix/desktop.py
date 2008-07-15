from pyglet.window.xlib import xlib 
import pyglet

import weakref

import samuraix

import logging
log = logging.getLogger(__name__)

class Desktop(pyglet.event.EventDispatcher):
    def __init__(self, screen, name):
        self.screen = screen
        self.name = name

        log.info('created new desktop %s' % self)

        self.clients = []

    def __str__(self):
        return "<Desktop '%s' on %s>" % (self.name, self.screen)

    def add_client(self, client):
        log.debug('adding client %s to desktop %s' % (client, self))
        self.clients.append(weakref.ref(client))
        client.desktop = self
        if client.desktop is self:
            client.unban()
        else:
            client.ban()

    def remove_client(self, client):
        assert client.desktop is self
        log.debug('removing client %s from desktop %s' % (client, self))
        client.desktop = None
        self.clients.remove(client)

    def on_show(self):
        log.info('showing desktop %s' % self)
        for client in self.clients:
            c = client()
            if c is not None:
                c.unban()
        
    def on_hide(self):
        log.info('hiding desktop %s' % self)
        for client in self.clients:
            c = client()
            if c is not None:
                c.ban()
    

Desktop.register_event_type('on_show')
Desktop.register_event_type('on_hide')

