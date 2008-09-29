import _xcb
import ctypes

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
            'window': WindowPropertyDescriptor,
            'atom': AtomPropertyDescriptor,
            'format': FormatPropertyDescriptor,
            }

def event_property(type_, *args, **kwargs):
    return PROPERTIES[type_](*args, **kwargs)

class Event(object):
    event_struct = None

    def __init__(self, connection, _event=None):
        self.connection = connection
        self._event = _event or self.event_struct()

    @property
    def char_p(self):
        return ctypes.cast(ctypes.pointer(self._event), ctypes.c_char_p)

class ClientMessageEvent(Event):
    event_struct = _xcb.xcb_client_message_event_t

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

EVENT_MAP = {
        #
        }

def pythonize_event(connection, _event):
    event_type = _event.response_type & ~0x80
    if event_type == 0:
        return None
    if event_type in EVENT_MAP:
        cls = EVENT_MAP[event_type]
        return cls(connection, ctypes.cast(event, ctypes.POINTER(cls.event_struct)))
    else:
        raise Exception('dunno %d' % event_type)
