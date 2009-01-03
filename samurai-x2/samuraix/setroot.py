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

import logging
log = logging.getLogger(__name__)

import samuraix.drawcontext
import pyxcb

from .utils import hex2cairocolor

def set_root_image(screen, color=None, image=None, position=None, size=None):
    """
        :Parameters:
            `screen`
                The pyxcb.screen.screen
            `color`
                Color as hex value (e.g. #ff0000)
            `image`
                The image filename
            `position`
                image position as tuple (default: (0, 0))
            `size`
                root size as tuple (default: screen's full size)
    """
    root = screen.root
    
    x, y = position or (0, 0)
    w, h = size or screen.size_in_pixels

    pixmap = pyxcb.pixmap.Pixmap.create(screen.connection, root, w, h, screen.root_depth)
    context = samuraix.drawcontext.DrawContext(screen, w, h, pixmap)

    if color is not None:
        context.fill(hex2cairocolor(color))

    if image is not None:
        if image.endswith('.svg'):
            context.svg(image, x, y, w, h)
        elif image.endswith('.png'):
            context.png(image, x, y, w, h)
        else:
            log.error('Can only render svg and png as root background at the moment! (%s) ' % image)
            
    root.attributes = {'back_pixmap': pixmap}

