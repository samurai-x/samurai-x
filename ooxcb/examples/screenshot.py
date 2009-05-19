import sys
sys.path.append('..')

import ooxcb
from ooxcb import xproto
from ooxcb.contrib.pil import get_pil_image

conn = ooxcb.connect()
root = conn.setup.roots[conn.pref_screen].root

image = get_pil_image(root)
image.save("screenshot.png")

conn.disconnect()
