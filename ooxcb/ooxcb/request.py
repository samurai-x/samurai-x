from .protobj import Protobj

class Request(Protobj):
    def __init__(self, conn, buffer, opcode, void, checked):
        # TODO: check size??
        self.opcode = opcode
        self.is_void = void
        self.is_checked = checked

        Protobj.__init__(self, conn, buffer)
        self._buf = buffer

