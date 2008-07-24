from subprocess import Popen


class spawn(object):
    def __init__(self, cmd):
        self.cmd = cmd
    def __call__(self, screen):
        pid = Popen(self.cmd, shell=True).pid


class screenfunc(object):
    def __init__(self, funcname, *args):
        self.funcname = funcname
        self.args = args
    def __call__(self, screen):
        func = getattr(screen, self.funcname)
        func(*self.args)


class activedesktopfunc(object):
    def __init__(self, funcname, *args):
        self.funcname = funcname
        self.args = args
    def __call__(self, screen):
        func = getattr(screen.active_desktop, self.funcname)
        func(*self.args)


class focusedwindowfunc(object):
    def __init__(self, funcname, *args):
        self.funcname = funcname
        self.args = args
    def __call__(self, screen):
        if screen.focused_client is not None:
            func = getattr(screen.focused_client, self.funcname)
            func(*self.args)


class clientfunc(object):
    def __init__(self, funcname, *args):
        self.funcname = funcname
        self.args = args

    def __call__(self, client):
        func = getattr(client, self.funcname)
        func(*self.args)


