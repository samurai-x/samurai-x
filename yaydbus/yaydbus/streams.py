import os

class SocketStream(object):
    def __init__(self, fd):
        self._fd = fd
        self.closed = False
        self._bytecount = 0
    
    def close(self):
        self.closed = True
        os.close(self._fd)
    
    def fileno(self):
        return self._fd

    def flush(self):
        pass

    def isatty(self):
        return False

    def readable(self):
        return True

    def readline(self, limit):
        buf = ''
        while (buf[-1] != '\n' and len(buf) < limit):
            buf += self.read(1)
        return buf

    def seek(self, offset, whence=0):
        if whence != 1:
            raise NotImplementedError("Only whence = 1 supported for SocketStream")
        self.read(offset)
        return self._bytecount

    def seekable(self):
        return True

    def tell(self):
        return self._bytecount

    def truncate(self, size):
        raise NotImplementedError()

    def writable(self):
        return True

    def writelines(self, lines):
        for line in lines:
            self.write(line + '\n')

    def read(self, n=-1):
        if n == -1:
            raise NotImplementedError("Stream has no end.")
        buf = ''
        while len(buf) < n:
            chunk = os.read(self._fd, n - len(buf))
            if not chunk:
                raise IOError("End of socket reached. Argh!")
            buf += chunk
        self._bytecount += n
        return buf

    def write(self, s):
        count = 0
        length = len(s)
        while count < length:
            count += os.write(self._fd, s[count:])
        return count

    def readall(self):
        return self.read()

    def readinto(self, n):
        raise NotImplementedError("Uh?")

    # Special method.
    def reset_count(self):
        self._bytecount = 0

class StreamSlice(object):
    """
        a stream that proxies all methods of the parent stream,
        but has its own byte counter. So, stream.tell()
        will return the number of bytes read via this stream
        slice.
    """
    def __init__(self, stream):
        self._stream = stream
        self._bytecount = 0

    def close(self):
        return self._stream.close()

    def fileno(self):
        return self._stream.fileno()

    def flush(self):
        return self._stream.flush()

    def isatty(self):
        return self._stream.isatty()

    def readable(self):
        return self._stream.readable()

    def readline(self, limit):
        buf = ''
        while (buf[-1] != '\n' and len(buf) < limit):
            buf += self.read(1)
        return buf

    def seek(self, offset, whence=0):
        if whence != 1:
            raise NotImplementedError("Only whence = 1 supported for SocketStream")
        self.read(offset)
        return self._bytecount

    def seekable(self):
        return self._stream.seekable()

    def tell(self):
        return self._bytecount

    def truncate(self, size):
        raise NotImplementedError()

    def writable(self):
        return self._stream.writable()

    def writelines(self, lines):
        for line in lines:
            self.write(line + '\n')

    def read(self, n=-1):
        if n == -1:
            raise NotImplementedError("Not possible for me!")
        self._bytecount += n
        return self._stream.read(n)

    def write(self, s):
        return self._stream.write(s)

    def readall(self):
        return self.read()

    def readinto(self, n):
        raise NotImplementedError("Uh?")

    # Special method.
    def reset_count(self):
        self._bytecount = 0
