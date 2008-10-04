import _xcb
import ctypes

from util import reverse_dict
import drawable
import window
import atom
import connection

class DummyStruct(object):
    pass

class BaseEventPropertyDescriptor(object):
    _class = None

    def __init__(self, property_name):
        self.property_name = property_name

    def x_to_py(self, connection, val):
        return val

    def py_to_x(self, connection, val):
        return val

    def __get__(self, instance, owner):
        return self.x_to_py(instance.connection, getattr(instance._event, self.property_name))

    def __set__(self, instance, value):
        return setattr(instance._event, self.property_name, self.py_to_x(instance.connection, value))

# TODO: should property descriptors cache objects and return the identical objects which were passed to them?

class DrawablePropertyDescriptor(BaseEventPropertyDescriptor):
    _class = drawable.Drawable

    def x_to_py(self, connection, val):
        return (drawable.Drawable(connection, val) if val else None)

    def py_to_x(self, connection, val):
        return val._xid

class WindowPropertyDescriptor(BaseEventPropertyDescriptor):
    _class = window.Window

    def x_to_py(self, connection, val):
        return (window.Window(connection, val) if val else None)

    def py_to_x(self, connection, val):
        return val._xid

class AtomPropertyDescriptor(BaseEventPropertyDescriptor):
    _class = atom.Atom

    def x_to_py(self, connection, val):
        return (atom.Atom(connection, val) if val else None)

    def py_to_x(self, connection, val):
        return val._atom

class FormatPropertyDescriptor(BaseEventPropertyDescriptor):
    _class = None

    def x_to_py(self, connection, val):
        return val

    def py_to_x(self, connection, val):
        assert val in (8, 16, 32)
        return val

PROPERTIES = {
            'unchanged': BaseEventPropertyDescriptor,
            'drawable': DrawablePropertyDescriptor,
            'window': WindowPropertyDescriptor,
            'atom': AtomPropertyDescriptor,
            'format': FormatPropertyDescriptor,
            }

def event_property(type_, *args, **kwargs):
    return PROPERTIES[type_](*args, **kwargs)

class EventMeta(type):
    def __new__(mcs, name, bases, dct):
        obj = type.__new__(mcs, name, bases, dct)
        obj.register_event_type()
        return obj

class Event(object):
    __metaclass__ = EventMeta

    event_type = 0
    event_struct = None
    event_mask = 0
    event_name = 'on_event'
    _dispatch_target = None
    _dispatch_class = connection.Connection

    def __init__(self, connection, _event=None):
        self.connection = connection
        self._event = _event or self.event_struct()
        self._dispatch_target = self._dispatch_target or self.connection

    @classmethod
    def cast_to(cls, voidp):
        return ctypes.cast(voidp, ctypes.POINTER(cls.event_struct)).contents

    @property
    def char_p(self):
        return ctypes.cast(ctypes.pointer(self._event), ctypes.c_char_p)

    def dispatch(self):
        print 'dispatching', self, self._dispatch_target
        self._dispatch_target.dispatch_event(self.event_name, self)

    @classmethod
    def register_event_type(cls):
        cls._dispatch_class.register_event_type(cls.event_name)

class DummyEvent(Event):
    """
         an event class containing a dummy struct which just stores values.
    """
    event_struct = DummyStruct

    @classmethod
    def cast_to(cls, voidp):
        return None

class ClientMessageEvent(Event):
    event_type = _xcb.XCB_CLIENT_MESSAGE
    event_struct = _xcb.xcb_client_message_event_t
    event_mask = 0
    event_name = 'on_client_message'
    _dispatch_class = window.Window

    def __init__(self, connection, _event=None):
        super(ClientMessageEvent, self).__init__(connection, _event)
        self.response_type = _xcb.XCB_CLIENT_MESSAGE
        
    response_type = event_property('unchanged', 'response_type')
    _dispatch_target = window = event_property('window', 'window')
    type = event_property('atom', 'type')
    format = event_property('format', 'format')
    
    def _get_data_field(self):
        return {8: 'data8',
                16: 'data16',
                32: 'data32'}[self.format]

    def _get_data(self):
        assert self.format in (8, 16, 32) # TODO: friendlier
        return list(getattr(self._event.data, self._get_data_field()))

    def _set_data(self, val): # TODO: support slicing/attributes
        assert self.format in (8, 16, 32) # TODO: friendlier
        f = self._get_data_field()
        arr = getattr(self._event.data, f)
        for idx, v in enumerate(val):
            arr[idx] = v

    data = property(_get_data, _set_data)

class KeyEvent(Event):
    """
        Base class for key events because
        KeyPress and KeyRelease events are very similar.
    """
    keycode = detail = event_property('unchanged', 'detail') # TODO - only `detail`?
    time = event_property('unchanged', 'time')
    root = event_property('window', 'root')
    _dispatch_target = event = event_property('window', 'event')
    _dispatch_class = window.Window
    child = event_property('window', 'child')
    root_x = event_property('unchanged', 'root_x')
    root_y = event_property('unchanged', 'root_y')
    event_x = event_property('unchanged', 'event_x')
    event_y = event_property('unchanged', 'event_y')
    state = event_property('unchanged', 'state')
    # TODO: same_screen?

class KeyPressEvent(KeyEvent):
    event_name = 'on_key_press'

    event_type = _xcb.XCB_KEY_PRESS
    event_struct = _xcb.xcb_key_press_event_t
    event_mask = _xcb.XCB_EVENT_MASK_KEY_PRESS

class KeyReleaseEvent(KeyEvent):
    event_name = 'on_key_release'

    event_type = _xcb.XCB_KEY_RELEASE
    event_struct = _xcb.xcb_key_release_event_t
    event_mask = _xcb.XCB_EVENT_MASK_KEY_RELEASE

class ButtonEvent(Event):
    button = detail = event_property('unchanged', 'detail') # TODO - only `detail`?
    time = event_property('unchanged', 'time')
    root = event_property('window', 'root')
    _dispatch_target = event = event_property('window', 'event')
    _dispatch_class = window.Window
    child = event_property('window', 'child')
    root_x = event_property('unchanged', 'root_x')
    root_y = event_property('unchanged', 'root_y')
    event_x = event_property('unchanged', 'event_x')
    event_y = event_property('unchanged', 'event_y')
    state = event_property('unchanged', 'state')
    # TODO: same_screen?

class ButtonPressEvent(ButtonEvent):
    event_name = 'on_button_press'

    event_type = _xcb.XCB_BUTTON_PRESS
    event_struct = _xcb.xcb_button_press_event_t
    event_mask = _xcb.XCB_EVENT_MASK_BUTTON_PRESS

class ButtonReleaseEvent(ButtonEvent):
    event_name = 'on_button_release'

    event_type = _xcb.XCB_BUTTON_RELEASE
    event_struct = _xcb.xcb_button_release_event_t
    event_mask = _xcb.XCB_EVENT_MASK_BUTTON_RELEASE

class EnterLeaveNotifyEvent(Event):
    _dispatch_class = window.Window
    
    detail = event_property('unchanged', 'detail')
    time = event_property('unchanged', 'time')
    root = event_property('window', 'root')
    _dispatch_target = event = event_property('window', 'event')
    child = event_property('window', 'child')
    root_x = event_property('unchanged', 'root_x')
    root_y = event_property('unchanged', 'root_y')
    event_x = event_property('unchanged', 'event_x')
    event_y = event_property('unchanged', 'event_y')
    state = event_property('unchanged', 'state')
    mode = event_property('unchanged', 'mode')
    # TODO: same_screen_focus?

class EnterNotifyEvent(EnterLeaveNotifyEvent):
    event_type = _xcb.XCB_ENTER_NOTIFY
    event_struct = _xcb.xcb_enter_notify_event_t
    event_mask = _xcb.XCB_EVENT_MASK_ENTER_WINDOW

class LeaveNotifyEvent(EnterLeaveNotifyEvent):
    event_type = _xcb.XCB_LEAVE_NOTIFY
    event_struct = _xcb.xcb_leave_notify_event_t
    event_mask = _xcb.XCB_EVENT_MASK_LEAVE_WINDOW

class ExposeEvent(Event):
    event_name = 'on_expose'
    event_type = _xcb.XCB_EXPOSE
    event_struct = _xcb.xcb_graphics_exposure_event_t
    event_mask = _xcb.XCB_EVENT_MASK_EXPOSURE
    _dispatch_class = window.Window # TODO: it should be `drawable.Drawable`, but the pyglet event dispatcher does not want that.

    _dispatch_target = drawable = event_property('drawable', 'drawable')
    x = event_property('unchanged', 'x')
    y = event_property('unchanged', 'y')
    width = event_property('unchanged', 'width')
    height = event_property('unchanged', 'height')

class BaseMotionNotifyEvent(Event):
    event_type = _xcb.XCB_MOTION_NOTIFY
    event_struct = _xcb.xcb_motion_notify_event_t
    _dispatch_class = window.Window

    detail = event_property('unchanged', 'detail')
    time = event_property('unchanged', 'time')
    root = event_property('window', 'root')
    _dispatch_target = event = event_property('window', 'event')
    child = event_property('window', 'child')
    root_x = event_property('unchanged', 'root_x')
    root_y = event_property('unchanged', 'root_y')
    event_x = event_property('unchanged', 'event_x')
    event_y = event_property('unchanged', 'event_y')
    state = event_property('unchanged', 'state')
    # TODO: same_screen?

class MotionNotifyEvent(BaseMotionNotifyEvent): # TODO: what about XCB_EVENT_MASK_BUTTON_?_MOTION
    event_mask = _xcb.XCB_EVENT_MASK_POINTER_MOTION
    event_name = 'on_motion_notify'

class KeymapNotifyEvent(Event):
    event_type = _xcb.XCB_KEYMAP_NOTIFY
    event_struct = _xcb.xcb_keymap_notify_event_t
    event_mask = _xcb.XCB_EVENT_MASK_KEYMAP_STATE
    event_name = 'on_keymap_notify'

    keys = event_property('unchanged', 'keys') # TODO!: make Keymap objects!

class VisibilityNotifyEvent(Event):
    event_type = _xcb.XCB_VISIBILITY_NOTIFY
    event_struct = _xcb.xcb_visibility_notify_event_t
    event_mask = _xcb.XCB_EVENT_MASK_VISIBILITY_CHANGE
    event_name = 'on_visibility_notify'
    _dispatch_class = window.Window
    _dispatch_target = window = event_property('window', 'window')
    state = event_property('unchanged', 'state')

class StructureNotifyEvent(DummyEvent):
    event_mask = _xcb.XCB_EVENT_MASK_STRUCTURE_NOTIFY
    event_name = 'on_structure_notify'

class ResizeRedirectEvent(DummyEvent):
    event_mask = _xcb.XCB_EVENT_MASK_RESIZE_REDIRECT
    event_name = 'on_resize_redirect'

class SubstructureNotifyEvent(DummyEvent):
    event_mask = _xcb.XCB_EVENT_MASK_SUBSTRUCTURE_NOTIFY
    event_name = 'on_substructure_notify'

class SubstructureRedirectEvent(DummyEvent):
    event_mask = _xcb.XCB_EVENT_MASK_SUBSTRUCTURE_REDIRECT
    event_name = 'on_substructure_redirect'

class MapRequestEvent(Event):
    event_type = _xcb.XCB_MAP_REQUEST
    event_struct = _xcb.xcb_map_notify_event_t
    event_name = 'on_map_request'
    _dispatch_target = event = parent = event_property('window', 'event')
    _dispatch_class = window.Window
    window = event_property('window', 'window')
    override_redirect = event_property('unchanged', 'override_redirect')

class CreateNotifyEvent(Event):
    event_type = _xcb.XCB_CREATE_NOTIFY
    event_name = 'on_create_notify'
    event_struct = _xcb.xcb_create_notify_event_t

    window = event_property('window', 'window')
    parent = event_property('window', 'parent')
    x = event_property('unchanged', 'x')
    y = event_property('unchanged', 'y')
    width = event_property('unchanged', 'width')
    height = event_property('unchanged', 'height')
    border_width = event_property('unchanged', 'border_width')
    override_redirect = event_property('unchanged', 'override_redirect')

class DestroyNotifyEvent(Event):
    event_type = _xcb.XCB_DESTROY_NOTIFY
    event_name = 'on_destroy_notify'
    event_struct = _xcb.xcb_destroy_notify_event_t

    window = event_property('window', 'window')
    event = event_property('window', 'event')

class MapNotifyEvent(Event):
    event_type = _xcb.XCB_MAP_NOTIFY
    event_name = 'on_map_notify'
    event_struct = _xcb.xcb_map_notify_event_t
    
    window = event_property('window', 'window')
    event = event_property('window', 'event')
    override_redirect = event_property('unchanged', 'override_redirect')

class ConfigureRequestEvent(Event):
    event_type = _xcb.XCB_CONFIGURE_REQUEST
    event_name = 'on_configure_request'
    event_struct = _xcb.xcb_configure_request_event_t

    stack_mode = event_property('unchanged', 'stack_mode')
    _dispatch_class = window.Window
    _dispatch_target = window = event_property('window', 'window')
    parent = event_property('window', 'parent')
    sibling = event_property('window', 'sibling')

    x = event_property('unchanged', 'x')
    y = event_property('unchanged', 'y')
    width = event_property('unchanged', 'width')
    height = event_property('unchanged', 'height')
    border_width = event_property('unchanged', 'border_width')
    value_mask = event_property('unchanged', 'value_mask')

class ConfigureNotifyEvent(Event):
    event_type = _xcb.XCB_CONFIGURE_NOTIFY
    event_name = 'on_configure_notify'
    event_struct = _xcb.xcb_configure_notify_event_t

    _dispatch_class = window.Window
    window = event_property('window', 'window')
    _dispatch_target = event = event_property('window', 'event')
    above_sibling = event_property('window', 'above_sibling')
    x = event_property('unchanged', 'x')
    y = event_property('unchanged', 'y')
    width = event_property('unchanged', 'width')
    height = event_property('unchanged', 'height')
    border_width = event_property('unchanged', 'border_width')
    override_redirect = event_property('unchanged', 'override_redirect')

EVENTS = (KeyPressEvent, KeyReleaseEvent, ButtonPressEvent, ButtonReleaseEvent,
          EnterNotifyEvent, LeaveNotifyEvent, ExposeEvent,
          MotionNotifyEvent, KeymapNotifyEvent, VisibilityNotifyEvent,
          StructureNotifyEvent, ResizeRedirectEvent, SubstructureNotifyEvent,
          SubstructureRedirectEvent, MapRequestEvent,
          CreateNotifyEvent, ConfigureRequestEvent, MapNotifyEvent,
          DestroyNotifyEvent, ConfigureNotifyEvent,
          )

X_EVENT_MAP = dict((cls.event_type, cls) for cls in EVENTS)
EVENT_X_MAP = reverse_dict(X_EVENT_MAP)

def pythonize_event(connection, _event):
    event_type = _event.response_type & ~0x80 # strip 'send event' bit
    if event_type == 0:
        return None
    if event_type in X_EVENT_MAP:
        cls = X_EVENT_MAP[event_type]
        return cls(connection, cls.cast_to(ctypes.pointer(_event)))
    else:
        print 'ignoring event %d' % event_type
