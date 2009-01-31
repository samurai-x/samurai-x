from .memstream import MemoryInputStream

class Protobj(object):
    def __init__(self, conn):
        self.conn = conn

    def read(self, stream):
        raise NotImplementedError()

    def read_from_address(self, address):
        """
            parse the memory at `address`
        """
        return self.read(MemoryInputStream(address))

    @classmethod
    def create_from_address(cls, conn, address):
        self = cls(conn)
        self.read_from_address(address)
        return self

    @classmethod
    def create_from_stream(cls, conn, stream):
        self = cls(conn)
        self.read(stream)
        return self

