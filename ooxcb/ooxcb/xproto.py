# auto generated. yay.
import ooxcb
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
from struct import pack, unpack_from, calcsize
from array import array

def unpack_ex(fmt, protobj, offset=0):
    s = protobj.get_slice(calcsize(fmt), offset)
    return unpack_from(fmt, s, 0)

class GetModifierMappingCookie(object):
    pass

class TranslateCoordinatesReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxxxxxIHH", self, count)
        self.same_screen = _unpacked[0]
        self.child = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.dst_x = _unpacked[2]
        self.dst_y = _unpacked[3]

class PropMode(object):
    Replace = 0
    Prepend = 1
    Append = 2

class HostMode(object):
    Insert = 0
    Delete = 1

class QueryBestSizeCookie(object):
    pass

class GraphicsExposureEvent(ooxcb.Event):
    event_name = "on_graphics_exposure"
    event_target_class = "Drawable"
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHHHHHHB", self, count)
        self.drawable = conn.get_from_cache_fallback(_unpacked[0], Drawable)
        self.x = _unpacked[1]
        self.y = _unpacked[2]
        self.width = _unpacked[3]
        self.height = _unpacked[4]
        self.minor_opcode = _unpacked[5]
        self.count = _unpacked[6]
        self.major_opcode = _unpacked[7]
        self.event_target = self.drawable

class FontDraw(object):
    LeftToRight = 0
    RightToLeft = 1

class ClientMessageData(ooxcb.Union):
    def __init__(self, conn, parent, offset, size):
        ooxcb.Union.__init__(self, conn, parent, offset, size)
        count = 0
        self.data8 = ooxcb.List(conn, self, 0, 20, 'B', 1)
        count = max(count, len(self.data8.buf()))
        self.data16 = ooxcb.List(conn, self, 0, 10, 'H', 2)
        count = max(count, len(self.data16.buf()))
        self.data32 = ooxcb.List(conn, self, 0, 5, 'I', 4)
        count = max(count, len(self.data32.buf()))

class QueryExtensionReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxxxxxBBBB", self, count)
        self.present = _unpacked[0]
        self.major_opcode = _unpacked[1]
        self.first_event = _unpacked[2]
        self.first_error = _unpacked[3]

class QueryTreeReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxxxxxIIHxxxxxxxxxxxxxx", self, count)
        self.root = conn.get_from_cache_fallback(_unpacked[0], Window)
        self.parent = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.children_len = _unpacked[2]
        count += 32
        self.children = ooxcb.List(conn, self, count, self.children_len, 'I', 4)

class ListInstalledColormapsReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxxxxxHxxxxxxxxxxxxxxxxxxxxxx", self, count)
        self.cmaps_len = _unpacked[0]
        count += 32
        self.cmaps = ooxcb.List(conn, self, count, self.cmaps_len, 'I', 4)

class Rgb(ooxcb.Struct):
    def __init__(self, conn, parent, offset, size):
        ooxcb.Struct.__init__(self, conn, parent, offset, size)
        count = 0
        _unpacked = unpack_ex("HHHxx", self, count)
        self.red = _unpacked[0]
        self.green = _unpacked[1]
        self.blue = _unpacked[2]
        ooxcb._resize_obj(self, count)

class QueryTreeCookie(object):
    pass

class VisualClass(object):
    StaticGray = 0
    GrayScale = 1
    StaticColor = 2
    PseudoColor = 3
    TrueColor = 4
    DirectColor = 5

class GetWindowAttributesReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxxxxxIHBBIIBBBBIIIH", self, count)
        self.backing_store = _unpacked[0]
        self.visual = VisualID(conn, _unpacked[1])
        self._class = _unpacked[2]
        self.bit_gravity = _unpacked[3]
        self.win_gravity = _unpacked[4]
        self.backing_planes = _unpacked[5]
        self.backing_pixel = _unpacked[6]
        self.save_under = _unpacked[7]
        self.map_is_installed = _unpacked[8]
        self.map_state = _unpacked[9]
        self.override_redirect = _unpacked[10]
        self.colormap = conn.get_from_cache_fallback(_unpacked[11], Colormap)
        self.all_event_masks = _unpacked[12]
        self.your_event_mask = _unpacked[13]
        self.do_not_propagate_mask = _unpacked[14]

class FillStyle(object):
    Solid = 0
    Tiled = 1
    Stippled = 2
    OpaqueStippled = 3

class AllocColorCookie(object):
    pass

class Exposures(object):
    NotAllowed = 0
    Allowed = 1
    Default = 2

class AllocError(ooxcb.Error):
    def __init__(self, conn, parent):
        ooxcb.Error.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHB", self, count)
        self.bad_value = _unpacked[0]
        self.minor_opcode = _unpacked[1]
        self.major_opcode = _unpacked[2]

class ButtonIndex(object):
    Any = 0
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5

class Colormap(ooxcb.Resource):
    def __init__(self, conn, xid):
        ooxcb.Resource.__init__(self, conn, xid)

class SetModifierMappingReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxxxxx", self, count)
        self.status = _unpacked[0]

class ConfigWindow(object):
    X = (1 << 0)
    Y = (1 << 1)
    Width = (1 << 2)
    Height = (1 << 3)
    BorderWidth = (1 << 4)
    Sibling = (1 << 5)
    StackMode = (1 << 6)

class GrabPointerReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxxxxx", self, count)
        self.status = _unpacked[0]

class NameError(ooxcb.Error):
    def __init__(self, conn, parent):
        ooxcb.Error.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHB", self, count)
        self.bad_value = _unpacked[0]
        self.minor_opcode = _unpacked[1]
        self.major_opcode = _unpacked[2]

class BadAtom(ooxcb.ProtocolException):
    pass

class BadCursor(ooxcb.ProtocolException):
    pass

class GContextError(ooxcb.Error):
    def __init__(self, conn, parent):
        ooxcb.Error.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHB", self, count)
        self.bad_value = _unpacked[0]
        self.minor_opcode = _unpacked[1]
        self.major_opcode = _unpacked[2]

class GetPropertyType(object):
    Any = 0

class Coloritem(ooxcb.Struct):
    def __init__(self, conn, parent, offset, size):
        ooxcb.Struct.__init__(self, conn, parent, offset, size)
        count = 0
        _unpacked = unpack_ex("IHHHBx", self, count)
        self.pixel = _unpacked[0]
        self.red = _unpacked[1]
        self.green = _unpacked[2]
        self.blue = _unpacked[3]
        self.flags = _unpacked[4]
        ooxcb._resize_obj(self, count)

class BadAccess(ooxcb.ProtocolException):
    pass

class RequestError(ooxcb.Error):
    def __init__(self, conn, parent):
        ooxcb.Error.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHB", self, count)
        self.bad_value = _unpacked[0]
        self.minor_opcode = _unpacked[1]
        self.major_opcode = _unpacked[2]

class Setupauthenticate(ooxcb.Struct):
    def __init__(self, conn, parent, offset):
        ooxcb.Struct.__init__(self, conn, parent, offset)
        count = 0
        _unpacked = unpack_ex("BxxxxxH", self, count)
        self.status = _unpacked[0]
        self.length = _unpacked[1]
        count += 8
        self.reason = ooxcb.List(conn, self, count, (self.length * 4), 'b', 1)
        count += len(self.reason.buf())

class GetScreenSaverReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxxxxxHHBB", self, count)
        self.timeout = _unpacked[0]
        self.interval = _unpacked[1]
        self.prefer_blanking = _unpacked[2]
        self.allow_exposures = _unpacked[3]

class LengthError(ooxcb.Error):
    def __init__(self, conn, parent):
        ooxcb.Error.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHB", self, count)
        self.bad_value = _unpacked[0]
        self.minor_opcode = _unpacked[1]
        self.major_opcode = _unpacked[2]

class AccessControl(object):
    Disable = 0
    Enable = 1

class ListFontsWithInfoCookie(object):
    pass

class Blanking(object):
    NotPreferred = 0
    Preferred = 1
    Default = 2

class Fontable(ooxcb.Resource):
    def __init__(self, conn, xid):
        ooxcb.Resource.__init__(self, conn, xid)

class QueryShapeOf(object):
    LargestCursor = 0
    FastestTile = 1
    FastestStipple = 2

class ConfigureNotifyEvent(ooxcb.Event):
    event_name = "on_configure_notify"
    event_target_class = "Window"
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIIIhhHHHB", self, count)
        self.event = conn.get_from_cache_fallback(_unpacked[0], Window)
        self.window = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.above_sibling = conn.get_from_cache_fallback(_unpacked[2], Window)
        self.x = _unpacked[3]
        self.y = _unpacked[4]
        self.width = _unpacked[5]
        self.height = _unpacked[6]
        self.border_width = _unpacked[7]
        self.override_redirect = _unpacked[8]
        self.event_target = self.window

class Setup(ooxcb.Struct):
    def __init__(self, conn, parent, offset):
        ooxcb.Struct.__init__(self, conn, parent, offset)
        count = 0
        _unpacked = unpack_ex("BxHHHIIIIHHBBBBBBBBxxxx", self, count)
        self.status = _unpacked[0]
        self.protocol_major_version = _unpacked[1]
        self.protocol_minor_version = _unpacked[2]
        self.length = _unpacked[3]
        self.release_number = _unpacked[4]
        self.resource_id_base = _unpacked[5]
        self.resource_id_mask = _unpacked[6]
        self.motion_buffer_size = _unpacked[7]
        self.vendor_len = _unpacked[8]
        self.maximum_request_length = _unpacked[9]
        self.roots_len = _unpacked[10]
        self.pixmap_formats_len = _unpacked[11]
        self.image_byte_order = _unpacked[12]
        self.bitmap_format_bit_order = _unpacked[13]
        self.bitmap_format_scanline_unit = _unpacked[14]
        self.bitmap_format_scanline_pad = _unpacked[15]
        self.min_keycode = Keycode(conn, _unpacked[16])
        self.max_keycode = Keycode(conn, _unpacked[17])
        count += 40
        self.vendor = ooxcb.List(conn, self, count, self.vendor_len, 'b', 1)
        count += len(self.vendor.buf())
        count += ooxcb.type_pad(8, count)
        self.pixmap_formats = ooxcb.List(conn, self, count, self.pixmap_formats_len, Format, 8)
        count += len(self.pixmap_formats.buf())
        count += ooxcb.type_pad(4, count)
        self.roots = ooxcb.List(conn, self, count, self.roots_len, Screen, -1)
        count += len(self.roots.buf())

class WindowClass(object):
    CopyFromParent = 0
    InputOutput = 1
    InputOnly = 2

class SelectionClearEvent(ooxcb.Event):
    event_name = "on_selection_clear"
    event_target_class = ooxcb.Connection
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIII", self, count)
        self.time = Timestamp(conn, _unpacked[0])
        self.owner = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.selection = Atom(conn, _unpacked[2])
        self.event_target = self.conn

class GX(object):
    clear = 0x0
    _and = 0x1
    andReverse = 0x2
    copy = 0x3
    andInverted = 0x4
    noop = 0x5
    xor = 0x6
    _or = 0x7
    nor = 0x8
    equiv = 0x9
    invert = 0xa
    orReverse = 0xb
    copyInverted = 0xc
    orInverted = 0xd
    nand = 0xe
    set = 0xf

class Motion(object):
    Normal = 0
    Hint = 1

class GC(object):
    Function = (1 << 0)
    PlaneMask = (1 << 1)
    Foreground = (1 << 2)
    Background = (1 << 3)
    LineWidth = (1 << 4)
    LineStyle = (1 << 5)
    CapStyle = (1 << 6)
    JoinStyle = (1 << 7)
    FillStyle = (1 << 8)
    FillRule = (1 << 9)
    Tile = (1 << 10)
    Stipple = (1 << 11)
    TileStippleOriginX = (1 << 12)
    TileStippleOriginY = (1 << 13)
    Font = (1 << 14)
    SubwindowMode = (1 << 15)
    GraphicsExposures = (1 << 16)
    ClipOriginX = (1 << 17)
    ClipOriginY = (1 << 18)
    ClipMask = (1 << 19)
    DashOffset = (1 << 20)
    DashList = (1 << 21)
    ArcMode = (1 << 22)

class GetSelectionOwnerCookie(object):
    pass

class Keysym(ooxcb.Resource):
    def __init__(self, conn, xid):
        ooxcb.Resource.__init__(self, conn, xid)

class ImplementationError(ooxcb.Error):
    def __init__(self, conn, parent):
        ooxcb.Error.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHB", self, count)
        self.bad_value = _unpacked[0]
        self.minor_opcode = _unpacked[1]
        self.major_opcode = _unpacked[2]

class ListHostsReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxxxxxHxxxxxxxxxxxxxxxxxxxxxx", self, count)
        self.mode = _unpacked[0]
        self.hosts_len = _unpacked[1]
        count += 32
        self.hosts = ooxcb.List(conn, self, count, self.hosts_len, Host, -1)

class GetModifierMappingReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", self, count)
        self.keycodes_per_modifier = _unpacked[0]
        count += 32
        self.keycodes = ooxcb.List(conn, self, count, (self.keycodes_per_modifier * 8), 'B', 1)

class GetPointerMappingReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", self, count)
        self.map_len = _unpacked[0]
        count += 32
        self.map = ooxcb.List(conn, self, count, self.map_len, 'B', 1)

class DestroyNotifyEvent(ooxcb.Event):
    event_name = "on_destroy_notify"
    event_target_class = "Window"
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxII", self, count)
        self.event = conn.get_from_cache_fallback(_unpacked[0], Window)
        self.window = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.event_target = self.window

class QueryKeymapReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        count += 8
        self.keys = ooxcb.List(conn, self, count, 32, 'B', 1)

class AllocColorReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxxxxxHHHxxI", self, count)
        self.red = _unpacked[0]
        self.green = _unpacked[1]
        self.blue = _unpacked[2]
        self.pixel = _unpacked[3]

class BadName(ooxcb.ProtocolException):
    pass

class ListInstalledColormapsCookie(object):
    pass

class GetScreenSaverCookie(object):
    pass

class Arc(ooxcb.Struct):
    def __init__(self, conn, parent, offset, size):
        ooxcb.Struct.__init__(self, conn, parent, offset, size)
        count = 0
        _unpacked = unpack_ex("hhHHhh", self, count)
        self.x = _unpacked[0]
        self.y = _unpacked[1]
        self.width = _unpacked[2]
        self.height = _unpacked[3]
        self.angle1 = _unpacked[4]
        self.angle2 = _unpacked[5]
        ooxcb._resize_obj(self, count)

class Kill(object):
    AllTemporary = 0

class QueryFontCookie(object):
    pass

class Font(ooxcb.Resource):
    def __init__(self, conn, xid):
        ooxcb.Resource.__init__(self, conn, xid)

class QueryKeymapCookie(object):
    pass

class ExposeEvent(ooxcb.Event):
    event_name = "on_expose"
    event_target_class = ooxcb.Connection
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHHHHH", self, count)
        self.window = conn.get_from_cache_fallback(_unpacked[0], Window)
        self.x = _unpacked[1]
        self.y = _unpacked[2]
        self.width = _unpacked[3]
        self.height = _unpacked[4]
        self.count = _unpacked[5]
        self.event_target = self.conn

class GravityNotifyEvent(ooxcb.Event):
    event_name = "on_gravity_notify"
    event_target_class = ooxcb.Connection
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIIhh", self, count)
        self.event = conn.get_from_cache_fallback(_unpacked[0], Window)
        self.window = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.x = _unpacked[2]
        self.y = _unpacked[3]
        self.event_target = self.conn

class GrabKeyboardReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxxxxx", self, count)
        self.status = _unpacked[0]

class KeyPressEvent(ooxcb.Event):
    event_name = "on_key_press"
    event_target_class = "Window"
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxIIIIhhhhHB", self, count)
        self.detail = Keycode(conn, _unpacked[0])
        self.time = Timestamp(conn, _unpacked[1])
        self.root = conn.get_from_cache_fallback(_unpacked[2], Window)
        self.event = conn.get_from_cache_fallback(_unpacked[3], Window)
        self.child = conn.get_from_cache_fallback(_unpacked[4], Window)
        self.root_x = _unpacked[5]
        self.root_y = _unpacked[6]
        self.event_x = _unpacked[7]
        self.event_y = _unpacked[8]
        self.state = _unpacked[9]
        self.same_screen = _unpacked[10]
        self.event_target = self.event

class ListPropertiesReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxxxxxHxxxxxxxxxxxxxxxxxxxxxx", self, count)
        self.atoms_len = _unpacked[0]
        count += 32
        self.atoms = ooxcb.List(conn, self, count, self.atoms_len, 'I', 4)

class ListExtensionsReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", self, count)
        self.names_len = _unpacked[0]
        count += 32
        self.names = ooxcb.List(conn, self, count, self.names_len, Str, -1)

class CapStyle(object):
    NotLast = 0
    Butt = 1
    Round = 2
    Projecting = 3

class AllocNamedColorCookie(object):
    pass

class MatchError(ooxcb.Error):
    def __init__(self, conn, parent):
        ooxcb.Error.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHB", self, count)
        self.bad_value = _unpacked[0]
        self.minor_opcode = _unpacked[1]
        self.major_opcode = _unpacked[2]

class UnmapNotifyEvent(ooxcb.Event):
    event_name = "on_unmap_notify"
    event_target_class = "Window"
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIIB", self, count)
        self.event = conn.get_from_cache_fallback(_unpacked[0], Window)
        self.window = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.from_configure = _unpacked[2]
        self.event_target = self.window

class Setupfailed(ooxcb.Struct):
    def __init__(self, conn, parent, offset):
        ooxcb.Struct.__init__(self, conn, parent, offset)
        count = 0
        _unpacked = unpack_ex("BBHHH", self, count)
        self.status = _unpacked[0]
        self.reason_len = _unpacked[1]
        self.protocol_major_version = _unpacked[2]
        self.protocol_minor_version = _unpacked[3]
        self.length = _unpacked[4]
        count += 8
        self.reason = ooxcb.List(conn, self, count, self.reason_len, 'b', 1)
        count += len(self.reason.buf())

class IDChoiceError(ooxcb.Error):
    def __init__(self, conn, parent):
        ooxcb.Error.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHB", self, count)
        self.bad_value = _unpacked[0]
        self.minor_opcode = _unpacked[1]
        self.major_opcode = _unpacked[2]

class AllocColorCellsReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxxxxxHHxxxxxxxxxxxxxxxxxxxx", self, count)
        self.pixels_len = _unpacked[0]
        self.masks_len = _unpacked[1]
        count += 32
        self.pixels = ooxcb.List(conn, self, count, self.pixels_len, 'I', 4)
        count += len(self.pixels.buf())
        count += ooxcb.type_pad(4, count)
        self.masks = ooxcb.List(conn, self, count, self.masks_len, 'I', 4)

class ConfigureRequestEvent(ooxcb.Event):
    event_name = "on_configure_request"
    event_target_class = "Window"
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxIIIhhHHHH", self, count)
        self.stack_mode = _unpacked[0]
        self.parent = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.window = conn.get_from_cache_fallback(_unpacked[2], Window)
        self.sibling = conn.get_from_cache_fallback(_unpacked[3], Window)
        self.x = _unpacked[4]
        self.y = _unpacked[5]
        self.width = _unpacked[6]
        self.height = _unpacked[7]
        self.border_width = _unpacked[8]
        self.value_mask = _unpacked[9]
        self.event_target = self.window

class BadImplementation(ooxcb.ProtocolException):
    pass

class TranslateCoordinatesCookie(object):
    pass

class BadRequest(ooxcb.ProtocolException):
    pass

class FillRule(object):
    EvenOdd = 0
    Winding = 1

class GrabMode(object):
    Sync = 0
    Async = 1

class GetKeyboardControlCookie(object):
    pass

class ColormapAlloc(object):
    _None = 0
    All = 1

class FontError(ooxcb.Error):
    def __init__(self, conn, parent):
        ooxcb.Error.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHB", self, count)
        self.bad_value = _unpacked[0]
        self.minor_opcode = _unpacked[1]
        self.major_opcode = _unpacked[2]

class ModMask(object):
    Shift = (1 << 0)
    Lock = (1 << 1)
    Control = (1 << 2)
    _1 = (1 << 3)
    _2 = (1 << 4)
    _3 = (1 << 5)
    _4 = (1 << 6)
    _5 = (1 << 7)

class Setuprequest(ooxcb.Struct):
    def __init__(self, conn, parent, offset):
        ooxcb.Struct.__init__(self, conn, parent, offset)
        count = 0
        _unpacked = unpack_ex("BxHHHH", self, count)
        self.byte_order = _unpacked[0]
        self.protocol_major_version = _unpacked[1]
        self.protocol_minor_version = _unpacked[2]
        self.authorization_protocol_name_len = _unpacked[3]
        self.authorization_protocol_data_len = _unpacked[4]
        count += 10
        self.authorization_protocol_name = ooxcb.List(conn, self, count, self.authorization_protocol_name_len, 'b', 1)
        count += len(self.authorization_protocol_name.buf())
        count += ooxcb.type_pad(1, count)
        self.authorization_protocol_data = ooxcb.List(conn, self, count, self.authorization_protocol_data_len, 'b', 1)
        count += len(self.authorization_protocol_data.buf())

class Visibility(object):
    Unobscured = 0
    PartiallyObscured = 1
    FullyObscured = 2

class xprotoExtension(ooxcb.Extension):
    header = "xproto"
    def create_window_checked(self, depth, wid_, parent_, x, y, width, height, border_width, _class, visual_, value_mask, value_list):
        wid = wid_.get_internal()
        parent = parent_.get_internal()
        visual = visual_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIIhhHHHHII", depth, wid, parent, x, y, width, height, border_width, _class, visual, value_mask))
        buf.write(str(buffer(array("I", value_list))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 1, True, True), \
            ooxcb.VoidCookie())

    def create_window(self, depth, wid_, parent_, x, y, width, height, border_width, _class, visual_, value_mask, value_list):
        wid = wid_.get_internal()
        parent = parent_.get_internal()
        visual = visual_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIIhhHHHHII", depth, wid, parent, x, y, width, height, border_width, _class, visual, value_mask))
        buf.write(str(buffer(array("I", value_list))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 1, True, False), \
            ooxcb.VoidCookie())

    def change_window_attributes_checked(self, window_, value_mask, value_list):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", window, value_mask))
        buf.write(str(buffer(array("I", value_list))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 2, True, True), \
            ooxcb.VoidCookie())

    def change_window_attributes(self, window_, value_mask, value_list):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", window, value_mask))
        buf.write(str(buffer(array("I", value_list))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 2, True, False), \
            ooxcb.VoidCookie())

    def get_window_attributes(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 3, False, True), \
            GetWindowAttributesCookie(),
            GetWindowAttributesReply)

    def get_window_attributes_unchecked(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 3, False, False), \
            GetWindowAttributesCookie(),
            GetWindowAttributesReply)

    def destroy_window_checked(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 4, True, True), \
            ooxcb.VoidCookie())

    def destroy_window(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 4, True, False), \
            ooxcb.VoidCookie())

    def destroy_subwindows_checked(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 5, True, True), \
            ooxcb.VoidCookie())

    def destroy_subwindows(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 5, True, False), \
            ooxcb.VoidCookie())

    def change_save_set_checked(self, mode, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxI", mode, window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 6, True, True), \
            ooxcb.VoidCookie())

    def change_save_set(self, mode, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxI", mode, window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 6, True, False), \
            ooxcb.VoidCookie())

    def reparent_window_checked(self, window_, parent_, x, y):
        window = window_.get_internal()
        parent = parent_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIhh", window, parent, x, y))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 7, True, True), \
            ooxcb.VoidCookie())

    def reparent_window(self, window_, parent_, x, y):
        window = window_.get_internal()
        parent = parent_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIhh", window, parent, x, y))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 7, True, False), \
            ooxcb.VoidCookie())

    def map_subwindows_checked(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 9, True, True), \
            ooxcb.VoidCookie())

    def map_subwindows(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 9, True, False), \
            ooxcb.VoidCookie())

    def unmap_window_checked(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 10, True, True), \
            ooxcb.VoidCookie())

    def unmap_window(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 10, True, False), \
            ooxcb.VoidCookie())

    def unmap_subwindows_checked(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 11, True, True), \
            ooxcb.VoidCookie())

    def unmap_subwindows(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 11, True, False), \
            ooxcb.VoidCookie())

    def configure_window_checked(self, window_, value_mask, value_list):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIH", window, value_mask))
        buf.write(str(buffer(array("I", value_list))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 12, True, True), \
            ooxcb.VoidCookie())

    def configure_window(self, window_, value_mask, value_list):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIH", window, value_mask))
        buf.write(str(buffer(array("I", value_list))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 12, True, False), \
            ooxcb.VoidCookie())

    def circulate_window_checked(self, direction, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxI", direction, window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 13, True, True), \
            ooxcb.VoidCookie())

    def circulate_window(self, direction, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxI", direction, window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 13, True, False), \
            ooxcb.VoidCookie())

    def get_geometry(self, drawable_):
        drawable = drawable_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", drawable))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 14, False, True), \
            GetGeometryCookie(),
            GetGeometryReply)

    def get_geometry_unchecked(self, drawable_):
        drawable = drawable_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", drawable))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 14, False, False), \
            GetGeometryCookie(),
            GetGeometryReply)

    def query_tree(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 15, False, True), \
            QueryTreeCookie(),
            QueryTreeReply)

    def query_tree_unchecked(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 15, False, False), \
            QueryTreeCookie(),
            QueryTreeReply)

    def intern_atom(self, only_if_exists, name_len, name):
        buf = StringIO.StringIO()
        buf.write(pack("xBxxHxx", only_if_exists, name_len))
        buf.write(str(buffer(array("b", name))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 16, False, True), \
            InternAtomCookie(),
            InternAtomReply)

    def intern_atom_unchecked(self, only_if_exists, name_len, name):
        buf = StringIO.StringIO()
        buf.write(pack("xBxxHxx", only_if_exists, name_len))
        buf.write(str(buffer(array("b", name))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 16, False, False), \
            InternAtomCookie(),
            InternAtomReply)

    def get_atom_name(self, atom_):
        atom = atom_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", atom))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 17, False, True), \
            GetAtomNameCookie(),
            GetAtomNameReply)

    def get_atom_name_unchecked(self, atom_):
        atom = atom_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", atom))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 17, False, False), \
            GetAtomNameCookie(),
            GetAtomNameReply)

    def change_property_checked(self, mode, window_, property_, type_, format, data_len, data):
        window = window_.get_internal()
        property = property_.get_internal()
        type = type_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIIIBxxxI", mode, window, property, type, format, data_len))
        buf.write(str(buffer(array("B", data))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 18, True, True), \
            ooxcb.VoidCookie())

    def change_property(self, mode, window_, property_, type_, format, data_len, data):
        window = window_.get_internal()
        property = property_.get_internal()
        type = type_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIIIBxxxI", mode, window, property, type, format, data_len))
        buf.write(str(buffer(array("B", data))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 18, True, False), \
            ooxcb.VoidCookie())

    def delete_property_checked(self, window_, property_):
        window = window_.get_internal()
        property = property_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", window, property))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 19, True, True), \
            ooxcb.VoidCookie())

    def delete_property(self, window_, property_):
        window = window_.get_internal()
        property = property_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", window, property))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 19, True, False), \
            ooxcb.VoidCookie())

    def list_properties(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 21, False, True), \
            ListPropertiesCookie(),
            ListPropertiesReply)

    def list_properties_unchecked(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 21, False, False), \
            ListPropertiesCookie(),
            ListPropertiesReply)

    def set_selection_owner_checked(self, owner_, selection_, time_):
        owner = owner_.get_internal()
        selection = selection_.get_internal()
        time = time_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIII", owner, selection, time))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 22, True, True), \
            ooxcb.VoidCookie())

    def set_selection_owner(self, owner_, selection_, time_):
        owner = owner_.get_internal()
        selection = selection_.get_internal()
        time = time_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIII", owner, selection, time))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 22, True, False), \
            ooxcb.VoidCookie())

    def get_selection_owner(self, selection_):
        selection = selection_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", selection))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 23, False, True), \
            GetSelectionOwnerCookie(),
            GetSelectionOwnerReply)

    def get_selection_owner_unchecked(self, selection_):
        selection = selection_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", selection))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 23, False, False), \
            GetSelectionOwnerCookie(),
            GetSelectionOwnerReply)

    def convert_selection_checked(self, requestor_, selection_, target_, property_, time_):
        requestor = requestor_.get_internal()
        selection = selection_.get_internal()
        target = target_.get_internal()
        property = property_.get_internal()
        time = time_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIIII", requestor, selection, target, property, time))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 24, True, True), \
            ooxcb.VoidCookie())

    def convert_selection(self, requestor_, selection_, target_, property_, time_):
        requestor = requestor_.get_internal()
        selection = selection_.get_internal()
        target = target_.get_internal()
        property = property_.get_internal()
        time = time_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIIII", requestor, selection, target, property, time))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 24, True, False), \
            ooxcb.VoidCookie())

    def send_event_checked(self, propagate, destination_, event_mask, event):
        destination = destination_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxII", propagate, destination, event_mask))
        buf.write(str(buffer(array("b", event))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 25, True, True), \
            ooxcb.VoidCookie())

    def send_event(self, propagate, destination_, event_mask, event):
        destination = destination_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxII", propagate, destination, event_mask))
        buf.write(str(buffer(array("b", event))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 25, True, False), \
            ooxcb.VoidCookie())

    def grab_pointer(self, owner_events, grab_window_, event_mask, pointer_mode, keyboard_mode, confine_to_, cursor_, time_):
        grab_window = grab_window_.get_internal()
        confine_to = confine_to_.get_internal()
        cursor = cursor_.get_internal()
        time = time_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIHBBIII", owner_events, grab_window, event_mask, pointer_mode, keyboard_mode, confine_to, cursor, time))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 26, False, True), \
            GrabPointerCookie(),
            GrabPointerReply)

    def grab_pointer_unchecked(self, owner_events, grab_window_, event_mask, pointer_mode, keyboard_mode, confine_to_, cursor_, time_):
        grab_window = grab_window_.get_internal()
        confine_to = confine_to_.get_internal()
        cursor = cursor_.get_internal()
        time = time_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIHBBIII", owner_events, grab_window, event_mask, pointer_mode, keyboard_mode, confine_to, cursor, time))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 26, False, False), \
            GrabPointerCookie(),
            GrabPointerReply)

    def ungrab_pointer_checked(self, time_):
        time = time_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", time))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 27, True, True), \
            ooxcb.VoidCookie())

    def ungrab_pointer(self, time_):
        time = time_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", time))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 27, True, False), \
            ooxcb.VoidCookie())

    def grab_button_checked(self, owner_events, grab_window_, event_mask, pointer_mode, keyboard_mode, confine_to_, cursor_, button, modifiers):
        grab_window = grab_window_.get_internal()
        confine_to = confine_to_.get_internal()
        cursor = cursor_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIHBBIIBxH", owner_events, grab_window, event_mask, pointer_mode, keyboard_mode, confine_to, cursor, button, modifiers))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 28, True, True), \
            ooxcb.VoidCookie())

    def grab_button(self, owner_events, grab_window_, event_mask, pointer_mode, keyboard_mode, confine_to_, cursor_, button, modifiers):
        grab_window = grab_window_.get_internal()
        confine_to = confine_to_.get_internal()
        cursor = cursor_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIHBBIIBxH", owner_events, grab_window, event_mask, pointer_mode, keyboard_mode, confine_to, cursor, button, modifiers))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 28, True, False), \
            ooxcb.VoidCookie())

    def ungrab_button_checked(self, button, grab_window_, modifiers):
        grab_window = grab_window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIHxx", button, grab_window, modifiers))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 29, True, True), \
            ooxcb.VoidCookie())

    def ungrab_button(self, button, grab_window_, modifiers):
        grab_window = grab_window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIHxx", button, grab_window, modifiers))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 29, True, False), \
            ooxcb.VoidCookie())

    def change_active_pointer_grab_checked(self, cursor_, time_, event_mask):
        cursor = cursor_.get_internal()
        time = time_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIH", cursor, time, event_mask))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 30, True, True), \
            ooxcb.VoidCookie())

    def change_active_pointer_grab(self, cursor_, time_, event_mask):
        cursor = cursor_.get_internal()
        time = time_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIH", cursor, time, event_mask))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 30, True, False), \
            ooxcb.VoidCookie())

    def grab_keyboard(self, owner_events, grab_window_, time_, pointer_mode, keyboard_mode):
        grab_window = grab_window_.get_internal()
        time = time_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIIBB", owner_events, grab_window, time, pointer_mode, keyboard_mode))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 31, False, True), \
            GrabKeyboardCookie(),
            GrabKeyboardReply)

    def grab_keyboard_unchecked(self, owner_events, grab_window_, time_, pointer_mode, keyboard_mode):
        grab_window = grab_window_.get_internal()
        time = time_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIIBB", owner_events, grab_window, time, pointer_mode, keyboard_mode))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 31, False, False), \
            GrabKeyboardCookie(),
            GrabKeyboardReply)

    def ungrab_keyboard_checked(self, time_):
        time = time_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", time))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 32, True, True), \
            ooxcb.VoidCookie())

    def ungrab_keyboard(self, time_):
        time = time_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", time))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 32, True, False), \
            ooxcb.VoidCookie())

    def grab_key_checked(self, owner_events, grab_window_, modifiers, key_, pointer_mode, keyboard_mode):
        grab_window = grab_window_.get_internal()
        key = key_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIHBBB", owner_events, grab_window, modifiers, key, pointer_mode, keyboard_mode))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 33, True, True), \
            ooxcb.VoidCookie())

    def grab_key(self, owner_events, grab_window_, modifiers, key_, pointer_mode, keyboard_mode):
        grab_window = grab_window_.get_internal()
        key = key_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIHBBB", owner_events, grab_window, modifiers, key, pointer_mode, keyboard_mode))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 33, True, False), \
            ooxcb.VoidCookie())

    def ungrab_key_checked(self, key_, grab_window_, modifiers):
        key = key_.get_internal()
        grab_window = grab_window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIH", key, grab_window, modifiers))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 34, True, True), \
            ooxcb.VoidCookie())

    def ungrab_key(self, key_, grab_window_, modifiers):
        key = key_.get_internal()
        grab_window = grab_window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIH", key, grab_window, modifiers))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 34, True, False), \
            ooxcb.VoidCookie())

    def allow_events_checked(self, mode, time_):
        time = time_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxI", mode, time))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 35, True, True), \
            ooxcb.VoidCookie())

    def allow_events(self, mode, time_):
        time = time_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxI", mode, time))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 35, True, False), \
            ooxcb.VoidCookie())

    def grab_server_checked(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 36, True, True), \
            ooxcb.VoidCookie())

    def grab_server(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 36, True, False), \
            ooxcb.VoidCookie())

    def ungrab_server_checked(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 37, True, True), \
            ooxcb.VoidCookie())

    def ungrab_server(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 37, True, False), \
            ooxcb.VoidCookie())

    def query_pointer(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 38, False, True), \
            QueryPointerCookie(),
            QueryPointerReply)

    def query_pointer_unchecked(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 38, False, False), \
            QueryPointerCookie(),
            QueryPointerReply)

    def get_motion_events(self, window_, start_, stop_):
        window = window_.get_internal()
        start = start_.get_internal()
        stop = stop_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIII", window, start, stop))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 39, False, True), \
            GetMotionEventsCookie(),
            GetMotionEventsReply)

    def get_motion_events_unchecked(self, window_, start_, stop_):
        window = window_.get_internal()
        start = start_.get_internal()
        stop = stop_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIII", window, start, stop))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 39, False, False), \
            GetMotionEventsCookie(),
            GetMotionEventsReply)

    def translate_coordinates(self, src_window_, dst_window_, src_x, src_y):
        src_window = src_window_.get_internal()
        dst_window = dst_window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIhh", src_window, dst_window, src_x, src_y))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 40, False, True), \
            TranslateCoordinatesCookie(),
            TranslateCoordinatesReply)

    def translate_coordinates_unchecked(self, src_window_, dst_window_, src_x, src_y):
        src_window = src_window_.get_internal()
        dst_window = dst_window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIhh", src_window, dst_window, src_x, src_y))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 40, False, False), \
            TranslateCoordinatesCookie(),
            TranslateCoordinatesReply)

    def warp_pointer_checked(self, src_window_, dst_window_, src_x, src_y, src_width, src_height, dst_x, dst_y):
        src_window = src_window_.get_internal()
        dst_window = dst_window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIhhHHhh", src_window, dst_window, src_x, src_y, src_width, src_height, dst_x, dst_y))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 41, True, True), \
            ooxcb.VoidCookie())

    def warp_pointer(self, src_window_, dst_window_, src_x, src_y, src_width, src_height, dst_x, dst_y):
        src_window = src_window_.get_internal()
        dst_window = dst_window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIhhHHhh", src_window, dst_window, src_x, src_y, src_width, src_height, dst_x, dst_y))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 41, True, False), \
            ooxcb.VoidCookie())

    def set_input_focus_checked(self, revert_to, focus_, time_):
        focus = focus_.get_internal()
        time = time_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxII", revert_to, focus, time))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 42, True, True), \
            ooxcb.VoidCookie())

    def set_input_focus(self, revert_to, focus_, time_):
        focus = focus_.get_internal()
        time = time_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxII", revert_to, focus, time))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 42, True, False), \
            ooxcb.VoidCookie())

    def get_input_focus(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 43, False, True), \
            GetInputFocusCookie(),
            GetInputFocusReply)

    def get_input_focus_unchecked(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 43, False, False), \
            GetInputFocusCookie(),
            GetInputFocusReply)

    def query_keymap(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 44, False, True), \
            QueryKeymapCookie(),
            QueryKeymapReply)

    def query_keymap_unchecked(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 44, False, False), \
            QueryKeymapCookie(),
            QueryKeymapReply)

    def open_font_checked(self, fid_, name_len, name):
        fid = fid_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIH", fid, name_len))
        buf.write(str(buffer(array("b", name))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 45, True, True), \
            ooxcb.VoidCookie())

    def open_font(self, fid_, name_len, name):
        fid = fid_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIH", fid, name_len))
        buf.write(str(buffer(array("b", name))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 45, True, False), \
            ooxcb.VoidCookie())

    def close_font_checked(self, font_):
        font = font_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", font))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 46, True, True), \
            ooxcb.VoidCookie())

    def close_font(self, font_):
        font = font_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", font))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 46, True, False), \
            ooxcb.VoidCookie())

    def query_font(self, font_):
        font = font_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", font))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 47, False, True), \
            QueryFontCookie(),
            QueryFontReply)

    def query_font_unchecked(self, font_):
        font = font_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", font))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 47, False, False), \
            QueryFontCookie(),
            QueryFontReply)

    def query_text_extents(self, font_, string_len, string_):
        font = font_.get_internal()
        string = string_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("x", ))
        buf.write(pack("B", (self.string_len & 1)))
        buf.write(pack("xxI", font))
        for elt in ooxcb.Iterator(string, 2, "string", True):
            buf.write(pack("BB", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 48, False, True), \
            QueryTextExtentsCookie(),
            QueryTextExtentsReply)

    def query_text_extents_unchecked(self, font_, string_len, string_):
        font = font_.get_internal()
        string = string_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("x", ))
        buf.write(pack("B", (self.string_len & 1)))
        buf.write(pack("xxI", font))
        for elt in ooxcb.Iterator(string, 2, "string", True):
            buf.write(pack("BB", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 48, False, False), \
            QueryTextExtentsCookie(),
            QueryTextExtentsReply)

    def list_fonts(self, max_names, pattern_len, pattern):
        buf = StringIO.StringIO()
        buf.write(pack("xxxxHH", max_names, pattern_len))
        buf.write(str(buffer(array("b", pattern))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 49, False, True), \
            ListFontsCookie(),
            ListFontsReply)

    def list_fonts_unchecked(self, max_names, pattern_len, pattern):
        buf = StringIO.StringIO()
        buf.write(pack("xxxxHH", max_names, pattern_len))
        buf.write(str(buffer(array("b", pattern))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 49, False, False), \
            ListFontsCookie(),
            ListFontsReply)

    def list_fonts_with_info(self, max_names, pattern_len, pattern):
        buf = StringIO.StringIO()
        buf.write(pack("xxxxHH", max_names, pattern_len))
        buf.write(str(buffer(array("b", pattern))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 50, False, True), \
            ListFontsWithInfoCookie(),
            ListFontsWithInfoReply)

    def list_fonts_with_info_unchecked(self, max_names, pattern_len, pattern):
        buf = StringIO.StringIO()
        buf.write(pack("xxxxHH", max_names, pattern_len))
        buf.write(str(buffer(array("b", pattern))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 50, False, False), \
            ListFontsWithInfoCookie(),
            ListFontsWithInfoReply)

    def set_font_path_checked(self, font_qty, path_len, path):
        buf = StringIO.StringIO()
        buf.write(pack("xxxxH", font_qty))
        buf.write(str(buffer(array("b", path))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 51, True, True), \
            ooxcb.VoidCookie())

    def set_font_path(self, font_qty, path_len, path):
        buf = StringIO.StringIO()
        buf.write(pack("xxxxH", font_qty))
        buf.write(str(buffer(array("b", path))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 51, True, False), \
            ooxcb.VoidCookie())

    def get_font_path(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 52, False, True), \
            GetFontPathCookie(),
            GetFontPathReply)

    def get_font_path_unchecked(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 52, False, False), \
            GetFontPathCookie(),
            GetFontPathReply)

    def create_pixmap_checked(self, depth, pid_, drawable_, width, height):
        pid = pid_.get_internal()
        drawable = drawable_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIIHH", depth, pid, drawable, width, height))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 53, True, True), \
            ooxcb.VoidCookie())

    def create_pixmap(self, depth, pid_, drawable_, width, height):
        pid = pid_.get_internal()
        drawable = drawable_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIIHH", depth, pid, drawable, width, height))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 53, True, False), \
            ooxcb.VoidCookie())

    def free_pixmap_checked(self, pixmap_):
        pixmap = pixmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", pixmap))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 54, True, True), \
            ooxcb.VoidCookie())

    def free_pixmap(self, pixmap_):
        pixmap = pixmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", pixmap))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 54, True, False), \
            ooxcb.VoidCookie())

    def create_g_c_checked(self, cid_, drawable_, value_mask, value_list):
        cid = cid_.get_internal()
        drawable = drawable_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIII", cid, drawable, value_mask))
        buf.write(str(buffer(array("I", value_list))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 55, True, True), \
            ooxcb.VoidCookie())

    def create_g_c(self, cid_, drawable_, value_mask, value_list):
        cid = cid_.get_internal()
        drawable = drawable_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIII", cid, drawable, value_mask))
        buf.write(str(buffer(array("I", value_list))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 55, True, False), \
            ooxcb.VoidCookie())

    def change_g_c_checked(self, gc_, value_mask, value_list):
        gc = gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", gc, value_mask))
        buf.write(str(buffer(array("I", value_list))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 56, True, True), \
            ooxcb.VoidCookie())

    def change_g_c(self, gc_, value_mask, value_list):
        gc = gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", gc, value_mask))
        buf.write(str(buffer(array("I", value_list))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 56, True, False), \
            ooxcb.VoidCookie())

    def copy_g_c_checked(self, src_gc_, dst_gc_, value_mask):
        src_gc = src_gc_.get_internal()
        dst_gc = dst_gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIII", src_gc, dst_gc, value_mask))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 57, True, True), \
            ooxcb.VoidCookie())

    def copy_g_c(self, src_gc_, dst_gc_, value_mask):
        src_gc = src_gc_.get_internal()
        dst_gc = dst_gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIII", src_gc, dst_gc, value_mask))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 57, True, False), \
            ooxcb.VoidCookie())

    def set_dashes_checked(self, gc_, dash_offset, dashes_len, dashes):
        gc = gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIHH", gc, dash_offset, dashes_len))
        buf.write(str(buffer(array("B", dashes))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 58, True, True), \
            ooxcb.VoidCookie())

    def set_dashes(self, gc_, dash_offset, dashes_len, dashes):
        gc = gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIHH", gc, dash_offset, dashes_len))
        buf.write(str(buffer(array("B", dashes))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 58, True, False), \
            ooxcb.VoidCookie())

    def set_clip_rectangles_checked(self, ordering, gc_, clip_x_origin, clip_y_origin, rectangles_len, rectangles_):
        gc = gc_.get_internal()
        rectangles = rectangles_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIhh", ordering, gc, clip_x_origin, clip_y_origin))
        for elt in ooxcb.Iterator(rectangles, 4, "rectangles", True):
            buf.write(pack("hhHH", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 59, True, True), \
            ooxcb.VoidCookie())

    def set_clip_rectangles(self, ordering, gc_, clip_x_origin, clip_y_origin, rectangles_len, rectangles_):
        gc = gc_.get_internal()
        rectangles = rectangles_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIhh", ordering, gc, clip_x_origin, clip_y_origin))
        for elt in ooxcb.Iterator(rectangles, 4, "rectangles", True):
            buf.write(pack("hhHH", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 59, True, False), \
            ooxcb.VoidCookie())

    def free_g_c_checked(self, gc_):
        gc = gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", gc))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 60, True, True), \
            ooxcb.VoidCookie())

    def free_g_c(self, gc_):
        gc = gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", gc))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 60, True, False), \
            ooxcb.VoidCookie())

    def clear_area_checked(self, exposures, window_, x, y, width, height):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIhhHH", exposures, window, x, y, width, height))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 61, True, True), \
            ooxcb.VoidCookie())

    def clear_area(self, exposures, window_, x, y, width, height):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIhhHH", exposures, window, x, y, width, height))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 61, True, False), \
            ooxcb.VoidCookie())

    def copy_area_checked(self, src_drawable_, dst_drawable_, gc_, src_x, src_y, dst_x, dst_y, width, height):
        src_drawable = src_drawable_.get_internal()
        dst_drawable = dst_drawable_.get_internal()
        gc = gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIIhhhhHH", src_drawable, dst_drawable, gc, src_x, src_y, dst_x, dst_y, width, height))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 62, True, True), \
            ooxcb.VoidCookie())

    def copy_area(self, src_drawable_, dst_drawable_, gc_, src_x, src_y, dst_x, dst_y, width, height):
        src_drawable = src_drawable_.get_internal()
        dst_drawable = dst_drawable_.get_internal()
        gc = gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIIhhhhHH", src_drawable, dst_drawable, gc, src_x, src_y, dst_x, dst_y, width, height))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 62, True, False), \
            ooxcb.VoidCookie())

    def copy_plane_checked(self, src_drawable_, dst_drawable_, gc_, src_x, src_y, dst_x, dst_y, width, height, bit_plane):
        src_drawable = src_drawable_.get_internal()
        dst_drawable = dst_drawable_.get_internal()
        gc = gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIIhhhhHHI", src_drawable, dst_drawable, gc, src_x, src_y, dst_x, dst_y, width, height, bit_plane))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 63, True, True), \
            ooxcb.VoidCookie())

    def copy_plane(self, src_drawable_, dst_drawable_, gc_, src_x, src_y, dst_x, dst_y, width, height, bit_plane):
        src_drawable = src_drawable_.get_internal()
        dst_drawable = dst_drawable_.get_internal()
        gc = gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIIhhhhHHI", src_drawable, dst_drawable, gc, src_x, src_y, dst_x, dst_y, width, height, bit_plane))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 63, True, False), \
            ooxcb.VoidCookie())

    def poly_point_checked(self, coordinate_mode, drawable_, gc_, points_len, points_):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        points = points_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxII", coordinate_mode, drawable, gc))
        for elt in ooxcb.Iterator(points, 2, "points", True):
            buf.write(pack("hh", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 64, True, True), \
            ooxcb.VoidCookie())

    def poly_point(self, coordinate_mode, drawable_, gc_, points_len, points_):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        points = points_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxII", coordinate_mode, drawable, gc))
        for elt in ooxcb.Iterator(points, 2, "points", True):
            buf.write(pack("hh", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 64, True, False), \
            ooxcb.VoidCookie())

    def poly_line_checked(self, coordinate_mode, drawable_, gc_, points_len, points_):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        points = points_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxII", coordinate_mode, drawable, gc))
        for elt in ooxcb.Iterator(points, 2, "points", True):
            buf.write(pack("hh", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 65, True, True), \
            ooxcb.VoidCookie())

    def poly_line(self, coordinate_mode, drawable_, gc_, points_len, points_):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        points = points_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxII", coordinate_mode, drawable, gc))
        for elt in ooxcb.Iterator(points, 2, "points", True):
            buf.write(pack("hh", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 65, True, False), \
            ooxcb.VoidCookie())

    def poly_segment_checked(self, drawable_, gc_, segments_len, segments_):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        segments = segments_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", drawable, gc))
        for elt in ooxcb.Iterator(segments, 4, "segments", True):
            buf.write(pack("hhhh", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 66, True, True), \
            ooxcb.VoidCookie())

    def poly_segment(self, drawable_, gc_, segments_len, segments_):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        segments = segments_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", drawable, gc))
        for elt in ooxcb.Iterator(segments, 4, "segments", True):
            buf.write(pack("hhhh", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 66, True, False), \
            ooxcb.VoidCookie())

    def poly_rectangle_checked(self, drawable_, gc_, rectangles_len, rectangles_):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        rectangles = rectangles_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", drawable, gc))
        for elt in ooxcb.Iterator(rectangles, 4, "rectangles", True):
            buf.write(pack("hhHH", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 67, True, True), \
            ooxcb.VoidCookie())

    def poly_rectangle(self, drawable_, gc_, rectangles_len, rectangles_):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        rectangles = rectangles_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", drawable, gc))
        for elt in ooxcb.Iterator(rectangles, 4, "rectangles", True):
            buf.write(pack("hhHH", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 67, True, False), \
            ooxcb.VoidCookie())

    def poly_arc_checked(self, drawable_, gc_, arcs_len, arcs_):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        arcs = arcs_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", drawable, gc))
        for elt in ooxcb.Iterator(arcs, 6, "arcs", True):
            buf.write(pack("hhHHhh", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 68, True, True), \
            ooxcb.VoidCookie())

    def poly_arc(self, drawable_, gc_, arcs_len, arcs_):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        arcs = arcs_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", drawable, gc))
        for elt in ooxcb.Iterator(arcs, 6, "arcs", True):
            buf.write(pack("hhHHhh", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 68, True, False), \
            ooxcb.VoidCookie())

    def fill_poly_checked(self, drawable_, gc_, shape, coordinate_mode, points_len, points_):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        points = points_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIBB", drawable, gc, shape, coordinate_mode))
        for elt in ooxcb.Iterator(points, 2, "points", True):
            buf.write(pack("hh", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 69, True, True), \
            ooxcb.VoidCookie())

    def fill_poly(self, drawable_, gc_, shape, coordinate_mode, points_len, points_):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        points = points_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIBB", drawable, gc, shape, coordinate_mode))
        for elt in ooxcb.Iterator(points, 2, "points", True):
            buf.write(pack("hh", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 69, True, False), \
            ooxcb.VoidCookie())

    def poly_fill_rectangle_checked(self, drawable_, gc_, rectangles_len, rectangles_):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        rectangles = rectangles_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", drawable, gc))
        for elt in ooxcb.Iterator(rectangles, 4, "rectangles", True):
            buf.write(pack("hhHH", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 70, True, True), \
            ooxcb.VoidCookie())

    def poly_fill_rectangle(self, drawable_, gc_, rectangles_len, rectangles_):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        rectangles = rectangles_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", drawable, gc))
        for elt in ooxcb.Iterator(rectangles, 4, "rectangles", True):
            buf.write(pack("hhHH", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 70, True, False), \
            ooxcb.VoidCookie())

    def poly_fill_arc_checked(self, drawable_, gc_, arcs_len, arcs_):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        arcs = arcs_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", drawable, gc))
        for elt in ooxcb.Iterator(arcs, 6, "arcs", True):
            buf.write(pack("hhHHhh", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 71, True, True), \
            ooxcb.VoidCookie())

    def poly_fill_arc(self, drawable_, gc_, arcs_len, arcs_):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        arcs = arcs_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", drawable, gc))
        for elt in ooxcb.Iterator(arcs, 6, "arcs", True):
            buf.write(pack("hhHHhh", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 71, True, False), \
            ooxcb.VoidCookie())

    def put_image_checked(self, format, drawable_, gc_, width, height, dst_x, dst_y, left_pad, depth, data_len, data):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIIHHhhBB", format, drawable, gc, width, height, dst_x, dst_y, left_pad, depth))
        buf.write(str(buffer(array("B", data))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 72, True, True), \
            ooxcb.VoidCookie())

    def put_image(self, format, drawable_, gc_, width, height, dst_x, dst_y, left_pad, depth, data_len, data):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIIHHhhBB", format, drawable, gc, width, height, dst_x, dst_y, left_pad, depth))
        buf.write(str(buffer(array("B", data))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 72, True, False), \
            ooxcb.VoidCookie())

    def get_image(self, format, drawable_, x, y, width, height, plane_mask):
        drawable = drawable_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIhhHHI", format, drawable, x, y, width, height, plane_mask))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 73, False, True), \
            GetImageCookie(),
            GetImageReply)

    def get_image_unchecked(self, format, drawable_, x, y, width, height, plane_mask):
        drawable = drawable_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIhhHHI", format, drawable, x, y, width, height, plane_mask))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 73, False, False), \
            GetImageCookie(),
            GetImageReply)

    def poly_text8_checked(self, drawable_, gc_, x, y, items_len, items):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIhh", drawable, gc, x, y))
        buf.write(str(buffer(array("B", items))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 74, True, True), \
            ooxcb.VoidCookie())

    def poly_text8(self, drawable_, gc_, x, y, items_len, items):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIhh", drawable, gc, x, y))
        buf.write(str(buffer(array("B", items))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 74, True, False), \
            ooxcb.VoidCookie())

    def poly_text16_checked(self, drawable_, gc_, x, y, items_len, items):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIhh", drawable, gc, x, y))
        buf.write(str(buffer(array("B", items))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 75, True, True), \
            ooxcb.VoidCookie())

    def poly_text16(self, drawable_, gc_, x, y, items_len, items):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIhh", drawable, gc, x, y))
        buf.write(str(buffer(array("B", items))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 75, True, False), \
            ooxcb.VoidCookie())

    def image_text8_checked(self, string_len, drawable_, gc_, x, y, string):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIIhh", string_len, drawable, gc, x, y))
        buf.write(str(buffer(array("b", string))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 76, True, True), \
            ooxcb.VoidCookie())

    def image_text8(self, string_len, drawable_, gc_, x, y, string):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIIhh", string_len, drawable, gc, x, y))
        buf.write(str(buffer(array("b", string))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 76, True, False), \
            ooxcb.VoidCookie())

    def image_text16_checked(self, string_len, drawable_, gc_, x, y, string_):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        string = string_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIIhh", string_len, drawable, gc, x, y))
        for elt in ooxcb.Iterator(string, 2, "string", True):
            buf.write(pack("BB", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 77, True, True), \
            ooxcb.VoidCookie())

    def image_text16(self, string_len, drawable_, gc_, x, y, string_):
        drawable = drawable_.get_internal()
        gc = gc_.get_internal()
        string = string_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIIhh", string_len, drawable, gc, x, y))
        for elt in ooxcb.Iterator(string, 2, "string", True):
            buf.write(pack("BB", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 77, True, False), \
            ooxcb.VoidCookie())

    def create_colormap_checked(self, alloc, mid_, window_, visual_):
        mid = mid_.get_internal()
        window = window_.get_internal()
        visual = visual_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIII", alloc, mid, window, visual))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 78, True, True), \
            ooxcb.VoidCookie())

    def create_colormap(self, alloc, mid_, window_, visual_):
        mid = mid_.get_internal()
        window = window_.get_internal()
        visual = visual_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIII", alloc, mid, window, visual))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 78, True, False), \
            ooxcb.VoidCookie())

    def free_colormap_checked(self, cmap_):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", cmap))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 79, True, True), \
            ooxcb.VoidCookie())

    def free_colormap(self, cmap_):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", cmap))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 79, True, False), \
            ooxcb.VoidCookie())

    def copy_colormap_and_free_checked(self, mid_, src_cmap_):
        mid = mid_.get_internal()
        src_cmap = src_cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", mid, src_cmap))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 80, True, True), \
            ooxcb.VoidCookie())

    def copy_colormap_and_free(self, mid_, src_cmap_):
        mid = mid_.get_internal()
        src_cmap = src_cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", mid, src_cmap))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 80, True, False), \
            ooxcb.VoidCookie())

    def install_colormap_checked(self, cmap_):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", cmap))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 81, True, True), \
            ooxcb.VoidCookie())

    def install_colormap(self, cmap_):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", cmap))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 81, True, False), \
            ooxcb.VoidCookie())

    def uninstall_colormap_checked(self, cmap_):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", cmap))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 82, True, True), \
            ooxcb.VoidCookie())

    def uninstall_colormap(self, cmap_):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", cmap))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 82, True, False), \
            ooxcb.VoidCookie())

    def list_installed_colormaps(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 83, False, True), \
            ListInstalledColormapsCookie(),
            ListInstalledColormapsReply)

    def list_installed_colormaps_unchecked(self, window_):
        window = window_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 83, False, False), \
            ListInstalledColormapsCookie(),
            ListInstalledColormapsReply)

    def alloc_color(self, cmap_, red, green, blue):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIHHH", cmap, red, green, blue))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 84, False, True), \
            AllocColorCookie(),
            AllocColorReply)

    def alloc_color_unchecked(self, cmap_, red, green, blue):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIHHH", cmap, red, green, blue))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 84, False, False), \
            AllocColorCookie(),
            AllocColorReply)

    def alloc_named_color(self, cmap_, name_len, name):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIH", cmap, name_len))
        buf.write(str(buffer(array("b", name))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 85, False, True), \
            AllocNamedColorCookie(),
            AllocNamedColorReply)

    def alloc_named_color_unchecked(self, cmap_, name_len, name):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIH", cmap, name_len))
        buf.write(str(buffer(array("b", name))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 85, False, False), \
            AllocNamedColorCookie(),
            AllocNamedColorReply)

    def alloc_color_cells(self, contiguous, cmap_, colors, planes):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIHH", contiguous, cmap, colors, planes))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 86, False, True), \
            AllocColorCellsCookie(),
            AllocColorCellsReply)

    def alloc_color_cells_unchecked(self, contiguous, cmap_, colors, planes):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIHH", contiguous, cmap, colors, planes))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 86, False, False), \
            AllocColorCellsCookie(),
            AllocColorCellsReply)

    def alloc_color_planes(self, contiguous, cmap_, colors, reds, greens, blues):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIHHHH", contiguous, cmap, colors, reds, greens, blues))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 87, False, True), \
            AllocColorPlanesCookie(),
            AllocColorPlanesReply)

    def alloc_color_planes_unchecked(self, contiguous, cmap_, colors, reds, greens, blues):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIHHHH", contiguous, cmap, colors, reds, greens, blues))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 87, False, False), \
            AllocColorPlanesCookie(),
            AllocColorPlanesReply)

    def free_colors_checked(self, cmap_, plane_mask, pixels_len, pixels):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", cmap, plane_mask))
        buf.write(str(buffer(array("I", pixels))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 88, True, True), \
            ooxcb.VoidCookie())

    def free_colors(self, cmap_, plane_mask, pixels_len, pixels):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxII", cmap, plane_mask))
        buf.write(str(buffer(array("I", pixels))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 88, True, False), \
            ooxcb.VoidCookie())

    def store_colors_checked(self, cmap_, items_len, items_):
        cmap = cmap_.get_internal()
        items = items_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", cmap))
        for elt in ooxcb.Iterator(items, 5, "items", True):
            buf.write(pack("IHHHBx", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 89, True, True), \
            ooxcb.VoidCookie())

    def store_colors(self, cmap_, items_len, items_):
        cmap = cmap_.get_internal()
        items = items_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", cmap))
        for elt in ooxcb.Iterator(items, 5, "items", True):
            buf.write(pack("IHHHBx", *elt))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 89, True, False), \
            ooxcb.VoidCookie())

    def store_named_color_checked(self, flags, cmap_, pixel, name_len, name):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIIH", flags, cmap, pixel, name_len))
        buf.write(str(buffer(array("b", name))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 90, True, True), \
            ooxcb.VoidCookie())

    def store_named_color(self, flags, cmap_, pixel, name_len, name):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIIH", flags, cmap, pixel, name_len))
        buf.write(str(buffer(array("b", name))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 90, True, False), \
            ooxcb.VoidCookie())

    def query_colors(self, cmap_, pixels_len, pixels):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", cmap))
        buf.write(str(buffer(array("I", pixels))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 91, False, True), \
            QueryColorsCookie(),
            QueryColorsReply)

    def query_colors_unchecked(self, cmap_, pixels_len, pixels):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", cmap))
        buf.write(str(buffer(array("I", pixels))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 91, False, False), \
            QueryColorsCookie(),
            QueryColorsReply)

    def lookup_color(self, cmap_, name_len, name):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIH", cmap, name_len))
        buf.write(str(buffer(array("b", name))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 92, False, True), \
            LookupColorCookie(),
            LookupColorReply)

    def lookup_color_unchecked(self, cmap_, name_len, name):
        cmap = cmap_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIH", cmap, name_len))
        buf.write(str(buffer(array("b", name))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 92, False, False), \
            LookupColorCookie(),
            LookupColorReply)

    def create_cursor_checked(self, cid_, source_, mask_, fore_red, fore_green, fore_blue, back_red, back_green, back_blue, x, y):
        cid = cid_.get_internal()
        source = source_.get_internal()
        mask = mask_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIIHHHHHHHH", cid, source, mask, fore_red, fore_green, fore_blue, back_red, back_green, back_blue, x, y))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 93, True, True), \
            ooxcb.VoidCookie())

    def create_cursor(self, cid_, source_, mask_, fore_red, fore_green, fore_blue, back_red, back_green, back_blue, x, y):
        cid = cid_.get_internal()
        source = source_.get_internal()
        mask = mask_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIIHHHHHHHH", cid, source, mask, fore_red, fore_green, fore_blue, back_red, back_green, back_blue, x, y))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 93, True, False), \
            ooxcb.VoidCookie())

    def create_glyph_cursor_checked(self, cid_, source_font_, mask_font_, source_char, mask_char, fore_red, fore_green, fore_blue, back_red, back_green, back_blue):
        cid = cid_.get_internal()
        source_font = source_font_.get_internal()
        mask_font = mask_font_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIIHHHHHHHH", cid, source_font, mask_font, source_char, mask_char, fore_red, fore_green, fore_blue, back_red, back_green, back_blue))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 94, True, True), \
            ooxcb.VoidCookie())

    def create_glyph_cursor(self, cid_, source_font_, mask_font_, source_char, mask_char, fore_red, fore_green, fore_blue, back_red, back_green, back_blue):
        cid = cid_.get_internal()
        source_font = source_font_.get_internal()
        mask_font = mask_font_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIIIHHHHHHHH", cid, source_font, mask_font, source_char, mask_char, fore_red, fore_green, fore_blue, back_red, back_green, back_blue))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 94, True, False), \
            ooxcb.VoidCookie())

    def free_cursor_checked(self, cursor_):
        cursor = cursor_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", cursor))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 95, True, True), \
            ooxcb.VoidCookie())

    def free_cursor(self, cursor_):
        cursor = cursor_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", cursor))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 95, True, False), \
            ooxcb.VoidCookie())

    def recolor_cursor_checked(self, cursor_, fore_red, fore_green, fore_blue, back_red, back_green, back_blue):
        cursor = cursor_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIHHHHHH", cursor, fore_red, fore_green, fore_blue, back_red, back_green, back_blue))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 96, True, True), \
            ooxcb.VoidCookie())

    def recolor_cursor(self, cursor_, fore_red, fore_green, fore_blue, back_red, back_green, back_blue):
        cursor = cursor_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxIHHHHHH", cursor, fore_red, fore_green, fore_blue, back_red, back_green, back_blue))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 96, True, False), \
            ooxcb.VoidCookie())

    def query_best_size(self, _class, drawable_, width, height):
        drawable = drawable_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIHH", _class, drawable, width, height))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 97, False, True), \
            QueryBestSizeCookie(),
            QueryBestSizeReply)

    def query_best_size_unchecked(self, _class, drawable_, width, height):
        drawable = drawable_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIHH", _class, drawable, width, height))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 97, False, False), \
            QueryBestSizeCookie(),
            QueryBestSizeReply)

    def query_extension(self, name_len, name):
        buf = StringIO.StringIO()
        buf.write(pack("xxxxH", name_len))
        buf.write(str(buffer(array("b", name))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 98, False, True), \
            QueryExtensionCookie(),
            QueryExtensionReply)

    def query_extension_unchecked(self, name_len, name):
        buf = StringIO.StringIO()
        buf.write(pack("xxxxH", name_len))
        buf.write(str(buffer(array("b", name))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 98, False, False), \
            QueryExtensionCookie(),
            QueryExtensionReply)

    def list_extensions(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 99, False, True), \
            ListExtensionsCookie(),
            ListExtensionsReply)

    def list_extensions_unchecked(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 99, False, False), \
            ListExtensionsCookie(),
            ListExtensionsReply)

    def change_keyboard_mapping_checked(self, keycode_count, first_keycode_, keysyms_per_keycode, keysyms_):
        first_keycode = first_keycode_.get_internal()
        keysyms = keysyms_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxBB", keycode_count, first_keycode, keysyms_per_keycode))
        buf.write(str(buffer(array("I", keysyms))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 100, True, True), \
            ooxcb.VoidCookie())

    def change_keyboard_mapping(self, keycode_count, first_keycode_, keysyms_per_keycode, keysyms_):
        first_keycode = first_keycode_.get_internal()
        keysyms = keysyms_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxBB", keycode_count, first_keycode, keysyms_per_keycode))
        buf.write(str(buffer(array("I", keysyms))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 100, True, False), \
            ooxcb.VoidCookie())

    def get_keyboard_mapping(self, first_keycode_, count):
        first_keycode = first_keycode_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxBB", first_keycode, count))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 101, False, True), \
            GetKeyboardMappingCookie(),
            GetKeyboardMappingReply)

    def get_keyboard_mapping_unchecked(self, first_keycode_, count):
        first_keycode = first_keycode_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxBB", first_keycode, count))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 101, False, False), \
            GetKeyboardMappingCookie(),
            GetKeyboardMappingReply)

    def change_keyboard_control_checked(self, value_mask, value_list):
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", value_mask))
        buf.write(str(buffer(array("I", value_list))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 102, True, True), \
            ooxcb.VoidCookie())

    def change_keyboard_control(self, value_mask, value_list):
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", value_mask))
        buf.write(str(buffer(array("I", value_list))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 102, True, False), \
            ooxcb.VoidCookie())

    def get_keyboard_control(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 103, False, True), \
            GetKeyboardControlCookie(),
            GetKeyboardControlReply)

    def get_keyboard_control_unchecked(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 103, False, False), \
            GetKeyboardControlCookie(),
            GetKeyboardControlReply)

    def bell_checked(self, percent):
        buf = StringIO.StringIO()
        buf.write(pack("xbxx", percent))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 104, True, True), \
            ooxcb.VoidCookie())

    def bell(self, percent):
        buf = StringIO.StringIO()
        buf.write(pack("xbxx", percent))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 104, True, False), \
            ooxcb.VoidCookie())

    def change_pointer_control_checked(self, acceleration_numerator, acceleration_denominator, threshold, do_acceleration, do_threshold):
        buf = StringIO.StringIO()
        buf.write(pack("xxxxhhhBB", acceleration_numerator, acceleration_denominator, threshold, do_acceleration, do_threshold))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 105, True, True), \
            ooxcb.VoidCookie())

    def change_pointer_control(self, acceleration_numerator, acceleration_denominator, threshold, do_acceleration, do_threshold):
        buf = StringIO.StringIO()
        buf.write(pack("xxxxhhhBB", acceleration_numerator, acceleration_denominator, threshold, do_acceleration, do_threshold))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 105, True, False), \
            ooxcb.VoidCookie())

    def get_pointer_control(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 106, False, True), \
            GetPointerControlCookie(),
            GetPointerControlReply)

    def get_pointer_control_unchecked(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 106, False, False), \
            GetPointerControlCookie(),
            GetPointerControlReply)

    def set_screen_saver_checked(self, timeout, interval, prefer_blanking, allow_exposures):
        buf = StringIO.StringIO()
        buf.write(pack("xxxxhhBB", timeout, interval, prefer_blanking, allow_exposures))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 107, True, True), \
            ooxcb.VoidCookie())

    def set_screen_saver(self, timeout, interval, prefer_blanking, allow_exposures):
        buf = StringIO.StringIO()
        buf.write(pack("xxxxhhBB", timeout, interval, prefer_blanking, allow_exposures))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 107, True, False), \
            ooxcb.VoidCookie())

    def get_screen_saver(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 108, False, True), \
            GetScreenSaverCookie(),
            GetScreenSaverReply)

    def get_screen_saver_unchecked(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 108, False, False), \
            GetScreenSaverCookie(),
            GetScreenSaverReply)

    def change_hosts_checked(self, mode, family, address_len, address):
        buf = StringIO.StringIO()
        buf.write(pack("xBxxBxH", mode, family, address_len))
        buf.write(str(buffer(array("b", address))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 109, True, True), \
            ooxcb.VoidCookie())

    def change_hosts(self, mode, family, address_len, address):
        buf = StringIO.StringIO()
        buf.write(pack("xBxxBxH", mode, family, address_len))
        buf.write(str(buffer(array("b", address))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 109, True, False), \
            ooxcb.VoidCookie())

    def list_hosts(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 110, False, True), \
            ListHostsCookie(),
            ListHostsReply)

    def list_hosts_unchecked(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 110, False, False), \
            ListHostsCookie(),
            ListHostsReply)

    def set_access_control_checked(self, mode):
        buf = StringIO.StringIO()
        buf.write(pack("xBxx", mode))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 111, True, True), \
            ooxcb.VoidCookie())

    def set_access_control(self, mode):
        buf = StringIO.StringIO()
        buf.write(pack("xBxx", mode))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 111, True, False), \
            ooxcb.VoidCookie())

    def set_close_down_mode_checked(self, mode):
        buf = StringIO.StringIO()
        buf.write(pack("xBxx", mode))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 112, True, True), \
            ooxcb.VoidCookie())

    def set_close_down_mode(self, mode):
        buf = StringIO.StringIO()
        buf.write(pack("xBxx", mode))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 112, True, False), \
            ooxcb.VoidCookie())

    def kill_client_checked(self, resource):
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", resource))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 113, True, True), \
            ooxcb.VoidCookie())

    def kill_client(self, resource):
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", resource))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 113, True, False), \
            ooxcb.VoidCookie())

    def rotate_properties_checked(self, window_, atoms_len, delta, atoms_):
        window = window_.get_internal()
        atoms = atoms_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xIxxHh", window, atoms_len, delta))
        buf.write(str(buffer(array("I", atoms))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 114, True, True), \
            ooxcb.VoidCookie())

    def rotate_properties(self, window_, atoms_len, delta, atoms_):
        window = window_.get_internal()
        atoms = atoms_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xIxxHh", window, atoms_len, delta))
        buf.write(str(buffer(array("I", atoms))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 114, True, False), \
            ooxcb.VoidCookie())

    def force_screen_saver_checked(self, mode):
        buf = StringIO.StringIO()
        buf.write(pack("xBxx", mode))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 115, True, True), \
            ooxcb.VoidCookie())

    def force_screen_saver(self, mode):
        buf = StringIO.StringIO()
        buf.write(pack("xBxx", mode))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 115, True, False), \
            ooxcb.VoidCookie())

    def set_pointer_mapping(self, map_len, map):
        buf = StringIO.StringIO()
        buf.write(pack("xBxx", map_len))
        buf.write(str(buffer(array("B", map))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 116, False, True), \
            SetPointerMappingCookie(),
            SetPointerMappingReply)

    def set_pointer_mapping_unchecked(self, map_len, map):
        buf = StringIO.StringIO()
        buf.write(pack("xBxx", map_len))
        buf.write(str(buffer(array("B", map))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 116, False, False), \
            SetPointerMappingCookie(),
            SetPointerMappingReply)

    def get_pointer_mapping(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 117, False, True), \
            GetPointerMappingCookie(),
            GetPointerMappingReply)

    def get_pointer_mapping_unchecked(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 117, False, False), \
            GetPointerMappingCookie(),
            GetPointerMappingReply)

    def set_modifier_mapping(self, keycodes_per_modifier, keycodes_):
        keycodes = keycodes_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxx", keycodes_per_modifier))
        buf.write(str(buffer(array("B", keycodes))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 118, False, True), \
            SetModifierMappingCookie(),
            SetModifierMappingReply)

    def set_modifier_mapping_unchecked(self, keycodes_per_modifier, keycodes_):
        keycodes = keycodes_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxx", keycodes_per_modifier))
        buf.write(str(buffer(array("B", keycodes))))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 118, False, False), \
            SetModifierMappingCookie(),
            SetModifierMappingReply)

    def get_modifier_mapping(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 119, False, True), \
            GetModifierMappingCookie(),
            GetModifierMappingReply)

    def get_modifier_mapping_unchecked(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 119, False, False), \
            GetModifierMappingCookie(),
            GetModifierMappingReply)

    def no_operation_checked(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 127, True, True), \
            ooxcb.VoidCookie())

    def no_operation(self):
        buf = StringIO.StringIO()
        buf.write(pack("xxxx", ))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 127, True, False), \
            ooxcb.VoidCookie())

class LedMode(object):
    Off = 0
    On = 1

class KeymapNotifyEvent(ooxcb.Event):
    event_name = "on_keymap_notify"
    event_target_class = ooxcb.Connection
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        count += 1
        self.keys = ooxcb.List(conn, self, count, 31, 'B', 1)
        self.event_target = self.conn

class BadIDChoice(ooxcb.ProtocolException):
    pass

class GetKeyboardMappingCookie(object):
    pass

class SubwindowMode(object):
    ClipByChildren = 0
    IncludeInferiors = 1

class Circulate(object):
    RaiseLowest = 0
    LowerHighest = 1

class Keycode(ooxcb.Resource):
    def __init__(self, conn, xid):
        ooxcb.Resource.__init__(self, conn, xid)

class BackingStore(object):
    NotUseful = 0
    WhenMapped = 1
    Always = 2

class StackMode(object):
    Above = 0
    Below = 1
    TopIf = 2
    BottomIf = 3
    Opposite = 4

class AllocColorPlanesCookie(object):
    pass

class BadMatch(ooxcb.ProtocolException):
    pass

class Visualtype(ooxcb.Struct):
    def __init__(self, conn, parent, offset, size):
        ooxcb.Struct.__init__(self, conn, parent, offset, size)
        count = 0
        _unpacked = unpack_ex("IBBHIIIxxxx", self, count)
        self.visual_id = VisualID(conn, _unpacked[0])
        self._class = _unpacked[1]
        self.bits_per_rgb_value = _unpacked[2]
        self.colormap_entries = _unpacked[3]
        self.red_mask = _unpacked[4]
        self.green_mask = _unpacked[5]
        self.blue_mask = _unpacked[6]
        ooxcb._resize_obj(self, count)

class ArcMode(object):
    Chord = 0
    PieSlice = 1

class BackPixmap(object):
    _None = 0
    ParentRelative = 1

class BadFont(ooxcb.ProtocolException):
    pass

class Cursor(ooxcb.Resource):
    def __init__(self, conn, xid):
        ooxcb.Resource.__init__(self, conn, xid)

class Place(object):
    OnTop = 0
    OnBottom = 1

class AutoRepeatMode(object):
    Off = 0
    On = 1
    Default = 2

class GrabPointerCookie(object):
    pass

class BadValue(ooxcb.ProtocolException):
    pass

class GetInputFocusCookie(object):
    pass

class Grab(object):
    Any = 0

class Property(object):
    NewValue = 0
    Delete = 1

class DrawableError(ooxcb.Error):
    def __init__(self, conn, parent):
        ooxcb.Error.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHB", self, count)
        self.bad_value = _unpacked[0]
        self.minor_opcode = _unpacked[1]
        self.major_opcode = _unpacked[2]

class AllocColorCellsCookie(object):
    pass

class MappingStatus(object):
    Success = 0
    Busy = 1
    Failure = 2

class SetPointerMappingCookie(object):
    pass

class SelectionNotifyEvent(ooxcb.Event):
    event_name = "on_selection_notify"
    event_target_class = ooxcb.Connection
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIIIII", self, count)
        self.time = Timestamp(conn, _unpacked[0])
        self.requestor = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.selection = Atom(conn, _unpacked[2])
        self.target = Atom(conn, _unpacked[3])
        self.property = Atom(conn, _unpacked[4])
        self.event_target = self.conn

class BadColormap(ooxcb.ProtocolException):
    pass

class NoExposureEvent(ooxcb.Event):
    event_name = "on_no_exposure"
    event_target_class = ooxcb.Connection
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHB", self, count)
        self.drawable = conn.get_from_cache_fallback(_unpacked[0], Drawable)
        self.minor_opcode = _unpacked[1]
        self.major_opcode = _unpacked[2]
        self.event_target = self.conn

class BadPixmap(ooxcb.ProtocolException):
    pass

class ColormapState(object):
    Uninstalled = 0
    Installed = 1

class ListPropertiesCookie(object):
    pass

class Gcontext(ooxcb.Resource):
    def __init__(self, conn, xid):
        ooxcb.Resource.__init__(self, conn, xid)

class ColorFlag(object):
    Red = (1 << 0)
    Green = (1 << 1)
    Blue = (1 << 2)

class BadGContext(ooxcb.ProtocolException):
    pass

class GetGeometryCookie(object):
    pass

class BadDrawable(ooxcb.ProtocolException):
    pass

class Allow(object):
    AsyncPointer = 0
    SyncPointer = 1
    ReplayPointer = 2
    AsyncKeyboard = 3
    SyncKeyboard = 4
    ReplayKeyboard = 5
    AsyncBoth = 6
    SyncBoth = 7

class AllocNamedColorReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxxxxxIHHHHHH", self, count)
        self.pixel = _unpacked[0]
        self.exact_red = _unpacked[1]
        self.exact_green = _unpacked[2]
        self.exact_blue = _unpacked[3]
        self.visual_red = _unpacked[4]
        self.visual_green = _unpacked[5]
        self.visual_blue = _unpacked[6]

class GetImageCookie(object):
    pass

class LookupColorCookie(object):
    pass

class EnterNotifyEvent(ooxcb.Event):
    event_name = "on_enter_notify"
    event_target_class = "Window"
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxIIIIhhhhHBB", self, count)
        self.detail = _unpacked[0]
        self.time = Timestamp(conn, _unpacked[1])
        self.root = conn.get_from_cache_fallback(_unpacked[2], Window)
        self.event = conn.get_from_cache_fallback(_unpacked[3], Window)
        self.child = conn.get_from_cache_fallback(_unpacked[4], Window)
        self.root_x = _unpacked[5]
        self.root_y = _unpacked[6]
        self.event_x = _unpacked[7]
        self.event_y = _unpacked[8]
        self.state = _unpacked[9]
        self.mode = _unpacked[10]
        self.same_screen_focus = _unpacked[11]
        self.event_target = self.event

class MapRequestEvent(ooxcb.Event):
    event_name = "on_map_request"
    event_target_class = "Window"
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxII", self, count)
        self.parent = conn.get_from_cache_fallback(_unpacked[0], Window)
        self.window = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.event_target = self.parent

class QueryPointerCookie(object):
    pass

class ColormapError(ooxcb.Error):
    def __init__(self, conn, parent):
        ooxcb.Error.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHB", self, count)
        self.bad_value = _unpacked[0]
        self.minor_opcode = _unpacked[1]
        self.major_opcode = _unpacked[2]

class NotifyDetail(object):
    Ancestor = 0
    Virtual = 1
    Inferior = 2
    Nonlinear = 3
    NonlinearVirtual = 4
    Pointer = 5
    PointerRoot = 6
    _None = 7

class AccessError(ooxcb.Error):
    def __init__(self, conn, parent):
        ooxcb.Error.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHB", self, count)
        self.bad_value = _unpacked[0]
        self.minor_opcode = _unpacked[1]
        self.major_opcode = _unpacked[2]

class GrabKeyboardCookie(object):
    pass

class KeyReleaseEvent(ooxcb.Event):
    event_name = "on_key_release"
    event_target_class = "Window"
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxIIIIhhhhHB", self, count)
        self.detail = Keycode(conn, _unpacked[0])
        self.time = Timestamp(conn, _unpacked[1])
        self.root = conn.get_from_cache_fallback(_unpacked[2], Window)
        self.event = conn.get_from_cache_fallback(_unpacked[3], Window)
        self.child = conn.get_from_cache_fallback(_unpacked[4], Window)
        self.root_x = _unpacked[5]
        self.root_y = _unpacked[6]
        self.event_x = _unpacked[7]
        self.event_y = _unpacked[8]
        self.state = _unpacked[9]
        self.same_screen = _unpacked[10]
        self.event_target = self.event

class QueryTextExtentsCookie(object):
    pass

class ClipOrdering(object):
    Unsorted = 0
    YSorted = 1
    YXSorted = 2
    YXBanded = 3

class Rectangle(ooxcb.Struct):
    def __init__(self, conn, parent, offset, size):
        ooxcb.Struct.__init__(self, conn, parent, offset, size)
        count = 0
        _unpacked = unpack_ex("hhHH", self, count)
        self.x = _unpacked[0]
        self.y = _unpacked[1]
        self.width = _unpacked[2]
        self.height = _unpacked[3]
        ooxcb._resize_obj(self, count)

class ImageOrder(object):
    LSBFirst = 0
    MSBFirst = 1

class ListFontsCookie(object):
    pass

class GetPropertyReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxxxxxIIIxxxxxxxxxxxx", self, count)
        self.format = _unpacked[0]
        self.type = Atom(conn, _unpacked[1])
        self.bytes_after = _unpacked[2]
        self.value_len = _unpacked[3]
        count += 32
        self.value = ooxcb.List(conn, self, count, self.value_len, 'B', 1)

class LookupColorReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxxxxxHHHHHH", self, count)
        self.exact_red = _unpacked[0]
        self.exact_green = _unpacked[1]
        self.exact_blue = _unpacked[2]
        self.visual_red = _unpacked[3]
        self.visual_green = _unpacked[4]
        self.visual_blue = _unpacked[5]

class Timestamp(ooxcb.Resource):
    def __init__(self, conn, xid):
        ooxcb.Resource.__init__(self, conn, xid)

class Screen(ooxcb.Struct):
    def __init__(self, conn, parent, offset):
        ooxcb.Struct.__init__(self, conn, parent, offset)
        count = 0
        _unpacked = unpack_ex("IIIIIHHHHHHIBBBB", self, count)
        self.root = conn.get_from_cache_fallback(_unpacked[0], Window)
        self.default_colormap = conn.get_from_cache_fallback(_unpacked[1], Colormap)
        self.white_pixel = _unpacked[2]
        self.black_pixel = _unpacked[3]
        self.current_input_masks = _unpacked[4]
        self.width_in_pixels = _unpacked[5]
        self.height_in_pixels = _unpacked[6]
        self.width_in_millimeters = _unpacked[7]
        self.height_in_millimeters = _unpacked[8]
        self.min_installed_maps = _unpacked[9]
        self.max_installed_maps = _unpacked[10]
        self.root_visual = VisualID(conn, _unpacked[11])
        self.backing_stores = _unpacked[12]
        self.save_unders = _unpacked[13]
        self.root_depth = _unpacked[14]
        self.allowed_depths_len = _unpacked[15]
        count += 40
        self.allowed_depths = ooxcb.List(conn, self, count, self.allowed_depths_len, Depth, -1)
        count += len(self.allowed_depths.buf())

class ReparentNotifyEvent(ooxcb.Event):
    event_name = "on_reparent_notify"
    event_target_class = "Window"
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIIIhhB", self, count)
        self.event = conn.get_from_cache_fallback(_unpacked[0], Window)
        self.window = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.parent = conn.get_from_cache_fallback(_unpacked[2], Window)
        self.x = _unpacked[3]
        self.y = _unpacked[4]
        self.override_redirect = _unpacked[5]
        self.event_target = self.window

class ClientMessageEvent(ooxcb.Event):
    event_name = "on_client_message"
    event_target_class = "Window"
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxII", self, count)
        self.format = _unpacked[0]
        self.window = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.type = Atom(conn, _unpacked[2])
        count += 12
        self.data = ClientMessageData(self, count, 60)
        self.event_target = self.window

class Host(ooxcb.Struct):
    def __init__(self, conn, parent, offset):
        ooxcb.Struct.__init__(self, conn, parent, offset)
        count = 0
        _unpacked = unpack_ex("BxH", self, count)
        self.family = _unpacked[0]
        self.address_len = _unpacked[1]
        count += 4
        self.address = ooxcb.List(conn, self, count, self.address_len, 'B', 1)
        count += len(self.address.buf())

class Char2b(ooxcb.Struct):
    def __init__(self, conn, parent, offset, size):
        ooxcb.Struct.__init__(self, conn, parent, offset, size)
        count = 0
        _unpacked = unpack_ex("BB", self, count)
        self.byte1 = _unpacked[0]
        self.byte2 = _unpacked[1]
        ooxcb._resize_obj(self, count)

class InternAtomCookie(object):
    pass

class ListFontsWithInfoReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxxxxx", self, count)
        self.name_len = _unpacked[0]
        count += 8
        self.min_bounds = CHARINFO(self, count, 12)
        count += 12
        count += 4
        count += ooxcb.type_pad(12, count)
        self.max_bounds = CHARINFO(self, count, 12)
        count += 12
        _unpacked = unpack_ex("xxxxHHHHBBBBhhI", self, count)
        self.min_char_or_byte2 = _unpacked[0]
        self.max_char_or_byte2 = _unpacked[1]
        self.default_char = _unpacked[2]
        self.properties_len = _unpacked[3]
        self.draw_direction = _unpacked[4]
        self.min_byte1 = _unpacked[5]
        self.max_byte1 = _unpacked[6]
        self.all_chars_exist = _unpacked[7]
        self.font_ascent = _unpacked[8]
        self.font_descent = _unpacked[9]
        self.replies_hint = _unpacked[10]
        count += 24
        count += ooxcb.type_pad(8, count)
        self.properties = ooxcb.List(conn, self, count, self.properties_len, Fontprop, 8)
        count += len(self.properties.buf())
        count += ooxcb.type_pad(1, count)
        self.name = ooxcb.List(conn, self, count, self.name_len, 'b', 1)

class QueryTextExtentsReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxxxxxhhhhiii", self, count)
        self.draw_direction = _unpacked[0]
        self.font_ascent = _unpacked[1]
        self.font_descent = _unpacked[2]
        self.overall_ascent = _unpacked[3]
        self.overall_descent = _unpacked[4]
        self.overall_width = _unpacked[5]
        self.overall_left = _unpacked[6]
        self.overall_right = _unpacked[7]

class ButtonReleaseEvent(ooxcb.Event):
    event_name = "on_button_release"
    event_target_class = "Window"
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxIIIIhhhhHB", self, count)
        self.detail = Button(conn, _unpacked[0])
        self.time = Timestamp(conn, _unpacked[1])
        self.root = conn.get_from_cache_fallback(_unpacked[2], Window)
        self.event = conn.get_from_cache_fallback(_unpacked[3], Window)
        self.child = conn.get_from_cache_fallback(_unpacked[4], Window)
        self.root_x = _unpacked[5]
        self.root_y = _unpacked[6]
        self.event_x = _unpacked[7]
        self.event_y = _unpacked[8]
        self.state = _unpacked[9]
        self.same_screen = _unpacked[10]
        self.event_target = self.event

class MapIndex(object):
    Shift = 0
    Lock = 1
    Control = 2
    _1 = 3
    _2 = 4
    _3 = 5
    _4 = 6
    _5 = 7

class Charinfo(ooxcb.Struct):
    def __init__(self, conn, parent, offset, size):
        ooxcb.Struct.__init__(self, conn, parent, offset, size)
        count = 0
        _unpacked = unpack_ex("hhhhhH", self, count)
        self.left_side_bearing = _unpacked[0]
        self.right_side_bearing = _unpacked[1]
        self.character_width = _unpacked[2]
        self.ascent = _unpacked[3]
        self.descent = _unpacked[4]
        self.attributes = _unpacked[5]
        ooxcb._resize_obj(self, count)

class BadLength(ooxcb.ProtocolException):
    pass

class ButtonPressEvent(ooxcb.Event):
    event_name = "on_button_press"
    event_target_class = "Window"
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxIIIIhhhhHB", self, count)
        self.detail = Button(conn, _unpacked[0])
        self.time = Timestamp(conn, _unpacked[1])
        self.root = conn.get_from_cache_fallback(_unpacked[2], Window)
        self.event = conn.get_from_cache_fallback(_unpacked[3], Window)
        self.child = conn.get_from_cache_fallback(_unpacked[4], Window)
        self.root_x = _unpacked[5]
        self.root_y = _unpacked[6]
        self.event_x = _unpacked[7]
        self.event_y = _unpacked[8]
        self.state = _unpacked[9]
        self.same_screen = _unpacked[10]
        self.event_target = self.event

class GetKeyboardControlReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxxxxxIBBHHxx", self, count)
        self.global_auto_repeat = _unpacked[0]
        self.led_mask = _unpacked[1]
        self.key_click_percent = _unpacked[2]
        self.bell_percent = _unpacked[3]
        self.bell_pitch = _unpacked[4]
        self.bell_duration = _unpacked[5]
        count += 20
        self.auto_repeats = ooxcb.List(conn, self, count, 32, 'B', 1)

class GetPointerControlCookie(object):
    pass

class GetPropertyCookie(object):
    pass

class JoinStyle(object):
    Mitre = 0
    Round = 1
    Bevel = 2

class Gravity(object):
    BitForget = 0
    WinUnmap = 0
    NorthWest = 1
    North = 2
    NorthEast = 3
    West = 4
    Center = 5
    East = 6
    SouthWest = 7
    South = 8
    SouthEast = 9
    Static = 10

class GetAtomNameCookie(object):
    pass

class Str(ooxcb.Struct):
    def __init__(self, conn, parent, offset):
        ooxcb.Struct.__init__(self, conn, parent, offset)
        count = 0
        _unpacked = unpack_ex("B", self, count)
        self.name_len = _unpacked[0]
        count += 1
        self.name = ooxcb.List(conn, self, count, self.name_len, 'b', 1)
        count += len(self.name.buf())

class AllocColorPlanesReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxxxxxHxxIIIxxxxxxxx", self, count)
        self.pixels_len = _unpacked[0]
        self.red_mask = _unpacked[1]
        self.green_mask = _unpacked[2]
        self.blue_mask = _unpacked[3]
        count += 32
        self.pixels = ooxcb.List(conn, self, count, self.pixels_len, 'I', 4)

class CirculateNotifyEvent(ooxcb.Event):
    event_name = "on_circulate_notify"
    event_target_class = ooxcb.Connection
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIIxxxxB", self, count)
        self.event = conn.get_from_cache_fallback(_unpacked[0], Window)
        self.window = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.place = _unpacked[2]
        self.event_target = self.conn

class CW(object):
    BackPixmap = (1 << 0)
    BackPixel = (1 << 1)
    BorderPixmap = (1 << 2)
    BorderPixel = (1 << 3)
    BitGravity = (1 << 4)
    WinGravity = (1 << 5)
    BackingStore = (1 << 6)
    BackingPlanes = (1 << 7)
    BackingPixel = (1 << 8)
    OverrideRedirect = (1 << 9)
    SaveUnder = (1 << 10)
    EventMask = (1 << 11)
    DontPropagate = (1 << 12)
    Colormap = (1 << 13)
    Cursor = (1 << 14)

class QueryExtensionCookie(object):
    pass

class GetWindowAttributesCookie(object):
    pass

class KB(object):
    KeyClickPercent = (1 << 0)
    BellPercent = (1 << 1)
    BellPitch = (1 << 2)
    BellDuration = (1 << 3)
    Led = (1 << 4)
    LedMode = (1 << 5)
    Key = (1 << 6)
    AutoRepeatMode = (1 << 7)

class GetMotionEventsReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxxxxxIxxxxxxxxxxxxxxxxxxxx", self, count)
        self.events_len = _unpacked[0]
        count += 32
        self.events = ooxcb.List(conn, self, count, self.events_len, Timecoord, 8)

class ListFontsReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxxxxxHxxxxxxxxxxxxxxxxxxxxxx", self, count)
        self.names_len = _unpacked[0]
        count += 32
        self.names = ooxcb.List(conn, self, count, self.names_len, Str, -1)

class Family(object):
    Internet = 0
    DECnet = 1
    Chaos = 2
    ServerInterpreted = 5
    Internet6 = 6

class EventMask(object):
    NoEvent = 0
    KeyPress = (1 << 0)
    KeyRelease = (1 << 1)
    ButtonPress = (1 << 2)
    ButtonRelease = (1 << 3)
    EnterWindow = (1 << 4)
    LeaveWindow = (1 << 5)
    PointerMotion = (1 << 6)
    PointerMotionHint = (1 << 7)
    Button1Motion = (1 << 8)
    Button2Motion = (1 << 9)
    Button3Motion = (1 << 10)
    Button4Motion = (1 << 11)
    Button5Motion = (1 << 12)
    ButtonMotion = (1 << 13)
    KeymapState = (1 << 14)
    Exposure = (1 << 15)
    VisibilityChange = (1 << 16)
    StructureNotify = (1 << 17)
    ResizeRedirect = (1 << 18)
    SubstructureNotify = (1 << 19)
    SubstructureRedirect = (1 << 20)
    FocusChange = (1 << 21)
    PropertyChange = (1 << 22)
    ColorMapChange = (1 << 23)
    OwnerGrabButton = (1 << 24)

class InternAtomReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxxxxxI", self, count)
        self.atom = Atom(conn, _unpacked[0])

class Point(ooxcb.Struct):
    def __init__(self, conn, parent, offset, size):
        ooxcb.Struct.__init__(self, conn, parent, offset, size)
        count = 0
        _unpacked = unpack_ex("hh", self, count)
        self.x = _unpacked[0]
        self.y = _unpacked[1]
        ooxcb._resize_obj(self, count)

class GetPointerControlReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxxxxxHHH", self, count)
        self.acceleration_numerator = _unpacked[0]
        self.acceleration_denominator = _unpacked[1]
        self.threshold = _unpacked[2]

class GetFontPathCookie(object):
    pass

class LeaveNotifyEvent(ooxcb.Event):
    event_name = "on_leave_notify"
    event_target_class = "Window"
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxIIIIhhhhHBB", self, count)
        self.detail = _unpacked[0]
        self.time = Timestamp(conn, _unpacked[1])
        self.root = conn.get_from_cache_fallback(_unpacked[2], Window)
        self.event = conn.get_from_cache_fallback(_unpacked[3], Window)
        self.child = conn.get_from_cache_fallback(_unpacked[4], Window)
        self.root_x = _unpacked[5]
        self.root_y = _unpacked[6]
        self.event_x = _unpacked[7]
        self.event_y = _unpacked[8]
        self.state = _unpacked[9]
        self.mode = _unpacked[10]
        self.same_screen_focus = _unpacked[11]
        self.event_target = self.event

class VisualID(ooxcb.Resource):
    def __init__(self, conn, xid):
        ooxcb.Resource.__init__(self, conn, xid)

class QueryColorsCookie(object):
    pass

class AtomError(ooxcb.Error):
    def __init__(self, conn, parent):
        ooxcb.Error.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHB", self, count)
        self.bad_value = _unpacked[0]
        self.minor_opcode = _unpacked[1]
        self.major_opcode = _unpacked[2]

class ListHostsCookie(object):
    pass

class GetMotionEventsCookie(object):
    pass

class Pixmap(ooxcb.Resource):
    def __init__(self, conn, xid):
        ooxcb.Resource.__init__(self, conn, xid)

class MapNotifyEvent(ooxcb.Event):
    event_name = "on_map_notify"
    event_target_class = "Window"
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIIB", self, count)
        self.event = conn.get_from_cache_fallback(_unpacked[0], Window)
        self.window = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.override_redirect = _unpacked[2]
        self.event_target = self.window

class GetAtomNameReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxxxxxHxxxxxxxxxxxxxxxxxxxxxx", self, count)
        self.name_len = _unpacked[0]
        count += 32
        self.name = ooxcb.List(conn, self, count, self.name_len, 'B', 1)

class Fontprop(ooxcb.Struct):
    def __init__(self, conn, parent, offset, size):
        ooxcb.Struct.__init__(self, conn, parent, offset, size)
        count = 0
        _unpacked = unpack_ex("II", self, count)
        self.name = Atom(conn, _unpacked[0])
        self.value = _unpacked[1]
        ooxcb._resize_obj(self, count)

class Window(ooxcb.Resource):
    def __init__(self, conn, xid):
        ooxcb.Resource.__init__(self, conn, xid)

    def map(self):
        window = self.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 8, True, True), \
            ooxcb.VoidCookie())

    def map(self):
        window = self.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xxxxI", window))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 8, True, False), \
            ooxcb.VoidCookie())

    def get_property(self, delete, property_, type_, long_offset=0, long_length=2**32-1):
        window = self.get_internal()
        property = property_.get_internal()
        type = type_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIIIII", delete, window, property, type, long_offset, long_length))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 20, False, True), \
            GetPropertyCookie(),
            GetPropertyReply)

    def get_property_unchecked(self, delete, property_, type_, long_offset=0, long_length=2**32-1):
        window = self.get_internal()
        property = property_.get_internal()
        type = type_.get_internal()
        buf = StringIO.StringIO()
        buf.write(pack("xBxxIIIII", delete, window, property, type, long_offset, long_length))
        return self.conn.xproto.send_request(ooxcb.Request(self.conn, buf.getvalue(), 20, False, False), \
            GetPropertyCookie(),
            GetPropertyReply)

    @classmethod
    def create(cls, conn, parent, depth, visual, x=0, y=0, width=640, height=480, border_width=0, _class=WindowClass.InputOutput, **values):
        wid = conn.generate_id()
        win = cls(conn, wid)
        value_mask, value_list = 0, []
        if "back_pixmap" in values:
            value_mask |= (1 << 0)
            value_list.append(values["back_pixmap"].get_internal())
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
        conn.core.create_window_checked(depth, win, parent, x, y, width, height, border_width, _class, visual, value_mask, value_list).check()
        conn.add_to_cache(wid, win)
        return win

class CoordMode(object):
    Origin = 0
    Previous = 1

class ImageFormat(object):
    XYBitmap = 0
    XYPixmap = 1
    ZPixmap = 2

class GrabStatus(object):
    Success = 0
    AlreadyGrabbed = 1
    InvalidTime = 2
    NotViewable = 3
    Frozen = 4

class LineStyle(object):
    Solid = 0
    OnOffDash = 1
    DoubleDash = 2

class QueryBestSizeReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxxxxxHH", self, count)
        self.width = _unpacked[0]
        self.height = _unpacked[1]

class InputFocus(object):
    _None = 0
    PointerRoot = 1
    Parent = 2

class VisibilityNotifyEvent(ooxcb.Event):
    event_name = "on_visibility_notify"
    event_target_class = "Window"
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIB", self, count)
        self.window = conn.get_from_cache_fallback(_unpacked[0], Window)
        self.state = _unpacked[1]
        self.event_target = self.window

class FocusOutEvent(ooxcb.Event):
    event_name = "on_focus_out"
    event_target_class = ooxcb.Connection
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxIB", self, count)
        self.detail = _unpacked[0]
        self.event = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.mode = _unpacked[2]
        self.event_target = self.conn

class SendEventDest(object):
    PointerWindow = 0
    ItemFocus = 1

class Format(ooxcb.Struct):
    def __init__(self, conn, parent, offset, size):
        ooxcb.Struct.__init__(self, conn, parent, offset, size)
        count = 0
        _unpacked = unpack_ex("BBBxxxxx", self, count)
        self.depth = _unpacked[0]
        self.bits_per_pixel = _unpacked[1]
        self.scanline_pad = _unpacked[2]
        ooxcb._resize_obj(self, count)

class ColormapNotifyEvent(ooxcb.Event):
    event_name = "on_colormap_notify"
    event_target_class = ooxcb.Connection
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIIBB", self, count)
        self.window = conn.get_from_cache_fallback(_unpacked[0], Window)
        self.colormap = conn.get_from_cache_fallback(_unpacked[1], Colormap)
        self.new = _unpacked[2]
        self.state = _unpacked[3]
        self.event_target = self.conn

class CirculateRequestEvent(ooxcb.Event):
    event_name = "on_circulate_request"
    event_target_class = ooxcb.Connection
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIIxxxxB", self, count)
        self.event = conn.get_from_cache_fallback(_unpacked[0], Window)
        self.window = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.place = _unpacked[2]
        self.event_target = self.conn

class QueryFontReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        count += 8
        self.min_bounds = CHARINFO(self, count, 12)
        count += 12
        count += 4
        count += ooxcb.type_pad(12, count)
        self.max_bounds = CHARINFO(self, count, 12)
        count += 12
        _unpacked = unpack_ex("xxxxHHHHBBBBhhI", self, count)
        self.min_char_or_byte2 = _unpacked[0]
        self.max_char_or_byte2 = _unpacked[1]
        self.default_char = _unpacked[2]
        self.properties_len = _unpacked[3]
        self.draw_direction = _unpacked[4]
        self.min_byte1 = _unpacked[5]
        self.max_byte1 = _unpacked[6]
        self.all_chars_exist = _unpacked[7]
        self.font_ascent = _unpacked[8]
        self.font_descent = _unpacked[9]
        self.char_infos_len = _unpacked[10]
        count += 24
        count += ooxcb.type_pad(8, count)
        self.properties = ooxcb.List(conn, self, count, self.properties_len, Fontprop, 8)
        count += len(self.properties.buf())
        count += ooxcb.type_pad(12, count)
        self.char_infos = ooxcb.List(conn, self, count, self.char_infos_len, Charinfo, 12)

class CreateNotifyEvent(ooxcb.Event):
    event_name = "on_create_notify"
    event_target_class = "Window"
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIIhhHHHB", self, count)
        self.parent = conn.get_from_cache_fallback(_unpacked[0], Window)
        self.window = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.x = _unpacked[2]
        self.y = _unpacked[3]
        self.width = _unpacked[4]
        self.height = _unpacked[5]
        self.border_width = _unpacked[6]
        self.override_redirect = _unpacked[7]
        self.event_target = self.parent

class Mapping(object):
    Modifier = 0
    Keyboard = 1
    Pointer = 2

class ResizeRequestEvent(ooxcb.Event):
    event_name = "on_resize_request"
    event_target_class = ooxcb.Connection
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHH", self, count)
        self.window = conn.get_from_cache_fallback(_unpacked[0], Window)
        self.width = _unpacked[1]
        self.height = _unpacked[2]
        self.event_target = self.conn

class QueryColorsReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxxxxxHxxxxxxxxxxxxxxxxxxxxxx", self, count)
        self.colors_len = _unpacked[0]
        count += 32
        self.colors = ooxcb.List(conn, self, count, self.colors_len, Rgb, 8)

class MotionNotifyEvent(ooxcb.Event):
    event_name = "on_motion_notify"
    event_target_class = "Window"
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxIIIIhhhhHB", self, count)
        self.detail = _unpacked[0]
        self.time = Timestamp(conn, _unpacked[1])
        self.root = conn.get_from_cache_fallback(_unpacked[2], Window)
        self.event = conn.get_from_cache_fallback(_unpacked[3], Window)
        self.child = conn.get_from_cache_fallback(_unpacked[4], Window)
        self.root_x = _unpacked[5]
        self.root_y = _unpacked[6]
        self.event_x = _unpacked[7]
        self.event_y = _unpacked[8]
        self.state = _unpacked[9]
        self.same_screen = _unpacked[10]
        self.event_target = self.event

class Atom(ooxcb.Resource):
    def __init__(self, conn, xid):
        ooxcb.Resource.__init__(self, conn, xid)

class ScreenSaver(object):
    Reset = 0
    Active = 1

class CloseDown(object):
    DestroyAll = 0
    RetainPermanent = 1
    RetainTemporary = 2

class SetPointerMappingReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxxxxx", self, count)
        self.status = _unpacked[0]

class Segment(ooxcb.Struct):
    def __init__(self, conn, parent, offset, size):
        ooxcb.Struct.__init__(self, conn, parent, offset, size)
        count = 0
        _unpacked = unpack_ex("hhhh", self, count)
        self.x1 = _unpacked[0]
        self.y1 = _unpacked[1]
        self.x2 = _unpacked[2]
        self.y2 = _unpacked[3]
        ooxcb._resize_obj(self, count)

class ValueError(ooxcb.Error):
    def __init__(self, conn, parent):
        ooxcb.Error.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHB", self, count)
        self.bad_value = _unpacked[0]
        self.minor_opcode = _unpacked[1]
        self.major_opcode = _unpacked[2]

class GetInputFocusReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxxxxxI", self, count)
        self.revert_to = _unpacked[0]
        self.focus = conn.get_from_cache_fallback(_unpacked[1], Window)

class MappingNotifyEvent(ooxcb.Event):
    event_name = "on_mapping_notify"
    event_target_class = ooxcb.Connection
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxBBB", self, count)
        self.request = _unpacked[0]
        self.first_keycode = Keycode(conn, _unpacked[1])
        self.count = _unpacked[2]
        self.event_target = self.conn

class GetGeometryReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxxxxxIhhHHH", self, count)
        self.depth = _unpacked[0]
        self.root = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.x = _unpacked[2]
        self.y = _unpacked[3]
        self.width = _unpacked[4]
        self.height = _unpacked[5]
        self.border_width = _unpacked[6]

class Button(ooxcb.Resource):
    def __init__(self, conn, xid):
        ooxcb.Resource.__init__(self, conn, xid)

class SelectionRequestEvent(ooxcb.Event):
    event_name = "on_selection_request"
    event_target_class = ooxcb.Connection
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIIIIII", self, count)
        self.time = Timestamp(conn, _unpacked[0])
        self.owner = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.requestor = conn.get_from_cache_fallback(_unpacked[2], Window)
        self.selection = Atom(conn, _unpacked[3])
        self.target = Atom(conn, _unpacked[4])
        self.property = Atom(conn, _unpacked[5])
        self.event_target = self.conn

class BadWindow(ooxcb.ProtocolException):
    pass

class MapState(object):
    Unmapped = 0
    Unviewable = 1
    Viewable = 2

class Depth(ooxcb.Struct):
    def __init__(self, conn, parent, offset):
        ooxcb.Struct.__init__(self, conn, parent, offset)
        count = 0
        _unpacked = unpack_ex("BxHxxxx", self, count)
        self.depth = _unpacked[0]
        self.visuals_len = _unpacked[1]
        count += 8
        self.visuals = ooxcb.List(conn, self, count, self.visuals_len, Visualtype, 24)
        count += len(self.visuals.buf())

class ListExtensionsCookie(object):
    pass

class ButtonMask(object):
    _1 = (1 << 8)
    _2 = (1 << 9)
    _3 = (1 << 10)
    _4 = (1 << 11)
    _5 = (1 << 12)
    Any = (1 << 15)

class CursorError(ooxcb.Error):
    def __init__(self, conn, parent):
        ooxcb.Error.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHB", self, count)
        self.bad_value = _unpacked[0]
        self.minor_opcode = _unpacked[1]
        self.major_opcode = _unpacked[2]

class Drawable(ooxcb.Resource):
    def __init__(self, conn, xid):
        ooxcb.Resource.__init__(self, conn, xid)

class FocusInEvent(ooxcb.Event):
    event_name = "on_focus_in"
    event_target_class = ooxcb.Connection
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxIB", self, count)
        self.detail = _unpacked[0]
        self.event = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.mode = _unpacked[2]
        self.event_target = self.conn

class GetImageReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxxxxxIxxxxxxxxxxxxxxxxxxxx", self, count)
        self.depth = _unpacked[0]
        self.visual = VisualID(conn, _unpacked[1])
        count += 32
        self.data = ooxcb.List(conn, self, count, (self.length * 4), 'B', 1)

class PixmapError(ooxcb.Error):
    def __init__(self, conn, parent):
        ooxcb.Error.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHB", self, count)
        self.bad_value = _unpacked[0]
        self.minor_opcode = _unpacked[1]
        self.major_opcode = _unpacked[2]

class BadAlloc(ooxcb.ProtocolException):
    pass

class QueryPointerReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxxxxxIIhhhhH", self, count)
        self.same_screen = _unpacked[0]
        self.root = conn.get_from_cache_fallback(_unpacked[1], Window)
        self.child = conn.get_from_cache_fallback(_unpacked[2], Window)
        self.root_x = _unpacked[3]
        self.root_y = _unpacked[4]
        self.win_x = _unpacked[5]
        self.win_y = _unpacked[6]
        self.mask = _unpacked[7]

class Timecoord(ooxcb.Struct):
    def __init__(self, conn, parent, offset, size):
        ooxcb.Struct.__init__(self, conn, parent, offset, size)
        count = 0
        _unpacked = unpack_ex("Ihh", self, count)
        self.time = Timestamp(conn, _unpacked[0])
        self.x = _unpacked[1]
        self.y = _unpacked[2]
        ooxcb._resize_obj(self, count)

class PolyShape(object):
    Complex = 0
    Nonconvex = 1
    Convex = 2

class SetModifierMappingCookie(object):
    pass

class GetPointerMappingCookie(object):
    pass

class GetSelectionOwnerReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxxxxxI", self, count)
        self.owner = conn.get_from_cache_fallback(_unpacked[0], Window)

class WindowError(ooxcb.Error):
    def __init__(self, conn, parent):
        ooxcb.Error.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIHB", self, count)
        self.bad_value = _unpacked[0]
        self.minor_opcode = _unpacked[1]
        self.major_opcode = _unpacked[2]

class SetMode(object):
    Insert = 0
    Delete = 1

class NotifyMode(object):
    Normal = 0
    Grab = 1
    Ungrab = 2
    WhileGrabbed = 3

class PropertyNotifyEvent(ooxcb.Event):
    event_name = "on_property_notify"
    event_target_class = ooxcb.Connection
    def __init__(self, conn, parent):
        ooxcb.Event.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxIIIB", self, count)
        self.window = conn.get_from_cache_fallback(_unpacked[0], Window)
        self.atom = Atom(conn, _unpacked[1])
        self.time = Timestamp(conn, _unpacked[2])
        self.state = _unpacked[3]
        self.event_target = self.conn

class GetFontPathReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xxxxxxxxHxxxxxxxxxxxxxxxxxxxxxx", self, count)
        self.path_len = _unpacked[0]
        count += 32
        self.path = ooxcb.List(conn, self, count, self.path_len, Str, -1)

class GetKeyboardMappingReply(object):
    def __init__(self, conn, parent):
        ooxcb.Reply.__init__(self, conn, parent)
        count = 0
        _unpacked = unpack_ex("xBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", self, count)
        self.keysyms_per_keycode = _unpacked[0]
        count += 32
        self.keysyms = ooxcb.List(conn, self, count, self.length, 'I', 4)

_events = {
    24: GravityNotifyEvent,
    25: ResizeRequestEvent,
    26: CirculateNotifyEvent,
    27: CirculateRequestEvent,
    20: MapRequestEvent,
    21: ReparentNotifyEvent,
    22: ConfigureNotifyEvent,
    23: ConfigureRequestEvent,
    28: PropertyNotifyEvent,
    29: SelectionClearEvent,
    3: KeyReleaseEvent,
    2: KeyPressEvent,
    5: ButtonReleaseEvent,
    4: ButtonPressEvent,
    7: EnterNotifyEvent,
    6: MotionNotifyEvent,
    9: FocusInEvent,
    8: LeaveNotifyEvent,
    11: KeymapNotifyEvent,
    10: FocusOutEvent,
    13: GraphicsExposureEvent,
    12: ExposeEvent,
    15: VisibilityNotifyEvent,
    14: NoExposureEvent,
    17: DestroyNotifyEvent,
    16: CreateNotifyEvent,
    19: MapNotifyEvent,
    18: UnmapNotifyEvent,
    31: SelectionNotifyEvent,
    30: SelectionRequestEvent,
    34: MappingNotifyEvent,
    33: ClientMessageEvent,
    32: ColormapNotifyEvent,
}

_errors = {
    11: (AllocError, BadAlloc),
    10: (AccessError, BadAccess),
    13: (GContextError, BadGContext),
    12: (ColormapError, BadColormap),
    15: (NameError, BadName),
    14: (IDChoiceError, BadIDChoice),
    17: (ImplementationError, BadImplementation),
    16: (LengthError, BadLength),
    1: (RequestError, BadRequest),
    3: (WindowError, BadWindow),
    2: (ValueError, BadValue),
    5: (AtomError, BadAtom),
    4: (PixmapError, BadPixmap),
    7: (FontError, BadFont),
    6: (CursorError, BadCursor),
    9: (DrawableError, BadDrawable),
    8: (MatchError, BadMatch),
}

for ev in _events.itervalues():
    if isinstance(ev.event_target_class, str):
        ev.event_target_class = globals()[ev.event_target_class]

ooxcb._add_core(xprotoExtension, Setup, _events, _errors)

