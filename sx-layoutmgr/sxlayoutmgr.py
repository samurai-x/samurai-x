from samuraix.plugin import Plugin 

import logging
log = logging.getLogger(__name__)


class Layout(object):
    def __init__(self, desktop):
        self.desktop = desktop    
        desktop.push_handlers(self)

    def on_rearrange(self, desktop):
        self.layout()

    def layout(self):
        raise NotImplemented()


class MaxLayout(Layout):
    """ make the focused window fill the screen """

    name = 'max'

    def layout(self):
        geom = self.desktop.screen.get_geometry()
        client = self.desktop.clients.current()
        client.actor.configure(x=geom.x, y=geom.y, width=geom.width, height=geom.height)


class VertLayout(Layout):
    """ arrange windows vertically with equal height """

    name = 'vert'

    def layout(self):
        if self.desktop.clients:
            geom = self.desktop.screen.get_geometry()
            h = geom.height / len(self.desktop.clients)
            t = 0 
            for client in self.desktop.clients:
                client.actor.configure(x=0, y=t, width=geom.width, height=h)
                t += h


class HorizLayout(Layout):
    """ arrange windows horizontally with equal width """

    name = 'horiz'

    def layout(self):
        if self.desktop.clients:
            geom = self.desktop.screen.get_geometry()
            w = geom.width / len(self.desktop.clients)
            t = 0 
            for client in self.desktop.clients:
                client.actor.configure(x=t, y=0, width=w, height=geom.height)
                t += w


class SXLayoutMgr(Plugin):
    key = 'layoutmgr'

    def __init__(self, app):
        self.layouters = {}
        self.register(MaxLayout)
        self.register(VertLayout)

        self.app = app
        app.push_handlers(self)

    def register(self, layouter_cls):
        name = getattr(layouter_cls, 'name', layouter_cls.__name__)
        log.info('registering layouter %s = %s', name, layouter_cls)
        self.layouters[name] = layouter_cls

    def on_ready(self, app):
        # should potentially do this in on_create_screen but 
        # that means making sure desktop.on_create_screen is called 
        # first...
        for screen in app.screens:
            screendata = screen.data['desktops']
            screendata.push_handlers(self)
            for desktop in screendata.desktops:
                log.debug('trying to attach to %s...', desktop)
                layouter_name = desktop.config.get('layout')
                if not layouter_name:
                    log.debug('no layouter_name')
                    continue
                layouter_cls = self.layouters.get(layouter_name)
                if not layouter_cls:
                    log.error('cant find layouter %s', layouter_name)
                    continue
                log.debug('attached %s', layouter_cls)
                self.attach_data_to(desktop, layouter_cls(desktop))
                #desktop.push_handlers(on_rearrange=self.on_rearrange)
        
