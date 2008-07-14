class Focus(object):
    def __init__(self):
        self.stack = []   

    def add_client(self, client):
        if client in self.stack:
            self.stack.remove(client)
        self.stack.append(client)

    def del_client(self, client):
        self.stack.remove(client)
