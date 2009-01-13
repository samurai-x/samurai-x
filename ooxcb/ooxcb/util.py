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

class cached_property(object):
    """
        A simple cached property descriptor.
        from http://ronny.uberhost.de/simple-cached-for-properties-done-right
    """
    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        
        result = self.func(obj) 
        setattr(obj, self.name, result)
        return result

