import sys
sys.path.append('..')

import ooxcb
import ooxcb.xproto as X

conn = ooxcb.connect()

fonts = conn.core.list_fonts(1, '10x20').reply().names
font = X.Font.open(conn, fonts[0])
print font.query().reply()
print vars(font.query_text_extents('foobar').reply())

conn.disconnect()
