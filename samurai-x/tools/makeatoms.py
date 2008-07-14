import os
assert os.path.exists('setup.py'), 'this must be run from the root!'

import re

out = [
    'from pyglet.window.xlib.xlib import Atom\n',
    '\n',
]

define_re = re.compile('#define ([A-Z0-9_]+) \(\(Atom\) ([0-9]+)\)')

for line in open('/usr/include/X11/Xatom.h'):
    if line.startswith('#define'):
        mo = define_re.match(line)
        if mo is None: continue
        print mo.group(1), mo.group(2)
        out.append('%s = Atom(%s)\n' % (mo.group(1), mo.group(2)))

open('samuraix/xatom.py', 'w').writelines(out)
