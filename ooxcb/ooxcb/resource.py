from .eventsys import EventDispatcher

class Resource(EventDispatcher):
    def __init__(self, conn, xid):
        self.conn = conn
        self.xid = xid

    def __repr__(self):
        return '<%s XID=%d (0x%x)>' % (self.__class__.__name__, self.xid, id(self))

    def get_internal(self):
        return self.xid

