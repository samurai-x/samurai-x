from .protobj import Protobj

class Request(Protobj):
    def __init__(self, buffer, opcode, void, checked):
        # TODO: check size??
        self.opcode = opcode
        self.is_void = void
        self.is_checked = checked

        Protobj.__init__(self, buffer)
        self._buf = buffer

