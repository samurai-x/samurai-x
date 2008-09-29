import window

class Screen(object):
    def __init__(self, connection, _screen):
        self.connection = connection
        self._screen = _screen

    @property
    def root(self):
        """
            return the root window instance
        """
        return window.Window(self.connection, self._screen.root)

    @property
    def root_visual(self):
        return self._screen.root_visual

    @property
    def white_pixel(self):
        return self._screen.white_pixel

    @property
    def black_pixel(self):
        return self._screen.black_pixel
