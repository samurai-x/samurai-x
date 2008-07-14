class Rule(object):
    def match(self, client):
        return False

class TitleRule(object):
    def __init__(self, title):
        self.title = title
    def match(self, client):
        return client.title == self.title 


class Rules(object):
    def __init__(self, screen):
        self.screen = screen 
        screen.push_handlers(self)

        self.rules = [
            TitleRule("firefox", 

    def on_client_add(self, client):
        
