ResourceClasses:
    - WINDOW
    - DRAWABLE
    - COLORMAP

Xizers:
    CW:
        type: values 
        enum_name: CW
        values_dict_name: values
        xize:
            - back_pixmap

ClassAliases:
    VISUALID: VisualID

Requests:
    # Window objects
    GetProperty:
        subject: window
        defaults:
            long_offset: 0
            long_length: 2**32-1
    MapWindow:
        subject: window
        name: map

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
        member: window # is that correct??
    ConfigureNotify:
        member: window # correct??
    ReparentNotify:
        member: window # correct??
    PropertyChange:
        member: window

    # TODO: hundreds of events to be mapped.
