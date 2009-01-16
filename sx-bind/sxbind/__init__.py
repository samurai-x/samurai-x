import logging
log = logging.getLogger(__name__)

from samuraix.plugin import Plugin

from ooxcb.xproto import ModMask

class SXBind(Plugin):
    key = 'bind'

    def __init__(self, app):
        self.app = app
        self.bindings = {}

        app.push_handlers(self)

    def on_ready(self, config):
        self.bind_key(ModMask._4, 24, self.app.screens[0].data['desktop'].cycle_desktops)
        self.setup_handlers()

    def setup_handlers(self):
        for screen in self.app.screens:
            screen.root.push_handlers(on_key_press=self.on_key_press)

    def on_key_press(self, event):
        info = (event.state, event.detail)
        if info in self.bindings:
            self.bindings[info]() # TODO
        else:
            log.warning('received an invalid key press event: %s' % info)

    def bind_key(self, modifiers, keycode, func):
        """ 
            TODO: support keysyms
        """
        self.bindings[(modifiers, keycode)] = func
        for screen in self.app.screens:
            screen.root.grab_key(modifiers, keycode)


