from pyglet.window.xlib import xlib 
import pyglet

import samuraix

class Desktop(pyglet.event.EventDispatcher):
    def __init__(self, screen, name):
        self.screen = screen
        self.name = name

        self.clients = []

