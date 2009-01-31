import ctypes

class MemoryInputStream(object):
    """
        `MemoryInputStream` is an object implementing the buffer
        interface which reads its data from a certain
        memory buffer. It is interpreted as an infinite
        array of 8-bit chars.
    """
    def __init__(self, address):
        """
            :Parameters:
                `address` : int
                    The address of the first character.
        """
        self._root = address
        self._ptr = address
        self._opened = True

    def close(self):
        self._opened = False

    @property
    def closed(self):
        return not self._opened

    def fileno(self):
        """ We are not using a file descriptor """
        raise IOError()

    def flush(self):
        pass

    def isatty(self):
        return False

    def readable(self):
        return True

    def readline(self, limit):
        raise NotImplementedError()
    
    def readlines(self, hint):
        raise NotImplementedError()

    def seek(self, offset, whence=0):
        """
            Currently you can not use whence=2.
            The stream has no end.
        """
        if whence == 0: 
            # from the start position of the stream
            self._ptr = self._root + offset
            return offset
        elif whence == 1:
            # from the current position of the stream
            self._ptr += offset
            return self._ptr - self._root
        elif whence == 2:
            # from the end of the stream ... impossible, sorry.
            raise NotImplementedError('The memory stream has no end!')
        else:
            raise NotImplementedError('Unknown whence: %d' % whence)

    @property
    def address(self):
        return self._root

    def seekable(self):
        return True

    def tell(self):
        return self._ptr - self._root

    def truncate(self):
        """ 
            That's a no-op here. I can't think of anyone needing that
            for a memory buffer, really.
            However, it will raise a NotImplementedError. But we can
            remove that.
        """
        raise NotImplementedError() # hmmm ...

    def writable(self):
        return False

    def write(self, b):
        raise IOError()

    def read(self, b=None):
        if b is None:
            raise NotImplementedError('The memory stream has no end!')
        chunk = ctypes.string_at(self._ptr, b)
        self._ptr += b
        return chunk

    def readall(self):
        raise NotImplementedError('The memory stream has no end!')

    def readinto(self, b):
        length = len(b)
        b.extend(self.read(length))
        return length

if __name__ == '__main__':
    # TODO: build a nice test for that.
    buf = ctypes.create_string_buffer('abcdefghijklmnopqrstuvwxyz')
    stream = MemoryInputStream(ctypes.addressof(buf))
    print stream.read(2)
    print stream.read(4)
    print stream.seek(0)
    print stream.read(26)
    print repr(stream.read(10))

