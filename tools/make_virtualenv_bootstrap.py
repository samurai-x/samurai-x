""" script to generate virtual env bootstrap script """

import virtualenv, textwrap
from glob import iglob
import os
import sys

if not os.path.exists('samurai-x2/setup.py'):
    print "you need to run this from the root of your checkout"
    sys.exit(1)


to_install = [
    'ooxcb',
    'samurai-x2',
    'yahiko',
]
to_install.extend(p for p in iglob('sx-*') if os.path.exists(os.path.join(p, 'setup.py')))

print "will install: ", ", ".join(to_install)

extra_text = """
import os, subprocess
def after_install(options, home_dir):
    etc = join(home_dir, 'etc')
    if not os.path.exists(etc):
        os.makedirs(etc)
"""

for module in to_install:
    extra_text += "    subprocess.call([join(home_dir, 'bin', 'easy_install'), '%s'])\n" % module
    
output = virtualenv.create_bootstrap_script(extra_text)

f = open('bootstrap.py', 'w').write(output)

