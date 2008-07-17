class FocusStack(list):
    def __init__(self):
        self.stack = []   

    def focus(self, client):
        if client in self.stack:
            self.stack.remove(client)
        self.stack.append(client)

    def remove(self, client):
        self.stack.remove(client)

    def add(self, client):
        self.focus(client)

    def prev(self):
        c = self.stack.pop(-1)
        self.stack.insert(0, c)

    def next(self):
        c = self.stack.pop(0)
        self.stack.append(c)

    def current(self):
        return self.stack[-1]
