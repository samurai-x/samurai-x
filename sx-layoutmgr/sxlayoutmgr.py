from samuraix.plugin import Plugin
from samuraix import app

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
        app.conn.flush()


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
            app.conn.flush()


class HorizLayout(Layout):
    """ arrange windows horizontally with equal width """

    name = 'horiz'

    def layout(self):
        if self.desktop.clients:
            log.warning('YEEX, LAYOUTER %s' % repr(self.desktop.clients))
            geom = self.desktop.screen.get_geometry()
            w = geom.width / len(self.desktop.clients)
            t = 0 
            for client in self.desktop.clients:
                client.actor.configure(x=t, y=0, width=w, height=geom.height)
                t += w
            app.conn.flush()


class SXLayoutMgr(Plugin):
    key = 'layoutmgr'

    def __init__(self, app):
        self.layouters = {}
        self.register(MaxLayout)
        self.register(VertLayout)
        self.register(HorizLayout)

        self.app = app
        app.push_handlers(self)

        # register actions
        app.plugins['actions'].register('layoutmgr.set_layout', self.action_set_layout)

    def action_set_layout(self, info):
        """
            set the layout of the current desktop.
            parameters:
                `name`: str
                    identifier of the layout
            needed:
                `screen`
        """
        self.attach_layouter(
                info['screen'].data['desktops'].active_desktop,
                self.layouters[info['name']]
                )

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
                    log.error('cant find layouter %s', name)
                    return
                self.attach_layouter(desktop, layouter_cls)

    def attach_layouter(self, desktop, layouter_cls):
        """
            attach the layouter class *layouter_cls* to *desktop*.
            That will overwrite any layouter that was
            attached before.
        """
        if self.has_data(desktop):
            self.remove_data(desktop)
        log.debug('attached %s', layouter_cls)
        layouter = layouter_cls(desktop)
        self.attach_data_to(desktop, layouter)
        #desktop.push_handlers(on_rearrange=self.on_rearrange)
        # rearrange it automatically
        layouter.layout()
