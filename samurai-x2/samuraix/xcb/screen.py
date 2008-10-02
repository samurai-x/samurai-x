import _xcb
import window

from util import cached_property

class Screen(object):
    def __init__(self, connection, _screen):
        self.connection = connection
        self._screen = _screen


    @property
    def root(self):
        """
            return the root window instance
        """
        return window.Window(self.connection, self._screen.root)

    @property
    def root_visual(self):
        return self._screen.root_visual

    @property
    def white_pixel(self):
        return self._screen.white_pixel

    @property
    def black_pixel(self):
        return self._screen.black_pixel

    @cached_property # TODO: really cache it?
    def root_visual_type(self):
        """
            returns either a root visual type or None.
            TODO: implement pythinonic iterators
            TODO: add a `Visual` object?
        """
        depth_iter = _xcb.xcb_screen_allowed_depths_iterator(self._screen)
        while depth_iter.rem:
            visual_iter = _xcb.xcb_depth_visuals_iterator(depth_iter.data)
            while visual_iter.rem:
                if self._screen.root_visual == visual_iter.data.contents.visual_id:
                    return visual_iter.data.contents
                _xcb.xcb_visualtype_next(visual_iter.contents)
            _xcb.xcb_depth_next(depth_iter)
        return None

    @property
    def root_depth(self):
        return self._screen.root_depth

    @property
    def width_in_pixels(self):
        return self._screen.width_in_pixels

    @property
    def height_in_pixels(self):
        return self._screen.height_in_pixels

    @property
    def size_in_pixels(self):
        return (self.width_in_pixels, self.height_in_pixels)
