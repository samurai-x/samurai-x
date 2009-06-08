from samuraix.plugin import Plugin 

import logging
log = logging.getLogger(__name__)

class SXAutoClient(Plugin):
    def __init__(self, app):
        self.app = app
        app.push_handlers(self)

    def on_load_config(self, config):
        log.debug('on_load_config')
        self.config = config 

    def on_ready(self, app):
        for screen in app.screens:
            self.on_add_screen(app, screen)

    def on_add_screen(self, app, screen):
        log.debug('on_add_screen %s %s', app, screen)
        screen.push_handlers(on_new_client=self.screen_on_new_client)

    def screen_on_new_client(self, screen, client):
        log.debug('screen_on_new_client %s %s', screen, client)
        rules = self.config.get('autoclient.rules', [])
        log.debug('rules %s', rules)
        for rule in rules:
            log.debug('rule %s %s %s', rule, screen, client)
            rule(screen, client)
        
