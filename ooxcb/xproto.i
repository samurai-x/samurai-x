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

    GC:
        type: values
        enum_name: GC
        values_dict_name: values
        xize: []

    ConfigWindow:
        type: values
        enum_name: ConfigWindow
        values_dict_name: values

    Name:
        type: seq
        seq_in: name
        length_out: name_len
        seq_out: name

    String:
        type: seq
        seq_in: string
        length_out: string_len
        seq_out: string

    Data:
        type: seq
        seq_in: data
        length_out: data_len
        seq_out: data

    PropertyName:
        type: lazy_atom
        name: property

    PropertyType:
        type: lazy_atom
        name: type

    CursorNone:
        type: lazy_none
        value: cursor

    ConfineToNone:
        type: lazy_none
        value: confine_to

ClassAliases:
    GCONTEXT: GContext

Requests:
    # xproto objects
    InternAtom:
        arguments: ["name", "only_if_exists"]
        precode: [!xizer "Name"]

    # Atom objects
    GetAtomName:
        subject: atom
        name: get_name

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
        'buf.write(pack("xBxxIIIBxxxI", mode, self.get_internal(), property.get_internal(), type.get_internal(), format, data_len))',
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
            - 'buf.write(pack("xxxxIH", window, value_mask))'
            - 'buf.write(pack("xx"))' # NOTE: The pad has to be after the value mask, but xcbgen seems to put it after the value list. So, that's just a workaround.

            # Well, another workaround. The xproto spec says x and y are signed ints.
            # Here we would have an array of unsigned ints.
            # Handcraft needed!
            - 'if value_mask & ConfigWindow.X:'
            - !indent
            - 'buf.write(pack("i", value_list[0]))'
            - 'del value_list[0]'
            - !dedent
            - 'if value_mask & ConfigWindow.Y:'
            - !indent
            - 'buf.write(pack("i", value_list[0]))'
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

    QueryTree:
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
        
    # GContext objects
    #
    ImageText8:
        subject: gc
        precode: [!xizer "String"]
        arguments: ["drawable", "x", "y", "string"]
    
    PolyRectangle:
        subject: gc
        arguments: ["drawable", "rectangles"]
        initcode:
            - "gc = self.get_internal()"
            - "drawable = drawable.get_internal()"
            - "buf = StringIO.StringIO()"
            - 'buf.write(pack("xxxxII", drawable, gc))'
            - "for rect in rectangles:"
            - !indent
            - 'buf.write(pack("hhHH", rect.x, rect.y, rect.width, rect.height))'
            - !dedent

    FreeGC:
        subject: gc
        name: free

    # Font objects
    
    OpenFont:
        precode: [!xizer "Name"]

    CloseFont:
        name: close

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
    
    GContext:
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
                - "conn.core.create_glyph_cursor_checked(cid, source_font, mask_font, source_char, mask_char, fore_red, fore_green, fore_blue, back_red, back_green, back_blue).check()"
                - "conn.add_to_cache(cid, cursor)"
                - "return cursor"

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
