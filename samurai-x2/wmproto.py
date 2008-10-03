import samuraix.drawcontext
import samuraix.xcb

connection = samuraix.xcb.connection.Connection()
screen = connection.screens[0]
root = screen.root
print 'root window', root

def set_back_pixmap():
    w, h = screen.size_in_pixels

    pixmap = samuraix.xcb.pixmap.Pixmap.create(connection, root, w, h, screen.root_depth)
    context = samuraix.drawcontext.DrawContext(screen, w, h, pixmap)

    context.svg('../gfx/samuraix.svg', width=w, height=h)

    root.attributes = {'back_pixmap': pixmap}

root.attributes = {'event_mask': (samuraix.xcb.event.MapRequestEvent,
                                  samuraix.xcb.event.SubstructureRedirectEvent,
                                  samuraix.xcb.event.SubstructureNotifyEvent,
                                  samuraix.xcb.event.StructureNotifyEvent,
                                  samuraix.xcb.event.KeyPressEvent,
                                  )
                    }

class Handler(object):
    def on_map_request(self, event):
        print 'There was a map request', event, event.window
        event.window.map()
#        event.window.configure(x=300, width=20)
        event.window.push_handlers(self)

    def on_key_press(self, event):
        print 'root child', event.root, event.child
        if event.keycode == 27: # 'r' for me ...
#        print event.child.query_pointer().child, event.window
            print event.root.query_pointer().child, root

set_back_pixmap()
handler = Handler()

connection.push_handlers(handler)
root.push_handlers(handler)

while 1:
    connection.wait_for_event_dispatch()

connection.disconnect()
