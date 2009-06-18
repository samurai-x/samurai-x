from StringIO import StringIO
from string import Template

def tmpl(s, **kwargs):
    return Template(s).substitute(**kwargs)

EXTENSIONS = ('xproto', 'xtest', 'render', 'composite')

print 'all: %s\n' % ' '.join(EXTENSIONS)

for ext in EXTENSIONS:
    print tmpl(
"""$ext: ../ooxcb/$ext.py ../docs/source/api/$ext.rst

../docs/source/api/$ext.rst: $ext.rst
\tcp $ext.rst ../docs/source/api/$ext.rst

$ext.rst: ../ooxcb/$ext.py

../ooxcb/$ext.py: $ext.xml $ext.i
\tpython ooxcb_client.py $ext > ../ooxcb/$ext.py
""", ext=ext)

print tmpl("""clean:
\trm -f ../docs/source/api/{$exts}.rst ../ooxcb/{$exts}.py {$exts}.rst

.phony: $names
""", exts=','.join(EXTENSIONS), names=' '.join(EXTENSIONS))
