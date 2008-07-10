from pyglet.window.xlib import xlib 
import samuraix

class Atoms(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            r = self[item] = xlib.XInternAtom(samuraix.display, item, False)
            return r


