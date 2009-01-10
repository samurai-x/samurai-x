import xcb.xproto
from oobase import Wrapper

class Pixmap(Wrapper):
    pass

class GraphicsExposureEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.drawable = Drawable(self.conn, _internal.drawable)
        self.x = _internal.x
        self.y = _internal.y
        self.width = _internal.width
        self.height = _internal.height
        self.minor_opcode = _internal.minor_opcode
        self.count = _internal.count
        self.major_opcode = _internal.major_opcode

class GetAtomNameReply(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.length = _internal.length
        self.name_len = _internal.name_len
        self.name = _internal.name
        self.name = ''.join(map(chr, self.name))

class GravityNotifyEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.event = Window(self.conn, _internal.event)
        self.window = Window(self.conn, _internal.window)
        self.x = _internal.x
        self.y = _internal.y

class Fontprop(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.name = Atom(self.conn, _internal.name)
        self.value = _internal.value

class ClientMessageEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.format = _internal.format
        self.window = Window(self.conn, _internal.window)
        self.type = Atom(self.conn, _internal.type)
        self.data = _internal.data

class ListPropertiesReply(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.length = _internal.length
        self.atoms_len = _internal.atoms_len
        self.atoms = _internal.atoms
        self.atoms = [Atom(conn, xid) for xid in self.atoms]

class EnterNotifyEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.detail = _internal.detail
        self.time = Timestamp(self.conn, _internal.time)
        self.root = Window(self.conn, _internal.root)
        self.event = Window(self.conn, _internal.event)
        self.child = Window(self.conn, _internal.child)
        self.root_x = _internal.root_x
        self.root_y = _internal.root_y
        self.event_x = _internal.event_x
        self.event_y = _internal.event_y
        self.state = _internal.state
        self.mode = _internal.mode
        self.same_screen_focus = _internal.same_screen_focus

class MapRequestEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.parent = Window(self.conn, _internal.parent)
        self.window = Window(self.conn, _internal.window)

class UnmapNotifyEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.event = Window(self.conn, _internal.event)
        self.window = Window(self.conn, _internal.window)
        self.from_configure = _internal.from_configure

class GetGeometryCookie(Wrapper):
    def reply(self):
        return GetGeometryReply(self.conn, self._internal.reply())

    def check(self):
        return self._internal.check()

class GrabPointerCookie(Wrapper):
    def reply(self):
        return GrabPointerReply(self.conn, self._internal.reply())

    def check(self):
        return self._internal.check()

class SetupRequest(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.byte_order = _internal.byte_order
        self.protocol_major_version = _internal.protocol_major_version
        self.protocol_minor_version = _internal.protocol_minor_version
        self.authorization_protocol_name_len = _internal.authorization_protocol_name_len
        self.authorization_protocol_data_len = _internal.authorization_protocol_data_len
        self.authorization_protocol_name = _internal.authorization_protocol_name
        self.authorization_protocol_data = _internal.authorization_protocol_data

class QueryTreeCookie(Wrapper):
    def reply(self):
        return QueryTreeReply(self.conn, self._internal.reply())

    def check(self):
        return self._internal.check()

class ConfigureRequestEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.stack_mode = _internal.stack_mode
        self.parent = Window(self.conn, _internal.parent)
        self.window = Window(self.conn, _internal.window)
        self.sibling = Window(self.conn, _internal.sibling)
        self.x = _internal.x
        self.y = _internal.y
        self.width = _internal.width
        self.height = _internal.height
        self.border_width = _internal.border_width
        self.value_mask = _internal.value_mask

class KeyReleaseEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.detail = Keycode(self.conn, _internal.detail)
        self.time = Timestamp(self.conn, _internal.time)
        self.root = Window(self.conn, _internal.root)
        self.event = Window(self.conn, _internal.event)
        self.child = Window(self.conn, _internal.child)
        self.root_x = _internal.root_x
        self.root_y = _internal.root_y
        self.event_x = _internal.event_x
        self.event_y = _internal.event_y
        self.state = _internal.state
        self.same_screen = _internal.same_screen

class GetSelectionOwnerCookie(Wrapper):
    def reply(self):
        return GetSelectionOwnerReply(self.conn, self._internal.reply())

    def check(self):
        return self._internal.check()

class Rectangle(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.x = _internal.x
        self.y = _internal.y
        self.width = _internal.width
        self.height = _internal.height

class MapNotifyEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.event = Window(self.conn, _internal.event)
        self.window = Window(self.conn, _internal.window)
        self.override_redirect = _internal.override_redirect

class VisibilityNotifyEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.window = Window(self.conn, _internal.window)
        self.state = _internal.state

class FocusOutEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.detail = _internal.detail
        self.event = Window(self.conn, _internal.event)
        self.mode = _internal.mode

class CirculateNotifyEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.event = Window(self.conn, _internal.event)
        self.window = Window(self.conn, _internal.window)
        self.place = _internal.place

class Colormap(Wrapper):
    pass

class GetAtomNameCookie(Wrapper):
    def reply(self):
        return GetAtomNameReply(self.conn, self._internal.reply())

    def check(self):
        return self._internal.check()

class Format(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.depth = _internal.depth
        self.bits_per_pixel = _internal.bits_per_pixel
        self.scanline_pad = _internal.scanline_pad

class Timestamp(Wrapper):
    pass

class Screen(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.root = Window(self.conn, _internal.root)
        self.default_colormap = Colormap(self.conn, _internal.default_colormap)
        self.white_pixel = _internal.white_pixel
        self.black_pixel = _internal.black_pixel
        self.current_input_masks = _internal.current_input_masks
        self.width_in_pixels = _internal.width_in_pixels
        self.height_in_pixels = _internal.height_in_pixels
        self.width_in_millimeters = _internal.width_in_millimeters
        self.height_in_millimeters = _internal.height_in_millimeters
        self.min_installed_maps = _internal.min_installed_maps
        self.max_installed_maps = _internal.max_installed_maps
        self.root_visual = VisualID(self.conn, _internal.root_visual)
        self.backing_stores = _internal.backing_stores
        self.save_unders = _internal.save_unders
        self.root_depth = _internal.root_depth
        self.allowed_depths_len = _internal.allowed_depths_len
        self.allowed_depths = [Depth(conn, d) for d in allowed_depths]

class ReparentNotifyEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.event = Window(self.conn, _internal.event)
        self.window = Window(self.conn, _internal.window)
        self.parent = Window(self.conn, _internal.parent)
        self.x = _internal.x
        self.y = _internal.y
        self.override_redirect = _internal.override_redirect

class CreateNotifyEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.parent = Window(self.conn, _internal.parent)
        self.window = Window(self.conn, _internal.window)
        self.x = _internal.x
        self.y = _internal.y
        self.width = _internal.width
        self.height = _internal.height
        self.border_width = _internal.border_width
        self.override_redirect = _internal.override_redirect

class Char2b(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.byte1 = _internal.byte1
        self.byte2 = _internal.byte2

class SetupFailed(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.status = _internal.status
        self.reason_len = _internal.reason_len
        self.protocol_major_version = _internal.protocol_major_version
        self.protocol_minor_version = _internal.protocol_minor_version
        self.length = _internal.length
        self.reason = _internal.reason

class Host(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.family = _internal.family
        self.address_len = _internal.address_len
        self.address = _internal.address

class VisualID(Wrapper):
    pass

class MotionNotifyEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.detail = _internal.detail
        self.time = Timestamp(self.conn, _internal.time)
        self.root = Window(self.conn, _internal.root)
        self.event = Window(self.conn, _internal.event)
        self.child = Window(self.conn, _internal.child)
        self.root_x = _internal.root_x
        self.root_y = _internal.root_y
        self.event_x = _internal.event_x
        self.event_y = _internal.event_y
        self.state = _internal.state
        self.same_screen = _internal.same_screen

class Atom(Wrapper):
    def get_name_request(self):
        return GetAtomNameCookie(self.conn, self.conn.xproto.GetAtomName(self._internal))

    def get_selection_owner_request(self, selection):
        return GetSelectionOwnerCookie(self.conn, self.conn.xproto.GetSelectionOwner(selection._internal))

    def convert_selection(self, *args, **kwargs):
        return self.convert_selection_request(*args, **kwargs).check()

    def convert_selection_request(self, requestor, selection, target, property, time=0):
        return self.conn.xproto.ConvertSelectionChecked(requestor._internal, selection._internal, target._internal, property._internal, time._internal)

    def get_name(self, *args, **kwargs):
        return self.get_name_request(*args, **kwargs).reply()

    def set_selection_owner(self, *args, **kwargs):
        return self.set_selection_owner_request(*args, **kwargs).check()

    def get_selection_owner(self, *args, **kwargs):
        return self.get_selection_owner_request(*args, **kwargs).reply()

    def set_selection_owner_request(self, owner, selection, time=0):
        return self.conn.xproto.SetSelectionOwnerChecked(owner._internal, selection._internal, time._internal)

class Charinfo(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.left_side_bearing = _internal.left_side_bearing
        self.right_side_bearing = _internal.right_side_bearing
        self.character_width = _internal.character_width
        self.ascent = _internal.ascent
        self.descent = _internal.descent
        self.attributes = _internal.attributes

class ButtonReleaseEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.detail = _internal.detail
        self.time = Timestamp(self.conn, _internal.time)
        self.root = Window(self.conn, _internal.root)
        self.event = Window(self.conn, _internal.event)
        self.child = Window(self.conn, _internal.child)
        self.root_x = _internal.root_x
        self.root_y = _internal.root_y
        self.event_x = _internal.event_x
        self.event_y = _internal.event_y
        self.state = _internal.state
        self.same_screen = _internal.same_screen

class Segment(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.x1 = _internal.x1
        self.y1 = _internal.y1
        self.x2 = _internal.x2
        self.y2 = _internal.y2

class Keycode(Wrapper):
    pass

class InternAtomCookie(Wrapper):
    def reply(self):
        return InternAtomReply(self.conn, self._internal.reply())

    def check(self):
        return self._internal.check()

class MappingNotifyEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.request = _internal.request
        self.first_keycode = Keycode(self.conn, _internal.first_keycode)
        self.count = _internal.count

class Rgb(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.red = _internal.red
        self.green = _internal.green
        self.blue = _internal.blue

class ButtonPressEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.detail = _internal.detail
        self.time = Timestamp(self.conn, _internal.time)
        self.root = Window(self.conn, _internal.root)
        self.event = Window(self.conn, _internal.event)
        self.child = Window(self.conn, _internal.child)
        self.root_x = _internal.root_x
        self.root_y = _internal.root_y
        self.event_x = _internal.event_x
        self.event_y = _internal.event_y
        self.state = _internal.state
        self.same_screen = _internal.same_screen

class Fontable(Wrapper):
    pass

class GetGeometryReply(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.depth = _internal.depth
        self.length = _internal.length
        self.root = Window(self.conn, _internal.root)
        self.x = _internal.x
        self.y = _internal.y
        self.width = _internal.width
        self.height = _internal.height
        self.border_width = _internal.border_width

class ConfigureNotifyEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.event = Window(self.conn, _internal.event)
        self.window = Window(self.conn, _internal.window)
        self.above_sibling = Window(self.conn, _internal.above_sibling)
        self.x = _internal.x
        self.y = _internal.y
        self.width = _internal.width
        self.height = _internal.height
        self.border_width = _internal.border_width
        self.override_redirect = _internal.override_redirect

class Setup(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.status = _internal.status
        self.protocol_major_version = _internal.protocol_major_version
        self.protocol_minor_version = _internal.protocol_minor_version
        self.length = _internal.length
        self.release_number = _internal.release_number
        self.resource_id_base = _internal.resource_id_base
        self.resource_id_mask = _internal.resource_id_mask
        self.motion_buffer_size = _internal.motion_buffer_size
        self.vendor_len = _internal.vendor_len
        self.maximum_request_length = _internal.maximum_request_length
        self.roots_len = _internal.roots_len
        self.pixmap_formats_len = _internal.pixmap_formats_len
        self.image_byte_order = _internal.image_byte_order
        self.bitmap_format_bit_order = _internal.bitmap_format_bit_order
        self.bitmap_format_scanline_unit = _internal.bitmap_format_scanline_unit
        self.bitmap_format_scanline_pad = _internal.bitmap_format_scanline_pad
        self.min_keycode = Keycode(self.conn, _internal.min_keycode)
        self.max_keycode = Keycode(self.conn, _internal.max_keycode)
        self.vendor = _internal.vendor
        self.pixmap_formats = [Format(conn, d) for d in pixmap_formats]
        self.roots = [Screen(conn, d) for d in roots]

class SelectionClearEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.time = Timestamp(self.conn, _internal.time)
        self.owner = Window(self.conn, _internal.owner)
        self.selection = Atom(self.conn, _internal.selection)

class SelectionRequestEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.time = Timestamp(self.conn, _internal.time)
        self.owner = Window(self.conn, _internal.owner)
        self.requestor = Window(self.conn, _internal.requestor)
        self.selection = Atom(self.conn, _internal.selection)
        self.target = Atom(self.conn, _internal.target)
        self.property = Atom(self.conn, _internal.property)

class GetSelectionOwnerReply(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.length = _internal.length
        self.owner = Window(self.conn, _internal.owner)

class Cursor(Wrapper):
    pass

class Depth(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.depth = _internal.depth
        self.visuals_len = _internal.visuals_len
        self.visuals = [Visualtype(conn, d) for d in visuals]

class GetPropertyCookie(Wrapper):
    def reply(self):
        return GetPropertyReply(self.conn, self._internal.reply())

    def check(self):
        return self._internal.check()

class ColormapNotifyEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.window = Window(self.conn, _internal.window)
        self.colormap = Colormap(self.conn, _internal.colormap)
        self.new = _internal.new
        self.state = _internal.state

class ResizeRequestEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.window = Window(self.conn, _internal.window)
        self.width = _internal.width
        self.height = _internal.height

class Str(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.name_len = _internal.name_len
        self.name = _internal.name

class Coloritem(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.pixel = _internal.pixel
        self.red = _internal.red
        self.green = _internal.green
        self.blue = _internal.blue
        self.flags = _internal.flags

class GrabPointerReply(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.status = _internal.status
        self.length = _internal.length

class Drawable(Wrapper):
    def get_geometry(self, *args, **kwargs):
        return self.get_geometry_request(*args, **kwargs).reply()

    def get_geometry_request(self):
        return GetGeometryCookie(self.conn, self.conn.xproto.GetGeometry(self._internal))

class FocusInEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.detail = _internal.detail
        self.event = Window(self.conn, _internal.event)
        self.mode = _internal.mode

class Keysym(Wrapper):
    pass

class SetupAuthenticate(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.status = _internal.status
        self.length = _internal.length
        self.reason = _internal.reason

class GetPropertyReply(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.format = _internal.format
        self.length = _internal.length
        self.type = Atom(self.conn, _internal.type)
        self.bytes_after = _internal.bytes_after
        self.value_len = _internal.value_len
        self.value = _internal.value

class PropertyNotifyEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.window = Window(self.conn, _internal.window)
        self.atom = Atom(self.conn, _internal.atom)
        self.time = Timestamp(self.conn, _internal.time)
        self.state = _internal.state

class DestroyNotifyEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.event = Window(self.conn, _internal.event)
        self.window = Window(self.conn, _internal.window)

class Point(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.x = _internal.x
        self.y = _internal.y

class InternAtomReply(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.length = _internal.length
        self.atom = Atom(self.conn, _internal.atom)

class KeyPressEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.detail = Keycode(self.conn, _internal.detail)
        self.time = Timestamp(self.conn, _internal.time)
        self.root = Window(self.conn, _internal.root)
        self.event = Window(self.conn, _internal.event)
        self.child = Window(self.conn, _internal.child)
        self.root_x = _internal.root_x
        self.root_y = _internal.root_y
        self.event_x = _internal.event_x
        self.event_y = _internal.event_y
        self.state = _internal.state
        self.same_screen = _internal.same_screen

class Timecoord(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.time = Timestamp(self.conn, _internal.time)
        self.x = _internal.x
        self.y = _internal.y

class Window(Drawable):
    def get_property(self, *args, **kwargs):
        return self.get_property_request(*args, **kwargs).reply()

    def configure_window(self, *args, **kwargs):
        return self.configure_window_request(*args, **kwargs).check()

    def send_event(self, *args, **kwargs):
        return self.send_event_request(*args, **kwargs).check()

    def list_properties(self, *args, **kwargs):
        return self.list_properties_request(*args, **kwargs).reply()

    def grab_button(self, *args, **kwargs):
        return self.grab_button_request(*args, **kwargs).check()

    def grab_pointer(self, *args, **kwargs):
        return self.grab_pointer_request(*args, **kwargs).reply()

    def destroy_subwindows(self, *args, **kwargs):
        return self.destroy_subwindows_request(*args, **kwargs).check()

    def destroy_subwindows_request(self):
        return self.conn.xproto.DestroySubwindowsChecked(self._internal)

    def change_attributes(self, *args, **kwargs):
        return self.change_attributes_request(*args, **kwargs).check()

    def unmap_subwindows_request(self):
        return self.conn.xproto.UnmapSubwindowsChecked(self._internal)

    def intern_atom_request(self, name, only_if_exists=False):
        name_len = len(name)
        return InternAtomCookie(self.conn, self.conn.xproto.InternAtom(only_if_exists, name_len, name))

    def unmap_request(self):
        return self.conn.xproto.UnmapWindowChecked(self._internal)

    def intern_atom(self, *args, **kwargs):
        return self.intern_atom_request(*args, **kwargs).reply()

    def grab_button_request(self, owner_events, event_mask, pointer_mode, keyboard_mode, confine_to, cursor, button, modifiers):
        return self.conn.xproto.GrabButtonChecked(owner_events, self._internal, event_mask, pointer_mode, keyboard_mode, confine_to._internal, cursor._internal, button, modifiers)

    @classmethod
    def create(cls, conn, parent, depth, visual, x=0, y=0, width=640, height=480, border_width=0, _class=xcb.xproto.WindowClass.InputOutput, **values):
        value_mask, value_list = 0, []
        if "back_pixmap" in values:
            value_mask |= (1 << 0)
            value_list.append(values["back_pixmap"]._internal)
        if "back_pixel" in values:
            value_mask |= (1 << 1)
            value_list.append(values["back_pixel"])
        if "border_pixmap" in values:
            value_mask |= (1 << 2)
            value_list.append(values["border_pixmap"])
        if "border_pixel" in values:
            value_mask |= (1 << 3)
            value_list.append(values["border_pixel"])
        if "bit_gravity" in values:
            value_mask |= (1 << 4)
            value_list.append(values["bit_gravity"])
        if "win_gravity" in values:
            value_mask |= (1 << 5)
            value_list.append(values["win_gravity"])
        if "backing_store" in values:
            value_mask |= (1 << 6)
            value_list.append(values["backing_store"])
        if "backing_planes" in values:
            value_mask |= (1 << 7)
            value_list.append(values["backing_planes"])
        if "backing_pixel" in values:
            value_mask |= (1 << 8)
            value_list.append(values["backing_pixel"])
        if "override_redirect" in values:
            value_mask |= (1 << 9)
            value_list.append(values["override_redirect"])
        if "save_under" in values:
            value_mask |= (1 << 10)
            value_list.append(values["save_under"])
        if "event_mask" in values:
            value_mask |= (1 << 11)
            value_list.append(values["event_mask"])
        if "dont_propagate" in values:
            value_mask |= (1 << 12)
            value_list.append(values["dont_propagate"])
        if "colormap" in values:
            value_mask |= (1 << 13)
            value_list.append(values["colormap"])
        if "cursor" in values:
            value_mask |= (1 << 14)
            value_list.append(values["cursor"])
        wid = conn.generate_id()
        conn.xproto.CreateWindowChecked(depth, wid, parent._internal, x, y, width, height, border_width, _class, visual._internal, value_mask, value_list).check()
        return cls(conn, wid)

    def change_property(self, *args, **kwargs):
        return self.change_property_request(*args, **kwargs).check()

    def list_properties_request(self):
        return ListPropertiesCookie(self.conn, self.conn.xproto.ListProperties(self._internal))

    def delete_property_request(self, property):
        return self.conn.xproto.DeletePropertyChecked(self._internal, property._internal)

    def configure_window_request(self, **values):
        value_mask, value_list = 0, []
        if "x" in values:
            value_mask |= (1 << 0)
            value_list.append(values["x"])
        if "y" in values:
            value_mask |= (1 << 1)
            value_list.append(values["y"])
        if "width" in values:
            value_mask |= (1 << 2)
            value_list.append(values["width"])
        if "height" in values:
            value_mask |= (1 << 3)
            value_list.append(values["height"])
        if "border_width" in values:
            value_mask |= (1 << 4)
            value_list.append(values["border_width"])
        if "sibling" in values:
            value_mask |= (1 << 5)
            value_list.append(values["sibling"])
        if "stack_mode" in values:
            value_mask |= (1 << 6)
            value_list.append(values["stack_mode"])
        return self.conn.xproto.ConfigureWindowChecked(self._internal, value_mask, value_list)

    def query_tree_request(self):
        return QueryTreeCookie(self.conn, self.conn.xproto.QueryTree(self._internal))

    def change_save_set_request(self, mode):
        return self.conn.xproto.ChangeSaveSetChecked(mode, self._internal)

    def circulate_request(self, direction):
        return self.conn.xproto.CirculateWindowChecked(direction, self._internal)

    def ungrab_pointer(self, *args, **kwargs):
        return self.ungrab_pointer_request(*args, **kwargs).check()

    def grab_pointer_request(self, owner_events, event_mask, pointer_mode, keyboard_mode, confine_to, cursor, time=0):
        return GrabPointerCookie(self.conn, self.conn.xproto.GrabPointer(owner_events, self._internal, event_mask, pointer_mode, keyboard_mode, confine_to._internal, cursor._internal, time._internal))

    def reparent_request(self, parent, x, y):
        return self.conn.xproto.ReparentWindowChecked(self._internal, parent._internal, x, y)

    def map(self, *args, **kwargs):
        return self.map_request(*args, **kwargs).check()

    def get_property_request(self, delete, property, type, long_offset=0, long_length=2**32-1):
        return GetPropertyCookie(self.conn, self.conn.xproto.GetProperty(delete, self._internal, property._internal, type._internal, long_offset, long_length))

    def map_request(self):
        return self.conn.xproto.MapWindowChecked(self._internal)

    def ungrab_button_request(self, button, modifiers):
        return self.conn.xproto.UngrabButtonChecked(button, self._internal, modifiers)

    def change_attributes_request(self, **values):
        value_mask, value_list = 0, []
        if "back_pixmap" in values:
            value_mask |= (1 << 0)
            value_list.append(values["back_pixmap"]._internal)
        if "back_pixel" in values:
            value_mask |= (1 << 1)
            value_list.append(values["back_pixel"])
        if "border_pixmap" in values:
            value_mask |= (1 << 2)
            value_list.append(values["border_pixmap"])
        if "border_pixel" in values:
            value_mask |= (1 << 3)
            value_list.append(values["border_pixel"])
        if "bit_gravity" in values:
            value_mask |= (1 << 4)
            value_list.append(values["bit_gravity"])
        if "win_gravity" in values:
            value_mask |= (1 << 5)
            value_list.append(values["win_gravity"])
        if "backing_store" in values:
            value_mask |= (1 << 6)
            value_list.append(values["backing_store"])
        if "backing_planes" in values:
            value_mask |= (1 << 7)
            value_list.append(values["backing_planes"])
        if "backing_pixel" in values:
            value_mask |= (1 << 8)
            value_list.append(values["backing_pixel"])
        if "override_redirect" in values:
            value_mask |= (1 << 9)
            value_list.append(values["override_redirect"])
        if "save_under" in values:
            value_mask |= (1 << 10)
            value_list.append(values["save_under"])
        if "event_mask" in values:
            value_mask |= (1 << 11)
            value_list.append(values["event_mask"])
        if "dont_propagate" in values:
            value_mask |= (1 << 12)
            value_list.append(values["dont_propagate"])
        if "colormap" in values:
            value_mask |= (1 << 13)
            value_list.append(values["colormap"])
        if "cursor" in values:
            value_mask |= (1 << 14)
            value_list.append(values["cursor"])
        return self.conn.xproto.ChangeWindowAttributesChecked(self._internal, value_mask, value_list)

    def send_event_request(self, propagate, event_mask, event):
        return self.conn.xproto.SendEventChecked(propagate, self._internal, event_mask, event)

    def change_property_request(self, mode, property, type, format, data):
        data_len = len(data)
        return self.conn.xproto.ChangePropertyChecked(mode, self._internal, property._internal, type._internal, format, data_len, data)

    def destroy(self, *args, **kwargs):
        return self.destroy_request(*args, **kwargs).check()

    def unmap_subwindows(self, *args, **kwargs):
        return self.unmap_subwindows_request(*args, **kwargs).check()

    def unmap(self, *args, **kwargs):
        return self.unmap_request(*args, **kwargs).check()

    def query_tree(self, *args, **kwargs):
        return self.query_tree_request(*args, **kwargs).reply()

    def reparent(self, *args, **kwargs):
        return self.reparent_request(*args, **kwargs).check()

    def change_save_set(self, *args, **kwargs):
        return self.change_save_set_request(*args, **kwargs).check()

    def destroy_request(self):
        return self.conn.xproto.DestroyWindowChecked(self._internal)

    def delete_property(self, *args, **kwargs):
        return self.delete_property_request(*args, **kwargs).check()

    def ungrab_button(self, *args, **kwargs):
        return self.ungrab_button_request(*args, **kwargs).check()

    def ungrab_pointer_request(self, time=0):
        return self.conn.xproto.UngrabPointerChecked(time._internal)

    def circulate(self, *args, **kwargs):
        return self.circulate_request(*args, **kwargs).check()

class SelectionNotifyEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.time = Timestamp(self.conn, _internal.time)
        self.requestor = Window(self.conn, _internal.requestor)
        self.selection = Atom(self.conn, _internal.selection)
        self.target = Atom(self.conn, _internal.target)
        self.property = Atom(self.conn, _internal.property)

class NoExposureEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.drawable = Drawable(self.conn, _internal.drawable)
        self.minor_opcode = _internal.minor_opcode
        self.major_opcode = _internal.major_opcode

class LeaveNotifyEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.detail = _internal.detail
        self.time = Timestamp(self.conn, _internal.time)
        self.root = Window(self.conn, _internal.root)
        self.event = Window(self.conn, _internal.event)
        self.child = Window(self.conn, _internal.child)
        self.root_x = _internal.root_x
        self.root_y = _internal.root_y
        self.event_x = _internal.event_x
        self.event_y = _internal.event_y
        self.state = _internal.state
        self.mode = _internal.mode
        self.same_screen_focus = _internal.same_screen_focus

class Arc(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.x = _internal.x
        self.y = _internal.y
        self.width = _internal.width
        self.height = _internal.height
        self.angle1 = _internal.angle1
        self.angle2 = _internal.angle2

class Visualtype(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.visual_id = VisualID(self.conn, _internal.visual_id)
        self._class = _internal._class
        self.bits_per_rgb_value = _internal.bits_per_rgb_value
        self.colormap_entries = _internal.colormap_entries
        self.red_mask = _internal.red_mask
        self.green_mask = _internal.green_mask
        self.blue_mask = _internal.blue_mask

class KeymapNotifyEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.keys = _internal.keys

class ListPropertiesCookie(Wrapper):
    def reply(self):
        return ListPropertiesReply(self.conn, self._internal.reply())

    def check(self):
        return self._internal.check()

class QueryTreeReply(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.length = _internal.length
        self.root = Window(self.conn, _internal.root)
        self.parent = Window(self.conn, _internal.parent)
        self.children_len = _internal.children_len
        self.children = Window(self.conn, _internal.children)

class Font(Wrapper):
    pass

class Gcontext(Wrapper):
    pass

class CirculateRequestEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.event = Window(self.conn, _internal.event)
        self.window = Window(self.conn, _internal.window)
        self.place = _internal.place

class ExposeEvent(Wrapper):
    def __init__(self, conn, _internal):
        Wrapper.__init__(self, conn, _internal)
        self.window = Window(self.conn, _internal.window)
        self.x = _internal.x
        self.y = _internal.y
        self.width = _internal.width
        self.height = _internal.height
        self.count = _internal.count


