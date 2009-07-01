import sys
sys.path.append('../..')

from wrapobjects.wrap import wrap
from wrapobjects.oo import regex_method, regex_classmethod, argument_tag
from wrapobjects.properties import make_properties

with wrap(
        ('/usr/include/cairo/cairo-xcb.h', '/usr/include/cairo/cairo.h'),
        output='cairo.py',
        library='cairo'
        ) as w:
    w.add_pointer_class_wrappers(
            ('cairo_t', 'Context'),
            ('cairo_path_t', 'Path'),
            ('cairo_pattern_t', 'Pattern'),
            ('cairo_font_face_t', 'FontFace'),
            ('cairo_scaled_font_t', 'ScaledFont'),
            ('cairo_font_options_t', 'FontOptions'),
            ('cairo_matrix_t', 'Matrix'),
            ('cairo_toy_font_face_t', 'ToyFontFace'),
            ('cairo_user_font_face_t', 'UserFontFace'),
            ('cairo_surface_t', 'Surface'),
            ('cairo_image_surface_t', 'ImageSurface'),
            ('cairo_xcb_surface_t', 'XcbSurface'),
            ('cairo_glyph_t', 'Glyph'),
            )

    w.objects['ToyFontFace'].base = 'FontFace'
    w.objects['UserFontFace'].base = 'FontFace'
    w.objects['ImageSurface'].base = 'Surface'
    w.objects['XcbSurface'].base = 'Surface'

    w.add_init_redirects(
            ('Context', 'Context.create'),
            ('ImageSurface', 'ImageSurface.create'),
            )

    w.add_rules(
            argument_tag(
                0,
                'POINTER(cairo_t)',
                regex_method(r'cairo_(.*)', 'Context'),
                ),
            regex_classmethod(r'cairo_(create)', 'Context'),

            regex_method(r'cairo_path_(.*)', 'Path'),

            regex_method(r'cairo_pattern_(.*)', 'Pattern'),
            regex_classmethod(r'cairo_pattern_(create_rgb|create_rgba|create_for_surface|create_linear|create_radial)', 'Pattern'),

            # all other glyph functions scare me.
            regex_classmethod(r'cairo_glyph_(allocate)', 'Glyph'),

            regex_method(r'cairo_font_face_(.*)', 'FontFace'),
            
            regex_method(r'cairo_toy_font_face_(.*)', 'ToyFontFace'),
            regex_classmethod(r'cairo_toy_font_face_(create)', 'ToyFontFace'),
            
            regex_method(r'cairo_user_font_face_(.*)', 'UserFontFace'),
            regex_classmethod(r'cairo_user_font_face_(create)', 'UserFontFace'),

            regex_method(r'cairo_scaled_font_(.*)', 'ScaledFont'),
            regex_classmethod(r'cairo_scaled_font_(create)', 'ScaledFont'),
            
            regex_method(r'cairo_font_options_(.*)', 'FontOptions'),
            regex_classmethod(r'cairo_font_options_(create)', 'FontOptions'),

            regex_method(r'cairo_matrix_(.*)', 'Matrix'),

            regex_method(r'cairo_surface_(.*)', 'Surface'),
            
            regex_method(r'cairo_image_surface_(.*)', 'ImageSurface'),
            regex_classmethod(r'cairo_image_surface_(create.*)$', 'ImageSurface'),

            regex_method(r'cairo_xcb_surface_(.*)', 'XcbSurface'),
            regex_classmethod(r'cairo_xcb_surface_(create.*)$', 'XcbSurface'),
            )

    w.add_synonyms(
            (r'CAIRO_(.*)$', r'\1'),
            (r'cairo_(.*)$', r'\1'),
            (r'cairo_t$', r'cairo_t'),
            )

    w.add_wrappers_visitor(make_properties)
