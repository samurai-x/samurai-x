import ctypes

class MemBuffer(object):
    def __init__(self, address, size=0):
        self.address = address 
        self.size = size #ctypes.sizeof(self.struct_instance)

    def get_slice(self, size, offset=0):
        return ctypes.string_at(self.address + offset, size)

    def get_subobject(self, offset):
        return MemBuffer(self.address + offset)

    def __len__(self):
        return self.size

    def get_string(self):
        return ctypes.string_at(self.address, self.size)

def struct_to_str(struct):
    return ctypes.string_at(ctypes.addressof(struct), ctypes.sizeof(struct))
