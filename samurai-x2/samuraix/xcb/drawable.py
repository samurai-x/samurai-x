from .resource import Resource

class Drawable(Resource):
    def __init__(self, connection, xid):
        super(Drawable, self).__init__(connection, xid)
