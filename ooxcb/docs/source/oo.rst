The 'oo' of 'ooxcb'
===================

... stands for *object oriented*. Yes, ooxcb tries to be as object oriented as possible, 
like Python.

The X world often is object oriented. There are some server-side things that are identified
by an X ID: let's call them resources. Examples for resources are Windows, GCs, Drawables
or Fonts. In contrast to `xpyb`_, ooxcb creates wrapper classes for them, and it also tries
to adopt the X server's kind of object type inheritance: A Window is a subclass of Drawable.
GC is a subclass of Fontable, same for Font.
And they have got real Python methods. In most cases, it is easy to figure out what the
'subject' of a request is (e.g. ConfigureWindow should map to a `configure` method on Window
objects). Sometimes it isn't, but we try to use the best solution.

You can always get the X id of a resource by calling its `get_internal` method, or, more
obvious, by accessing its `xid` attribute.

The Cache
---------

If the X IDs of two objects are equal, they are representing identical objects. And it is not nice
to have two objects for the same X resource in Python. So we need a cache, and ooxcb has one!
However, it is a very simple cache. Assuming that two different objects will not have the same
X id if they are not identical, regardless if they have the same 'type', it is possible to use
an X id -> Python object dictionary as a cache.

In the samurai-x2 ctypes pyxcb binding, we had an implicit cache:

::

    # Note: That is NOT working in ooxcb!
    a = Window(conn, 123)
    b = Window(conn, 123)
    a is b # -> True

(that was done using some metaclass magic)

However, as we all know, explicit is better than implicit, and because of that, the above
code snippet will not produce identical objects `a` and `b` in ooxcb. You will have to manually
invoke the cache:

::

    # if there is no object managing the X id 123, instantiate Window and return.
    a = conn.get_from_cache_fallback(123, Window)
    # so, there is one now, so return it from the cache.
    b = conn.get_from_cache_fallback(123, Window)
    a is b # -> True

That's a bit more verbose, but explicit.

The connection uses a `weak value dictionary`_ as cache, so you don't have to
explictly remove items from the cache. If you want to do anyway, try this:

::

    # will raise a KeyError if there is no object managing the X id 123.
    conn.remove_from_cache(123)
    # that one won't.
    conn.remove_from_cache_safe(123)

.. _mixins:

Mixins
------

So, ooxcb is object-oriented. The module of the core protocol, :mod:`ooxcb.protocol.xproto`,
defines some classes, and each class has some methods. All fine.

But what if you want to load and use an extension module now? Let's say you want to use
the xtest extension. It defines one method whose subject is a window:
:meth:`compare_cursor <ooxcb.protocol.xtest.WindowMixin.compare_cursor>`. It would
be consistent to have that method as a member of the ordinary :class:`Window <ooxcb.protocol.xproto.Window>`
class, so that we don't have to write calls like
``ooxcb.protocol.xtest.window_compare_cursor(my_window, my_cursor)`` - ``my_window.compare_cursor(my_cursor)``
is much clearer and consistent.

So, ooxcb uses mixins for extensions. However, not everyone likes mixins, so they're optional -
if you want an extension to mix its additional methods into the core classes, you have to
say that explicitly by calling its ``mixin`` function.

Let's take the xtest example. If you want to call the
:meth:`compare_cursor <ooxcb.protocol.xtest.WindowMixin.compare_cursor>` method on a window object
(let's call it ``my_window``) with the argument ``my_cursor``, you can do it that way using mixins::

    import ooxcb.protocol.xtest
    # The following method makes xtest mix all additional methods into the base classes.
    ooxcb.protocol.xtest.mixin()
    # Now we can call them, just as they were regular methods.
    my_window.compare_cursor(my_cursor)

If you don't like mixins, you can achive the same without them::

    import ooxcb.protocol.xtest
    # We don't call .mixin() here.
    # Now, just call the method with the subject (`self`) as the first argument.
    ooxcb.protocol.xtest.WindowMixin.compare_cursor(my_window, my_cursor)
    # A bit verbose. Keep in mind that you can of course use
    # imports to get rid of the namespaces - like `from ooxcb.protocol import xtest`.

You see, the class that defines `compare_cursor` inside the xtest module is named
``WindowMixin`` - it's just the name of the target class plus 'Mixin'.

.. note:: Don't try to instantiate :class:`WindowMixin <ooxcb.protocol.xtest.WindowMixin>`
          or any other mixin class.
          It won't work.

This concept of mixins doesn't only apply to protocol extensions, but also to some of
the modules inside :mod:`ooxcb.contrib` (e.g. :mod:`ooxcb.contrib.ewmh`). However,
these don't necessarily use the concept of *classes* whose methods are mixed into
other classes; it is also possible that they just add a defined set of functions as methods
to a class. For more information, just check out the corresponding module documentation.

.. _xpyb: http://cgit.freedesktop.org/xcb/xpyb
.. _weak value dictionary: http://docs.python.org/library/weakref.html#weakref.WeakValueDictionary
