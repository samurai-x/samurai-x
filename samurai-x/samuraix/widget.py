class Widget(object):
    def __init__(self, screen, name, **options):
        self.window = None
        self.screen = screen
        self.dirty = True
        self.name = name
        self.options = options

    def draw(self):
        pass

    def test_window(self, window):
        return False

    def refresh(self):
        pass
