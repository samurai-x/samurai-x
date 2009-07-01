import sys
sys.path.append('../..')

from wrapobjects.wrap import wrap
from wrapobjects.wraplib.codegen import transform
from wrapobjects.oo import regex_method, regex_classmethod, regex_match, succeed
from wrapobjects.properties import make_properties

with wrap(['/usr/include/xosd.h'],
        output='xosd.py',
        library='xosd') as w:


    w.add_pointer_class_wrappers(
            ('xosd', 'XOSD'),
            )

    w.add_init_redirect('XOSD', 'XOSD.create')

    meth = w.get_pyclass('XOSD').new_method('get_colour')
    meth.code.extend(transform(\
"""r, g, b = c_int(), c_int(), c_int()
xosd_get_colour(self._internal, byref(r), byref(g), byref(b))
return (r.value, g.value, b.value)
"""))
    w.add_rules(
            regex_method('xosd_(.*)', 'XOSD'),
            regex_match('xosd_init', succeed),
            regex_match('xosd_get_colour', succeed),
            regex_classmethod('xosd_(create)', 'XOSD'),
            )

    w.add_wrappers_visitor(make_properties)
    w.add_synonyms(
            ('XOSD_(.*)', r'\1')
            )

