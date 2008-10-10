import warnings

import samuraix.event

import cookie
import _xcb
import ctypes
import util
from .drawable import Drawable
from .pixmap import Pixmap

import logging 
log = logging.getLogger(__name__)

def _xize_event_mask(events):
    """
        convert an iterable containing `event.Event` subclasses
        to an xcb event mask and return it.

        :note: A warning will be displayed if you do not add the
        exposure mask.
    """
    mask = 0
    for cls in events:
        mask |= cls.event_mask
    if not _xcb.XCB_EVENT_MASK_EXPOSURE & mask:
        warnings.warn('You did not add the exposure event to your event mask.\n'
                      'Do you really want that?')
    return mask

def _xize_resource(res):
    """
        return a `resource.Resource`'s internal representation: 
        its xid.
    """
    return res._xid

def _xize_pixmap(pixmap):
    """
        return the internal representation of a pixmap: its xid.
        This function does call `_xize_resource`, but additionally
        asserts that `pixmap` is really a `pixmap.Pixmap` instance.
    """
    assert isinstance(pixmap, Pixmap)
    return _xize_resource(pixmap)

CLASS_INPUT_OUTPUT = _xcb.XCB_WINDOW_CLASS_INPUT_OUTPUT

STACK_MODE_ABOVE = _xcb.XCB_STACK_MODE_ABOVE
STACK_MODE_BELOW = _xcb.XCB_STACK_MODE_BELOW

GRAB_MODE_ASYNC = _xcb.XCB_GRAB_MODE_ASYNC
GRAB_MODE_SYNC = _xcb.XCB_GRAB_MODE_SYNC

ATTRIBUTE_ORDER = [
            ('back_pixmap', _xcb.XCB_CW_BACK_PIXMAP, _xize_pixmap),
            ('back_pixel', _xcb.XCB_CW_BACK_PIXEL),# TODO: xizer
            ('border_pixmap', _xcb.XCB_CW_BORDER_PIXMAP, _xize_pixmap),
            ('border_pixel', _xcb.XCB_CW_BORDER_PIXEL),# TODO: xizer
            ('bit_gravity', _xcb.XCB_CW_BIT_GRAVITY),
            ('win_gravity', _xcb.XCB_CW_WIN_GRAVITY),
            ('backing_store', _xcb.XCB_CW_BACKING_STORE),
            ('backing_planes', _xcb.XCB_CW_BACKING_PLANES),
            ('backing_pixel', _xcb.XCB_CW_BACKING_PIXEL),
            ('override_redirect', _xcb.XCB_CW_OVERRIDE_REDIRECT),
            ('save_under', _xcb.XCB_CW_SAVE_UNDER),
            ('event_mask', _xcb.XCB_CW_EVENT_MASK, _xize_event_mask),
            ('dont_propagate', _xcb.XCB_CW_DONT_PROPAGATE),
            ('colormap', _xcb.XCB_CW_COLORMAP), # TODO: xizer
            ('cursor', _xcb.XCB_CW_CURSOR) # TODO: xizer
           ]

WINDOW_CONFIG= [
            ('x', _xcb.XCB_CONFIG_WINDOW_X),
            ('y', _xcb.XCB_CONFIG_WINDOW_Y),
            ('width', _xcb.XCB_CONFIG_WINDOW_WIDTH),
            ('height', _xcb.XCB_CONFIG_WINDOW_HEIGHT),
            ('border_width', _xcb.XCB_CONFIG_WINDOW_BORDER_WIDTH),
            ('sibling', _xcb.XCB_CONFIG_WINDOW_SIBLING),
            ('stack_mode', _xcb.XCB_CONFIG_WINDOW_STACK_MODE)
        ]

class Window(Drawable):
    """
        a window.
    """
    def __init__(self, connection, xid):
        """
            instantiate a window from a known X id.
            
            :Parameters:
                `connection` : connection.Connection
                    The corresponding connection
                `xid` : int
                    The X id which has to exist.
        """
        super(Window, self).__init__(connection, xid)

    def __repr__(self):
        return '<Window object XID: %d>' % self._xid

    def request_get_property(self, prop):
        """
            request the property `name`

            :Parameters:
                `name` : str or `atom.Atom`
                    The property's name *or* the corresponding
                    `atom.Atom` object
            :rtype: `cookie.PropertyRequest`
        """
        return cookie.PropertyRequest(self.connection, self, \
                                      (self.connection.get_atom_by_name(prop) if isinstance(prop, basestring) \
                                          else prop),
                                      )

    def get_property(self, name):
        """
            request a property and return its value.
            :see: `Window.request_get_property`
        """
        return self.request_get_property(name).value

    def request_set_property(self, prop, content, format):
        """
            request the setting of the property `prop` to `content`
            using the format `format`.

            :Parameters:
                `prop` : str or `atom.Atom`
                    The property's name *or* the corresponding
                    `atom.Atom` object
                `content` : list
                    The object list the property should be set to.
                    (can be very much, e.g. a Window list, an Atom list, ...)
                `format` : int
                    The format to use. Has to be one of 8, 16, 32
            :rtype: `cookie.ChangePropertyRequest`
        """
        return cookie.ChangePropertyRequest(self.connection, self, \
                                            (self.connection.get_atom_by_name(prop) if isinstance(prop, basestring) \
                                          else prop),
                                      content, format)

    def set_property(self, name, content, format):
        """
            request a property change and execute it immediately.
            :see: `Window.request_set_property`
        """
        return self.request_set_property(name, content, format).execute()

    def request_send_event(self, event):
        """
            request the sending of the event `event`.
            
            :Parameters:
                `event` : event.Event subclass instance
                    The event to send.
            :rtype: `cookie.SendEventRequest`
        """
        return cookie.SendEventRequest(self.connection, self, event)

    def send_event(self, event):
        """
            request an event sending and execute.
        """
        self.request_send_event(event).execute()

    def delete(self):
        """
            delete me. TODO.
        """
        # delete myself!
        super(Window, self).delete()

    @classmethod
    def create(cls, connection, screen, x, y, width, height, border_width=0, parent=None, class_=None, visual=None, attributes=None):
        """
            create a new window and return an instance.

            :Parameters:
                `connection` : connection.Connection
                    The corresponding connection.
                `screen` : screen.Screen
                    The corresponding screen instance.
                    If you specify `parent` *and* `visual`, you can
                    set `screen` to None.
                `x` : int
                    The initial x coordinate.
                `y` : int
                    The initial y coordinate.
                `width` : int
                    The inital width (in pixels).
                `height` : int
                    The initial height (in pixels).
                `border_width` : int
                    The border size (in pixels).
                `parent` : window.Window
                    The parent window instance. If this is None,
                    use `screen`'s root window
                `class_` : int
                    One of CLASS_INPUT_OUTPUT (TODO: complete)
                    defaults to CLASS_INPUT_OUTPUT
                `visual` : int
                    The visual ID to use. If this is None,
                    use `screen`'s root visual.
                `attributes` : dict
                    a dictionary {key: attribute} containing
                    attributes which should be set. see `Window.attributes`.
            :rtype: `window.Window`
        """
        if not class_:
            class_ = CLASS_INPUT_OUTPUT
        if not visual:
            visual = screen.root_visual
        if not attributes:
            attributes = {}
        if not parent:
            parent = screen.root

        parent = parent._xid

        xid = _xcb.xcb_generate_id(connection._connection) # TODO
        attr, mask = util.xize_attributes(attributes, ATTRIBUTE_ORDER)

        _xcb.xcb_create_window(connection._connection, # connection
                               _xcb.XCB_COPY_FROM_PARENT, # depth
                               xid, # xid
                               parent, # parent xid
                               x, y,
                               width, height,
                               border_width,
                               class_,
                               visual,
                               mask,
                               attr)

        if not 'event_mask' in attributes:
            warnings.warn('You did not an event mask to your window.\n'
                          'Do you really want that?')
        connection.flush()

        return cls(connection, xid)

    def request_get_attributes(self):
        return cookie.GetWindowAttributesRequest(self.connection, self)

    def get_attributes(self):
        return self.request_get_attributes().value

    def set_attributes(self, attributes):
        attr, mask = util.xize_attributes(attributes, ATTRIBUTE_ORDER)
        _xcb.xcb_change_window_attributes_checked(self.connection._connection,
                                                  self._xid,
                                                  mask,
                                                  attr)
        self.connection.flush()

    attributes = property(get_attributes, set_attributes, doc="""
    Change attributes. Item assignment is currently not supported.
    TODO: check whether already set events survive.
    
    Valid attributes are:
        back_pixmap : pixmap.Pixmap
            The background pixmap.
        back_pixel
        border_pixmap : pixmap.Pixmap
            The pixmap used for the borders
        bit_gravity
        win_gravity
        backing_store
        backing_planes
        backing_pixel
        override_redirect : bool
            Should be window be visible to the window manager?
        save_under
        event_mask : iterable of `event.Event` subclasses
            The event classes which should be propagated to the window.
        dont_propagate
        colormap
        cursor

    TODO:
    Not all attributes are 'pythonized' yet.
    Only attribute changing is supported for now, not retrieving.
    """)

    def map(self):
        """
            show the window.
        """
        _xcb.xcb_map_window(self.connection._connection, self._xid)
        self.connection.flush()

    def configure(self, **config):
        attr, mask = util.xize_attributes(config, WINDOW_CONFIG)
        cookie = _xcb.xcb_configure_window(self.connection._connection,
                                  self._xid,
                                  mask,
                                  attr)
        self.connection.flush()
        util.check_void_cookie(cookie)

    def request_query_pointer(self):
        return cookie.QueryPointerRequest(self.connection, self)

    def query_pointer(self):
        return self.request_query_pointer().value

    def reparent(self, parent, x, y):
        _xcb.xcb_reparent_window(self.connection._connection,
                                 self._xid,
                                 parent._xid,
                                 x,
                                 y)
        self.connection.flush()

    def request_get_geometry(self):
        return cookie.GetGeometryRequest(self.connection, self)

    def get_geometry(self):
        return self.request_get_geometry().value

    def circulate(self, direction):
        cookie = _xcb.xcb_circulate_window(self.connection._connection,
                                self._xid,
                                direction)
        self.connection.flush()
        util.check_void_cookie(cookie)

    @property #should cache? i dont think it should change...
    def _tree_cookie(self):
        return _xcb.xcb_query_tree_unchecked(self.connection._connection, self._xid)

    @property
    def children(self):
        """ return a generator for all direct children of the window """
        tree_r = _xcb.xcb_query_tree_reply(self.connection._connection, self._tree_cookie, None)
        if not tree_r:
            return False

        wins = _xcb.xcb_query_tree_children(tree_r)
        if not wins:
            raise Exception('cant get tree children')
        
        tree_len = _xcb.xcb_query_tree_children_length(tree_r)

        return (Window(self.connection, wins[i]) for i in range(tree_len))
            
    def grab_key(self, keycode, modifiers=0, owner_events=True, pointer_mode=GRAB_MODE_ASYNC, keyboard_mode=GRAB_MODE_ASYNC):
        cookie = _xcb.xcb_grab_key(self.connection._connection,
                                   owner_events,
                                   self._xid,
                                   modifiers,
                                   keycode,
                                   pointer_mode,
                                   keyboard_mode)
        self.connection.flush()
        util.check_void_cookie(cookie)
