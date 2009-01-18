import logging
log = logging.getLogger(__name__)

from samuraix.plugin import Plugin
from samuraix.rect import Rect
from ooxcb import xproto

from sxbind import MODIFIERS # Oh no, we depend on sxbind! TODO? (maybe move into samuraix.contrib or something like that?)
from sxactions import ActionInfo

BAR_HEIGHT = 20

def parse_buttonstroke(s):
    """
        Return (modifiers, button id), extracted from the string `s`.

        It has to contain several modifiers and a button index,
        joined together with a '+':

        CTRL+1
        MOD4+2

        1 is the left mouse button,
        2 the middle,
        3 the right button.
    """
    modmask, button = 0, 0

    parts = s.split('+') 
    modifiers = parts[:-1]
    buttonpart = parts[-1]
    
    # create modmask
    for mod in modifiers:
        try:
            modmask |= MODIFIERS[mod.lower()]
        except KeyError:
            log.error('Unknown modifier: "%s"' % mod)

    # get button
    try:
        button = int(buttonpart)
    except ValueError:
        log.error('Invalid button: "%s"' % buttonpart)

    return modmask, button

def compute_window_geom(geom):
    """ convert the 'frame geom' to the 'window geom' """
    geom.y += BAR_HEIGHT
    geom.height -= BAR_HEIGHT

def compute_actor_geom(geom):
    """ convert the 'window geom' to the 'geom geom' """
    geom.y = max(0, geom.y - BAR_HEIGHT)
    geom.height = max(1, geom.height + BAR_HEIGHT)

class ClientData(object):
    def __init__(self, plugin, screen, client):
        self.plugin = plugin
        self.client = client

        self._obsolete = False
        self._active = True
        # This counter ensures that we don't run into
        # an infinite loop. If the window is configured,
        # we configure the actor. If the actor is configured,
        # we configure the window --> much fun.
        # Now, we increment the counter if we configure the
        # window. The actor will only be configured if
        # the counter equals 0. If it is greater than 0,
        # it is simply decremented.
        # Maybe that's not necessary, but it seems to be.
        self._window_configures = 0
        
        self.gc = xproto.GContext.create(self.client.conn,
                self.client.actor,
                foreground=screen.info.black_pixel,
                background=screen.info.white_pixel
                )

        self.client.actor.push_handlers(
                on_configure_notify=self.actor_on_configure_notify,
                on_expose=self.on_expose,
                on_unmap_notify=self.on_unmap_notify,
                on_map_notify=self.on_map_notify,
                on_button_press=self.on_button_press,
                )
        self.client.window.push_handlers(
                on_property_notify=self.on_property_notify,
                on_configure_notify=self.window_on_configure_notify
                )

    def on_expose(self, evt):
        if (self._active and not self._obsolete):
            self.redraw()

    def on_unmap_notify(self, evt):
        if not self._obsolete:
            self._active = False
            self.client.actor.unmap()
            self.client.conn.flush()

    def on_map_notify(self, evt):
        if not self._obsolete:
            self._active = True
            self.client.actor.map()
            self.client.conn.flush()

    def on_button_press(self, evt):
        self.plugin.emit_action(self.client, evt)

    def on_property_notify(self, evt):
        """
            if a window changes a watched atom, redraw
            the title bar.
        """
        print evt.atom, self.plugin.watched_atoms
        if evt.atom in self.plugin.watched_atoms:
            self.redraw()

    def redraw(self):
        self.client.actor.clear_area(0, 0, self.client.geom.width, self.client.geom.height)

        wm_name = self.client.window.get_property("WM_NAME", "STRING").reply().value.to_string()
        self.gc.image_text8(self.client.actor, 1, BAR_HEIGHT - 4, wm_name)
        self.client.conn.flush()

    def actor_on_configure_notify(self, evt):
        """ if the actor is configured, configure the window, too """
        geom = Rect(width=evt.width, height=evt.height)
        compute_window_geom(geom)
        self._window_configures += 1
        self.client.window.configure(**geom.to_dict()) # TODO: is that efficient?
        self.client.conn.flush()

    def window_on_configure_notify(self, evt):
        """ if the window is configured, configure the actor, too """
        if self._window_configures == 0:
            geom = self.client.geom.copy()
            compute_actor_geom(geom)
            self.client.actor.configure(**geom.to_dict())
            self.client.conn.flush()
        else:
            self._window_configures -= 1

    def remove(self):
        """ the end. """
        self.client.actor.destroy()
        self.gc.free()
        self.client.conn.flush()
        del self.client
        self._obsolete = True

class SXDeco(Plugin):
    key = 'decoration'

    def __init__(self, app):
        self.app = app
        app.push_handlers(self)
        self.bindings = {}

        self.watched_atoms = [self.app.conn.atoms[name] for name in
                ["WM_NAME"]
                ]

    def on_load_config(self, config):
        for stroke, action in config.get('decoration.bindings', {}).iteritems():
            self.bindings[parse_buttonstroke(stroke)] = action

    def on_ready(self, app):
        for screen in app.screens:
            screen.push_handlers(self)
            for client in screen.clients:
                self.create_client_data(screen, client)
        
    def on_new_client(self, screen, client):
        self.create_client_data(screen, client)

    def on_unmanage_client(self, screen, client):
        self.get_data(client).remove()

    def create_client_data(self, screen, client):
        client.actor = xproto.Window.create(self.app.conn, 
                screen.root,
                screen.info.root_depth,
                screen.info.root_visual,
                client.geom.x,
                client.geom.y,
                client.geom.width,
                client.geom.height + BAR_HEIGHT,
                override_redirect=True,
                back_pixel=screen.info.white_pixel,
                event_mask=
                    xproto.EventMask.Exposure | 
                    xproto.EventMask.StructureNotify | 
                    xproto.EventMask.SubstructureNotify |
                    xproto.EventMask.ButtonPress,
                )
        client.window.reparent(client.actor, 0, BAR_HEIGHT)
        
        data = ClientData(self, screen, client)
        self.attach_data_to(client, data)
        client.actor.map()
        log.debug('created client actor client=%s actor=%s data=%s', client, client.actor, data)

    def emit_action(self, client, evt):
        stroke = (evt.state, evt.detail)
        if stroke in self.bindings:
            info = ActionInfo(screen = self.app.get_screen_by_root(evt.root),
                    x=evt.event_x,
                    y=evt.event_y,
                    client=client) # TODO: no additional info? :/
            # ... call the action
            self.app.plugins['actions'].emit(self.bindings[stroke], info)
  
