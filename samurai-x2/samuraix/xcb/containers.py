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

US_POSITION = 1 << 0
US_SIZE = 1 << 1
P_POSITION = 1 << 2
P_SIZE = 1 << 3

class SizeHints(object):
    properties = ('x', 'y', 'width', 'height', 'min_width', \
              'min_height', 'max_width', 'max_height', 'width_inc',
              'height_inc', 'min_aspect_num', 'min_aspect_den',
              'max_aspect_num', 'max_aspect_den', 'base_width', 'base_height',
              'flags', 'win_gravity')
 
    def __init__(self, **kwargs):
        for prop_name in self.properties:
            setattr(self, prop_name, kwargs.get(prop_name, 0)) # TODO: not so nice

        # TODO: implement aspect ratios (using `fractions`?)

    def __repr__(self):
        return '<SizeHints perfect size = %s>' % (self.perfect_size,)

    @property
    def perfect_position(self):
        return (self.perfect_x, self.perfect_y)

    @property
    def perfect_x(self):
        return self.x # TODO

    @property
    def perfect_y(self):
        return self.y # TODO

    @property
    def perfect_size(self):
        return (self.perfect_width, self.perfect_height)

    @property
    def perfect_width(self):
        if self.user_specified_size: #or self.program_specified_size:
            return self.width # User-specified size
        i = 10
        return (self.base_width or self.min_width) + i * self.width_inc # TODO: let the user choose `i` 

    @property
    def perfect_height(self):
        if self.user_specified_size: #or self.program_specified_size:
            return self.height # User-specified size
        j = 10
        return (self.base_height or self.min_height) + j * self.height_inc # TODO: let the user choose `j` 

    @property
    def user_specified_size(self):
        return bool(self.flags & US_SIZE)

    @property
    def user_specified_position(self):
        return bool(self.flags & US_POSITION)

    @property
    def program_specified_size(self):
        return bool(self.flags & P_SIZE)

    @property
    def program_specified_position(self):
        return bool(self.flags & P_POSITION)
