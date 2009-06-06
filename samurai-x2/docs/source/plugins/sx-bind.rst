.. _sx-bind:

sx-bind
=======

With sx-bind, you can bind keystrokes to actions.
Its plugin key is "bind".

Dependencies
------------

sx-bind depends on :ref:`sx-actions`.

Provided Parameters
-------------------

There is just one parameter that sx-bind provides in its parameter dictionary:
'screen' is the :class:`samuraix.screen.Screen` object the keystroke was pressed
on.

Configuration
-------------

.. attribute:: bind.keys

    A dictionary connecting :ref:`keystrokes` to action lines.

    Example::

        'bind.keys': {
                'Meta+n': 'desktops.cycle offset=1',
                'Meta+p': 'desktops.cycle offset=-1',
                'Meta+c': 'desktops.cycle_clients',
                'Meta+d': 'log message="pressed d"',
                'Meta+Q': 'quit',
                'Ctrl+R': 'restart',
                'Meta+L': 'layoutmgr.cycle',
        }

.. _keystrokes:

Keystrokes
----------

A keystroke describes a combination of modifier keys and one normal key pressed.
They are joined together by a "+" char. The modifiers are case-insensitive,
the key is not.

Valid modifier names are: 'alt', 'numlock', 'meta', 'altgr', 'shift', 'lock',
'ctrl', 'control', 'mod1', 'mod2', 'mod3', 'mod4', 'mod5'. 

The valid key values are listed in the :mod:`ooxcb documentation <ooxcb.keysymdef>`.

Examples::

    # the following three keystrokes are equal
    Meta+n
    META+n
    mEtA+n
    # some more examples
    SHIFT+metA+0
    Ctrl+alt+Delete

API documentation
-----------------

.. automodule:: sxbind
    :members:
    :undoc-members:

