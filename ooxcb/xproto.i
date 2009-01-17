ImportCode:
    ["from ooxcb.types import make_void_array"]

ResourceClasses:
    - WINDOW
    - DRAWABLE
    - COLORMAP

Ignored:
    - KEYCODE
    - KEYSYM

Xizers:
    CW:
        type: values 
        enum_name: CW
        values_dict_name: values
        xize:
            - back_pixmap

    ConfigWindow:
        type: values
        enum_name: ConfigWindow
        values_dict_name: values

    Name:
        type: seq
        seq_in: name
        length_out: name_len
        seq_out: name

    Data:
        type: seq
        seq_in: data
        length_out: data_len
        seq_out: data

    PropertyName:
        type: lazy_atom
        name: property_

    PropertyType:
        type: lazy_atom
        name: type_

ClassAliases:
    VISUALID: VisualID

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
        arguments: ["property_", "type_", "format", "data", "mode=PropMode.Replace"]
        initcode: [!xizer "Data", !xizer "PropertyName", !xizer "PropertyType",
        "buf = StringIO.StringIO()",
        'buf.write(pack("xBxxIIIBxxxI", mode, self.get_internal(), property_.get_internal(), type_.get_internal(), format, data_len))',
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

Classes:
    Window:
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
        member: window
    MapNotify:
        member: window
    UnmapNotify:
        member: window
    ConfigureRequest:
        member: parent # is that correct?? TODO: we should change that
    ConfigureNotify:
        member: window # correct??
    ReparentNotify:
        member: window # correct??
    PropertyChange:
        member: window

    # TODO: hundreds of events to be mapped.

# vim: ft=yaml
