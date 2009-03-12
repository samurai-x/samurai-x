Getting Started
===============

If you want to use ooxcb in your application, you first have to import it.
You also need to import a module that provides with a core protocol
implementation. That's most likely the :mod:`ooxcb.xproto` module:

::

    import ooxcb
    import ooxcb.xproto

The second import registers the xproto module as core module, so that import
is necessary.

Then, you will want to establish a connection to the X server. That is done
using the :func:`ooxcb.connect` method:
