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

installs_text = []
dev_installs_text = []

for module in to_install:
    installs_text.append("    subprocess.call([join(home_dir, 'bin', 'easy_install'), '%s'])" % module)
    dev_installs_text.append("    print home_dir")
    dev_installs_text.append("    os.chdir('%s')" % module)
    dev_installs_text.append("    print str(([os.path.normpath(join('..', home_dir, 'bin', 'python')), 'setup.py', 'develop']))")
    dev_installs_text.append("    subprocess.call([os.path.normpath(join('..', home_dir, 'bin', 'python')), 'setup.py', 'develop'])")
    dev_installs_text.append("    os.chdir('..')")

open('bootstrap.py', 'w').write(virtualenv.create_bootstrap_script(extra_text + "\n".join(installs_text)))
open('dev_bootstrap.py', 'w').write(virtualenv.create_bootstrap_script(extra_text + "\n".join(dev_installs_text)))

