import _xcb
import ctypes

from util import reverse_dict
import drawable
import window
import atom

class BaseEventPropertyDescriptor(object):
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
    def x_to_py(self, connection, val):
        return (drawable.Drawable(connection, val) if val else None)

    def py_to_x(self, connection, val):
        return val._xid

class WindowPropertyDescriptor(BaseEventPropertyDescriptor):
    def x_to_py(self, connection, val):
        return (window.Window(connection, val) if val else None)

    def py_to_x(self, connection, val):
        return val._xid

class AtomPropertyDescriptor(BaseEventPropertyDescriptor):
    def x_to_py(self, connection, val):
        return (atom.Atom(connection, val) if val else None)

    def py_to_x(self, connection, val):
        return val._atom

class FormatPropertyDescriptor(BaseEventPropertyDescriptor):
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

class Event(object):
    event_type = 0
    event_struct = None
    event_mask = 0

    def __init__(self, connection, _event=None):
        self.connection = connection
        self._event = _event or self.event_struct()

    @property
    def char_p(self):
        return ctypes.cast(ctypes.pointer(self._event), ctypes.c_char_p)

class ClientMessageEvent(Event):
    event_type = _xcb.XCB_CLIENT_MESSAGE
    event_struct = _xcb.xcb_client_message_event_t
    event_mask = 0

    def __init__(self, connection, _event=None):
        super(ClientMessageEvent, self).__init__(connection, _event)
        self.response_type = _xcb.XCB_CLIENT_MESSAGE
        
    response_type = event_property('unchanged', 'response_type')
    window = event_property('window', 'window')
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
    event = event_property('window', 'event')
    child = event_property('window', 'child')
    root_x = event_property('unchanged', 'root_x')
    root_y = event_property('unchanged', 'root_y')
    event_x = event_property('unchanged', 'event_x')
    event_y = event_property('unchanged', 'event_y')
    state = event_property('unchanged', 'state')
    # TODO: same_screen?

class KeyPressEvent(KeyEvent):
    event_type = _xcb.XCB_KEY_PRESS
    event_struct = _xcb.xcb_key_press_event_t
    event_mask = _xcb.XCB_EVENT_MASK_KEY_PRESS

class KeyReleaseEvent(KeyEvent):
    event_type = _xcb.XCB_KEY_RELEASE
    event_struct = _xcb.xcb_key_release_event_t
    event_mask = _xcb.XCB_EVENT_MASK_KEY_RELEASE

class ExposureEvent(Event):
    event_type = _xcb.XCB_EXPOSE
    event_struct = _xcb.xcb_graphics_exposure_event_t
    event_mask = _xcb.XCB_EVENT_MASK_EXPOSURE

    drawable = event_property('drawable', 'drawable')
    x = event_property('unchanged', 'x')
    y = event_property('unchanged', 'y')
    width = event_property('unchanged', 'width')
    height = event_property('unchanged', 'height')

EVENTS = (KeyPressEvent, KeyReleaseEvent, ExposureEvent,)
X_EVENT_MAP = dict((cls.event_type, cls) for cls in EVENTS)
EVENT_X_MAP = reverse_dict(X_EVENT_MAP)

def pythonize_event(connection, _event):
    event_type = _event.response_type & ~0x80 # strip 'send event' bit
    if event_type == 0:
        return None
    if event_type in X_EVENT_MAP:
        cls = X_EVENT_MAP[event_type]
        return cls(connection, ctypes.cast(ctypes.pointer(_event), ctypes.POINTER(cls.event_struct)).contents)
    else:
        print 'ignoring event %d' % event_type
