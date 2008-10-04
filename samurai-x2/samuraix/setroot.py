import samuraix.drawcontext
import samuraix.xcb

def set_root_image(screen, image, position=None, size=None):
    root = screen.root
    
    x, y = position or (0, 0)
    w, h = size or screen.size_in_pixels

    pixmap = samuraix.xcb.pixmap.Pixmap.create(screen.connection, root, w, h, screen.root_depth)
    context = samuraix.drawcontext.DrawContext(screen, w, h, pixmap)

    assert image.endswith('.svg'), 'can only render svg at the moment!'
    context.svg(image, x, y, w, h)

    root.attributes = {'back_pixmap':pixmap}
