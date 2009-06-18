ImportCode:
    - "from ooxcb.xproto import Window"

ExternallyWrapped:
    - WINDOW

ResourceClasses:
    - REGION

Xizers:
    RectanglesObjects:
        type: objects
        name: rectangles

    Rectangles:
        type: seq
        seq_in: rectangles
        length_out: rectangles_len
        seq_out: rectangles

Mixins:
    WINDOW: Window

Requests:
    ChangeSaveSet:
        subject: window

    SelectSelectionInput:
        subject: window

    SelectCursorInput:
        subject: window

#    GetCursorImage: # all ok

    CreateRegion:
        
        

Events:
    SelectionNotify:
        member: owner # TODO: not sure if `owner` or `window`

    CursorNotify:
        member: window

    
    
# vim: ft=yaml
