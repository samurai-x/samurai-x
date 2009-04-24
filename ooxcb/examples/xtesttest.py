# a simple xtest extension test.
from __future__ import with_statement

import sys
sys.path.append('..')

import ooxcb
import ooxcb.xproto
import ooxcb.xtest

conn = ooxcb.connect()

with conn.bunch():
    conn.xtest.fake_input(2,
            38,
            0,
            ooxcb.xproto.XNone,
            0,
            0,
            0
    )

    conn.xtest.fake_input(3,
            38,
            0,
            ooxcb.xproto.XNone,
            0,
            0,
            0
    )
