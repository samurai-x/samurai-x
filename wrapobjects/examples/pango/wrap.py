import sys
sys.path.append('../..')
sys.path.insert(0, '../cairo')

from wrapobjects.wrap import wrap
from wrapobjects.wraplib.codegen import transform, DummyCodegen
from wrapobjects.oo import regex_method, regex_classmethod, argument_tag, succeed, regex_match, function
from wrapobjects.properties import make_properties

with wrap(
        ['pango-new.h'],
        output='pango.py',
        link_modules=['cairo'],
        library='pangocairo-1.0') as w:

    w.add_pointer_class_wrappers(
            ('PangoContext', 'Context'),
            ('PangoLayout', 'Layout'),
            ('PangoFontDescription', 'FontDescription'),
            ('PangoFontMap', 'FontMap'),
            ('PangoCairoFontMap', 'CairoFontMap'),
            )
    w.wrappers['POINTER(cairo_t)'] = DummyCodegen(name='cairo.Context') # <- hacky, to get pango_cairo_* working

    w.get_pyclass('CairoFontMap').base = 'FontMap'

    w.add_init_redirects(
            ('Context', 'Context.new'),
            ('Layout', 'Layout.new'),
            ('FontDescription', 'FontDescription.new'),
            ('CairoFontMap', 'CairoFontMap.new'),
            )

    w.add_rules(
            regex_match(r'(pango_cairo_.*)', function),
            regex_method(r'pango_context_(.*)', 'Context'),
            regex_classmethod(r'pango_context_(new)', 'Context'),

            regex_method(r'pango_layout_(.*)', 'Layout'),
            regex_match(r'pango_layout_get_size', succeed), # separatedly wrapped
            regex_classmethod(r'pango_layout_(new)', 'Layout'),

            regex_method(r'pango_font_description_(.*)', 'FontDescription'),
            regex_classmethod(r'pango_font_description_(new|from_string)$', 'FontDescription'),

            regex_method(r'pango_font_map_(.*)', 'FontMap'),

            regex_method(r'pango_cairo_font_map_(.*)', 'CairoFontMap'),
            regex_classmethod(r'pango_cairo_font_map_(new|new_for_font_type)$', 'CairoFontMap'),
            )

    w.add_wrappers_visitor(make_properties)
    w.add_synonyms(
            (r'PANGO_(.*)$', r'\1'),
            (r'pango_(.*)$', r'\1'),
            )

    meth = w.get_pyclass('Layout').new_method('get_size')
    meth.code.extend(transform(
"""width, height = c_int(), c_int()
pango_layout_get_size(self._internal, byref(width), byref(height))
return (width.value, height.value)
"""))
