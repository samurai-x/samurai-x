""" usage status_bar_tail.py <slot_name> <logfile> """

import time
import os
import sys
from select import select

from yaydbus.bus import SessionBus
from yaydbus.dbus_types import Array

bus = SessionBus()

obj = bus.get_object('/org/yahiko/status_bar/'+sys.argv[1], 'org.yahiko.status_bar')
proxy = obj.get_bound('org.yahiko.status_bar')

fh = open(sys.argv[2])

st_results = os.stat(sys.argv[2])
st_size = st_results[6]
fh.seek(st_size)

while True:
    where = fh.tell()
    line = fh.readline()
    if not line:
        time.sleep(1)
        fh.seek(where)
    else:
        proxy.set_text(line.strip())

