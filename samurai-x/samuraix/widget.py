class Widget(object):
    def __init__(self, screen):
        self.window = None
        self.screen = screen
        self.dirty = True

    def draw(self):
        pass

    def test_window(self, window):
        return False

    def refresh(self):
        pass
