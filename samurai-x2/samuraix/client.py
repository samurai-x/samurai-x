import weakref

import samuraix.event
import samuraix.xcb

from .rect import Rect

class Client(samuraix.event.EventDispatcher):
    all_clients = []
    window_2_client_map = weakref.WeakValueDictionary()
    
    all_frames = []
    window_2_frame_map = weakref.WeakValueDictionary()

    @classmethod
    def get_by_window(cls, window):
        return cls.window_2_client_map.get(window)

    def __init__(self, screen, window, wa, geometry):
        self.screen = screen
        self.window = window
        self.window.attributes = {'event_mask': (samuraix.xcb.event.StructureNotifyEvent,)}

        self.geom = Rect(geometry['x'], geometry['y'], geometry['width'], geometry['height'])

        self.all_clients.append(self)
        self.window_2_client_map[self.window] = self

        self.create_frame()
        self.window.map()

        self.window.push_handlers(self)

        self._moving = False

    def on_configure_notify(self, evt):
        self.update_geom()

    def create_frame(self):
        self.frame_geom = frame_geom = self.geom.copy()
        frame_geom.height += 15
        frame_geom.width += 2
        frame_geom.x -= 7
        frame_geom.width -= 1
        frame = samuraix.xcb.window.Window.create(self.screen.connection,
                                                  self.screen,
                                                  frame_geom.x,
                                                  frame_geom.y,
                                                  frame_geom.width,
                                                  frame_geom.height,
                                                  1,
                                                  attributes={'event_mask': (samuraix.xcb.event.ExposeEvent,
                                                                             samuraix.xcb.event.ButtonPressEvent,
                                                                             samuraix.xcb.event.ButtonReleaseEvent),
                                                              'override_redirect': True})
        self.window.reparent(frame, 1, 11)
        frame.map()
        frame.set_handler('on_button_press', self.frame_on_button_press)
        frame.set_handler('on_button_release', self.frame_on_button_release)
        self.frame = frame

    def update_geom(self, new_geom):
        self.geom = new_geom

    def frame_on_button_press(self, evt):
        if evt.detail == 1:
            self._moving = True

    def frame_on_button_release(self, evt):
        if self._moving and evt.detail == 1:
            self.frame.configure(x=evt.root_x, y=evt.root_y)
            self._moving = False
