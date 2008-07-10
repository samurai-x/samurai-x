
class Rect(object):
    __slots__ = ['x', 'y', 'width', 'height']
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def copy(self):
        return Rect(self.x, self.y, self.width, self.height)   

    def __str__(self):
        return "<Rect %s %s %s %s>" % (self.x, self.y, self.width, self.height)


