.. _client-concept:

The Client concept
==================

Like in most window managers, a foreign top-level window is internally
represented by a kind of wrapper class. In samurai-x2, that's the
:class:`samuraix.client.Client`.

Because we wanted to be able to use samurai-x2 with or without a window
decoration plugin, we decided to use an 'actor': A client has
two attributes containing windows, :attr:`samuraix.client.Client.window` and
:attr:`samuraix.client.Client.actor`. The former is *always* the foreign
window, the latter is the decoration window: the actor. If there is no
decoration plugin activated, the actor window is the same as the foreign
window. So it is possible to develop plugins without having to know if there
is a decoration plugin enabled or not, you just have to take care of using
the correct window for each action.

Decoration plugins should just react to the Screen's `on_new_client` event
and set `client.actor` to the desired window. The foreign window *has* to be
reparented to the actor window; so if you move the actor window, the foreign
window will also move because it's a child of the actor window.

When the foreign window was destroyed, the client will also be removed from
the samurai-x2 system. The decoration plugin that injected the actor window
also has to take care of destroying it properly. That is most likely done
in a Screen's `on_unmanage_client` event handler.

You see, you will have to decide if you have to use the actor or the foreign
window:
If your plugin has to resize the displayed window, you should use 
`client.actor.configure`. The decoration should take care of applying the new
size to the window, too.
If your plugin has to read properties of the foreign window, you should use
`client.window.get_property` (of course).
