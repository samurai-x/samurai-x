import _xcb
from .iterator import BaseIterator

class VisualType(object):
    def __init__(self, _visualtype):
        self._visualtype = _visualtype
        self.visual_id = _visualtype.visual_id
        self._class = _visualtype._class
        self.bits_per_rgb_value = _visualtype.bits_per_rgb_value
        self.colormap_entries = _visualtype.colormap_entries
        self.red_mask = _visualtype.red_mask
        self.green_mask = _visualtype.green_mask
        self.blue_mask = _visualtype.blue_mask

class VisualTypeIterator(BaseIterator):
    next_func = _xcb.xcb_visualtype_next

    def _transform(self, data):
        return VisualType(data)
        
class Depth(object):
    def __init__(self, _depth):
        self._depth = _depth
        self.depth = _depth.depth
        self.visuals_len = _depth.visuals_len

    @property
    def visualtypes(self):
        return VisualTypeIterator(_xcb.xcb_depth_visuals_iterator(self._depth))
