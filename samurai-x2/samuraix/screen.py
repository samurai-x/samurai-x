import logging
log = logging.getLogger(__name__)

import weakref
import os.path

import samuraix.xcb
from samuraix.xcb import _xcb

from .setroot import set_root_image
from .client import Client

SVGFILE = '/home/fred/dev/wmanager/samurai-x/gfx/samuraix.svg' # TODO: just for testing

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
                                  samuraix.xcb.event.ExposeEvent,
                                  )
                    }
        self.root.grab_key(self.connection.keysymbols.get_keycode(0x71),
                    samuraix.xcb.modifiers.MOD_MASK_4) # 'CTRL-q' for me
        self.root.push_handlers(self)

        self.rootset = False
    
    def on_map_request(self, evt):
        #if evt.override_redirect:
        #    return # TODO: strange override_redirect values (88? oO)
        client = Client.get_by_window(evt.window)
        if client is None:
            # not created yet
            # NB we still not might manage this window - check manage()
            self.manage(evt.window, evt.window.attributes, evt.window.get_geometry())

    def on_expose(self, evt):
        if not self.rootset and os.path.isfile(os.path.abspath(SVGFILE)): # TODO: not hardcoded ;-)
            set_root_image(self, SVGFILE)
            self.rootset = True

    def on_key_press(self, evt):
        print 'The user pressed keysym', self.connection.keysymbols.get_keysym(evt.keycode)
        if samuraix.xcb.keylookup.keysym_to_str(self.connection.keysymbols.get_keysym(evt.keycode)) == 'q':
            print "It's q, so I'll shutdown."
            import sys
            self.connection.disconnect()
            sys.exit(0)

    def manage(self, window, wa=None, geom=None):
        """ manage a new window - this may *not* result in a window being managed 
        if it is unsuitable """
        if window.attributes['override_redirect']:
            log.debug('%s not managing %s override_redirect is set', self, window)
            return False
        elif window.attributes['map_state'] != _xcb.XCB_MAP_STATE_VIEWABLE:
            log.debug('%s not managing %s - not viewable', self, window)
            return False

        client = self.client_class(self, window, wa or window.attributes, geom or window.get_geometry())
        logging.debug('screen %s is now managing %s' % (self, client))
        self.clients.append(weakref.ref(client))
        return client 

    def scan(self):
        for child in self.root.children:
            log.debug('%s found child %s %s', self, child, child.get_property('WM_NAME')[0])
            log.debug('attr %s', child.get_attributes())

            # NB we still not might manage this window - check manage()
            self.manage(child)



