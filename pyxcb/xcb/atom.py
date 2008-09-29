from util import cached_property

class Atom(object):
    def __init__(self, connection, _atom):
        self.connection = connection
        self._atom = _atom

    def __repr__(self):
        return '<XCB Atom ID: %d>' % self._atom

    def get_name(self):
        return self.request_name().value

    def request_name(self):
        import cookie # TODO: not nice.
        return cookie.AtomNameRequest(self.connection, self)

    def __eq__(self, other):
        return self._atom == other._atom

    def __ne__(self, other):
        return self._atom != other._atom

    def __bool__(self):
        return self._atom > 0
