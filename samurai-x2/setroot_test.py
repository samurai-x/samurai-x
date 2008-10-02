import samuraix.xcb as xcb
import samuraix.drawcontext

c = xcb.connection.Connection()
screen = c.screens[0]
root = screen.root

w, h = screen.size_in_pixels

pixmap = xcb.pixmap.Pixmap.create(c, root, w, h, screen.root_depth)
context = samuraix.drawcontext.DrawContext(screen, w, h, pixmap)

context.svg('../gfx/samuraix.svg', width=w, height=h)

root.attributes = {'back_pixmap': pixmap}

c.disconnect()
