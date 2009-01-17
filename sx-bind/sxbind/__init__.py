import logging
log = logging.getLogger(__name__)

from samuraix.plugin import Plugin
from ooxcb.xproto import ModMask

from sxactions import ActionInfo

class SXBind(Plugin):
    key = 'bind'

    def __init__(self, app):
        self.app = app
        self.bindings = {} # (modifier, keycode): 'action line'

        app.push_handlers(self)

    def on_ready(self, config):
        self.bind_key_to_action(ModMask._4, 24, 'desktop.cycle count=1')
        self.setup_handlers()

    def setup_handlers(self):
        for screen in self.app.screens:
            screen.root.push_handlers(on_key_press=self.on_key_press)

    def on_key_press(self, event):
        key = (event.state, event.detail)
        if key in self.bindings:
            info = ActionInfo() # TODO: no additional info? :/
            # ... call the action
            self.app.plugins['actions'].emit(self.bindings[key], info)
        else:
            log.warning('received an invalid key press event: %s' % key)

    def bind_key_to_action(self, modifiers, keycode, line):
        """ 
            TODO: support keysyms
        """
        self.bindings[(modifiers, keycode)] = line 
        for screen in self.app.screens:
            screen.root.grab_key(modifiers, keycode)
        print self.bindings

