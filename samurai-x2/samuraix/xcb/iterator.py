class BaseIterator(object):
    next_func = None

    def __init__(self, _iter):
        self._iter = _iter
        self._stop = False

    def _transform(self, data):
        """ a placeholder to transform the iterator data `data`
            to a python object, if needed
            
            :param data: an iterator's data
        """
        return data

    def __iter__(self):
        while self._iter.rem:
            yield self._transform(self._iter.data.contents)
            self.next_func(self._iter)

