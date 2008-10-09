import ctypes
import _xcb
import copy

class BaseIterator(object):
    next_func = None

    def __init__(self, _iter):
        self._iter = _iter
        self._stop = False

    def __iter__(self):
        return self

    def next(self):
        if not self._iter.rem:
            raise StopIteration()
        data = self._iter.data
        print self._iter.data
        self.next_func(self._iter)
        print self._iter.data
        return data.contents
class DepthIterator(BaseIterator):
    next_func = _xcb.xcb_depth_next
