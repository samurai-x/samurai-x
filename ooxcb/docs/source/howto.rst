How to ...
==========

... get the title of the current window
---------------------------------------

There are several properties that can contain the title
of the current window. First, there is `_NET_WM_VISIBLE_NAME` (UTF-8 encoded).
If that property does not exist, there is `_NET_WM_NAME` (UTF-8).
If that property does not exist, there is `WM_NAME` (latin-1).
If that property does not exist, there is no title set.

For your convenience, there is the
:meth:`ewmh_get_window_title <ooxcb.contrib.ewmh.ewmh_get_window_title>` method
in the :mod:`ooxcb.contrib.ewmh` mixin module (see :ref:`mixins`).

