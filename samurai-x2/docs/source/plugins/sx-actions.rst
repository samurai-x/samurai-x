.. _sx-actions:

sx-actions
==========

sx-actions is a plugin that:

 * provides a simple notation to describe actions that should be emitted when
   a certain event occurs
 * provides an interface for other plugins to register action handlers or
   emit actions.

Its plugin key is "actions", sx-actions is not configurable.

Concept
-------

An action handler is just a callable that takes one argument::

    def handler(info)

*info* is a dictionary containing information about the situation in which the
action is emitted. It can also contain information the user provided in the
so-called action line. We call that *info* dictionary the "parameter dictionary".
It contains parameters.

For example, let's say you want to spawn a firefox instance pointing
to http://www.python.org when the user presses Meta+F.
You would have an entry like the following in your samurai-x configuration file::

    config = {
        'bind.keys': {
            'Meta+F': 'spawn cmdline="firefox http://www.python.org"'
        }
    }

The :ref:`sx-bind` plugin has the responsibility to emit the action line
`spawn cmdline="firefox http://www.python.org"` when the user presses the
key combination Meta+F. Then, the sx-actions plugin will see if there is a
Python callable registered as handler for the "spawn" action. This callable
will get a dictionary as its first arguments, containing the parameters
the user specified in the action line plus, if given, some additional
parameters provided by the plugin that emitted the action (the
:ref:`sx-cairodeco` and :ref:`sx-simpledeco` do that, for example).
In this case, the *info* dict will look like this::

    {
        'cmdline': "firefox http://www.python.org"
    }

So, not every action can be emitted from every plugin (because some
action handlers need some special additional parameters that not provided by
every plugin). But don't worry, you will find the required parameters
in the descriptions of every action.

Predefined actions
------------------

There are some predefined actions:

.. function:: spawn(cmdline)

    spawns an application.

    :Parameters:
        `cmdline`
            the command line of the application to launch

.. function:: quit()

    quits samurai-x2 gracefully.

.. function:: log(message)

    logs the message *message* into the log (debug level)

    :Parameters:
        `message`: str

