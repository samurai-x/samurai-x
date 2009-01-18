import logging
log = logging.getLogger(__name__)

from samuraix.plugin import Plugin
from samuraix.rect import Rect

from ooxcb import xproto

MOUSE_MASK = xproto.EventMask.ButtonPress | xproto.EventMask.ButtonRelease | xproto.EventMask.PointerMotion

class ClientHandler(object):
    def __init__(self, client, x, y, cursor=None):
        self.client = client
        self.offset_x, self.offset_y = x, y

        self.gc = xproto.GContext.create(
                self.client.conn,
                self.client.window,
                function=xproto.GX.xor, 
                foreground=self.client.screen.info.white_pixel,
                subwindow_mode=xproto.SubwindowMode.IncludeInferiors,
        )

        client.screen.root.grab_pointer(MOUSE_MASK, cursor_=cursor) # TODO: cursor_ is UGLY!
        client.conn.flush()

    def on_motion_notify(self, evt):
        pass

    def on_button_release(self, evt):
        pass

class MoveHandler(ClientHandler):
    def __init__(self, client, x, y):
        ClientHandler.__init__(self, client, x, y) # TODO: cursor
        log.info('Now moving %s' % client)
        self._x = None
        self._y = None

    def on_motion_notify(self, evt):
        self.clear_preview()
        x, y = evt.root_x - self.offset_x, evt.root_y - self.offset_y
        self.gc.poly_rectangle(self.client.screen.root,
                                [Rect(x, y, self.client.geom.width, self.client.geom.height)])
        self.client.conn.flush()
        self._x = evt.root_x
        self._y = evt.root_y
        return True

    def on_button_release(self, evt):
        self.client.screen.root.remove_handlers(self)
        self.client.conn.core.ungrab_pointer()
        self.clear_preview()
        if self._x is not None:
            self.client.actor.configure(x=self._x - self.offset_x, y=self._y - self.offset_y)
#            self.client.force_update_geom()
        self.client.conn.flush()
        return True

    def clear_preview(self):
        """ clear old preview if necessary """
        if self._x is not None:
            x, y = self._x - self.offset_x, self._y - self.offset_y
            self.gc.poly_rectangle(self.client.screen.root,
                                    [Rect(x, y, self.client.geom.width, self.client.geom.height)])

class ResizeHandler(ClientHandler):
    def __init__(self, client, x, y):
        ClientHandler.__init__(self, client, x, y) # TODO: cursor

#        geom = self.client.geom
#        client.frame.warp_pointer(geom.width, geom.height)

        self._w = None
        self._h = None

    def on_motion_notify(self, evt):
        self.clear_preview()
        geom = self.client.geom # TODO: I'm sure that's wrong. -- is it?
        w = evt.root_x - geom.x
        h = evt.root_y - geom.y
        self.gc.poly_rectangle(self.client.screen.root,
                                [Rect(geom.x, geom.y, w, h)])
        self.client.conn.flush()
        self._w = w
        self._h = h
        return True

    def on_button_release(self, evt):
        self.clear_preview()

        geom = self.client.geom.copy()
        geom.width, geom.height = self._w, self._h
        if geom.width:
            self.client.resize(geom)
        #configure(width=w, height=h)

        self.client.screen.root.remove_handlers(self)
        self.client.conn.core.ungrab_pointer()
        # put the mouse back where it was # TODO: necessary?
#        self.client.frame.warp_pointer(self.offset_x, self.offset_y)
        self.client.conn.flush()

        return True

    def clear_preview(self):
        """ clear old preview if necessary """
        if self._w:
            self.gc.poly_rectangle(
                    self.client.screen.root,
                    [Rect(
                        self.client.geom.x, self.client.geom.y, 
                        self._w, self._h
                    )]
            )

class SXMoveResize(Plugin):
    key = 'moveresize'

    def __init__(self, app):
        self.app = app

        app.plugins['actions'].register('moveresize.move', self.action_move)
        app.plugins['actions'].register('moveresize.resize', self.action_resize)

    def action_move(self, info):
        client = info.get('client', info['screen'].focused_client)
        if client is not None:
            client.screen.root.push_handlers(
                    MoveHandler(client, info.get('x', 0), info.get('y', 0))
                )

    def action_resize(self, info):
        client = info.get('client', info['screen'].focused_client)
        if client is not None:
            client.screen.root.push_handlers(
                    ResizeHandler(client, info.get('x', 0), info.get('y', 0))
                )

