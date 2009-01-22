class AtomDict(dict):
    """
        A dictionary which is able to lazily load an atom:

        ::

            dic = AtomDict(my_connection)
            print dic['WM_CLASS'] # Yay, it is lazily loaded!

        You should not modify that manually.

    """
    def __init__(self, conn, *boo, **far):
        dict.__init__(self, *boo, **far)
        self.conn = conn
        self._by_id = {}

    def __missing__(self, key):
        self[key] = value = self.conn.core.intern_atom(key, False).reply().atom
        self._by_id[value.get_internal()] = value
        return value

    def get_by_id(self, aid):
        from .xproto import Atom # TODO: uuuuuuuugly
        if aid == 0:
            return None # TODO: That's basically AnyProperty ... better solution?
        try:
            return self._by_id[aid]
        except KeyError:
            self._by_id[aid] = atom = Atom(self.conn, aid)
            name = atom.get_name().reply().name.to_string()
            self[name] = aid
            return atom
