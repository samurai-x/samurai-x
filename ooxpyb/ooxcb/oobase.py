class Wrapper(object):
    """
        Base class for all wrappers.
    """
    def __init__(self, conn, _internal):
        self.conn = conn
        self._internal = _internal

