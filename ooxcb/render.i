ImportCode:
    - "from ooxcb.xproto import Drawable"

ResourceClasses:
    - PICTURE
    - PICTFORMAT

ExternallyWrapped:
    - WINDOW
    - DRAWABLE

Ignored:
    - COLOR

Mixins:
    DRAWABLE: Drawable

Xizers:
    CP:
        type: values
        enum_name: CP
        values_dict_name: values
        xize:
            - alpha_map # TODO: can be none
            - clip_mask # TODO: can be None
            - dither # TODO: can be None

    RectanglesObjects:
        type: objects
        name: rectangles

    Rectangles:
        type: seq
        seq_in: rectangles
        length_out: rectangles_len
        seq_out: rectangles

    MaskNone:
        type: lazy_none
        value: mask

    MaskFormatNone:
        type: lazy_none
        value: mask_format

Requests:
    QueryFilters:
        subject: drawable

    QueryPictIndexValues:
        subject: format

#    CreatePicture:

    ChangePicture:
        name: change
        subject: picture
        arguments:
            - "**values"
        precode:
            - !xizer "CP"

    SetPictureClipRectangles:
        name: set_clip_rectangles
        subject: picture
        arguments: ["clip_x_origin", "clip_y_origin", "rectangles"]
        initcode:
            - !xizer "Rectangles"
            - "picture = self.get_internal()"
            - "buf = StringIO.StringIO()"
            - 'buf.write(pack("=xxxxIhh", picture, clip_x_origin, clip_y_origin)) '
            - !xizer "RectanglesObjects"
        do_not_xize: ["rectangles"]
        doc: ":type rectangles: a list of :class:`Rectangle` instances"

    FreePicture:
        name: free
        subject: picture

    Composite:
        subject: src
        precode:
            - !xizer "MaskNone"
        arguments: ["clip_x_origin", "clip_y_origin", "rectangles"]
        initcode:
            - !xizer "Rectangles"
            - "picture = self.get_internal()"
            - "buf = StringIO.StringIO()"
            - 'buf.write(pack("=xxxxIhh", picture, clip_x_origin, clip_y_origin)) '
            - !xizer "RectanglesObjects"
        do_not_xize: ["rectangles"]
        doc: ":type rectangles: a list of :class:`Rectangle` instances"

    FillRectangles:
        subject: dst
        arguments: ["op", "color", "rectangles"]
        initcode:
            - !xizer "Rectangles"
            - "dst = self.get_internal()"
            - "buf = StringIO.StringIO()"
            - 'buf.write(pack("=xxxxBxxxI", op, dst))'
            - 'buf.write(pack("=HHHH", *color))'
            - !xizer "RectanglesObjects"
        do_not_xize: ["rectangles", "color"]
        doc: ":type rectangles: a list of :class:`Rectangle` instances\n:type color: a (r, g, b, alpha) tuple"

Classes:
    Picture:
        - classmethod:
            name: create
            arguments: ["conn", "drawable", "format", "**values"]
            code:
                - "pid = conn.generate_id()"
                - "pict = cls(conn, pid)"
                - !xizer "CP"
                - "conn.render.create_picture_checked(pict, drawable, format, value_mask, value_list).check()"
                - "conn.add_to_cache(pid, pict)"
                - "return pict"

# vim: ft=yaml
