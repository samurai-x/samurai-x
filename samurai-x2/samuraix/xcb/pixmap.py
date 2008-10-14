import _xcb
from .drawable import Drawable
from .util import check_void_cookie

class Pixmap(Drawable):
    def __init__(self, connection, xid):
        super(Pixmap, self).__init__(connection, xid)

    @classmethod
    def create(cls, connection, drawable, width, height, depth=0):
        xid = _xcb.xcb_generate_id(connection._connection)
        check_void_cookie(connection._connection, _xcb.xcb_create_pixmap_checked(connection._connection,
                                        depth,
                                        xid,
                                        drawable._xid,
                                        width,
                                        height))
        connection.flush()
        return cls(connection, xid)
