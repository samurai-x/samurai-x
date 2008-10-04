import weakref

import samuraix.xcb

from .client import Client

class Screen(samuraix.xcb.screen.Screen):
    client_class = Client

    def __init__(self, app, num):
        super(Screen, self).__init__(app.connection, app.connection.screens[num]._screen)
        
        self.desktops = []
        self.active_desktop = None
        self.clients = []
        self.focused_client = None

        self.root.attributes = {'event_mask': (samuraix.xcb.event.MapRequestEvent,
                                  samuraix.xcb.event.SubstructureRedirectEvent,
                                  samuraix.xcb.event.SubstructureNotifyEvent,
                                  samuraix.xcb.event.StructureNotifyEvent,
                                  samuraix.xcb.event.KeyPressEvent,
                                  )
                    }
        self.root.push_handlers(self)

    def on_map_request(self, evt):
        #if evt.override_redirect:
        #    return # TODO
        client = Client.get_by_window(evt.window)
        if client is None:
            # not created yet
            self.manage(evt.window, evt.window.attributes, evt.window.get_geometry())

    def manage(self, window, wa, geom):
        client = self.client_class(self, window, wa, geom)
        print 'screen %s managing %s' % (self, client)
        self.clients.append(weakref.ref(client))

