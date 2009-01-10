{
    "aliases": {
        "VISUALID": "VisualID"
    },

    "ignore_classes": ["BUTTON"],
    "ignore_parameters": ["major_opcode", "length"],
    "classes": {
        "Atom": [
            "order_id",
            0,
            "method",
            {
                "request": "GetAtomName",
                "subjectname": "atom",
                "methname": "get_name",
                "reply_pythonizers": {
                    "name": "string"
                }
            },
            "method",
            {
                "request": "SetSelectionOwner",
                "subject": "selection",
                "defaults": {"time": 0}
            },
            "method",
            {
                "request": "GetSelectionOwner",
                "subject": "selection"
            },
            "method",
            {
                "request": "ConvertSelection",
                "subject": "selection",
                "defaults": {"time": 0}
            }
        ],

        "Drawable": [
            "method",
            {
                "request": "GetGeometry",
                "subjectname": "drawable"
            }
        ],

        "Window": [
            "basecls",
            "Drawable",

            "method",
            {
                "request": "CreateWindow",
                "decorators": ["classmethod"],
                "code": [
                    "wid = conn.generate_id()",
                    "conn.xproto.CreateWindowChecked(depth, wid, parent._internal, x, y, width, height, border_width, _class, visual._internal, value_mask, value_list).check()",
                    "return cls(conn, wid)"
                ],
                "methname": "create",
                "methargs": ["parent", "depth", "visual", "x=0", "y=0", "width=640", "height=480", "border_width=0", "_class=xcb.xproto.WindowClass.InputOutput", "**values"], 
                "make_get": false,
                "NOTE": "ATTR HERE",
                "extended": {
                    "make_values_xizer": {
                        "values_dict_name": "values",
                        "enum_name": "CW",
                        "xize": ["back_pixmap"]
                    }
                }      
            },
            "method",
            {
                "request": "ChangeWindowAttributes",
                "methargs": ["**values"],
                "NOTE": "ATTR HERE",
                "extended": {
                    "make_values_xizer": {
                        "values_dict_name": "values",
                        "enum_name": "CW",
                        "xize": ["back_pixmap"]
                    }
                },
                "subjectname": "window",
                "methname": "change_attributes"
            },
            "method",
            {
                "request": "DestroyWindow",
                "subjectname": "window",
                "methname": "destroy"
            },
            "method",
            {
                "request": "DestroySubwindows",
                "subjectname": "window"
            },
            "method",
            {
                "request": "ChangeSaveSet",
                "subjectname": "window"
            },
            "method",
            {
                "request": "ReparentWindow",
                "subjectname": "window",
                "methname": "reparent"
            },
            "method",
            {
                "request": "MapWindow",
                "subjectname": "window",
                "methname": "map"
            },
            "method",
            {
                "request": "UnmapWindow",
                "subjectname": "window",
                "methname": "unmap"
            },
            "method",
            {
                "request": "UnmapSubwindows",
                "subjectname": "window"
            },
            "method",
            {
                "request": "ConfigureWindow",
                "subjectname": "window",
                "methargs": ["**values"],
                "extended": {
                    "make_values_xizer": {
                        "values_dict_name": "values",
                        "enum_name": "ConfigWindow",
                        "xize": []
                    }
                }
            },
            "method",
            {
                "request": "CirculateWindow",
                "subjectname": "window",
                "methname": "circulate"
            },
            "method",
            {
                "request": "QueryTree",
                "subjectname": "window"
            },
            "method",
            {
                "request": "InternAtom",
                "methargs": ["name", "only_if_exists=False"],
                "extended": {
                    "make_seq_xizer": {
                        "seq_in": "name",
                        "seq_out": "name",
                        "length_out": "name_len"
                    }
                }
            },
            "method",
            {
                "request": "ChangeProperty",
                "subjectname": "window",
                "methargs": ["mode", "property", "type", "format", "data"],
                "extended": {
                    "make_seq_xizer": {
                        "seq_in": "data",
                        "seq_out": "data",
                        "length_out": "data_len"
                    }
                }
            },
            "method",
            {
                "request": "DeleteProperty",
                "subjectname": "window"
            },
            "method",
            {
                "request": "GetProperty",
                "subjectname": "window",
                "defaults": {"long_offset": 0, "long_length": "2**32-1"}
            },
            "method",
            {
                "request": "ListProperties",
                "subjectname": "window",
                "reply_pythonizers": {
                    "atoms": "atoms"   
                }
            },
            "method",
            {
                "request": "SendEvent",
                "subjectname": "destination"
            },
            "method",
            {
                "request": "GrabPointer",
                "subjectname": "grab_window",
                "defaults": {"time": 0}
            },
            "method",
            {
                "request": "UngrabPointer",
                "defaults": {"time": 0}
            },
            "method",
            {
                "request": "GrabButton",
                "subjectname": "grab_window"
            },
            "method",
            {
                "request": "UngrabButton",
                "subjectname": "grab_window"
            }
        ]
    }
}
