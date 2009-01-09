from . import libxcb

class ExtensionKey(object):
    def __init__(self, name):
        self.key = libxcb.xcb_extension_t()
        self.key.name = name
        self.name = name

    def __hash__(self):
        return hash(self.name)

