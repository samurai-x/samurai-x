import samuraix

class ClientWindow(object):
    def __init__(self, client, wrapped_window):
        self.client = client
        self.wrapped_window = wrapped_window

    def window(self):
        return self.wrapped_window

            
class DecoratedClientWindow(ClientWindow):
    def __init__(self, client, wrapped_window):
        ClientWindow.__init__(self, client, wrapped_window)

        self.frame = SimpleWindow(self.client.screen,
                        self.client.geom, 1)
        xlib.XReparentWindow(samuraix.display, self.wrapped_window, self.frame, 1, 15)
        xlib.XMapWindow(samuraix.display, self.window)

        xlib.XSelectInput(samuraix.display, self.frame, 
                            xlib.StructureNotifyMask | 
                            xlib.PropertyChangeMask | 
                            xlib.EnterWindowMask)

    def window(self):
        return self.frame


class UndecoratedClientWindow(ClientWindow):
    def __init__(self, client, wrapped_window):
        ClientWindow.__init__(self, client, wrapped_window)

    
