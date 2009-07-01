import cairo

w = 400
h = 400

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
ctx = cairo.Context(surface)

# clear to black
ctx.set_source_rgb(0, 0, 0)
ctx.paint()
# lifted from pycairo example...
ctx.set_line_width(15)
ctx.set_source_rgb(255, 0, 0)
ctx.move_to(0, -100)
ctx.line_to(100, 100)
ctx.rel_line_to(-200, 0)
ctx.close_path()
ctx.stroke()

surface.write_to_png("test.png")
