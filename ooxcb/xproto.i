ImportCode:
    ["from ooxcb.types import make_void_array"]

ResourceClasses:
    - WINDOW
    - DRAWABLE
    - COLORMAP

Ignored:
    - KEYCODE
    - KEYSYM
    - TIMESTAMP
    - BUTTON
    - VISUALID

Xizers:
    CW:
        type: values
        enum_name: CW
        values_dict_name: values
        xize:
            - back_pixmap
            - cursor

    GC:
        type: values
        enum_name: GC
        values_dict_name: values
        xize:
            - font

    ConfigWindow:
        type: values
        enum_name: ConfigWindow
        values_dict_name: values

    Name:
        type: seq
        seq_in: name
        length_out: name_len
        seq_out: name

    Points:
        type: seq
        seq_in: points
        length_out: points_len
        seq_out: points

    Segments:
        type: seq
        seq_in: segments
        length_out: segments_len
        seq_out: segments

    RectanglesObjects:
        type: objects
        name: rectangles

    ArcsObjects:
        type: objects
        name: arcs

    Arcs:
        type: seq
        seq_in: arcs
        length_out: arcs_length
        seq_out: arcs

    String:
        type: string
        seq_in: string
        length_out: string_len
        seq_out: string

    UTF16:
        type: utf16
        seq_in: string
        length_out: string_len
        seq_out: string

    Pattern:
        type: seq
        seq_in: pattern
        length_out: pattern_len
        seq_out: pattern

    Data:
        type: seq
        seq_in: data
        length_out: data_len
        seq_out: data

    FontQtyPaths:
        type: seq
        seq_in: path
        length_out: font_qty
        seq_out: path

    PropertyName:
        type: lazy_atom
        name: property

    PropertyType:
        type: lazy_atom
        name: type

    Selection:
        type: lazy_atom
        name: selection

    CursorNone:
        type: lazy_none
        value: cursor

    ConfineToNone:
        type: lazy_none
        value: confine_to

    OwnerNone:
        type: lazy_none
        value: owner

    PropertyNone:
        type: lazy_none
        value: property

    SrcWindowNone:
        type: lazy_none
        value: src_w

    DestWindowNone:
        type: lazy_none
        value: dest_w

ClassAliases:
    GCONTEXT: GContext

Requests:
    # xproto objects
    InternAtom:
        arguments: ["name", "only_if_exists=False"]
        precode: [!xizer "Name"]

    AllowEvents:
        defaults:
            time: 0 # CurrentTime

    WarpPointer:
        # That's not a method of a window, because it is not clear
        # if src_w or dest_w is the subject.
        precode:
            - !xizer "SrcWindowNone"
            - !xizer "DestWindowNone"

    ListFonts:
        arguments: ["max_names", "pattern"]
        precode:
            - !xizer "Pattern"

    ListFontsWithInfo:
        arguments: ["max_names", "pattern"]
        precode:
            - !xizer "Pattern"

    SetFontPath:
        # `font_qty` seems to be `path_len`, and `path_len`
        # is unused. WTF o_O
        arguments: ["path"]
        # TODO: No idea how what format `path` has. It doesn't seem to be
        # len(s1) + s1 + \x00 + len(s2) + s2 + \x00 ... :/
#        initcode:
#            - !xizer "FontQtyPaths"
#            - 'buf = StringIO.StringIO()'
#            - 'buf.write(pack("=xxxxH", font_qty))'
#            - 'for item in path:'
#            - !indent
#            - 'buf.write(pack("=H", len(item)) + array("B", item).tostring() + "\x00")'
#            - !dedent

    # Atom objects
    GetAtomName:
        subject: atom
        name: get_name

    # TODO: should the selection stuff really be in the Atom objects?
    SetSelectionOwner:
        subject: selection
        precode: [!xizer "OwnerNone"]
        defaults:
            owner: None
            time: 0 # CurrentTime

    GetSelectionOwner:
        subject: selection

    ConvertSelection:
        subject: selection
        precode: [!xizer "PropertyNone"]
        defaults:
            property: None
            time: 0 # CurrentTime

    # Window objects
    GetProperty:
        subject: window
        precode: [!xizer "PropertyName", !xizer "PropertyType"]
        defaults:
            long_offset: 0
            long_length: 2**32-1
            delete: False

    ChangeProperty:
        subject: window
        arguments: ["property", "type", "format", "data", "mode=PropMode.Replace"]
        initcode: [!xizer "Data", !xizer "PropertyName", !xizer "PropertyType",
        "buf = StringIO.StringIO()",
        'buf.write(pack("=xBxxIIIBxxxI", mode, self.get_internal(), property.get_internal(), type.get_internal(), format, data_len))',
        'buf.write(make_void_array(data, format))']

    MapWindow:
        subject: window
        name: map

    SetInputFocus:
        subject: focus
        defaults:
            revert_to: 1 # TODO: well, 1 is InputFocus.PointerRoot, but Python gets angry if InputFocus isn't defined before set_input_focus, so that's a workaround.
            time: 0 # TODO: CurrentTime?

    UnmapWindow:
        subject: window
        name: unmap

    ConfigureWindow:
        subject: window
        initcode:
            - !xizer "ConfigWindow"
            - "window = self.get_internal()"
            - "buf = StringIO.StringIO()"
            - 'buf.write(pack("=xxxxIH", window, value_mask))'
            - 'buf.write(pack("=xx"))' # NOTE: The pad has to be after the value mask, but xcbgen seems to put it after the value list. So, that's just a workaround.

            # Well, another workaround. The xproto spec says x and y are signed ints.
            # Here we would have an array of unsigned ints.
            # Handcraft needed!
            - 'if value_mask & ConfigWindow.X:'
            - !indent
            - 'buf.write(pack("=i", value_list[0]))'
            - 'del value_list[0]'
            - !dedent
            - 'if value_mask & ConfigWindow.Y:'
            - !indent
            - 'buf.write(pack("=i", value_list[0]))'
            - 'del value_list[0]'
            - !dedent
            - 'buf.write(array("I", value_list).tostring())'

        arguments: ["**values"]
        name: "configure"

    ChangeWindowAttributes:
        subject: window
        name: change_attributes
        arguments: ["**values"]
        precode: [!xizer "CW"]

    GetWindowAttributes:
        subject: window
        name: get_attributes

    DestroyWindow:
        subject: window
        name: destroy

    DestroySubwindows:
        subject: window

    ChangeSaveSet:
        subject: window

    MapSubwindows:
        subject: window

    UnmapSubwindows:
        subject: window

    CirculateWindow:
        subject: window

    QueryTree:
        subject: window

    DeleteProperty:
        subject: window
        precode: [!xizer "PropertyName"]

    ListProperties:
        subject: window

    GetGeometry:
        subject: drawable
        class: Window # TODO: for drawable, not for Window!

    GrabKey:
        subject: grab_window
        defaults:
            owner_events: True
            pointer_mode: GrabMode.Async
            keyboard_mode: GrabMode.Async

    ReparentWindow:
        name: reparent
        subject: window
        defaults:
            x: 0
            y: 0

    ClearArea:
        name: clear_area
        subject: window
        defaults:
            exposures: False

    GrabPointer:
        subject: grab_window
        defaults:
            owner_events: True
            pointer_mode: GrabMode.Async
            keyboard_mode: GrabMode.Async
            time: 0 # TODO: CurrentTime
            confine_to: 'None'
            cursor: 'None'
        precode:
            - !xizer "ConfineToNone"
            - !xizer "CursorNone"

        # TODO: (!!!) confine_to can be None. Maybe with a xizer? -- is XNone the cool solution?

    UngrabPointer:
        defaults:
            time: 0 # TODO: CurrentTime

    SendEvent:
        subject: destination # TODO: add PointerWindow and InputFocus!
        arguments: ["event_mask", "event", "propagate=False"]
        # hardcoded because of `event`.
        initcode:
            - "destination = self.get_internal()"
            - "buf = StringIO.StringIO()"
            - 'buf.write(pack("=xBxxII", propagate, destination, event_mask))'
            - "event.build(buf)"

    QueryPointer:
        subject: window

    GetMotionEvents:
        subject: window

    TranslateCoordinates:
        subject: src_window

    # GContext objects
    ImageText8:
        subject: gc
        precode: [!xizer "String"]
        arguments: ["drawable", "x", "y", "string"]

    ImageText16:
        # CHAR2B xizer is there ...
        subject: gc
        precode: ["string_len = len(string)"]
        arguments: ["drawable", "x", "y", "string"]
        do_not_xize: ["string"]

    PolyRectangle:
        subject: gc
        arguments: ["drawable", "rectangles"]
        initcode:
            - "gc = self.get_internal()"
            - "drawable = drawable.get_internal()"
            - "buf = StringIO.StringIO()"
            - 'buf.write(pack("=xxxxII", drawable, gc))'
            - "for rect in rectangles:"
            - !indent
            - 'buf.write(pack("=hhHH", rect.x, rect.y, rect.width, rect.height))'
            - !dedent

    PolyPoint:
        subject: gc
        arguments: ["drawable", "points", "coordinate_mode=0"] # CoordMode.Origin
        precode:
            - !xizer "Points"
        do_not_xize:
            - "points"
        doc: ":param points: a list of tuples (x, y)\n:type coordinate_mode: :class:CoordMode"

    PolySegment:
        subject: gc
        arguments: ["drawable", "segments"]
        precode:
            - !xizer "Segments"
        do_not_xize:
            - "segments"

    PolyLine:
        subject: gc
        arguments: ["drawable", "points", "coordinate_mode=0"] # CoordMode.Origin
        precode:
            - !xizer "Points"
        do_not_xize:
            - "points"
        doc: ":param points: a list of tuples (x, y)\n:type coordinate_mode: :class:CoordMode"

    PolyArc:
        subject: gc
        arguments: ["drawable", "arcs"]
        initcode:
            - !xizer "Arcs"
            - "drawable = drawable.get_internal()"
            - "gc = self.get_internal()"
            - "buf = StringIO.StringIO()"
            - "buf.write(pack('xxxxII', drawable, gc))"
            - !xizer "ArcsObjects"

        do_not_xize: ["arcs"]
        doc: ":type arcs: a list of :class:`Arc` instances"

    FreeGC:
        subject: gc
        name: free

    # Colormap objects

    AllocColor:
        subject: cmap

    AllocNamedColor:
        subject: cmap
        arguments: ["name"]
        precode:
            - !xizer "Name"

    # Font objects
    OpenFont:
        arguments: ["fid", "name"]
        precode: [!xizer "Name"]

    CloseFont:
        name: close
        subject: font

    QueryFont:
        name: query
        subject: font
        # TODO: that can also be a GContext method.

    QueryTextExtents:
        # TODO: not working.
        subject: font
        precode: ["string_len = len(string)"]
        arguments: ["string"]
        do_not_xize: ["string"]

    # Cursor objects

    # TODO: wrap create_cursor

    # no need to hack CreateGlyphCursor ...

Classes:
    Window:
#        - base: Drawable # TODO: fix the class 'order'?
        - classmethod:
            name: create
            arguments: ["conn", "parent", "depth", "visual", "x=0", "y=0", "width=640", "height=480", "border_width=0", "_class=WindowClass.InputOutput", "**values"]
            code: [
                    'wid = conn.generate_id()',
                    'win = cls(conn, wid)',
                    !xizer "CW" ,
                    'conn.core.create_window_checked(depth, win, parent, x, y, width, height, border_width, _class, visual, value_mask, value_list).check()',
                    'conn.add_to_cache(wid, win)',
                    'return win'
                ]

        - classmethod:
            name: create_toplevel_on_screen
            arguments: ["conn", "screen", "*args", "**kwargs"]
            code:
                - "return cls.create(conn, screen.root, screen.root_depth, screen.root_visual, *args, **kwargs)"


    GContext:
        - base: Fontable
        - classmethod:
            name: create
            arguments: ["conn", "drawable", "**values"]
            code: [
                    'cid = conn.generate_id()',
                    'gc = cls(conn, cid)',
                    !xizer "GC" ,
                    'conn.core.create_g_c_checked(gc, drawable, value_mask, value_list).check()',
                    'conn.add_to_cache(cid, gc)',
                    'return gc'
                ]

    Font:
        - base: Fontable
        - classmethod:
            name: open
            arguments: ["conn", "name"]
            code:
                - "fid = conn.generate_id()"
                - "font = cls(conn, fid)"
                - "conn.core.open_font_checked(font, name).check()"
                - "conn.add_to_cache(fid, font)"
                - "return font"

    Cursor:
        - classmethod:
            name: create_glyph
            arguments: ["conn", "source_font", "mask_font", "source_char", "mask_char", "fore_red", "fore_green", "fore_blue", "back_red", "back_green", "back_blue"]
            code:
                - "cid = conn.generate_id()"
                - "cursor = cls(conn, cid)"
                - "conn.core.create_glyph_cursor_checked(cursor, source_font, mask_font, source_char, mask_char, fore_red, fore_green, fore_blue, back_red, back_green, back_blue).check()"
                - "conn.add_to_cache(cid, cursor)"
                - "return cursor"

    GetPropertyReply:
        - method:
            name: exists
            decorators: ["property"]
            code: ["''' is True if the queried property exists. (If a property does not exist, self.format is 0.) '''", "return self.format != 0"]

    Arc:
        - classmethod:
            name: create
            arguments: ["conn", "x", "y", "width", "height", "angle1", "angle2"]
            code:
                - "arc = cls(conn)"
                - "arc.x = x"
                - "arc.y = y"
                - "arc.width = width"
                - "arc.height = height"
                - "arc.angle1 = angle1"
                - "arc.angle2 = angle2"
                - "return arc"

    Rectangle:
        - classmethod:
            name: create
            arguments: ["conn", "x", "y", "width", "height"]
            code:
                - "rect = cls(conn)"
                - "rect.x = x"
                - "rect.y = y"
                - "rect.width = width"
                - "rect.height = height"
                - "return rect"
    
    Colormap:
        - method:
            name: alloc_hex_color
            arguments: ["color"]
            code:
                - "color = color.strip('#')"
                - "r, g, b = [65535 * int(v, base=16) // 255"
                - "           for v in (color[:2], color[2:4], color[4:])]"
                - "return self.alloc_color(r, g, b)"
    Screen:
        - method:
            name: get_active_window
            code:
                - "return self.root.get_property('_NET_ACTIVE_WINDOW', 'WINDOW').reply().value.to_windows()[0]"

    # some additional enums

    # Enum for WM_STATE state values
    WMState:
        - attribute:
            name: Withdrawn
            value: 0
        - attribute:
            name: Normal
            value: 1
        - attribute:
            name: Iconic
            value: 3

    # nice __str__ and __repr__ for the `Str` struct
    # and a `pythonize_lazy` method so that users don't have to
    # mess around with `Str` structs. They will just get a
    # Python string instead. Is that cool? (y/n)
    Str:
        - method:
            name: __str__
            code: ["return self.name.to_string()"]
        - method:
            name: __repr__
            code: ["return '<ooxcb.xproto.Str %s>' % repr(self.name.to_string())"]
        - method:
            name: pythonize_lazy
            code: ["return self.name.to_string()"]
        - classmethod:
            name: create_lazy
            arguments: ["conn", "string"]
            code:
                - "struct = Str(conn)"
                - "struct.name = string"
                - "struct.name_len = len(string)"
                - "return struct"

Events:
    KeyPress:
        member: event
    KeyRelease:
        member: event
    ClientMessage:
        member: window
    ButtonPress:
        member: event
    ButtonRelease:
        member: event
    EnterNotify:
        member: event
    LeaveNotify:
        member: event
    GraphicsExposure:
        member: drawable
    Expose:
        member: window
    MotionNotify:
        member: event
    #KeymapNotify:
    VisibilityNotify:
        member: window
    MapRequest:
        member: parent
    CreateNotify:
        member: parent
    DestroyNotify:
        member: event
    MapNotify:
        member: event
    UnmapNotify:
        member: event
    ConfigureRequest:
        member: parent # is that correct?? TODO: we should change that
    ConfigureNotify:
        member: event # correct??
    ReparentNotify:
        member: window # correct??
    PropertyNotify:
        member: window

    # TODO: hundreds of events to be mapped.

# vim: ft=yaml
