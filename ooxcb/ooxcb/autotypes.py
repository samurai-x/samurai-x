from .protocol import xproto

def _resource(type):
    def _converter(conn, values):
        return [conn.get_from_cache_fallback(value, type) for value in values]
    return _converter

AUTO_TYPES = {
    'WINDOW': _resource(xproto.Window),
    'DRAWABLE': _resource(xproto.Drawable),
    'STRING': lambda conn, values: ''.join(map(chr, values)),
    'UTF8_STRING': lambda conn, values: ''.join(map(chr, values)).decode('utf-8'),
    'CARDINAL': lambda conn, values: values,
    'ATOM': lambda conn, values: map(conn.atoms.get_by_id, values),
    'INTEGER': lambda conn, values: values,
}

class AutotypesError(Exception):
    pass

def autoconvert_value(conn, type, values):
    """
        Return a converted version of *values*.
        :Parameters:
            `conn`
            `type`: Atom
            `values`:
                A list of numeric values descsribing the value.
    """
    type_name = type.get_name().reply().name
    if type_name not in AUTO_TYPES:
        raise AutotypesError("Don't know how to convert %r" % type_name)
    return AUTO_TYPES[type_name](conn, values)
