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

.. _xpyb: http://cgit.freedesktop.org/xcb/xpyb
.. _weak value dictionary: http://docs.python.org/library/weakref.html#weakref.WeakValueDictionary
