# Copyright (c) 2008-2009, samurai-x.org
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the samurai-x.org nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SAMURAI-X.ORG ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL SAMURAI-X.ORG  BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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

