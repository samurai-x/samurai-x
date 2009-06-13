# Copyright (c) 2008-2009, samurai-x.org
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the samurai-x.org nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SAMURAI-X.ORG ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL SAMURAI-X.ORG  BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
    sx-moveresize is a plugin that adds the actions 'moveresize.move' and 'moveresize.resize' 
    which move and resize the current or specified window respectivly.

    Configuration
    -------------
        
    .. attribute:: moveresize.border-move

        Boolean value that when True shows a rectangle preview of the moved/resized
        window instead of moving/resizing the window directly

    .. attribute:: moveresize.hide-win
    
        Boolean value that when True will hide the window that is being moved/resized.
        Most usefull when moveresize.border-move is True. 

    Actions
    -------

    .. function:: moveresize.move
        :module:

        Start moving the current window

    .. function:: moveresize.resize
        :module:
        
        Start resizing the current window 

"""


import logging
log = logging.getLogger(__name__)

from samuraix.plugin import Plugin
from samuraix.rect import Rect
from samuraix.util import DictProxy

from ooxcb import xproto

MOUSE_MASK = xproto.EventMask.ButtonPress | xproto.EventMask.ButtonRelease | xproto.EventMask.PointerMotion

class ClientHandler(object):
    def __init__(self, client, x, y, cursor=None, border_move=True, hide_win=True):
        log.debug('created %s', self)

        self.client = client
        self.offset_x, self.offset_y = x, y
        self.border_move = border_move
        self.hide_win = hide_win

        self.gc = xproto.GContext.create(
                self.client.conn,
                self.client.window,
                function=xproto.GX.xor, 
                foreground=self.client.screen.info.white_pixel,
                subwindow_mode=xproto.SubwindowMode.IncludeInferiors,
        )

        client.screen.root.grab_pointer(MOUSE_MASK, cursor=cursor)
        client.screen.focus(client)
        if self.hide_win:
            client.ban()
        client.conn.flush()

    def on_motion_notify(self, evt):
        pass

    def on_button_release(self, evt):
        pass


class MoveHandler(ClientHandler):
    def __init__(self, client, x, y, cursor=None, **kwargs):
        ClientHandler.__init__(self, client, x, y, client.app.cursors['Move'], **kwargs)
        self._x = None
        self._y = None

    def on_motion_notify(self, evt):
        x, y = evt.root_x - self.offset_x, evt.root_y - self.offset_y
        if self.border_move:
            self.clear_preview()
            self.gc.poly_rectangle(self.client.screen.root,
                    [Rect(x, y, self.client.geom.width, self.client.geom.height)])
        else:
            self.client.actor.configure(x=x, y=y)
        self.client.conn.flush()
        self._x = evt.root_x
        self._y = evt.root_y
        return True

    def on_button_release(self, evt):
        self.client.screen.root.remove_handlers(self)
        self.client.conn.core.ungrab_pointer()
        if self.border_move:
            self.clear_preview()
        if self.hide_win:
            self.client.unban()
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
    def __init__(self, client, x, y, **kwargs):
        ClientHandler.__init__(self, client, x, y, client.app.cursors['Resize'], **kwargs)

#        geom = self.client.geom
#        client.frame.warp_pointer(geom.width, geom.height)

        self._w = None
        self._h = None

    def on_motion_notify(self, evt):
        geom = self.client.geom # TODO: I'm sure that's wrong. -- is it?
        w = evt.root_x - geom.x
        h = evt.root_y - geom.y
        if self.border_move: 
            self.clear_preview()
            self.gc.poly_rectangle(self.client.screen.root,
                    [Rect(geom.x, geom.y, w, h)])
        else:
            self.client.actor.configure(w=w, h=h)
        self.client.conn.flush()
        self._w = w
        self._h = h
        return True

    def on_button_release(self, evt):
        if self.border_move:
            self.clear_preview()

        geom = self.client.geom.copy()
        geom.width, geom.height = self._w, self._h
        if geom.width:
            # we cannot use self.client.resize here, because
            # that resizes the window. we want to resize the
            # actor. That's not really optimal. TODO?
            self.client.actor.configure(
                    width=geom.width,
                    height=geom.height
                    )
        self.client.screen.root.remove_handlers(self)
        self.client.conn.core.ungrab_pointer()
        self.client.unban()
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
        app.push_handlers(self)

        app.plugins['actions'].register('moveresize.move', self.action_move)
        app.plugins['actions'].register('moveresize.resize', self.action_resize)

    def on_load_config(self, config):
        self.config = DictProxy(config, self.key+'.')

    def action_move(self, info):
        client = info.get('client', info['screen'].focused_client)
        if client is not None:
            client.screen.root.push_handlers(
                    MoveHandler(client, info.get('x', 0), info.get('y', 0), 
                            border_move=self.config.get('border-move', True),
                            hide_win=self.config.get('hide-win', True),
                    )
            )

    def action_resize(self, info):
        client = info.get('client', info['screen'].focused_client)
        if client is not None:
            client.screen.root.push_handlers(
                    ResizeHandler(client, info.get('x', 0), info.get('y', 0),
                            border_move=self.config.get('border-move', True),
                            hide_win=self.config.get('hide-win', True),
                    )
            )

