import logging
log = logging.getLogger(__name__)


class FocusStack(list):

    def __init__(self):
        self.stack = []   

    def move_to_top(self, client):
        if self.stack[-1] and self.stack[-1]() == client:
            return 
        for c in self.stack:
            if c() == client:
                self.stack.remove(c)
                self.stack.append(c)
                break
        raise ValueError(client)

    def remove(self, client):
        self.stack.remove(client)

    def add(self, client):
        self.stack.append(client)

    def prev(self):
        c = self.stack.pop(-1)
        self.stack.insert(0, c)
        return self.current()

    def next(self):
        c = self.stack.pop(0)
        self.stack.append(c)
        return self.current()

    def current(self):
        return self.stack[-1]
