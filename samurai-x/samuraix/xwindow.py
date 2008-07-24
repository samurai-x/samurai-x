from pyglet.window.xlib import xlib


class XWindow(object):

    all_windows = {}

    def __init__(self, window):
        self.window = window
        self.all_windows[window] = self

    def __del__(self):
        try:
            self.delete()
        except KeyError:
            pass

    def delete(self):
        del self.all_windows[self.window]
        xlib.XDestroyWindow(samuraix.display, self.window)

    @classmethod 
    def create(cls, screen, geom, border_width, event_mask=None, 
                override_redirect=1, background_pixmap=xlib.ParentRelative):
        wa = xlib.XSetWindowAttributes()
        if event_mask is None:
            wa.event_mask = (
                         xlib.SubstructureRedirectMask |
                         xlib.SubstructureNotifyMask |
                         xlib.EnterWindowMask | 
                         xlib.LeaveWindowMask | 
                         xlib.StructureNotifyMask |
                         xlib.ButtonPressMask | 
                         xlib.KeyPressMask | 
                         xlib.ExposureMask
            )
        else:
            wa.event_mask = event_mask

        wa.override_redirect = override_redirect
        wa.background_pixmap = background_pixmap

        win = xlib.XCreateWindow(samuraix.display, screen.root_window, 
                    geom.x, geom.y, geom.width, geom.height,
                    border_width,
                    screen.default_depth,
                    xlib.CopyFromParent,
                    screen.default_visual,
                    xlib.CWOverrideRedirect | xlib.CWBackPixmap | xlib.CWEventMask,
                    byref(wa))
    
        return cls(win)

    def move(self, x, y):
        xlib.XMoveWindow(samuraix.display, self.window, x, y)

    def resize(self, width, height):
        xlib.XResizeWindow(samuraix.display, self.window, width, height)
        
