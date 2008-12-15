# Copyright (c) 2008, samurai-x.org
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

class Pythonizer(object):
    """
        This is a pythonizer manager class.
        A pythonizer is a function with the following signature:

        ::

            def pythonizer(connection, data)

        It takes a `Connection` object as first argument, the
        internal xcb data as second argument and returns
        the Python representation of the resource.
        
        You can register pythonizers using this class:

        ::

            def pythonizer(connection, data):
                # ...

            Pythonizer.register_pythonizer('WINDOW', pythonizer)

        is equivalent to:

        ::

            @Pythonizer.pythonizer('WINDOW')
            def pythonizer(connection, data):
                # ...

        All pythonizers are stored in the class member `pythonizers`.

        You can now instantiate a `Pythonizer` instance for a specified
        `Connection`:

        ::

            connection_pythonizer = Pythonizer(connection)
            window_object = connection.pythonize('WINDOW', 135)

        The second line invokes the pythonizer and returns the pythonized value.

    """
    pythonizers = {}

    def __init__(self, connection):
        self.connection = connection

    @classmethod
    def register_pythonizer(cls, identifier, pythonizer):
        """
            register `pythonizer` as pythonizer for
            the identifier `identifier`
        """
        cls.pythonizers[identifier] = pythonizer

    @classmethod
    def pythonizer(cls, identifier):
        """
            A convenience decorator generator.
           
            Example:
            ::

                @Pythonizer.pythonizer('WINDOW')
                def pythonizer(connection, data):
                    # ...

        """
        def deco(func):
            cls.register_pythonizer(identifier, func)
            return func
        return deco

    def pythonize(self, identifier, data):
        """
            return the Python equivalent for `data`,
            use the pythonizer for the identifier `identifier`.
        """
        return self.pythonizers[identifier](self.connection, data)

