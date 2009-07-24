from yahiko import cairo

def rounded_rectangle(cr, x, y, width, height, radius):
    assert width and height

    x2 = x + width
    y2 = y + height

    if width / 2 < radius:
        if height / 2 < radius:
            cr.move_to  (x, (y + y2)/2)
            cr.curve_to (x ,y, x, y, (x + x2)/2, y)
            cr.curve_to (x2, y, x2, y, x2, (y + y2)/2)
            cr.curve_to (x2, y2, x2, y2, (x2 + x)/2, y2)
            cr.curve_to (x, y2, x, y2, x, (y + y2)/2)
        else:
            cr.move_to  (x, y + radius)
            cr.curve_to (x ,y, x, y, (x + x2)/2, y)
            cr.curve_to (x2, y, x2, y, x2, y + radius)
            cr.line_to (x2 , y2 - radius)
            cr.curve_to (x2, y2, x2, y2, (x2 + x)/2, y2)
            cr.curve_to (x, y2, x, y2, x, y2- radius)
    else:
        if height / 2 < radius:
            cr.move_to  (x, (y + y2)/2)
            cr.curve_to (x , y, x , y, x + radius, y)
            cr.line_to (x2 - radius, y)
            cr.curve_to (x2, y, x2, y, x2, (y + y2)/2)
            cr.curve_to (x2, y2, x2, y2, x2 - radius, y2)
            cr.line_to (x + radius, y2)
            cr.curve_to (x, y2, x, y2, x, (y + y2)/2)
        else:
            cr.move_to  (x, y + radius)
            cr.curve_to (x , y, x , y, x + radius, y)
            cr.line_to (x2 - radius, y)
            cr.curve_to (x2, y, x2, y, x2, y + radius)
            cr.line_to (x2 , y2 - radius)
            cr.curve_to (x2, y2, x2, y2, x2 - radius, y2)
            cr.line_to (x + radius, y2)
            cr.curve_to (x, y2, x, y2, x, y2- radius)
    cr.close_path ()

    #cr.set_source_rgb (0.5, 0.5, 1)
    #cr.fill_preserve (cr)
    #cr.set_source_rgba (0.5, 0, 0, 0.5)
    #cr.set_line_width (10.0)
    #cr.stroke (cr)

def mixin():
    from ooxcb.util import mixin_functions
    from yahiko.cairo import Context
    mixin_functions((rounded_rectangle,), Context)

