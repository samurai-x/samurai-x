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

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from PIL import Image

from ooxcb.xproto import ImageFormat

def put_pil_image(gc, drawable, image, dst_x=0, dst_y=0):
    """
        display the PIL image instance *image* on the drawable
        *drawable* using the graphics context *gc*, at
        x = *dst_x* and y = *dst_y*.
        You have to take care that the depths of the drawable
        and the window match.
        No connection flushing is done.

        :todo: use image's depth
    """
    data = image.tostring("raw", "BGRX")
    depth = drawable.get_geometry().reply().depth 
    # ^^^ That's a bit hacky. What if the depths do not match?
    gc.put_image(
        drawable,
        ImageFormat.ZPixmap,
        image.size[0],
        image.size[1],
        dst_x,
        dst_y,
        0,
        depth,
        data)

def get_pil_image(drawable, x=0, y=0, width=None, height=None):
    if (width is None or height is None):
        geom = drawable.get_geometry().reply()
        width = geom.width
        height = geom.height
    reply = drawable.get_image(
           ImageFormat.ZPixmap,
           x, y,
           width, height,
           0xffffffff # to get all bits (this should be big enough)
           ).reply()
    data = ''.join(map(chr, reply.data))
    return Image.fromstring("RGBX", (width - x, height - y),
            data, "raw", "BGRX").convert("RGB")
