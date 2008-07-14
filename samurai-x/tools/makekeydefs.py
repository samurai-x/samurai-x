import os
assert os.path.exists('setup.py'), 'this must be run from the root!'

import re

out = []

for line in open('/usr/include/X11/keysymdef.h'):
    if line.startswith('#define'):
        parts = re.split(' +', line, 3)
        if len(parts) == 3:
            out.append("%s = %s" % (parts[1], parts[2]))
        elif len(parts) == 4:
            out.append("%s = %s # %s" % (parts[1], parts[2], parts[3]))

open('samuraix/keysymdef.py', 'w').writelines(out)
