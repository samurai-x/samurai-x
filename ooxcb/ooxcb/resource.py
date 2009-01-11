from .eventsys import EventDispatcher

class Resource(EventDispatcher):
    def __init__(self, conn, xid):
        self.conn = conn
        self.xid = xid

    def get_internal(self):
        return self.xid

