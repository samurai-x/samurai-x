Introduction
============

What is ooxcb?
--------------

ooxcb is a new Python binding to the X server, developed for the `samurai-x`_ window manager.
xpyb uses a wrapper generator to create python modules out of the XML X protocol descriptions 
of the `xcb`_ project. It aims to provide with an easy-to-use pure-python interface to the X server.

Why?
----

There already is a similar project called `xpyb`_ which is able to create an usable Python
module for every X extension supported by `xcb-proto`_. However, the most important parts
of xpyb are in a C extension, and we wanted `samurai-x`_ to be pure-python. So we ported
the whole C code of xpyb to Python, just using some functions of the libxcb API invoked by
the ctypes module (you can get it `here <http://samurai-x.org/browser/xpyb-ctypes>`_, but beware:
it's a bit unstable).
Apart from that, xpyb-generated bindings are very close to the X protocol. For every extension, 
you have one class that has some methods for each request. On the one hand, xpyb is able to cover
all the extensions supported by xcb-proto this way; on the other hand, the binding is not very
comfortable to use. Because of that, we decided to write our own binding, based on the xpyb-ctypes code.
The xpyb wrapper generator uses so-called interface files that describe the desired Python API of
a specific extension - so we can create an API that is more comfortable and easy-to-use.
However, somebody has to write these interface files, and depending on the size and complexity of
the extension, that's a time-intensive job. At the moment, only the most important parts of the
xproto (the core) extension. You can see the current state of the interface file 
`here <http://samurai-x.org/browser/ooxcb/xproto.i>`_ (yes, it's YAML!).

Additionally, ooxcb comes with a simple and powerful event dispatching system (stolen from `pyglet`_) -
you don't have to use it necessarily, but it can make life much easier.

How does it look?
-----------------

Here's a minimal example that displays a white window and exits if a mouse button is pressed:

::

    import sys

    import ooxcb
    from ooxcb.xproto import *

    conn = ooxcb.connect()

    setup = conn.get_setup()
    root = setup.roots[0].root
    depth = setup.roots[0].root_depth
    visual = setup.roots[0].root_visual

    win = Window.create(conn, root, depth, visual, back_pixel=setup.roots[0].white_pixel, 
            event_mask=EventMask.Exposure | EventMask.ButtonPress)
    win.configure(width=100)
    win.map()
    conn.flush()

    @win.event
    def on_button_press(evt):
        print 'Button pressed, exiting!'
        conn.disconnect()
        sys.exit()

    while True:
        try:
            conn.wait_for_event().dispatch()
        except ooxcb.ProtocolException, error:
            print "Protocol error %s received!" % error.__class__.__name__
            break
    conn.disconnect()

Is it usable?
-------------

As said above, much of the xproto extension is already wrapped, and ooxcb is relatively stable, so it
should be possible to use it (we are already using it for samurai-x).
If you stumble upon bugs or missing important functions, please report them on the 
`bug tracker <http://samurai-x.org/newticket>`_.

.. _xcb: http://xcb.freedesktop.org
.. _xpyb: http://cgit.freedesktop.org/xcb/xpyb/
.. _xcb-proto: http://cgit.freedesktop.org/xcb/proto/
.. _samurai-x: http://samurai-x.org
.. _pyglet: http://pyglet.org
