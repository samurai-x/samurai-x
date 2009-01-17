from samuraix.plugin import Plugin

class UnsuitableAction(Exception):
    pass

class ActionInfo(dict):
    def __missing__(self, key):
        raise UnsuitableAction('The action and its emitter are unsuitable.') # TODO: more helpful message

def parse_emission(line):
    """
        parse an action emission line.

        "foo.bar a=4 slurp='bla\tbla'" would result in
        ('foo.bar', {'a':4, 'slurp': 'bla\tbla'}).
    """
    gen = iter(line)

    def push_blank():
        char = gen.next()
        while char in ' \t':
            char = gen_next()
        return char

    def p_string(char):
        # `char` is " or '
        s = ''
        while True:
            char = gen.next()
            if char == '\\':
                # escaped character follows ...
                char = (char + gen.next()).decode('string-escape')
            if char in '"\'':
                break
            s += char
        return s

    def p_ident(char=''):
        py = char
        while True:
            try:
                char = gen.next()
            except StopIteration:
                break
            if char in ' \t:=':
                break
            py += char
        try:    
            py = int(py)
        except ValueError:
            pass

        return py

    def p_value(c):
        py = c
        char = gen.next()
        if char in '"\'':
            py = p_string(char)
        else:
            py = p_ident(char)
        return py

    def p_kwargs():
        py = {}
        while True:
            try:
                c = push_blank()
                name = p_ident(c)
            except StopIteration:
                break
            else:
                try:
                    value = p_value(c)
                except StopIteration:
                    raise Exception('Incomplete arguments list')
                except AssertionError:
                    raise Exception('= expected')
                py[name] = value
        return py

    # first, parse the name
    name = p_ident()
    # parse the kwargs
    kwargs = p_kwargs()
    return name, kwargs

class SXActions(Plugin):
    key = 'actions'

    def __init__(self, app):
        self.app = app
        self.actions = {}

    def register(self, ident, action):
        """
            add an action an user can connect
            to. `ident` is a, preferable dotted,
            name to identify the action.
            `action` is a callable taking one
            argument:

            ::

                def my_action(info)

            `info` is an `Info` instance. If you
            try to access a non-existing item 
            (so the action and the emitter do not fit),
            it will print an error message to the user.
        """
        self.actions[ident] = action

    def emit(self, line, info):
        """
            emit the action specified by the emission line `line`.
            `info` will be updated with the information from the
            emission line!
        """
        ident, kwargs = parse_emission(line)
        info.update(kwargs)
        return self.actions[ident](info)

