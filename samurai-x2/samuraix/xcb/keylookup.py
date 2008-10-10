from . import keysymdef

X_KEYS = ['Home', 'Left', 'Up', 'Right', 'Down', 'Page_Up',
          'Page_Down', 'End', 'Begin', 'BackSpace',
          'Return', 'Escape', 'KP_Enter'] + \
         ['F%d' % i for i in range(1, 36)]

def keysym_to_str(keysym):
    """
        convert a keysym to its equivalent character and return it.
        Should work for most keys.

        Ported from awesome's keygrabber.c:keysym_to_str
    """
    # first, check the X keys
    for xkey in X_KEYS:
        if keysym == getattr(keysymdef, 'XK_%s' % xkey):
            return xkey
    # then check KP_Space
    if keysym == keysymdef.XK_KP_Space:
        return ' '
    # then check the hyphen
    elif keysym == keysymdef.XK_hyphen:
        return '-'
    # it must be a char, return it
    return chr(keysym & 0x7F)

