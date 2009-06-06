.. _sx-actions:

.. currentmodule:: sxactions

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

*info* is a dictionary (i.e. a :class:`ActionInfo` instance)
containing information about the situation in which the
action is emitted. It can also contain information the user provided in the
so-called action line. We call that *info* dictionary the "parameter dictionary".
It contains parameters.

If the handler tries to access items that do not exist in the *info*, a
warning is printed to the log.

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
    :module:

    spawns an application.

    :Parameters:
        `cmdline`
            the command line of the application to launch

.. function:: quit()
    :module:

    quits samurai-x2 gracefully.

.. function:: log(message)
    :module:

    logs the message *message* into the log (debug level)

    :Parameters:
        `message`: str

How to use it in your plugin
----------------------------

Registering an action handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to provide an action handler, you have to think of
a nice name for your action first. It would be nice if you'd
choose a dotted name, with the key of your plugin as the first
element. For example, if your plugin is `sx-webbrowser`, and
you want to register an action that opens a webbrowser,
a nice name for it would be `webbrowser.open`.

After that, you need a Python callable that takes one argument.
That will most likely be a function or a method::

    def open_webbrowser_action(info)

*info* is a dictionary containing the parameters the user provided
in his action emission line and, maybe, some additional information
provided by the emitting plugin.

Let's say your `webbrowser.open` action takes one parameter that
the user has to specify in his emission line: *url*, the address
to point to. The *info* dictionary contains it.

Now you can write your handler function (note that we import the
:mod:`webbrowser` module from the Python standard library)::

    import webbrowser

    def open_webbrowser_action(info):
        webbrowser.open(info['url'])

Fine. Now you just have to register your handler function (you need
a reference to the samurai-x2 :class:`samuraix.appl.App`)::

    app.plugins['actions'].register('webbrowser.open', open_webbrowser_action)

Now, the user is able to emit your action!

Emitting actions
~~~~~~~~~~~~~~~~

If you have a plugin that deals with events and you want to make it possible
to connect these events to actions, you can just use sx-actions this way::

    # ...
    info = {"parameter": some_value, "some_other_parameter": some_other_value}
    app.plugins['actions'].emit(action_line, info)

The connection of events to action lines (and the storing of action lines) is
the responsibility of your plugin.

D-Bus interface
---------------

If a plugin providing the *dbus* key is available, sx-actions registers the
following D-Bus methods:

.. method:: org.samuraix.ActionsInterface.action(action_line)

    Emit the action *action_line*.

API documentation
-----------------

.. automodule:: sxactions
    :members:
    :undoc-members:
