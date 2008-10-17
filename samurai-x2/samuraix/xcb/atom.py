from util import cached_property

class Atom(object):
    def __init__(self, connection, _atom):
        self.connection = connection
        self._atom = _atom

    def __repr__(self):
        return '<XCB Atom ID: %d>' % self._atom

    @cached_property
    def name(self):
        return self.get_name()

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


class AtomDict(dict):
    def __init__(self, connection, *boo, **far):
        super(AtomDict, self).__init__(*boo, **far)
        self.connection = connection

    def __missing__(self, key):
        self[key] = value = self.connection.get_atom_by_name(key)
        return value
