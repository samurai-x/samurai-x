import ctypes
import _xcb
import util

COORD_MODE_ORIGIN = _xcb.XCB_COORD_MODE_ORIGIN
COORD_MODE_PREVIOUS = _xcb.XCB_COORD_MODE_PREVIOUS

POLY_SHAPE_COMPLEX = _xcb.XCB_POLY_SHAPE_COMPLEX
POLY_SHAPE_CONVEX = _xcb.XCB_POLY_SHAPE_CONVEX
POLY_SHAPE_NONCONVEX = _xcb.XCB_POLY_SHAPE_NONCONVEX

GC_ATTRIBUTES = [('function', _xcb.XCB_GC_FUNCTION),
                 ('plane_mask', _xcb.XCB_GC_PLANE_MASK),
                 ('foreground', _xcb.XCB_GC_FOREGROUND)] # TODO: complete

def convert_point(point):
    c_point = _xcb.xcb_point_t()
    c_point.x = point[0]
    c_point.y = point[1]
    return c_point

def convert_segment(point1, point2):
    c_segment = _xcb.xcb_segment_t()
    c_segment.x1 = point1[0]
    c_segment.y1 = point1[1]
    c_segment.x2 = point2[0]
    c_segment.y2 = point2[1]
    return c_segment

def convert_points(points):
    c_points_list = []
    for point in points:
        c_points_list.append(convert_point(point))
    return (_xcb.xcb_point_t * len(points))(*c_points_list)

def convert_segments(points):
    c_segments_list = []
    for point1, point2 in points:
        c_segments_list.append(convert_segment(point1, point2))
    return (_xcb.xcb_segment_t * len(points))(*c_segments_list)
   
Rectangle = _xcb.xcb_rectangle_t # TODO: really use a xcb internal type? :/
Arc = _xcb.xcb_arc_t

class GraphicsContext(object):
    def __init__(self, connection, xid):
        self.connection = connection
        self._xid = xid

    def poly_point(self, drawable, points, coordinate_mode=COORD_MODE_ORIGIN):
        """
            :Parameters:
                drawable : `drawable.Drawable`

                points : list
                    A list of [(x, y), (x, y), ...]

        """
        c_points = convert_points(points)
        _xcb.xcb_poly_point(self.connection._connection,
                            coordinate_mode,
                            drawable._xid,
                            self._xid,
                            len(c_points),
                            c_points)
        self.connection.flush()

    def poly_line(self, drawable, points, coordinate_mode=COORD_MODE_ORIGIN):
        """
            :Parameters:
                drawable : `drawable.Drawable`

                points : list
                    A list of [(x, y), (x, y), ...]

        """
        c_points = convert_points(points)
        _xcb.xcb_poly_line(self.connection._connection,
                            coordinate_mode,
                            drawable._xid,
                            self._xid,
                            len(c_points),
                            c_points)
        self.connection.flush()

    def poly_segment(self, drawable, segments):
        c_segments = convert_segments(segments)
        _xcb.xcb_poly_segment(self.connection._connection,
                              drawable._xid,
                              self._xid,
                              len(c_segments),
                              c_segments)
        self.connection.flush()

    def poly_rectangle(self, drawable, rectangles, fill=False):
        c_rectangles = (_xcb.xcb_rectangle_t * len(rectangles))(*rectangles)

        func = (_xcb.xcb_poly_fill_rectangle if fill else _xcb.xcb_poly_rectangle)

        func(self.connection._connection,
                              drawable._xid,
                              self._xid,
                              len(rectangles),
                              c_rectangles)
        self.connection.flush()

    def poly_arc(self, drawable, arcs, fill=False):
        c_arcs = (_xcb.xcb_arc_t * len(arcs))(*arcs)

        func = (_xcb.xcb_poly_fill_arc if fill else _xcb.xcb_poly_arc)

        func(self.connection._connection,
                            drawable._xid,
                            self._xid,
                            len(arcs),
                            c_arcs)
        self.connection.flush()

    def fill_poly(self, drawable, points, shape=POLY_SHAPE_COMPLEX, coordinate_mode=COORD_MODE_ORIGIN):
        c_points = convert_points(points)
        _xcb.xcb_fill_poly(self.connection._connection,
                            drawable._xid,
                            self._xid,
                            shape,
                            coordinate_mode,
                            len(c_points),
                            c_points)
        self.connection.flush()


    @classmethod
    def create(cls, connection, drawable, attributes=None):
        if not attributes:
            attributes = {}
        xid = _xcb.xcb_generate_id(connection._connection)
        attr, mask = util.xize_attributes(attributes, GC_ATTRIBUTES)
        _xcb.xcb_create_gc(connection._connection,
                           xid,
                           drawable._xid,
                           mask,
                           attr)
        connection.flush()

        return cls(connection, xid)
