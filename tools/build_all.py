""" dunk's shitty build all script to build and upload everything """

import sys
import os
from glob import iglob

if len(sys.argv) > 1:
    all_dirs = sys.argv[1:]
else:
    all_dirs = [
        'samurai-x2',
        'yahiko', 
        'ooxcb',
    ] + list(iglob('sx-*'))


curdir = os.getcwd()

for dir in all_dirs:
    os.chdir(curdir)
    os.chdir(dir)
    os.system('python setup.py rotate -m.mp3,.zip,.tar.gz -k0 bdist_egg sdist')
    os.system('python2.5 setup.py bdist_egg')
    os.system('scp dist/* samurai-x.org:/var/www/samuraix_downloads')
    os.system('python setup.py register')
