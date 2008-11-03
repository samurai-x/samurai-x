import logging
log = logging.getLogger(__name__)

import weakref
import os.path
import functools

import samuraix
import samuraix.xcb
import samuraix.event
from samuraix.xcb import _xcb

from .setroot import set_root_image
from .client import Client
from .desktop import Desktop, DesktopList
from .rect import Rect
from samuraix.xcb import keysymdef

import os.path
SVGFILE = os.path.abspath('../gfx/samuraix.svg') # TODO: just for testing


class Screen(samuraix.xcb.screen.Screen, samuraix.event.EventDispatcher):
    client_class = Client
    desktop_class = Desktop

    def __init__(self, app, num):
        self.app = app
        super(Screen, self).__init__(app.connection, app.connection.screens[num]._screen)
        
        self.desktops = DesktopList()
        self.clients = []
        self.active_desktop = None
        self.focused_client = None

        self.root.attributes = {
            'event_mask': (
                samuraix.xcb.event.MapRequestEvent,
                samuraix.xcb.event.SubstructureRedirectEvent,
                samuraix.xcb.event.SubstructureNotifyEvent,
                samuraix.xcb.event.StructureNotifyEvent,
                samuraix.xcb.event.KeyPressEvent,
                samuraix.xcb.event.ExposeEvent,
            ),
        }

        self.keys = {}

        self.read_config()

        self.root.push_handlers(self)

        self.set_supported_hints()

        self.rootset = False

        self.on_expose(None)

    def get_geometry(self):
        return Rect.from_dict(self.root.get_geometry())

    @property
    def active_desktop_idx(self):
        return self.desktops.index(self.active_desktop)

    def read_config(self):
        self.read_keybindings()
        self.read_desktops()

    def read_keybindings(self):
        for (mod, keysym), action in samuraix.config.get('manager.keybindings', {}).iteritems():
            self.bind_key(mod, keysym, action)

    def read_desktops(self):
        for desktop_name in samuraix.config.get('manager.desktops', []) \
                or ['Main desktop']: # we want at least one desktop
            self.add_desktop(desktop_name)

    def add_desktop(self, name):
        desktop = self.desktop_class(self, name)
        self.desktops.append(desktop)
        self.dispatch_event('on_desktop_add', desktop)
        self.set_active_desktop(self.desktops[0])
    
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

    def bind_key(self, mod, keysym, callback):
        keycode = self.connection.keysymbols.get_keycode(keysym)
        self.keys[(mod, keycode)] = callback
        self.root.grab_key(keycode, mod)

    def on_key_press(self, evt):
        log.debug(str((evt, type(evt), dir(evt))))

        try:
            func = self.keys[(evt.state, evt.keycode)]
        except KeyError:
            log.warn('cant find key!')
        else:
            func(self)

    def manage(self, window, wa=None, geom=None):
        """ manage a new window - this may *not* result in a window being managed 
        if it is unsuitable """
        # override redirect windows need to be ignored - theyre not for us
        if window.attributes['override_redirect']:
            log.debug('%s not managing %s override_redirect is set', self, window)
            return False

        # TODO: is that correct?
        client = self.client_class(self, window, wa or window.attributes, geom or window.get_geometry())

        logging.debug('screen %s is now managing %s' % (self, client))
        self.clients.append(weakref.ref(client)) # do we need that?
        self.active_desktop.add_client(client)
        client.push_handlers(on_removed=self.update_client_list)

        try:
            window_type = window.get_property('_NET_WM_WINDOW_TYPE')[0].name
            if window_type == '_NET_WM_WINDOW_TYPE_DOCK':
                # make it sticky!
                # ugly ugly
                client.sticky = True
            log.info('window is a %s' % window_type)
        except Exception, e:
            log.error(e)
        self.update_client_list()
        return client

    def on_client_message(self, event):
        log.info('client message received: %s %s' % (event.type.name, event.data))
        if event.type.name == '_NET_CURRENT_DESKTOP': # client message from pager: change desktop
            self.set_active_desktop_by_index(event.data[0])

    def update_client_list(self):
        # re-set _NET_CLIENT_LIST
        self.root.set_property('_NET_CLIENT_LIST', [c.window for c in self.client_class.all_clients], 32, 'WINDOW')

    def scan(self):
        """ scan a screen for windows to manage """
        for child in self.root.children:
            log.debug('%s found child %s %s', self, child, child.get_property('WM_NAME'))
            log.debug('attr %s', child.get_attributes())

            # according to awesome we only do this when scanning...
            # ( not 100% sure why yet... )
            if child.attributes['map_state'] != _xcb.XCB_MAP_STATE_VIEWABLE:
                log.debug('%s not managing %s - not viewable', self, child)
                continue

            self.manage(child)

    def set_active_desktop(self, desktop):
        assert desktop in self.desktops
        if desktop is self.active_desktop:
            return
        if self.active_desktop:
            logging.debug('hiding desktop %s' % self.active_desktop)
            self.active_desktop.dispatch_event('on_hide')
        self.active_desktop = desktop
        logging.debug('showing desktop %s' % desktop)
        desktop.dispatch_event('on_show')
        self.dispatch_event('on_desktop_change')

    def set_active_desktop_by_index(self, index):
        self.set_active_desktop(self.desktops[index])

    def next_desktop(self):
        self.set_active_desktop(self.desktops.next(self.active_desktop_idx))

    def previous_desktop(self):
        self.set_active_desktop(self.desktops.previous(self.active_desktop_idx))

    def maximise_client(self):
        if self.focused_client:
            self.focused_client.toggle_maximize()

    def on_desktop_add(self, desktop):
        # update _NET_NUMBER_OF_DESKTOPS, _NET_DESKTOP_NAMES
        self.root.set_property('_NET_NUMBER_OF_DESKTOPS', [len(self.desktops)], 32, 'CARDINAL')
        self.root.set_property('_NET_DESKTOP_NAMES', [d.name for d in self.desktops], 8, 'UTF8_STRING')

    def on_desktop_change(self):
        # update _NET_CURRENT_DESKTOP
        self.root.set_property('_NET_CURRENT_DESKTOP', [self.active_desktop_idx], 32, 'CARDINAL')

    def set_supported_hints(self):
        connection = self.root.connection # TODO?
        atoms = [
            connection.atoms['_NET_SUPPORTED'],
            connection.atoms['_NET_CLIENT_LIST'],
            connection.atoms['_NET_NUMBER_OF_DESKTOPS'],
            connection.atoms['_NET_CURRENT_DESKTOP'],
            connection.atoms['_NET_DESKTOP_NAMES'],
            connection.atoms['_NET_ACTIVE_WINDOW'],
            connection.atoms['_NET_CLOSE_WINDOW'],

            connection.atoms['_NET_WM_NAME'],
            connection.atoms['_NET_WM_ICON_NAME'],
            connection.atoms['_NET_WM_WINDOW_TYPE'],
            connection.atoms['_NET_WM_WINDOW_TYPE_NORMAL'],
            connection.atoms['_NET_WM_WINDOW_TYPE_DOCK'],
            connection.atoms['_NET_WM_WINDOW_TYPE_SPLASH'],
            connection.atoms['_NET_WM_WINDOW_TYPE_DIALOG'],
            connection.atoms['_NET_WM_STATE'],
            connection.atoms['_NET_WM_STATE_STICKY'],
            connection.atoms['_NET_WM_STATE_SKIP_TASKBAR'],
            connection.atoms['_NET_WM_STATE_FULLSCREEN'],

            connection.atoms['UTF8_STRING'],
        ]
        self.root.set_property('_NET_SUPPORTED', atoms, 32, 'ATOM')

Screen.register_event_type('on_desktop_add')
Screen.register_event_type('on_desktop_change')
