.. _sx-cairodeco:

sx-cairodeco
============

sx-cairodeco is a plugin that uses the `cairo`_ graphics library
to render some nice window decoration.

It's plugin key is "decoration".

Dependencies
------------

sx-cairodeco depends on the `cairo`_ library and :ref:`sx-actions`.

Configuration
-------------

.. attribute:: cairodeco.bindings

    A dictionary mapping :ref:`buttonstrokes` to to action lines.
    The actions are emitted if the user clicks on the title bar.
    Provided information:

        * `screen`, the current :class:`Screen <samuraix.screen.Screen>` instance
        * `x` and
        * `y`, the coordinates of the button click event.
        * `client`, the :class:`client <samuraix.client.Client>` the frame belongs to.

    Default: no bindings.

.. attribute:: cairodeco.height

    The height of the title bar (int, in pixels).

    Required.

.. attribute:: cairodeco.title.position

    Alignment of the title text (one of "left", "center", "right").

    Required.

.. attribute:: cairodeco.color
    
    Background color of the titlebar in hexadecimal rgb notation
    (#RRGGBB, example: #FF0000 for red) for the focused window.

    Required.

.. attribute:: cairodeco.title.color

    Color of the window title in hexadecimal rgb notation for
    the focused window.

    Required.

.. attribute:: cairodeco.inactive_color

    Background color of the titlebar in hexadecimal rgb notation
    for inactive (= not focused) windows.

    Defaults to the value of :attr:`cairodeco.color`.

.. attribute:: cairodeco.title.inactive_color

    Color of the window title in hexadecimal rgb notation for
    inactive windows.

    Defaults to the value of :attr:`cairodeco.title.color`.

Example
~~~~~~~

::

    'cairodeco.bindings': {
            '1': 'moveresize.move',
            '3': 'moveresize.resize',
        },
    'cairodeco.height': 15,
    'cairodeco.title.position': "center",
    'cairodeco.color': '#cc0000',
    'cairodeco.title.color': '#ffffff',
    'cairodeco.title.inactive_color': '#000000'

.. _buttonstrokes:

Buttonstrokes
-------------

Buttonstrokes are similar to :ref:`keystrokes`, except that they take
button indices (1, 2 or 3) instead of keys.

Examples::

    1
    CTRL+3
    Meta+2
    ctrl+Shift+1

API documentation
-----------------

.. automodule:: sxcairodeco
    :members:
    :undoc-members:


.. _cairo: http://www.cairographics.org
