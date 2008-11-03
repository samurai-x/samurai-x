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

import sys

from pyglet.window.xlib import xlib

import samuraix
from samuraix.drawcontext import DrawContext
from samuraix.sxctypes import byref


def hex2xlibcolor(screen, color):
    #"CIEXYZ:0.3227/0.28133/0.2493"
    #"RGBi:1.0/0.0/0.0"
    #"rgb:00/ff/00"
    #"CIELuv:50.0/0.0/0.0"

    color = 'rgb:%s/%s/%s' % (color[:2], color[2:4], color[4:6])

    ecolor = xlib.XColor()

    if not xlib.XParseColor(samuraix.display, screen.default_colormap, color, byref(ecolor)):
        raise ValueError("cant parse color %s" % color)

    if not xlib.XAllocColor(samuraix.display, screen.default_colormap, byref(ecolor)):
        raise "Cant alloc color"

    #DYNAMIC = 1

    #if (ecolor.pixel != screen.black_pixel and     
    #    ecolor.pixel != screen.white_pixel and
    #    screen.default_visual.class & DYNAMIC):
    return ecolor.pixel   


def hex2cairocolor(color):
    return (
        int(color[:2], 16) / 255.0,
        int(color[2:4], 16) / 255.0,
        int(color[4:6], 16) / 255.0,
    )


def set_root(screen, color=None, image=None, image_size=None, image_position=None):
    root = screen.root_window
    geom = screen.geom

    if color is not None and image is None:
        pixel = hex2xlibcolor(screen, color)

        xlib.XSetWindowBackground(samuraix.display, root, pixel)

    if image is not None:
        assert image.endswith('.svg'), "can only render svg images at the moment!"

        if image_size is None:
            image_size = geom.width, geom.height

        if image_position is None:
            image_position = 0, 0

        drawable = xlib.XCreatePixmap(samuraix.display, root, geom.width, geom.height, 
                                      screen.default_depth)

        context = DrawContext(screen, geom.width, geom.height, drawable)

        if color is not None:
            context.fill(hex2cairocolor(color))

        context.svg(image, x=image_position[0], y=image_position[1],
                           width=image_size[0], height=image_size[1])

        xlib.XSetWindowBackgroundPixmap(samuraix.display, root, drawable)

    xlib.XClearWindow(samuraix.display, root)


def run(args=None):
    from optparse import OptionParser

    from samuraix.screen import SimpleScreen
    from samuraix import xhelpers

    parser = OptionParser()

    parser.add_option("-d", "--display", dest="display_name", default=None,
                      help="display to use")
    parser.add_option("-s", "--screen", dest="screen_num", default=None, type="int",
                      help="screen number to use")

    parser.add_option("-c", "--color", dest="color", default=None,
                      help="color to use (hex style with no leading #, eg. ff0000)")
    parser.add_option("-i", "--image", dest="image", default=None,
                      help="image to use (currently only svg files are supported)")
    parser.add_option("-z", "--size", dest="image_size", nargs=2, default=None, type="int",
                      help="image size")
    parser.add_option("-p", "--pos", dest="image_position", nargs=2, default=None, type="int",
                      help="image position")
    

    #parser.add_option("-d", "--debug",
    #                  action="store_true", dest="debug", default=False,
    #                  help="print debug messages to stdout")
    #parser.add_option('-c', "--config",
    #                  dest='configfile', default=None,
    #                  help="config file to use")
    #parser.add_option('', '--dumpconfig', dest='dumpconfig', default=False,
    #                  help="dump the default config to stdout and quit")

    if args is None:
        args = sys.argv[1:]

    options, args = parser.parse_args(args=args)

    if args:
        print "this command takes no arguments - see --help"
        sys.exit(1)

    xhelpers.open_display(display_name=options.display_name)
    if options.screen_num is None:
        options.screen_num = xlib.XDefaultScreen(samuraix.display)
    screen = SimpleScreen(options.screen_num)

    try:
        set_root(screen, 
            color=options.color,
            image=options.image,
            image_size=options.image_size,
            image_position=options.image_position,
        )
    finally:
        xhelpers.close_display()


if __name__ == '__main__':
    run()

