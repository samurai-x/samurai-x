import weakref

import samuraix.event
import samuraix.drawcontext
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
        self._resizing = False

    def on_configure_notify(self, evt):
        self.update_geom()

    def create_frame(self):
        self.frame_geom = frame_geom = self.geom.copy()
        frame_geom.height += 15
        frame_geom.width += 2
        frame_geom.x -= 1
        frame_geom.y -= 7
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
        frame.set_handler('on_expose', self.frame_on_expose)

        context = samuraix.drawcontext.DrawContext(self.screen, frame_geom.width, frame_geom.height, frame)
        context.text(0, 0, self.window.get_property('WM_NAME')[0], (0, 255, 255))

        self.frame = frame

    def update_geom(self, new_geom):
        self.geom = new_geom
        print "%s geom %s" % (self, new_geom)

    def frame_on_button_press(self, evt):
        if evt.detail == 1:
            self._moving = True
            #assert self.screen.root.grab_pointer()
        if evt.detail == 3:
            self._resizing = True

    def frame_on_button_release(self, evt):
        if self._moving and evt.detail == 1:
            try:
                self.frame.configure(x=evt.root_x, y=evt.root_y)
            except Exception, e:
                print 'EXCEPTION occured when moving window:', e
            self._moving = False
        if self._resizing and evt.detail == 3:
            geom = self.window.get_geometry()
            try:
#                N = geom['x'] + x
            # x = N - geom['x']
                w = evt.root_x - geom['x']
                h = evt.root_y - geom['y']
                if w > 0 and h > 0:
                    self.frame.configure(width=w, height=h)
                    self.window.configure(width=w-3, height=h-22)
            except Exception, e:
                print 'EXCEPTION occured when resizing window:', e
            self._resizing = False

    def frame_on_expose(self, evt):
        context = samuraix.drawcontext.DrawContext(self.screen, self.frame_geom.width, self.frame_geom.height, self.frame)
        context.fill((255, 0, 255))
        context.text(0, 10, self.window.get_property('WM_NAME')[0], (255, 255, 255))
        # fred: why do I have to set y=10?
        # dunk: because its specifying the baseline of the text not the top 

