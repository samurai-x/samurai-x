from subprocess import Popen

class Action(object):
    def __init__(self):
        pass

    def __call__(self, screen):
        pass

class Spawn(Action):
    def __init__(self, cmd):
        self.cmd = cmd

    def __call__(self, screen):
        pid = Popen(self.cmd, shell=True).pid

class Quit(Action):
    def __call__(self, screen):
        screen.app.stop()

class NextDesktop(Action):
    def __init__(self):
        pass

    def __call__(self, screen):
        screen.next_desktop()

class PreviousDesktop(Action):
    def __init__(self):
        pass

    def __call__(self, screen):
        screen.previous_desktop()

class MaximiseClient(Action):
    def __init__(self):
        pass

    def __call__(self, screen):
        screen.maximise_client()

