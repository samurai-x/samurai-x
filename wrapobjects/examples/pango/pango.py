'''Wrapper for pangocairo-1.0

Generated with:
wrap.py

Do not modify this file.
'''

__docformat__ =  'restructuredtext'
__version__ = '$Id: wrap.py 1694 2008-01-30 23:12:00Z Alex.Holkner $'

import ctypes
import ctypes.util
from ctypes import *

def load_lib(name):
    libname = ctypes.util.find_library(name)
    if not libname:
        raise OSError("Could not find library '%s'" % name)
    else:
        return CDLL(libname)

_lib = load_lib('pangocairo-1.0')

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (ctypes.c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]


import cairo

gint8 = c_char 	# pango-new.h:3
guint8 = c_ubyte 	# pango-new.h:4
gint16 = c_short 	# pango-new.h:5
guint16 = c_ushort 	# pango-new.h:6
gint32 = c_int 	# pango-new.h:10
guint32 = c_uint 	# pango-new.h:11
gint64 = c_longlong 	# pango-new.h:17
guint64 = c_ulonglong 	# pango-new.h:18
gssize = c_int 	# pango-new.h:19
gsize = c_uint 	# pango-new.h:20
goffset = gint64 	# pango-new.h:21
gintptr = c_int 	# pango-new.h:22
guintptr = c_uint 	# pango-new.h:23
class struct__GStaticMutex(Structure):
    __slots__ = [
    ]
struct__GStaticMutex._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__GStaticMutex(Structure):
    __slots__ = [
    ]
struct__GStaticMutex._fields_ = [
    ('_opaque_struct', c_int)
]

GStaticMutex = struct__GStaticMutex 	# pango-new.h:24
class struct__GSystemThread(Union):
    __slots__ = [
    ]
struct__GSystemThread._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__GSystemThread(Union):
    __slots__ = [
    ]
struct__GSystemThread._fields_ = [
    ('_opaque_struct', c_int)
]

GSystemThread = struct__GSystemThread 	# pango-new.h:35
GPid = c_int 	# pango-new.h:43
class struct__PangoCoverage(Structure):
    __slots__ = [
    ]
struct__PangoCoverage._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoCoverage(Structure):
    __slots__ = [
    ]
struct__PangoCoverage._fields_ = [
    ('_opaque_struct', c_int)
]

PangoCoverage = struct__PangoCoverage 	# pango-new.h:49
enum_anon_2 = c_int
PANGO_COVERAGE_NONE = 0
PANGO_COVERAGE_FALLBACK = 1
PANGO_COVERAGE_APPROXIMATE = 2
PANGO_COVERAGE_EXACT = 3
PangoCoverageLevel = enum_anon_2 	# pango-new.h:56
# pango-new.h:58
pango_coverage_new = _lib.pango_coverage_new
pango_coverage_new.restype = POINTER(PangoCoverage)
pango_coverage_new.argtypes = []

# pango-new.h:59
pango_coverage_ref = _lib.pango_coverage_ref
pango_coverage_ref.restype = POINTER(PangoCoverage)
pango_coverage_ref.argtypes = [POINTER(PangoCoverage)]

# pango-new.h:60
pango_coverage_unref = _lib.pango_coverage_unref
pango_coverage_unref.restype = None
pango_coverage_unref.argtypes = [POINTER(PangoCoverage)]

# pango-new.h:61
pango_coverage_copy = _lib.pango_coverage_copy
pango_coverage_copy.restype = POINTER(PangoCoverage)
pango_coverage_copy.argtypes = [POINTER(PangoCoverage)]

# pango-new.h:62
pango_coverage_get = _lib.pango_coverage_get
pango_coverage_get.restype = PangoCoverageLevel
pango_coverage_get.argtypes = [POINTER(PangoCoverage), c_int]

# pango-new.h:64
pango_coverage_set = _lib.pango_coverage_set
pango_coverage_set.restype = None
pango_coverage_set.argtypes = [POINTER(PangoCoverage), c_int, PangoCoverageLevel]

# pango-new.h:67
pango_coverage_max = _lib.pango_coverage_max
pango_coverage_max.restype = None
pango_coverage_max.argtypes = [POINTER(PangoCoverage), POINTER(PangoCoverage)]

class struct__PangoLogAttr(Structure):
    __slots__ = [
    ]
struct__PangoLogAttr._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoLogAttr(Structure):
    __slots__ = [
    ]
struct__PangoLogAttr._fields_ = [
    ('_opaque_struct', c_int)
]

PangoLogAttr = struct__PangoLogAttr 	# pango-new.h:80
class struct__PangoEngineLang(Structure):
    __slots__ = [
    ]
struct__PangoEngineLang._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoEngineLang(Structure):
    __slots__ = [
    ]
struct__PangoEngineLang._fields_ = [
    ('_opaque_struct', c_int)
]

PangoEngineLang = struct__PangoEngineLang 	# pango-new.h:82
class struct__PangoEngineShape(Structure):
    __slots__ = [
    ]
struct__PangoEngineShape._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoEngineShape(Structure):
    __slots__ = [
    ]
struct__PangoEngineShape._fields_ = [
    ('_opaque_struct', c_int)
]

PangoEngineShape = struct__PangoEngineShape 	# pango-new.h:83
class struct__PangoFont(Structure):
    __slots__ = [
    ]
struct__PangoFont._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoFont(Structure):
    __slots__ = [
    ]
struct__PangoFont._fields_ = [
    ('_opaque_struct', c_int)
]

PangoFont = struct__PangoFont 	# pango-new.h:85
class struct__PangoFontMap(Structure):
    __slots__ = [
    ]
struct__PangoFontMap._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoFontMap(Structure):
    __slots__ = [
    ]
struct__PangoFontMap._fields_ = [
    ('_opaque_struct', c_int)
]

PangoFontMap = struct__PangoFontMap 	# pango-new.h:86
class struct__PangoRectangle(Structure):
    __slots__ = [
    ]
struct__PangoRectangle._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoRectangle(Structure):
    __slots__ = [
    ]
struct__PangoRectangle._fields_ = [
    ('_opaque_struct', c_int)
]

PangoRectangle = struct__PangoRectangle 	# pango-new.h:88
PangoGlyph = guint32 	# pango-new.h:93
# pango-new.h:94
pango_units_from_double = _lib.pango_units_from_double
pango_units_from_double.restype = c_int
pango_units_from_double.argtypes = [c_double]

# pango-new.h:95
pango_units_to_double = _lib.pango_units_to_double
pango_units_to_double.restype = c_double
pango_units_to_double.argtypes = [c_int]

# pango-new.h:109
pango_extents_to_pixels = _lib.pango_extents_to_pixels
pango_extents_to_pixels.restype = None
pango_extents_to_pixels.argtypes = [POINTER(PangoRectangle), POINTER(PangoRectangle)]

enum_anon_3 = c_int
PANGO_GRAVITY_SOUTH = 0
PANGO_GRAVITY_EAST = 1
PANGO_GRAVITY_NORTH = 2
PANGO_GRAVITY_WEST = 3
PANGO_GRAVITY_AUTO = 4
PangoGravity = enum_anon_3 	# pango-new.h:120
enum_anon_4 = c_int
PANGO_GRAVITY_HINT_NATURAL = 0
PANGO_GRAVITY_HINT_STRONG = 1
PANGO_GRAVITY_HINT_LINE = 2
PangoGravityHint = enum_anon_4 	# pango-new.h:125
class struct__PangoMatrix(Structure):
    __slots__ = [
    ]
struct__PangoMatrix._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoMatrix(Structure):
    __slots__ = [
    ]
struct__PangoMatrix._fields_ = [
    ('_opaque_struct', c_int)
]

PangoMatrix = struct__PangoMatrix 	# pango-new.h:128
# pango-new.h:141
pango_matrix_copy = _lib.pango_matrix_copy
pango_matrix_copy.restype = POINTER(PangoMatrix)
pango_matrix_copy.argtypes = [POINTER(PangoMatrix)]

# pango-new.h:142
pango_matrix_free = _lib.pango_matrix_free
pango_matrix_free.restype = None
pango_matrix_free.argtypes = [POINTER(PangoMatrix)]

# pango-new.h:144
pango_matrix_translate = _lib.pango_matrix_translate
pango_matrix_translate.restype = None
pango_matrix_translate.argtypes = [POINTER(PangoMatrix), c_double, c_double]

# pango-new.h:147
pango_matrix_scale = _lib.pango_matrix_scale
pango_matrix_scale.restype = None
pango_matrix_scale.argtypes = [POINTER(PangoMatrix), c_double, c_double]

# pango-new.h:150
pango_matrix_rotate = _lib.pango_matrix_rotate
pango_matrix_rotate.restype = None
pango_matrix_rotate.argtypes = [POINTER(PangoMatrix), c_double]

# pango-new.h:152
pango_matrix_concat = _lib.pango_matrix_concat
pango_matrix_concat.restype = None
pango_matrix_concat.argtypes = [POINTER(PangoMatrix), POINTER(PangoMatrix)]

# pango-new.h:154
pango_matrix_transform_point = _lib.pango_matrix_transform_point
pango_matrix_transform_point.restype = None
pango_matrix_transform_point.argtypes = [POINTER(PangoMatrix), POINTER(c_double), POINTER(c_double)]

# pango-new.h:157
pango_matrix_transform_distance = _lib.pango_matrix_transform_distance
pango_matrix_transform_distance.restype = None
pango_matrix_transform_distance.argtypes = [POINTER(PangoMatrix), POINTER(c_double), POINTER(c_double)]

# pango-new.h:160
pango_matrix_transform_rectangle = _lib.pango_matrix_transform_rectangle
pango_matrix_transform_rectangle.restype = None
pango_matrix_transform_rectangle.argtypes = [POINTER(PangoMatrix), POINTER(PangoRectangle)]

# pango-new.h:162
pango_matrix_transform_pixel_rectangle = _lib.pango_matrix_transform_pixel_rectangle
pango_matrix_transform_pixel_rectangle.restype = None
pango_matrix_transform_pixel_rectangle.argtypes = [POINTER(PangoMatrix), POINTER(PangoRectangle)]

# pango-new.h:164
pango_matrix_get_font_scale_factor = _lib.pango_matrix_get_font_scale_factor
pango_matrix_get_font_scale_factor.restype = c_double
pango_matrix_get_font_scale_factor.argtypes = [POINTER(PangoMatrix)]

class struct__PangoScriptIter(Structure):
    __slots__ = [
    ]
struct__PangoScriptIter._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoScriptIter(Structure):
    __slots__ = [
    ]
struct__PangoScriptIter._fields_ = [
    ('_opaque_struct', c_int)
]

PangoScriptIter = struct__PangoScriptIter 	# pango-new.h:176
enum_anon_5 = c_int
PANGO_SCRIPT_INVALID_CODE = -1
PANGO_SCRIPT_COMMON = 0
PANGO_SCRIPT_INHERITED = 1
PANGO_SCRIPT_ARABIC = 2
PANGO_SCRIPT_ARMENIAN = 3
PANGO_SCRIPT_BENGALI = 4
PANGO_SCRIPT_BOPOMOFO = 5
PANGO_SCRIPT_CHEROKEE = 6
PANGO_SCRIPT_COPTIC = 7
PANGO_SCRIPT_CYRILLIC = 8
PANGO_SCRIPT_DESERET = 9
PANGO_SCRIPT_DEVANAGARI = 10
PANGO_SCRIPT_ETHIOPIC = 11
PANGO_SCRIPT_GEORGIAN = 12
PANGO_SCRIPT_GOTHIC = 13
PANGO_SCRIPT_GREEK = 14
PANGO_SCRIPT_GUJARATI = 15
PANGO_SCRIPT_GURMUKHI = 16
PANGO_SCRIPT_HAN = 17
PANGO_SCRIPT_HANGUL = 18
PANGO_SCRIPT_HEBREW = 19
PANGO_SCRIPT_HIRAGANA = 20
PANGO_SCRIPT_KANNADA = 21
PANGO_SCRIPT_KATAKANA = 22
PANGO_SCRIPT_KHMER = 23
PANGO_SCRIPT_LAO = 24
PANGO_SCRIPT_LATIN = 25
PANGO_SCRIPT_MALAYALAM = 26
PANGO_SCRIPT_MONGOLIAN = 27
PANGO_SCRIPT_MYANMAR = 28
PANGO_SCRIPT_OGHAM = 29
PANGO_SCRIPT_OLD_ITALIC = 30
PANGO_SCRIPT_ORIYA = 31
PANGO_SCRIPT_RUNIC = 32
PANGO_SCRIPT_SINHALA = 33
PANGO_SCRIPT_SYRIAC = 34
PANGO_SCRIPT_TAMIL = 35
PANGO_SCRIPT_TELUGU = 36
PANGO_SCRIPT_THAANA = 37
PANGO_SCRIPT_THAI = 38
PANGO_SCRIPT_TIBETAN = 39
PANGO_SCRIPT_CANADIAN_ABORIGINAL = 40
PANGO_SCRIPT_YI = 41
PANGO_SCRIPT_TAGALOG = 42
PANGO_SCRIPT_HANUNOO = 43
PANGO_SCRIPT_BUHID = 44
PANGO_SCRIPT_TAGBANWA = 45
PANGO_SCRIPT_BRAILLE = 46
PANGO_SCRIPT_CYPRIOT = 47
PANGO_SCRIPT_LIMBU = 48
PANGO_SCRIPT_OSMANYA = 49
PANGO_SCRIPT_SHAVIAN = 50
PANGO_SCRIPT_LINEAR_B = 51
PANGO_SCRIPT_TAI_LE = 52
PANGO_SCRIPT_UGARITIC = 53
PANGO_SCRIPT_NEW_TAI_LUE = 54
PANGO_SCRIPT_BUGINESE = 55
PANGO_SCRIPT_GLAGOLITIC = 56
PANGO_SCRIPT_TIFINAGH = 57
PANGO_SCRIPT_SYLOTI_NAGRI = 58
PANGO_SCRIPT_OLD_PERSIAN = 59
PANGO_SCRIPT_KHAROSHTHI = 60
PANGO_SCRIPT_UNKNOWN = 61
PANGO_SCRIPT_BALINESE = 62
PANGO_SCRIPT_CUNEIFORM = 63
PANGO_SCRIPT_PHOENICIAN = 64
PANGO_SCRIPT_PHAGS_PA = 65
PANGO_SCRIPT_NKO = 66
PANGO_SCRIPT_KAYAH_LI = 67
PANGO_SCRIPT_LEPCHA = 68
PANGO_SCRIPT_REJANG = 69
PANGO_SCRIPT_SUNDANESE = 70
PANGO_SCRIPT_SAURASHTRA = 71
PANGO_SCRIPT_CHAM = 72
PANGO_SCRIPT_OL_CHIKI = 73
PANGO_SCRIPT_VAI = 74
PANGO_SCRIPT_CARIAN = 75
PANGO_SCRIPT_LYCIAN = 76
PANGO_SCRIPT_LYDIAN = 77
PangoScript = enum_anon_5 	# pango-new.h:266
# pango-new.h:270
pango_script_iter_new = _lib.pango_script_iter_new
pango_script_iter_new.restype = POINTER(PangoScriptIter)
pango_script_iter_new.argtypes = [c_char_p, c_int]

# pango-new.h:272
pango_script_iter_get_range = _lib.pango_script_iter_get_range
pango_script_iter_get_range.restype = None
pango_script_iter_get_range.argtypes = [POINTER(PangoScriptIter), POINTER(c_char_p), POINTER(c_char_p), POINTER(PangoScript)]

# pango-new.h:277
pango_script_iter_free = _lib.pango_script_iter_free
pango_script_iter_free.restype = None
pango_script_iter_free.argtypes = [POINTER(PangoScriptIter)]

class struct__PangoLanguage(Structure):
    __slots__ = [
    ]
struct__PangoLanguage._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoLanguage(Structure):
    __slots__ = [
    ]
struct__PangoLanguage._fields_ = [
    ('_opaque_struct', c_int)
]

PangoLanguage = struct__PangoLanguage 	# pango-new.h:281
# pango-new.h:286
pango_language_from_string = _lib.pango_language_from_string
pango_language_from_string.restype = POINTER(PangoLanguage)
pango_language_from_string.argtypes = [c_char_p]

# pango-new.h:288
pango_language_to_string = _lib.pango_language_to_string
pango_language_to_string.restype = c_char_p
pango_language_to_string.argtypes = [POINTER(PangoLanguage)]

# pango-new.h:292
pango_language_get_sample_string = _lib.pango_language_get_sample_string
pango_language_get_sample_string.restype = c_char_p
pango_language_get_sample_string.argtypes = [POINTER(PangoLanguage)]

# pango-new.h:293
pango_language_get_default = _lib.pango_language_get_default
pango_language_get_default.restype = POINTER(PangoLanguage)
pango_language_get_default.argtypes = []

# pango-new.h:301
pango_language_get_scripts = _lib.pango_language_get_scripts
pango_language_get_scripts.restype = POINTER(PangoScript)
pango_language_get_scripts.argtypes = [POINTER(PangoLanguage), POINTER(c_int)]

# pango-new.h:306
pango_script_get_sample_language = _lib.pango_script_get_sample_language
pango_script_get_sample_language.restype = POINTER(PangoLanguage)
pango_script_get_sample_language.argtypes = [PangoScript]

# pango-new.h:310
pango_gravity_to_rotation = _lib.pango_gravity_to_rotation
pango_gravity_to_rotation.restype = c_double
pango_gravity_to_rotation.argtypes = [PangoGravity]

# pango-new.h:311
pango_gravity_get_for_matrix = _lib.pango_gravity_get_for_matrix
pango_gravity_get_for_matrix.restype = PangoGravity
pango_gravity_get_for_matrix.argtypes = [POINTER(PangoMatrix)]

# pango-new.h:312
pango_gravity_get_for_script = _lib.pango_gravity_get_for_script
pango_gravity_get_for_script.restype = PangoGravity
pango_gravity_get_for_script.argtypes = [PangoScript, PangoGravity, PangoGravityHint]

enum_anon_6 = c_int
PANGO_BIDI_TYPE_L = 0
PANGO_BIDI_TYPE_LRE = 1
PANGO_BIDI_TYPE_LRO = 2
PANGO_BIDI_TYPE_R = 3
PANGO_BIDI_TYPE_AL = 4
PANGO_BIDI_TYPE_RLE = 5
PANGO_BIDI_TYPE_RLO = 6
PANGO_BIDI_TYPE_PDF = 7
PANGO_BIDI_TYPE_EN = 8
PANGO_BIDI_TYPE_ES = 9
PANGO_BIDI_TYPE_ET = 10
PANGO_BIDI_TYPE_AN = 11
PANGO_BIDI_TYPE_CS = 12
PANGO_BIDI_TYPE_NSM = 13
PANGO_BIDI_TYPE_BN = 14
PANGO_BIDI_TYPE_B = 15
PANGO_BIDI_TYPE_S = 16
PANGO_BIDI_TYPE_WS = 17
PANGO_BIDI_TYPE_ON = 18
PangoBidiType = enum_anon_6 	# pango-new.h:347
enum_anon_7 = c_int
PANGO_DIRECTION_LTR = 0
PANGO_DIRECTION_RTL = 1
PANGO_DIRECTION_TTB_LTR = 2
PANGO_DIRECTION_TTB_RTL = 3
PANGO_DIRECTION_WEAK_LTR = 4
PANGO_DIRECTION_WEAK_RTL = 5
PANGO_DIRECTION_NEUTRAL = 6
PangoDirection = enum_anon_7 	# pango-new.h:358
class struct__PangoFontDescription(Structure):
    __slots__ = [
    ]
struct__PangoFontDescription._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoFontDescription(Structure):
    __slots__ = [
    ]
struct__PangoFontDescription._fields_ = [
    ('_opaque_struct', c_int)
]

PangoFontDescription = struct__PangoFontDescription 	# pango-new.h:378
class struct__PangoFontMetrics(Structure):
    __slots__ = [
    ]
struct__PangoFontMetrics._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoFontMetrics(Structure):
    __slots__ = [
    ]
struct__PangoFontMetrics._fields_ = [
    ('_opaque_struct', c_int)
]

PangoFontMetrics = struct__PangoFontMetrics 	# pango-new.h:379
enum_anon_8 = c_int
PANGO_STYLE_NORMAL = 0
PANGO_STYLE_OBLIQUE = 1
PANGO_STYLE_ITALIC = 2
PangoStyle = enum_anon_8 	# pango-new.h:384
enum_anon_9 = c_int
PANGO_VARIANT_NORMAL = 0
PANGO_VARIANT_SMALL_CAPS = 1
PangoVariant = enum_anon_9 	# pango-new.h:389
enum_anon_10 = c_int
PANGO_WEIGHT_THIN = 100
PANGO_WEIGHT_ULTRALIGHT = 200
PANGO_WEIGHT_LIGHT = 300
PANGO_WEIGHT_BOOK = 380
PANGO_WEIGHT_NORMAL = 400
PANGO_WEIGHT_MEDIUM = 500
PANGO_WEIGHT_SEMIBOLD = 600
PANGO_WEIGHT_BOLD = 700
PANGO_WEIGHT_ULTRABOLD = 800
PANGO_WEIGHT_HEAVY = 900
PANGO_WEIGHT_ULTRAHEAVY = 1000
PangoWeight = enum_anon_10 	# pango-new.h:403
enum_anon_11 = c_int
PANGO_STRETCH_ULTRA_CONDENSED = 0
PANGO_STRETCH_EXTRA_CONDENSED = 1
PANGO_STRETCH_CONDENSED = 2
PANGO_STRETCH_SEMI_CONDENSED = 3
PANGO_STRETCH_NORMAL = 4
PANGO_STRETCH_SEMI_EXPANDED = 5
PANGO_STRETCH_EXPANDED = 6
PANGO_STRETCH_EXTRA_EXPANDED = 7
PANGO_STRETCH_ULTRA_EXPANDED = 8
PangoStretch = enum_anon_11 	# pango-new.h:415
enum_anon_12 = c_int
PANGO_FONT_MASK_FAMILY = 1
PANGO_FONT_MASK_STYLE = 2
PANGO_FONT_MASK_VARIANT = 4
PANGO_FONT_MASK_WEIGHT = 8
PANGO_FONT_MASK_STRETCH = 16
PANGO_FONT_MASK_SIZE = 32
PANGO_FONT_MASK_GRAVITY = 64
PangoFontMask = enum_anon_12 	# pango-new.h:425
# pango-new.h:427
pango_font_description_new = _lib.pango_font_description_new
pango_font_description_new.restype = POINTER(PangoFontDescription)
pango_font_description_new.argtypes = []

# pango-new.h:428
pango_font_description_copy = _lib.pango_font_description_copy
pango_font_description_copy.restype = POINTER(PangoFontDescription)
pango_font_description_copy.argtypes = [POINTER(PangoFontDescription)]

# pango-new.h:429
pango_font_description_copy_static = _lib.pango_font_description_copy_static
pango_font_description_copy_static.restype = POINTER(PangoFontDescription)
pango_font_description_copy_static.argtypes = [POINTER(PangoFontDescription)]

# pango-new.h:433
pango_font_description_free = _lib.pango_font_description_free
pango_font_description_free.restype = None
pango_font_description_free.argtypes = [POINTER(PangoFontDescription)]

# pango-new.h:434
pango_font_descriptions_free = _lib.pango_font_descriptions_free
pango_font_descriptions_free.restype = None
pango_font_descriptions_free.argtypes = [POINTER(POINTER(PangoFontDescription)), c_int]

# pango-new.h:437
pango_font_description_set_family = _lib.pango_font_description_set_family
pango_font_description_set_family.restype = None
pango_font_description_set_family.argtypes = [POINTER(PangoFontDescription), c_char_p]

# pango-new.h:439
pango_font_description_set_family_static = _lib.pango_font_description_set_family_static
pango_font_description_set_family_static.restype = None
pango_font_description_set_family_static.argtypes = [POINTER(PangoFontDescription), c_char_p]

# pango-new.h:441
pango_font_description_get_family = _lib.pango_font_description_get_family
pango_font_description_get_family.restype = c_char_p
pango_font_description_get_family.argtypes = [POINTER(PangoFontDescription)]

# pango-new.h:442
pango_font_description_set_style = _lib.pango_font_description_set_style
pango_font_description_set_style.restype = None
pango_font_description_set_style.argtypes = [POINTER(PangoFontDescription), PangoStyle]

# pango-new.h:444
pango_font_description_get_style = _lib.pango_font_description_get_style
pango_font_description_get_style.restype = PangoStyle
pango_font_description_get_style.argtypes = [POINTER(PangoFontDescription)]

# pango-new.h:445
pango_font_description_set_variant = _lib.pango_font_description_set_variant
pango_font_description_set_variant.restype = None
pango_font_description_set_variant.argtypes = [POINTER(PangoFontDescription), PangoVariant]

# pango-new.h:447
pango_font_description_get_variant = _lib.pango_font_description_get_variant
pango_font_description_get_variant.restype = PangoVariant
pango_font_description_get_variant.argtypes = [POINTER(PangoFontDescription)]

# pango-new.h:448
pango_font_description_set_weight = _lib.pango_font_description_set_weight
pango_font_description_set_weight.restype = None
pango_font_description_set_weight.argtypes = [POINTER(PangoFontDescription), PangoWeight]

# pango-new.h:450
pango_font_description_get_weight = _lib.pango_font_description_get_weight
pango_font_description_get_weight.restype = PangoWeight
pango_font_description_get_weight.argtypes = [POINTER(PangoFontDescription)]

# pango-new.h:451
pango_font_description_set_stretch = _lib.pango_font_description_set_stretch
pango_font_description_set_stretch.restype = None
pango_font_description_set_stretch.argtypes = [POINTER(PangoFontDescription), PangoStretch]

# pango-new.h:453
pango_font_description_get_stretch = _lib.pango_font_description_get_stretch
pango_font_description_get_stretch.restype = PangoStretch
pango_font_description_get_stretch.argtypes = [POINTER(PangoFontDescription)]

# pango-new.h:457
pango_font_description_set_absolute_size = _lib.pango_font_description_set_absolute_size
pango_font_description_set_absolute_size.restype = None
pango_font_description_set_absolute_size.argtypes = [POINTER(PangoFontDescription), c_double]

# pango-new.h:460
pango_font_description_set_gravity = _lib.pango_font_description_set_gravity
pango_font_description_set_gravity.restype = None
pango_font_description_set_gravity.argtypes = [POINTER(PangoFontDescription), PangoGravity]

# pango-new.h:462
pango_font_description_get_gravity = _lib.pango_font_description_get_gravity
pango_font_description_get_gravity.restype = PangoGravity
pango_font_description_get_gravity.argtypes = [POINTER(PangoFontDescription)]

# pango-new.h:464
pango_font_description_get_set_fields = _lib.pango_font_description_get_set_fields
pango_font_description_get_set_fields.restype = PangoFontMask
pango_font_description_get_set_fields.argtypes = [POINTER(PangoFontDescription)]

# pango-new.h:465
pango_font_description_unset_fields = _lib.pango_font_description_unset_fields
pango_font_description_unset_fields.restype = None
pango_font_description_unset_fields.argtypes = [POINTER(PangoFontDescription), PangoFontMask]

# pango-new.h:479
pango_font_description_from_string = _lib.pango_font_description_from_string
pango_font_description_from_string.restype = POINTER(PangoFontDescription)
pango_font_description_from_string.argtypes = [c_char_p]

# pango-new.h:480
pango_font_description_to_string = _lib.pango_font_description_to_string
pango_font_description_to_string.restype = c_char_p
pango_font_description_to_string.argtypes = [POINTER(PangoFontDescription)]

# pango-new.h:481
pango_font_description_to_filename = _lib.pango_font_description_to_filename
pango_font_description_to_filename.restype = c_char_p
pango_font_description_to_filename.argtypes = [POINTER(PangoFontDescription)]

# pango-new.h:489
pango_font_metrics_ref = _lib.pango_font_metrics_ref
pango_font_metrics_ref.restype = POINTER(PangoFontMetrics)
pango_font_metrics_ref.argtypes = [POINTER(PangoFontMetrics)]

# pango-new.h:490
pango_font_metrics_unref = _lib.pango_font_metrics_unref
pango_font_metrics_unref.restype = None
pango_font_metrics_unref.argtypes = [POINTER(PangoFontMetrics)]

# pango-new.h:491
pango_font_metrics_get_ascent = _lib.pango_font_metrics_get_ascent
pango_font_metrics_get_ascent.restype = c_int
pango_font_metrics_get_ascent.argtypes = [POINTER(PangoFontMetrics)]

# pango-new.h:492
pango_font_metrics_get_descent = _lib.pango_font_metrics_get_descent
pango_font_metrics_get_descent.restype = c_int
pango_font_metrics_get_descent.argtypes = [POINTER(PangoFontMetrics)]

# pango-new.h:493
pango_font_metrics_get_approximate_char_width = _lib.pango_font_metrics_get_approximate_char_width
pango_font_metrics_get_approximate_char_width.restype = c_int
pango_font_metrics_get_approximate_char_width.argtypes = [POINTER(PangoFontMetrics)]

# pango-new.h:494
pango_font_metrics_get_approximate_digit_width = _lib.pango_font_metrics_get_approximate_digit_width
pango_font_metrics_get_approximate_digit_width.restype = c_int
pango_font_metrics_get_approximate_digit_width.argtypes = [POINTER(PangoFontMetrics)]

# pango-new.h:495
pango_font_metrics_get_underline_position = _lib.pango_font_metrics_get_underline_position
pango_font_metrics_get_underline_position.restype = c_int
pango_font_metrics_get_underline_position.argtypes = [POINTER(PangoFontMetrics)]

# pango-new.h:496
pango_font_metrics_get_underline_thickness = _lib.pango_font_metrics_get_underline_thickness
pango_font_metrics_get_underline_thickness.restype = c_int
pango_font_metrics_get_underline_thickness.argtypes = [POINTER(PangoFontMetrics)]

# pango-new.h:497
pango_font_metrics_get_strikethrough_position = _lib.pango_font_metrics_get_strikethrough_position
pango_font_metrics_get_strikethrough_position.restype = c_int
pango_font_metrics_get_strikethrough_position.argtypes = [POINTER(PangoFontMetrics)]

# pango-new.h:498
pango_font_metrics_get_strikethrough_thickness = _lib.pango_font_metrics_get_strikethrough_thickness
pango_font_metrics_get_strikethrough_thickness.restype = c_int
pango_font_metrics_get_strikethrough_thickness.argtypes = [POINTER(PangoFontMetrics)]

class struct__PangoFontFamily(Structure):
    __slots__ = [
    ]
struct__PangoFontFamily._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoFontFamily(Structure):
    __slots__ = [
    ]
struct__PangoFontFamily._fields_ = [
    ('_opaque_struct', c_int)
]

PangoFontFamily = struct__PangoFontFamily 	# pango-new.h:499
class struct__PangoFontFace(Structure):
    __slots__ = [
    ]
struct__PangoFontFace._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoFontFace(Structure):
    __slots__ = [
    ]
struct__PangoFontFace._fields_ = [
    ('_opaque_struct', c_int)
]

PangoFontFace = struct__PangoFontFace 	# pango-new.h:500
# pango-new.h:504
pango_font_family_list_faces = _lib.pango_font_family_list_faces
pango_font_family_list_faces.restype = None
pango_font_family_list_faces.argtypes = [POINTER(PangoFontFamily), POINTER(POINTER(POINTER(PangoFontFace))), POINTER(c_int)]

# pango-new.h:507
pango_font_family_get_name = _lib.pango_font_family_get_name
pango_font_family_get_name.restype = c_char_p
pango_font_family_get_name.argtypes = [POINTER(PangoFontFamily)]

# pango-new.h:511
pango_font_face_describe = _lib.pango_font_face_describe
pango_font_face_describe.restype = POINTER(PangoFontDescription)
pango_font_face_describe.argtypes = [POINTER(PangoFontFace)]

# pango-new.h:512
pango_font_face_get_face_name = _lib.pango_font_face_get_face_name
pango_font_face_get_face_name.restype = c_char_p
pango_font_face_get_face_name.argtypes = [POINTER(PangoFontFace)]

# pango-new.h:513
pango_font_face_list_sizes = _lib.pango_font_face_list_sizes
pango_font_face_list_sizes.restype = None
pango_font_face_list_sizes.argtypes = [POINTER(PangoFontFace), POINTER(POINTER(c_int)), POINTER(c_int)]

# pango-new.h:519
pango_font_describe = _lib.pango_font_describe
pango_font_describe.restype = POINTER(PangoFontDescription)
pango_font_describe.argtypes = [POINTER(PangoFont)]

# pango-new.h:520
pango_font_describe_with_absolute_size = _lib.pango_font_describe_with_absolute_size
pango_font_describe_with_absolute_size.restype = POINTER(PangoFontDescription)
pango_font_describe_with_absolute_size.argtypes = [POINTER(PangoFont)]

# pango-new.h:521
pango_font_get_coverage = _lib.pango_font_get_coverage
pango_font_get_coverage.restype = POINTER(PangoCoverage)
pango_font_get_coverage.argtypes = [POINTER(PangoFont), POINTER(PangoLanguage)]

# pango-new.h:523
pango_font_find_shaper = _lib.pango_font_find_shaper
pango_font_find_shaper.restype = POINTER(PangoEngineShape)
pango_font_find_shaper.argtypes = [POINTER(PangoFont), POINTER(PangoLanguage), guint32]

# pango-new.h:526
pango_font_get_metrics = _lib.pango_font_get_metrics
pango_font_get_metrics.restype = POINTER(PangoFontMetrics)
pango_font_get_metrics.argtypes = [POINTER(PangoFont), POINTER(PangoLanguage)]

# pango-new.h:528
pango_font_get_glyph_extents = _lib.pango_font_get_glyph_extents
pango_font_get_glyph_extents.restype = None
pango_font_get_glyph_extents.argtypes = [POINTER(PangoFont), PangoGlyph, POINTER(PangoRectangle), POINTER(PangoRectangle)]

# pango-new.h:532
pango_font_get_font_map = _lib.pango_font_get_font_map
pango_font_get_font_map.restype = POINTER(PangoFontMap)
pango_font_get_font_map.argtypes = [POINTER(PangoFont)]

class struct__PangoColor(Structure):
    __slots__ = [
    ]
struct__PangoColor._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoColor(Structure):
    __slots__ = [
    ]
struct__PangoColor._fields_ = [
    ('_opaque_struct', c_int)
]

PangoColor = struct__PangoColor 	# pango-new.h:540
# pango-new.h:552
pango_color_copy = _lib.pango_color_copy
pango_color_copy.restype = POINTER(PangoColor)
pango_color_copy.argtypes = [POINTER(PangoColor)]

# pango-new.h:553
pango_color_free = _lib.pango_color_free
pango_color_free.restype = None
pango_color_free.argtypes = [POINTER(PangoColor)]

class struct__PangoAttribute(Structure):
    __slots__ = [
    ]
struct__PangoAttribute._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoAttribute(Structure):
    __slots__ = [
    ]
struct__PangoAttribute._fields_ = [
    ('_opaque_struct', c_int)
]

PangoAttribute = struct__PangoAttribute 	# pango-new.h:561
class struct__PangoAttrClass(Structure):
    __slots__ = [
    ]
struct__PangoAttrClass._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoAttrClass(Structure):
    __slots__ = [
    ]
struct__PangoAttrClass._fields_ = [
    ('_opaque_struct', c_int)
]

PangoAttrClass = struct__PangoAttrClass 	# pango-new.h:562
class struct__PangoAttrString(Structure):
    __slots__ = [
    ]
struct__PangoAttrString._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoAttrString(Structure):
    __slots__ = [
    ]
struct__PangoAttrString._fields_ = [
    ('_opaque_struct', c_int)
]

PangoAttrString = struct__PangoAttrString 	# pango-new.h:564
class struct__PangoAttrLanguage(Structure):
    __slots__ = [
    ]
struct__PangoAttrLanguage._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoAttrLanguage(Structure):
    __slots__ = [
    ]
struct__PangoAttrLanguage._fields_ = [
    ('_opaque_struct', c_int)
]

PangoAttrLanguage = struct__PangoAttrLanguage 	# pango-new.h:565
class struct__PangoAttrInt(Structure):
    __slots__ = [
    ]
struct__PangoAttrInt._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoAttrInt(Structure):
    __slots__ = [
    ]
struct__PangoAttrInt._fields_ = [
    ('_opaque_struct', c_int)
]

PangoAttrInt = struct__PangoAttrInt 	# pango-new.h:566
class struct__PangoAttrSize(Structure):
    __slots__ = [
    ]
struct__PangoAttrSize._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoAttrSize(Structure):
    __slots__ = [
    ]
struct__PangoAttrSize._fields_ = [
    ('_opaque_struct', c_int)
]

PangoAttrSize = struct__PangoAttrSize 	# pango-new.h:567
class struct__PangoAttrFloat(Structure):
    __slots__ = [
    ]
struct__PangoAttrFloat._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoAttrFloat(Structure):
    __slots__ = [
    ]
struct__PangoAttrFloat._fields_ = [
    ('_opaque_struct', c_int)
]

PangoAttrFloat = struct__PangoAttrFloat 	# pango-new.h:568
class struct__PangoAttrColor(Structure):
    __slots__ = [
    ]
struct__PangoAttrColor._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoAttrColor(Structure):
    __slots__ = [
    ]
struct__PangoAttrColor._fields_ = [
    ('_opaque_struct', c_int)
]

PangoAttrColor = struct__PangoAttrColor 	# pango-new.h:569
class struct__PangoAttrFontDesc(Structure):
    __slots__ = [
    ]
struct__PangoAttrFontDesc._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoAttrFontDesc(Structure):
    __slots__ = [
    ]
struct__PangoAttrFontDesc._fields_ = [
    ('_opaque_struct', c_int)
]

PangoAttrFontDesc = struct__PangoAttrFontDesc 	# pango-new.h:570
class struct__PangoAttrShape(Structure):
    __slots__ = [
    ]
struct__PangoAttrShape._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoAttrShape(Structure):
    __slots__ = [
    ]
struct__PangoAttrShape._fields_ = [
    ('_opaque_struct', c_int)
]

PangoAttrShape = struct__PangoAttrShape 	# pango-new.h:571
class struct__PangoAttrList(Structure):
    __slots__ = [
    ]
struct__PangoAttrList._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoAttrList(Structure):
    __slots__ = [
    ]
struct__PangoAttrList._fields_ = [
    ('_opaque_struct', c_int)
]

PangoAttrList = struct__PangoAttrList 	# pango-new.h:574
class struct__PangoAttrIterator(Structure):
    __slots__ = [
    ]
struct__PangoAttrIterator._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoAttrIterator(Structure):
    __slots__ = [
    ]
struct__PangoAttrIterator._fields_ = [
    ('_opaque_struct', c_int)
]

PangoAttrIterator = struct__PangoAttrIterator 	# pango-new.h:575
enum_anon_13 = c_int
PANGO_ATTR_INVALID = 0
PANGO_ATTR_LANGUAGE = 1
PANGO_ATTR_FAMILY = 2
PANGO_ATTR_STYLE = 3
PANGO_ATTR_WEIGHT = 4
PANGO_ATTR_VARIANT = 5
PANGO_ATTR_STRETCH = 6
PANGO_ATTR_SIZE = 7
PANGO_ATTR_FONT_DESC = 8
PANGO_ATTR_FOREGROUND = 9
PANGO_ATTR_BACKGROUND = 10
PANGO_ATTR_UNDERLINE = 11
PANGO_ATTR_STRIKETHROUGH = 12
PANGO_ATTR_RISE = 13
PANGO_ATTR_SHAPE = 14
PANGO_ATTR_SCALE = 15
PANGO_ATTR_FALLBACK = 16
PANGO_ATTR_LETTER_SPACING = 17
PANGO_ATTR_UNDERLINE_COLOR = 18
PANGO_ATTR_STRIKETHROUGH_COLOR = 19
PANGO_ATTR_ABSOLUTE_SIZE = 20
PANGO_ATTR_GRAVITY = 21
PANGO_ATTR_GRAVITY_HINT = 22
PangoAttrType = enum_anon_13 	# pango-new.h:602
enum_anon_14 = c_int
PANGO_UNDERLINE_NONE = 0
PANGO_UNDERLINE_SINGLE = 1
PANGO_UNDERLINE_DOUBLE = 2
PANGO_UNDERLINE_LOW = 3
PANGO_UNDERLINE_ERROR = 4
PangoUnderline = enum_anon_14 	# pango-new.h:610
# pango-new.h:691
pango_attr_type_get_name = _lib.pango_attr_type_get_name
pango_attr_type_get_name.restype = c_char_p
pango_attr_type_get_name.argtypes = [PangoAttrType]

# pango-new.h:693
pango_attribute_init = _lib.pango_attribute_init
pango_attribute_init.restype = None
pango_attribute_init.argtypes = [POINTER(PangoAttribute), POINTER(PangoAttrClass)]

# pango-new.h:695
pango_attribute_copy = _lib.pango_attribute_copy
pango_attribute_copy.restype = POINTER(PangoAttribute)
pango_attribute_copy.argtypes = [POINTER(PangoAttribute)]

# pango-new.h:696
pango_attribute_destroy = _lib.pango_attribute_destroy
pango_attribute_destroy.restype = None
pango_attribute_destroy.argtypes = [POINTER(PangoAttribute)]

# pango-new.h:700
pango_attr_language_new = _lib.pango_attr_language_new
pango_attr_language_new.restype = POINTER(PangoAttribute)
pango_attr_language_new.argtypes = [POINTER(PangoLanguage)]

# pango-new.h:701
pango_attr_family_new = _lib.pango_attr_family_new
pango_attr_family_new.restype = POINTER(PangoAttribute)
pango_attr_family_new.argtypes = [c_char_p]

# pango-new.h:702
pango_attr_foreground_new = _lib.pango_attr_foreground_new
pango_attr_foreground_new.restype = POINTER(PangoAttribute)
pango_attr_foreground_new.argtypes = [guint16, guint16, guint16]

# pango-new.h:705
pango_attr_background_new = _lib.pango_attr_background_new
pango_attr_background_new.restype = POINTER(PangoAttribute)
pango_attr_background_new.argtypes = [guint16, guint16, guint16]

# pango-new.h:708
pango_attr_size_new = _lib.pango_attr_size_new
pango_attr_size_new.restype = POINTER(PangoAttribute)
pango_attr_size_new.argtypes = [c_int]

# pango-new.h:709
pango_attr_size_new_absolute = _lib.pango_attr_size_new_absolute
pango_attr_size_new_absolute.restype = POINTER(PangoAttribute)
pango_attr_size_new_absolute.argtypes = [c_int]

# pango-new.h:710
pango_attr_style_new = _lib.pango_attr_style_new
pango_attr_style_new.restype = POINTER(PangoAttribute)
pango_attr_style_new.argtypes = [PangoStyle]

# pango-new.h:711
pango_attr_weight_new = _lib.pango_attr_weight_new
pango_attr_weight_new.restype = POINTER(PangoAttribute)
pango_attr_weight_new.argtypes = [PangoWeight]

# pango-new.h:712
pango_attr_variant_new = _lib.pango_attr_variant_new
pango_attr_variant_new.restype = POINTER(PangoAttribute)
pango_attr_variant_new.argtypes = [PangoVariant]

# pango-new.h:713
pango_attr_stretch_new = _lib.pango_attr_stretch_new
pango_attr_stretch_new.restype = POINTER(PangoAttribute)
pango_attr_stretch_new.argtypes = [PangoStretch]

# pango-new.h:714
pango_attr_font_desc_new = _lib.pango_attr_font_desc_new
pango_attr_font_desc_new.restype = POINTER(PangoAttribute)
pango_attr_font_desc_new.argtypes = [POINTER(PangoFontDescription)]

# pango-new.h:716
pango_attr_underline_new = _lib.pango_attr_underline_new
pango_attr_underline_new.restype = POINTER(PangoAttribute)
pango_attr_underline_new.argtypes = [PangoUnderline]

# pango-new.h:717
pango_attr_underline_color_new = _lib.pango_attr_underline_color_new
pango_attr_underline_color_new.restype = POINTER(PangoAttribute)
pango_attr_underline_color_new.argtypes = [guint16, guint16, guint16]

# pango-new.h:721
pango_attr_strikethrough_color_new = _lib.pango_attr_strikethrough_color_new
pango_attr_strikethrough_color_new.restype = POINTER(PangoAttribute)
pango_attr_strikethrough_color_new.argtypes = [guint16, guint16, guint16]

# pango-new.h:725
pango_attr_rise_new = _lib.pango_attr_rise_new
pango_attr_rise_new.restype = POINTER(PangoAttribute)
pango_attr_rise_new.argtypes = [c_int]

# pango-new.h:726
pango_attr_scale_new = _lib.pango_attr_scale_new
pango_attr_scale_new.restype = POINTER(PangoAttribute)
pango_attr_scale_new.argtypes = [c_double]

# pango-new.h:728
pango_attr_letter_spacing_new = _lib.pango_attr_letter_spacing_new
pango_attr_letter_spacing_new.restype = POINTER(PangoAttribute)
pango_attr_letter_spacing_new.argtypes = [c_int]

# pango-new.h:730
pango_attr_shape_new = _lib.pango_attr_shape_new
pango_attr_shape_new.restype = POINTER(PangoAttribute)
pango_attr_shape_new.argtypes = [POINTER(PangoRectangle), POINTER(PangoRectangle)]

# pango-new.h:738
pango_attr_gravity_new = _lib.pango_attr_gravity_new
pango_attr_gravity_new.restype = POINTER(PangoAttribute)
pango_attr_gravity_new.argtypes = [PangoGravity]

# pango-new.h:739
pango_attr_gravity_hint_new = _lib.pango_attr_gravity_hint_new
pango_attr_gravity_hint_new.restype = POINTER(PangoAttribute)
pango_attr_gravity_hint_new.argtypes = [PangoGravityHint]

# pango-new.h:742
pango_attr_list_new = _lib.pango_attr_list_new
pango_attr_list_new.restype = POINTER(PangoAttrList)
pango_attr_list_new.argtypes = []

# pango-new.h:743
pango_attr_list_ref = _lib.pango_attr_list_ref
pango_attr_list_ref.restype = POINTER(PangoAttrList)
pango_attr_list_ref.argtypes = [POINTER(PangoAttrList)]

# pango-new.h:744
pango_attr_list_unref = _lib.pango_attr_list_unref
pango_attr_list_unref.restype = None
pango_attr_list_unref.argtypes = [POINTER(PangoAttrList)]

# pango-new.h:745
pango_attr_list_copy = _lib.pango_attr_list_copy
pango_attr_list_copy.restype = POINTER(PangoAttrList)
pango_attr_list_copy.argtypes = [POINTER(PangoAttrList)]

# pango-new.h:746
pango_attr_list_insert = _lib.pango_attr_list_insert
pango_attr_list_insert.restype = None
pango_attr_list_insert.argtypes = [POINTER(PangoAttrList), POINTER(PangoAttribute)]

# pango-new.h:748
pango_attr_list_insert_before = _lib.pango_attr_list_insert_before
pango_attr_list_insert_before.restype = None
pango_attr_list_insert_before.argtypes = [POINTER(PangoAttrList), POINTER(PangoAttribute)]

# pango-new.h:750
pango_attr_list_change = _lib.pango_attr_list_change
pango_attr_list_change.restype = None
pango_attr_list_change.argtypes = [POINTER(PangoAttrList), POINTER(PangoAttribute)]

# pango-new.h:761
pango_attr_list_get_iterator = _lib.pango_attr_list_get_iterator
pango_attr_list_get_iterator.restype = POINTER(PangoAttrIterator)
pango_attr_list_get_iterator.argtypes = [POINTER(PangoAttrList)]

# pango-new.h:767
pango_attr_iterator_copy = _lib.pango_attr_iterator_copy
pango_attr_iterator_copy.restype = POINTER(PangoAttrIterator)
pango_attr_iterator_copy.argtypes = [POINTER(PangoAttrIterator)]

# pango-new.h:768
pango_attr_iterator_destroy = _lib.pango_attr_iterator_destroy
pango_attr_iterator_destroy.restype = None
pango_attr_iterator_destroy.argtypes = [POINTER(PangoAttrIterator)]

# pango-new.h:769
pango_attr_iterator_get = _lib.pango_attr_iterator_get
pango_attr_iterator_get.restype = POINTER(PangoAttribute)
pango_attr_iterator_get.argtypes = [POINTER(PangoAttrIterator), PangoAttrType]

class struct__PangoAnalysis(Structure):
    __slots__ = [
    ]
struct__PangoAnalysis._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoAnalysis(Structure):
    __slots__ = [
    ]
struct__PangoAnalysis._fields_ = [
    ('_opaque_struct', c_int)
]

PangoAnalysis = struct__PangoAnalysis 	# pango-new.h:792
class struct__PangoItem(Structure):
    __slots__ = [
    ]
struct__PangoItem._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoItem(Structure):
    __slots__ = [
    ]
struct__PangoItem._fields_ = [
    ('_opaque_struct', c_int)
]

PangoItem = struct__PangoItem 	# pango-new.h:793
# pango-new.h:826
pango_item_new = _lib.pango_item_new
pango_item_new.restype = POINTER(PangoItem)
pango_item_new.argtypes = []

# pango-new.h:827
pango_item_copy = _lib.pango_item_copy
pango_item_copy.restype = POINTER(PangoItem)
pango_item_copy.argtypes = [POINTER(PangoItem)]

# pango-new.h:828
pango_item_free = _lib.pango_item_free
pango_item_free.restype = None
pango_item_free.argtypes = [POINTER(PangoItem)]

# pango-new.h:829
pango_item_split = _lib.pango_item_split
pango_item_split.restype = POINTER(PangoItem)
pango_item_split.argtypes = [POINTER(PangoItem), c_int, c_int]

# pango-new.h:891
pango_get_log_attrs = _lib.pango_get_log_attrs
pango_get_log_attrs.restype = None
pango_get_log_attrs.argtypes = [c_char_p, c_int, c_int, POINTER(PangoLanguage), POINTER(PangoLogAttr), c_int]

class struct__PangoFontset(Structure):
    __slots__ = [
    ]
struct__PangoFontset._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoFontset(Structure):
    __slots__ = [
    ]
struct__PangoFontset._fields_ = [
    ('_opaque_struct', c_int)
]

PangoFontset = struct__PangoFontset 	# pango-new.h:901
# pango-new.h:908
pango_fontset_get_metrics = _lib.pango_fontset_get_metrics
pango_fontset_get_metrics.restype = POINTER(PangoFontMetrics)
pango_fontset_get_metrics.argtypes = [POINTER(PangoFontset)]

class struct__PangoContext(Structure):
    __slots__ = [
    ]
struct__PangoContext._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoContext(Structure):
    __slots__ = [
    ]
struct__PangoContext._fields_ = [
    ('_opaque_struct', c_int)
]

PangoContext = struct__PangoContext 	# pango-new.h:920
# pango-new.h:923
pango_font_map_create_context = _lib.pango_font_map_create_context
pango_font_map_create_context.restype = POINTER(PangoContext)
pango_font_map_create_context.argtypes = [POINTER(PangoFontMap)]

# pango-new.h:924
pango_font_map_load_font = _lib.pango_font_map_load_font
pango_font_map_load_font.restype = POINTER(PangoFont)
pango_font_map_load_font.argtypes = [POINTER(PangoFontMap), POINTER(PangoContext), POINTER(PangoFontDescription)]

# pango-new.h:927
pango_font_map_load_fontset = _lib.pango_font_map_load_fontset
pango_font_map_load_fontset.restype = POINTER(PangoFontset)
pango_font_map_load_fontset.argtypes = [POINTER(PangoFontMap), POINTER(PangoContext), POINTER(PangoFontDescription), POINTER(PangoLanguage)]

# pango-new.h:931
pango_font_map_list_families = _lib.pango_font_map_list_families
pango_font_map_list_families.restype = None
pango_font_map_list_families.argtypes = [POINTER(PangoFontMap), POINTER(POINTER(POINTER(PangoFontFamily))), POINTER(c_int)]

class struct__PangoContextClass(Structure):
    __slots__ = [
    ]
struct__PangoContextClass._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoContextClass(Structure):
    __slots__ = [
    ]
struct__PangoContextClass._fields_ = [
    ('_opaque_struct', c_int)
]

PangoContextClass = struct__PangoContextClass 	# pango-new.h:944
# pango-new.h:947
pango_context_new = _lib.pango_context_new
pango_context_new.restype = POINTER(PangoContext)
pango_context_new.argtypes = []

# pango-new.h:948
pango_context_set_font_map = _lib.pango_context_set_font_map
pango_context_set_font_map.restype = None
pango_context_set_font_map.argtypes = [POINTER(PangoContext), POINTER(PangoFontMap)]

# pango-new.h:950
pango_context_get_font_map = _lib.pango_context_get_font_map
pango_context_get_font_map.restype = POINTER(PangoFontMap)
pango_context_get_font_map.argtypes = [POINTER(PangoContext)]

# pango-new.h:952
pango_context_list_families = _lib.pango_context_list_families
pango_context_list_families.restype = None
pango_context_list_families.argtypes = [POINTER(PangoContext), POINTER(POINTER(POINTER(PangoFontFamily))), POINTER(c_int)]

# pango-new.h:955
pango_context_load_font = _lib.pango_context_load_font
pango_context_load_font.restype = POINTER(PangoFont)
pango_context_load_font.argtypes = [POINTER(PangoContext), POINTER(PangoFontDescription)]

# pango-new.h:957
pango_context_load_fontset = _lib.pango_context_load_fontset
pango_context_load_fontset.restype = POINTER(PangoFontset)
pango_context_load_fontset.argtypes = [POINTER(PangoContext), POINTER(PangoFontDescription), POINTER(PangoLanguage)]

# pango-new.h:961
pango_context_get_metrics = _lib.pango_context_get_metrics
pango_context_get_metrics.restype = POINTER(PangoFontMetrics)
pango_context_get_metrics.argtypes = [POINTER(PangoContext), POINTER(PangoFontDescription), POINTER(PangoLanguage)]

# pango-new.h:965
pango_context_set_font_description = _lib.pango_context_set_font_description
pango_context_set_font_description.restype = None
pango_context_set_font_description.argtypes = [POINTER(PangoContext), POINTER(PangoFontDescription)]

# pango-new.h:967
pango_context_get_font_description = _lib.pango_context_get_font_description
pango_context_get_font_description.restype = POINTER(PangoFontDescription)
pango_context_get_font_description.argtypes = [POINTER(PangoContext)]

# pango-new.h:968
pango_context_get_language = _lib.pango_context_get_language
pango_context_get_language.restype = POINTER(PangoLanguage)
pango_context_get_language.argtypes = [POINTER(PangoContext)]

# pango-new.h:969
pango_context_set_language = _lib.pango_context_set_language
pango_context_set_language.restype = None
pango_context_set_language.argtypes = [POINTER(PangoContext), POINTER(PangoLanguage)]

# pango-new.h:971
pango_context_set_base_dir = _lib.pango_context_set_base_dir
pango_context_set_base_dir.restype = None
pango_context_set_base_dir.argtypes = [POINTER(PangoContext), PangoDirection]

# pango-new.h:973
pango_context_get_base_dir = _lib.pango_context_get_base_dir
pango_context_get_base_dir.restype = PangoDirection
pango_context_get_base_dir.argtypes = [POINTER(PangoContext)]

# pango-new.h:974
pango_context_set_base_gravity = _lib.pango_context_set_base_gravity
pango_context_set_base_gravity.restype = None
pango_context_set_base_gravity.argtypes = [POINTER(PangoContext), PangoGravity]

# pango-new.h:976
pango_context_get_base_gravity = _lib.pango_context_get_base_gravity
pango_context_get_base_gravity.restype = PangoGravity
pango_context_get_base_gravity.argtypes = [POINTER(PangoContext)]

# pango-new.h:977
pango_context_get_gravity = _lib.pango_context_get_gravity
pango_context_get_gravity.restype = PangoGravity
pango_context_get_gravity.argtypes = [POINTER(PangoContext)]

# pango-new.h:978
pango_context_set_gravity_hint = _lib.pango_context_set_gravity_hint
pango_context_set_gravity_hint.restype = None
pango_context_set_gravity_hint.argtypes = [POINTER(PangoContext), PangoGravityHint]

# pango-new.h:980
pango_context_get_gravity_hint = _lib.pango_context_get_gravity_hint
pango_context_get_gravity_hint.restype = PangoGravityHint
pango_context_get_gravity_hint.argtypes = [POINTER(PangoContext)]

# pango-new.h:982
pango_context_set_matrix = _lib.pango_context_set_matrix
pango_context_set_matrix.restype = None
pango_context_set_matrix.argtypes = [POINTER(PangoContext), POINTER(PangoMatrix)]

# pango-new.h:984
pango_context_get_matrix = _lib.pango_context_get_matrix
pango_context_get_matrix.restype = POINTER(PangoMatrix)
pango_context_get_matrix.argtypes = [POINTER(PangoContext)]

class struct__PangoGlyphGeometry(Structure):
    __slots__ = [
    ]
struct__PangoGlyphGeometry._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoGlyphGeometry(Structure):
    __slots__ = [
    ]
struct__PangoGlyphGeometry._fields_ = [
    ('_opaque_struct', c_int)
]

PangoGlyphGeometry = struct__PangoGlyphGeometry 	# pango-new.h:1008
class struct__PangoGlyphVisAttr(Structure):
    __slots__ = [
    ]
struct__PangoGlyphVisAttr._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoGlyphVisAttr(Structure):
    __slots__ = [
    ]
struct__PangoGlyphVisAttr._fields_ = [
    ('_opaque_struct', c_int)
]

PangoGlyphVisAttr = struct__PangoGlyphVisAttr 	# pango-new.h:1009
class struct__PangoGlyphInfo(Structure):
    __slots__ = [
    ]
struct__PangoGlyphInfo._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoGlyphInfo(Structure):
    __slots__ = [
    ]
struct__PangoGlyphInfo._fields_ = [
    ('_opaque_struct', c_int)
]

PangoGlyphInfo = struct__PangoGlyphInfo 	# pango-new.h:1010
class struct__PangoGlyphString(Structure):
    __slots__ = [
    ]
struct__PangoGlyphString._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoGlyphString(Structure):
    __slots__ = [
    ]
struct__PangoGlyphString._fields_ = [
    ('_opaque_struct', c_int)
]

PangoGlyphString = struct__PangoGlyphString 	# pango-new.h:1011
PangoGlyphUnit = gint32 	# pango-new.h:1014
# pango-new.h:1062
pango_glyph_string_new = _lib.pango_glyph_string_new
pango_glyph_string_new.restype = POINTER(PangoGlyphString)
pango_glyph_string_new.argtypes = []

# pango-new.h:1066
pango_glyph_string_copy = _lib.pango_glyph_string_copy
pango_glyph_string_copy.restype = POINTER(PangoGlyphString)
pango_glyph_string_copy.argtypes = [POINTER(PangoGlyphString)]

# pango-new.h:1067
pango_glyph_string_free = _lib.pango_glyph_string_free
pango_glyph_string_free.restype = None
pango_glyph_string_free.argtypes = [POINTER(PangoGlyphString)]

# pango-new.h:1068
pango_glyph_string_extents = _lib.pango_glyph_string_extents
pango_glyph_string_extents.restype = None
pango_glyph_string_extents.argtypes = [POINTER(PangoGlyphString), POINTER(PangoFont), POINTER(PangoRectangle), POINTER(PangoRectangle)]

# pango-new.h:1072
pango_glyph_string_get_width = _lib.pango_glyph_string_get_width
pango_glyph_string_get_width.restype = c_int
pango_glyph_string_get_width.argtypes = [POINTER(PangoGlyphString)]

# pango-new.h:1074
pango_glyph_string_extents_range = _lib.pango_glyph_string_extents_range
pango_glyph_string_extents_range.restype = None
pango_glyph_string_extents_range.argtypes = [POINTER(PangoGlyphString), c_int, c_int, POINTER(PangoFont), POINTER(PangoRectangle), POINTER(PangoRectangle)]

# pango-new.h:1081
pango_glyph_string_get_logical_widths = _lib.pango_glyph_string_get_logical_widths
pango_glyph_string_get_logical_widths.restype = None
pango_glyph_string_get_logical_widths.argtypes = [POINTER(PangoGlyphString), c_char_p, c_int, c_int, POINTER(c_int)]

# pango-new.h:1094
pango_glyph_string_x_to_index = _lib.pango_glyph_string_x_to_index
pango_glyph_string_x_to_index.restype = None
pango_glyph_string_x_to_index.argtypes = [POINTER(PangoGlyphString), c_char_p, c_int, POINTER(PangoAnalysis), c_int, POINTER(c_int), POINTER(c_int)]

class struct__PangoGlyphItem(Structure):
    __slots__ = [
    ]
struct__PangoGlyphItem._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoGlyphItem(Structure):
    __slots__ = [
    ]
struct__PangoGlyphItem._fields_ = [
    ('_opaque_struct', c_int)
]

PangoGlyphItem = struct__PangoGlyphItem 	# pango-new.h:1169
# pango-new.h:1181
pango_glyph_item_split = _lib.pango_glyph_item_split
pango_glyph_item_split.restype = POINTER(PangoGlyphItem)
pango_glyph_item_split.argtypes = [POINTER(PangoGlyphItem), c_char_p, c_int]

# pango-new.h:1184
pango_glyph_item_copy = _lib.pango_glyph_item_copy
pango_glyph_item_copy.restype = POINTER(PangoGlyphItem)
pango_glyph_item_copy.argtypes = [POINTER(PangoGlyphItem)]

# pango-new.h:1185
pango_glyph_item_free = _lib.pango_glyph_item_free
pango_glyph_item_free.restype = None
pango_glyph_item_free.argtypes = [POINTER(PangoGlyphItem)]

# pango-new.h:1189
pango_glyph_item_letter_space = _lib.pango_glyph_item_letter_space
pango_glyph_item_letter_space.restype = None
pango_glyph_item_letter_space.argtypes = [POINTER(PangoGlyphItem), c_char_p, POINTER(PangoLogAttr), c_int]

class struct__PangoGlyphItemIter(Structure):
    __slots__ = [
    ]
struct__PangoGlyphItemIter._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoGlyphItemIter(Structure):
    __slots__ = [
    ]
struct__PangoGlyphItemIter._fields_ = [
    ('_opaque_struct', c_int)
]

PangoGlyphItemIter = struct__PangoGlyphItemIter 	# pango-new.h:1195
# pango-new.h:1214
pango_glyph_item_iter_copy = _lib.pango_glyph_item_iter_copy
pango_glyph_item_iter_copy.restype = POINTER(PangoGlyphItemIter)
pango_glyph_item_iter_copy.argtypes = [POINTER(PangoGlyphItemIter)]

# pango-new.h:1215
pango_glyph_item_iter_free = _lib.pango_glyph_item_iter_free
pango_glyph_item_iter_free.restype = None
pango_glyph_item_iter_free.argtypes = [POINTER(PangoGlyphItemIter)]

class struct__PangoTabArray(Structure):
    __slots__ = [
    ]
struct__PangoTabArray._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoTabArray(Structure):
    __slots__ = [
    ]
struct__PangoTabArray._fields_ = [
    ('_opaque_struct', c_int)
]

PangoTabArray = struct__PangoTabArray 	# pango-new.h:1231
enum_anon_15 = c_int
PANGO_TAB_LEFT = 0
PangoTabAlign = enum_anon_15 	# pango-new.h:1236
# pango-new.h:1248
pango_tab_array_copy = _lib.pango_tab_array_copy
pango_tab_array_copy.restype = POINTER(PangoTabArray)
pango_tab_array_copy.argtypes = [POINTER(PangoTabArray)]

# pango-new.h:1249
pango_tab_array_free = _lib.pango_tab_array_free
pango_tab_array_free.restype = None
pango_tab_array_free.argtypes = [POINTER(PangoTabArray)]

class struct__PangoLayout(Structure):
    __slots__ = [
    ]
struct__PangoLayout._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoLayout(Structure):
    __slots__ = [
    ]
struct__PangoLayout._fields_ = [
    ('_opaque_struct', c_int)
]

PangoLayout = struct__PangoLayout 	# pango-new.h:1272
class struct__PangoLayoutClass(Structure):
    __slots__ = [
    ]
struct__PangoLayoutClass._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoLayoutClass(Structure):
    __slots__ = [
    ]
struct__PangoLayoutClass._fields_ = [
    ('_opaque_struct', c_int)
]

PangoLayoutClass = struct__PangoLayoutClass 	# pango-new.h:1273
class struct__PangoLayoutLine(Structure):
    __slots__ = [
    ]
struct__PangoLayoutLine._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoLayoutLine(Structure):
    __slots__ = [
    ]
struct__PangoLayoutLine._fields_ = [
    ('_opaque_struct', c_int)
]

PangoLayoutLine = struct__PangoLayoutLine 	# pango-new.h:1274
PangoLayoutRun = PangoGlyphItem 	# pango-new.h:1276
enum_anon_16 = c_int
PANGO_ALIGN_LEFT = 0
PANGO_ALIGN_CENTER = 1
PANGO_ALIGN_RIGHT = 2
PangoAlignment = enum_anon_16 	# pango-new.h:1282
enum_anon_17 = c_int
PANGO_WRAP_WORD = 0
PANGO_WRAP_CHAR = 1
PANGO_WRAP_WORD_CHAR = 2
PangoWrapMode = enum_anon_17 	# pango-new.h:1288
enum_anon_18 = c_int
PANGO_ELLIPSIZE_NONE = 0
PANGO_ELLIPSIZE_START = 1
PANGO_ELLIPSIZE_MIDDLE = 2
PANGO_ELLIPSIZE_END = 3
PangoEllipsizeMode = enum_anon_18 	# pango-new.h:1294
# pango-new.h:1306
pango_layout_new = _lib.pango_layout_new
pango_layout_new.restype = POINTER(PangoLayout)
pango_layout_new.argtypes = [POINTER(PangoContext)]

# pango-new.h:1307
pango_layout_copy = _lib.pango_layout_copy
pango_layout_copy.restype = POINTER(PangoLayout)
pango_layout_copy.argtypes = [POINTER(PangoLayout)]

# pango-new.h:1309
pango_layout_get_context = _lib.pango_layout_get_context
pango_layout_get_context.restype = POINTER(PangoContext)
pango_layout_get_context.argtypes = [POINTER(PangoLayout)]

# pango-new.h:1311
pango_layout_set_attributes = _lib.pango_layout_set_attributes
pango_layout_set_attributes.restype = None
pango_layout_set_attributes.argtypes = [POINTER(PangoLayout), POINTER(PangoAttrList)]

# pango-new.h:1313
pango_layout_get_attributes = _lib.pango_layout_get_attributes
pango_layout_get_attributes.restype = POINTER(PangoAttrList)
pango_layout_get_attributes.argtypes = [POINTER(PangoLayout)]

# pango-new.h:1315
pango_layout_set_text = _lib.pango_layout_set_text
pango_layout_set_text.restype = None
pango_layout_set_text.argtypes = [POINTER(PangoLayout), c_char_p, c_int]

# pango-new.h:1318
pango_layout_get_text = _lib.pango_layout_get_text
pango_layout_get_text.restype = c_char_p
pango_layout_get_text.argtypes = [POINTER(PangoLayout)]

# pango-new.h:1320
pango_layout_set_markup = _lib.pango_layout_set_markup
pango_layout_set_markup.restype = None
pango_layout_set_markup.argtypes = [POINTER(PangoLayout), c_char_p, c_int]

# pango-new.h:1330
pango_layout_set_font_description = _lib.pango_layout_set_font_description
pango_layout_set_font_description.restype = None
pango_layout_set_font_description.argtypes = [POINTER(PangoLayout), POINTER(PangoFontDescription)]

# pango-new.h:1333
pango_layout_get_font_description = _lib.pango_layout_get_font_description
pango_layout_get_font_description.restype = POINTER(PangoFontDescription)
pango_layout_get_font_description.argtypes = [POINTER(PangoLayout)]

# pango-new.h:1335
pango_layout_set_width = _lib.pango_layout_set_width
pango_layout_set_width.restype = None
pango_layout_set_width.argtypes = [POINTER(PangoLayout), c_int]

# pango-new.h:1337
pango_layout_get_width = _lib.pango_layout_get_width
pango_layout_get_width.restype = c_int
pango_layout_get_width.argtypes = [POINTER(PangoLayout)]

# pango-new.h:1338
pango_layout_set_height = _lib.pango_layout_set_height
pango_layout_set_height.restype = None
pango_layout_set_height.argtypes = [POINTER(PangoLayout), c_int]

# pango-new.h:1340
pango_layout_get_height = _lib.pango_layout_get_height
pango_layout_get_height.restype = c_int
pango_layout_get_height.argtypes = [POINTER(PangoLayout)]

# pango-new.h:1341
pango_layout_set_wrap = _lib.pango_layout_set_wrap
pango_layout_set_wrap.restype = None
pango_layout_set_wrap.argtypes = [POINTER(PangoLayout), PangoWrapMode]

# pango-new.h:1343
pango_layout_get_wrap = _lib.pango_layout_get_wrap
pango_layout_get_wrap.restype = PangoWrapMode
pango_layout_get_wrap.argtypes = [POINTER(PangoLayout)]

# pango-new.h:1345
pango_layout_set_indent = _lib.pango_layout_set_indent
pango_layout_set_indent.restype = None
pango_layout_set_indent.argtypes = [POINTER(PangoLayout), c_int]

# pango-new.h:1347
pango_layout_get_indent = _lib.pango_layout_get_indent
pango_layout_get_indent.restype = c_int
pango_layout_get_indent.argtypes = [POINTER(PangoLayout)]

# pango-new.h:1348
pango_layout_set_spacing = _lib.pango_layout_set_spacing
pango_layout_set_spacing.restype = None
pango_layout_set_spacing.argtypes = [POINTER(PangoLayout), c_int]

# pango-new.h:1350
pango_layout_get_spacing = _lib.pango_layout_get_spacing
pango_layout_get_spacing.restype = c_int
pango_layout_get_spacing.argtypes = [POINTER(PangoLayout)]

# pango-new.h:1357
pango_layout_set_alignment = _lib.pango_layout_set_alignment
pango_layout_set_alignment.restype = None
pango_layout_set_alignment.argtypes = [POINTER(PangoLayout), PangoAlignment]

# pango-new.h:1359
pango_layout_get_alignment = _lib.pango_layout_get_alignment
pango_layout_get_alignment.restype = PangoAlignment
pango_layout_get_alignment.argtypes = [POINTER(PangoLayout)]

# pango-new.h:1361
pango_layout_set_tabs = _lib.pango_layout_set_tabs
pango_layout_set_tabs.restype = None
pango_layout_set_tabs.argtypes = [POINTER(PangoLayout), POINTER(PangoTabArray)]

# pango-new.h:1364
pango_layout_get_tabs = _lib.pango_layout_get_tabs
pango_layout_get_tabs.restype = POINTER(PangoTabArray)
pango_layout_get_tabs.argtypes = [POINTER(PangoLayout)]

# pango-new.h:1370
pango_layout_set_ellipsize = _lib.pango_layout_set_ellipsize
pango_layout_set_ellipsize.restype = None
pango_layout_set_ellipsize.argtypes = [POINTER(PangoLayout), PangoEllipsizeMode]

# pango-new.h:1372
pango_layout_get_ellipsize = _lib.pango_layout_get_ellipsize
pango_layout_get_ellipsize.restype = PangoEllipsizeMode
pango_layout_get_ellipsize.argtypes = [POINTER(PangoLayout)]

# pango-new.h:1375
pango_layout_get_unknown_glyphs_count = _lib.pango_layout_get_unknown_glyphs_count
pango_layout_get_unknown_glyphs_count.restype = c_int
pango_layout_get_unknown_glyphs_count.argtypes = [POINTER(PangoLayout)]

# pango-new.h:1377
pango_layout_context_changed = _lib.pango_layout_context_changed
pango_layout_context_changed.restype = None
pango_layout_context_changed.argtypes = [POINTER(PangoLayout)]

# pango-new.h:1383
pango_layout_index_to_pos = _lib.pango_layout_index_to_pos
pango_layout_index_to_pos.restype = None
pango_layout_index_to_pos.argtypes = [POINTER(PangoLayout), c_int, POINTER(PangoRectangle)]

# pango-new.h:1391
pango_layout_get_cursor_pos = _lib.pango_layout_get_cursor_pos
pango_layout_get_cursor_pos.restype = None
pango_layout_get_cursor_pos.argtypes = [POINTER(PangoLayout), c_int, POINTER(PangoRectangle), POINTER(PangoRectangle)]

# pango-new.h:1407
pango_layout_get_extents = _lib.pango_layout_get_extents
pango_layout_get_extents.restype = None
pango_layout_get_extents.argtypes = [POINTER(PangoLayout), POINTER(PangoRectangle), POINTER(PangoRectangle)]

# pango-new.h:1410
pango_layout_get_pixel_extents = _lib.pango_layout_get_pixel_extents
pango_layout_get_pixel_extents.restype = None
pango_layout_get_pixel_extents.argtypes = [POINTER(PangoLayout), POINTER(PangoRectangle), POINTER(PangoRectangle)]

# pango-new.h:1413
pango_layout_get_size = _lib.pango_layout_get_size
pango_layout_get_size.restype = None
pango_layout_get_size.argtypes = [POINTER(PangoLayout), POINTER(c_int), POINTER(c_int)]

# pango-new.h:1416
pango_layout_get_pixel_size = _lib.pango_layout_get_pixel_size
pango_layout_get_pixel_size.restype = None
pango_layout_get_pixel_size.argtypes = [POINTER(PangoLayout), POINTER(c_int), POINTER(c_int)]

# pango-new.h:1419
pango_layout_get_baseline = _lib.pango_layout_get_baseline
pango_layout_get_baseline.restype = c_int
pango_layout_get_baseline.argtypes = [POINTER(PangoLayout)]

# pango-new.h:1421
pango_layout_get_line_count = _lib.pango_layout_get_line_count
pango_layout_get_line_count.restype = c_int
pango_layout_get_line_count.argtypes = [POINTER(PangoLayout)]

# pango-new.h:1422
pango_layout_get_line = _lib.pango_layout_get_line
pango_layout_get_line.restype = POINTER(PangoLayoutLine)
pango_layout_get_line.argtypes = [POINTER(PangoLayout), c_int]

# pango-new.h:1424
pango_layout_get_line_readonly = _lib.pango_layout_get_line_readonly
pango_layout_get_line_readonly.restype = POINTER(PangoLayoutLine)
pango_layout_get_line_readonly.argtypes = [POINTER(PangoLayout), c_int]

# pango-new.h:1434
pango_layout_line_ref = _lib.pango_layout_line_ref
pango_layout_line_ref.restype = POINTER(PangoLayoutLine)
pango_layout_line_ref.argtypes = [POINTER(PangoLayoutLine)]

# pango-new.h:1435
pango_layout_line_unref = _lib.pango_layout_line_unref
pango_layout_line_unref.restype = None
pango_layout_line_unref.argtypes = [POINTER(PangoLayoutLine)]

# pango-new.h:1445
pango_layout_line_get_x_ranges = _lib.pango_layout_line_get_x_ranges
pango_layout_line_get_x_ranges.restype = None
pango_layout_line_get_x_ranges.argtypes = [POINTER(PangoLayoutLine), c_int, c_int, POINTER(POINTER(c_int)), POINTER(c_int)]

# pango-new.h:1450
pango_layout_line_get_extents = _lib.pango_layout_line_get_extents
pango_layout_line_get_extents.restype = None
pango_layout_line_get_extents.argtypes = [POINTER(PangoLayoutLine), POINTER(PangoRectangle), POINTER(PangoRectangle)]

# pango-new.h:1453
pango_layout_line_get_pixel_extents = _lib.pango_layout_line_get_pixel_extents
pango_layout_line_get_pixel_extents.restype = None
pango_layout_line_get_pixel_extents.argtypes = [POINTER(PangoLayoutLine), POINTER(PangoRectangle), POINTER(PangoRectangle)]

class struct__PangoLayoutIter(Structure):
    __slots__ = [
    ]
struct__PangoLayoutIter._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoLayoutIter(Structure):
    __slots__ = [
    ]
struct__PangoLayoutIter._fields_ = [
    ('_opaque_struct', c_int)
]

PangoLayoutIter = struct__PangoLayoutIter 	# pango-new.h:1457
# pango-new.h:1463
pango_layout_get_iter = _lib.pango_layout_get_iter
pango_layout_get_iter.restype = POINTER(PangoLayoutIter)
pango_layout_get_iter.argtypes = [POINTER(PangoLayout)]

# pango-new.h:1464
pango_layout_iter_copy = _lib.pango_layout_iter_copy
pango_layout_iter_copy.restype = POINTER(PangoLayoutIter)
pango_layout_iter_copy.argtypes = [POINTER(PangoLayoutIter)]

# pango-new.h:1465
pango_layout_iter_free = _lib.pango_layout_iter_free
pango_layout_iter_free.restype = None
pango_layout_iter_free.argtypes = [POINTER(PangoLayoutIter)]

# pango-new.h:1467
pango_layout_iter_get_index = _lib.pango_layout_iter_get_index
pango_layout_iter_get_index.restype = c_int
pango_layout_iter_get_index.argtypes = [POINTER(PangoLayoutIter)]

# pango-new.h:1468
pango_layout_iter_get_run = _lib.pango_layout_iter_get_run
pango_layout_iter_get_run.restype = POINTER(PangoLayoutRun)
pango_layout_iter_get_run.argtypes = [POINTER(PangoLayoutIter)]

# pango-new.h:1469
pango_layout_iter_get_run_readonly = _lib.pango_layout_iter_get_run_readonly
pango_layout_iter_get_run_readonly.restype = POINTER(PangoLayoutRun)
pango_layout_iter_get_run_readonly.argtypes = [POINTER(PangoLayoutIter)]

# pango-new.h:1470
pango_layout_iter_get_line = _lib.pango_layout_iter_get_line
pango_layout_iter_get_line.restype = POINTER(PangoLayoutLine)
pango_layout_iter_get_line.argtypes = [POINTER(PangoLayoutIter)]

# pango-new.h:1471
pango_layout_iter_get_line_readonly = _lib.pango_layout_iter_get_line_readonly
pango_layout_iter_get_line_readonly.restype = POINTER(PangoLayoutLine)
pango_layout_iter_get_line_readonly.argtypes = [POINTER(PangoLayoutIter)]

# pango-new.h:1473
pango_layout_iter_get_layout = _lib.pango_layout_iter_get_layout
pango_layout_iter_get_layout.restype = POINTER(PangoLayout)
pango_layout_iter_get_layout.argtypes = [POINTER(PangoLayoutIter)]

# pango-new.h:1480
pango_layout_iter_get_char_extents = _lib.pango_layout_iter_get_char_extents
pango_layout_iter_get_char_extents.restype = None
pango_layout_iter_get_char_extents.argtypes = [POINTER(PangoLayoutIter), POINTER(PangoRectangle)]

# pango-new.h:1482
pango_layout_iter_get_cluster_extents = _lib.pango_layout_iter_get_cluster_extents
pango_layout_iter_get_cluster_extents.restype = None
pango_layout_iter_get_cluster_extents.argtypes = [POINTER(PangoLayoutIter), POINTER(PangoRectangle), POINTER(PangoRectangle)]

# pango-new.h:1485
pango_layout_iter_get_run_extents = _lib.pango_layout_iter_get_run_extents
pango_layout_iter_get_run_extents.restype = None
pango_layout_iter_get_run_extents.argtypes = [POINTER(PangoLayoutIter), POINTER(PangoRectangle), POINTER(PangoRectangle)]

# pango-new.h:1488
pango_layout_iter_get_line_extents = _lib.pango_layout_iter_get_line_extents
pango_layout_iter_get_line_extents.restype = None
pango_layout_iter_get_line_extents.argtypes = [POINTER(PangoLayoutIter), POINTER(PangoRectangle), POINTER(PangoRectangle)]

# pango-new.h:1494
pango_layout_iter_get_line_yrange = _lib.pango_layout_iter_get_line_yrange
pango_layout_iter_get_line_yrange.restype = None
pango_layout_iter_get_line_yrange.argtypes = [POINTER(PangoLayoutIter), POINTER(c_int), POINTER(c_int)]

# pango-new.h:1497
pango_layout_iter_get_layout_extents = _lib.pango_layout_iter_get_layout_extents
pango_layout_iter_get_layout_extents.restype = None
pango_layout_iter_get_layout_extents.argtypes = [POINTER(PangoLayoutIter), POINTER(PangoRectangle), POINTER(PangoRectangle)]

# pango-new.h:1500
pango_layout_iter_get_baseline = _lib.pango_layout_iter_get_baseline
pango_layout_iter_get_baseline.restype = c_int
pango_layout_iter_get_baseline.argtypes = [POINTER(PangoLayoutIter)]

class struct__PangoRenderer(Structure):
    __slots__ = [
    ]
struct__PangoRenderer._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoRenderer(Structure):
    __slots__ = [
    ]
struct__PangoRenderer._fields_ = [
    ('_opaque_struct', c_int)
]

PangoRenderer = struct__PangoRenderer 	# pango-new.h:1505
class struct__PangoRendererClass(Structure):
    __slots__ = [
    ]
struct__PangoRendererClass._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoRendererClass(Structure):
    __slots__ = [
    ]
struct__PangoRendererClass._fields_ = [
    ('_opaque_struct', c_int)
]

PangoRendererClass = struct__PangoRendererClass 	# pango-new.h:1506
class struct__PangoRendererPrivate(Structure):
    __slots__ = [
    ]
struct__PangoRendererPrivate._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoRendererPrivate(Structure):
    __slots__ = [
    ]
struct__PangoRendererPrivate._fields_ = [
    ('_opaque_struct', c_int)
]

PangoRendererPrivate = struct__PangoRendererPrivate 	# pango-new.h:1507
enum_anon_19 = c_int
PANGO_RENDER_PART_FOREGROUND = 0
PANGO_RENDER_PART_BACKGROUND = 1
PANGO_RENDER_PART_UNDERLINE = 2
PANGO_RENDER_PART_STRIKETHROUGH = 3
PangoRenderPart = enum_anon_19 	# pango-new.h:1514
# pango-new.h:1615
pango_renderer_draw_layout = _lib.pango_renderer_draw_layout
pango_renderer_draw_layout.restype = None
pango_renderer_draw_layout.argtypes = [POINTER(PangoRenderer), POINTER(PangoLayout), c_int, c_int]

# pango-new.h:1619
pango_renderer_draw_layout_line = _lib.pango_renderer_draw_layout_line
pango_renderer_draw_layout_line.restype = None
pango_renderer_draw_layout_line.argtypes = [POINTER(PangoRenderer), POINTER(PangoLayoutLine), c_int, c_int]

# pango-new.h:1623
pango_renderer_draw_glyphs = _lib.pango_renderer_draw_glyphs
pango_renderer_draw_glyphs.restype = None
pango_renderer_draw_glyphs.argtypes = [POINTER(PangoRenderer), POINTER(PangoFont), POINTER(PangoGlyphString), c_int, c_int]

# pango-new.h:1628
pango_renderer_draw_glyph_item = _lib.pango_renderer_draw_glyph_item
pango_renderer_draw_glyph_item.restype = None
pango_renderer_draw_glyph_item.argtypes = [POINTER(PangoRenderer), c_char_p, POINTER(PangoGlyphItem), c_int, c_int]

# pango-new.h:1633
pango_renderer_draw_rectangle = _lib.pango_renderer_draw_rectangle
pango_renderer_draw_rectangle.restype = None
pango_renderer_draw_rectangle.argtypes = [POINTER(PangoRenderer), PangoRenderPart, c_int, c_int, c_int, c_int]

# pango-new.h:1639
pango_renderer_draw_error_underline = _lib.pango_renderer_draw_error_underline
pango_renderer_draw_error_underline.restype = None
pango_renderer_draw_error_underline.argtypes = [POINTER(PangoRenderer), c_int, c_int, c_int, c_int]

# pango-new.h:1644
pango_renderer_draw_trapezoid = _lib.pango_renderer_draw_trapezoid
pango_renderer_draw_trapezoid.restype = None
pango_renderer_draw_trapezoid.argtypes = [POINTER(PangoRenderer), PangoRenderPart, c_double, c_double, c_double, c_double, c_double, c_double]

# pango-new.h:1652
pango_renderer_draw_glyph = _lib.pango_renderer_draw_glyph
pango_renderer_draw_glyph.restype = None
pango_renderer_draw_glyph.argtypes = [POINTER(PangoRenderer), POINTER(PangoFont), PangoGlyph, c_double, c_double]

# pango-new.h:1658
pango_renderer_activate = _lib.pango_renderer_activate
pango_renderer_activate.restype = None
pango_renderer_activate.argtypes = [POINTER(PangoRenderer)]

# pango-new.h:1659
pango_renderer_deactivate = _lib.pango_renderer_deactivate
pango_renderer_deactivate.restype = None
pango_renderer_deactivate.argtypes = [POINTER(PangoRenderer)]

# pango-new.h:1661
pango_renderer_part_changed = _lib.pango_renderer_part_changed
pango_renderer_part_changed.restype = None
pango_renderer_part_changed.argtypes = [POINTER(PangoRenderer), PangoRenderPart]

# pango-new.h:1664
pango_renderer_set_color = _lib.pango_renderer_set_color
pango_renderer_set_color.restype = None
pango_renderer_set_color.argtypes = [POINTER(PangoRenderer), PangoRenderPart, POINTER(PangoColor)]

# pango-new.h:1667
pango_renderer_get_color = _lib.pango_renderer_get_color
pango_renderer_get_color.restype = POINTER(PangoColor)
pango_renderer_get_color.argtypes = [POINTER(PangoRenderer), PangoRenderPart]

# pango-new.h:1670
pango_renderer_set_matrix = _lib.pango_renderer_set_matrix
pango_renderer_set_matrix.restype = None
pango_renderer_set_matrix.argtypes = [POINTER(PangoRenderer), POINTER(PangoMatrix)]

# pango-new.h:1672
pango_renderer_get_matrix = _lib.pango_renderer_get_matrix
pango_renderer_get_matrix.restype = POINTER(PangoMatrix)
pango_renderer_get_matrix.argtypes = [POINTER(PangoRenderer)]

# pango-new.h:1674
pango_renderer_get_layout = _lib.pango_renderer_get_layout
pango_renderer_get_layout.restype = POINTER(PangoLayout)
pango_renderer_get_layout.argtypes = [POINTER(PangoRenderer)]

# pango-new.h:1675
pango_renderer_get_layout_line = _lib.pango_renderer_get_layout_line
pango_renderer_get_layout_line.restype = POINTER(PangoLayoutLine)
pango_renderer_get_layout_line.argtypes = [POINTER(PangoRenderer)]

# pango-new.h:1686
pango_split_file_list = _lib.pango_split_file_list
pango_split_file_list.restype = POINTER(c_char_p)
pango_split_file_list.argtypes = [c_char_p]

# pango-new.h:1688
pango_trim_string = _lib.pango_trim_string
pango_trim_string.restype = c_char_p
pango_trim_string.argtypes = [c_char_p]

# pango-new.h:1715
pango_quantize_line_geometry = _lib.pango_quantize_line_geometry
pango_quantize_line_geometry.restype = None
pango_quantize_line_geometry.argtypes = [POINTER(c_int), POINTER(c_int)]

# pango-new.h:1728
pango_version = _lib.pango_version
pango_version.restype = c_int
pango_version.argtypes = []

# pango-new.h:1731
pango_version_string = _lib.pango_version_string
pango_version_string.restype = c_char_p
pango_version_string.argtypes = []

# pango-new.h:1734
pango_version_check = _lib.pango_version_check
pango_version_check.restype = c_char_p
pango_version_check.argtypes = [c_int, c_int, c_int]

cairo_version = cairo.cairo_version
cairo_version_string = cairo.cairo_version_string
cairo_bool_t = cairo.cairo_bool_t
cairo_t = cairo.cairo_t
cairo_surface_t = cairo.cairo_surface_t
cairo_matrix_t = cairo.cairo_matrix_t
cairo_pattern_t = cairo.cairo_pattern_t
cairo_destroy_func_t = cairo.cairo_destroy_func_t
cairo_user_data_key_t = cairo.cairo_user_data_key_t
cairo_status_t = cairo.cairo_status_t
cairo_content_t = cairo.cairo_content_t
cairo_write_func_t = cairo.cairo_write_func_t
cairo_read_func_t = cairo.cairo_read_func_t
cairo_create = cairo.cairo_create
cairo_reference = cairo.cairo_reference
cairo_destroy = cairo.cairo_destroy
cairo_get_reference_count = cairo.cairo_get_reference_count
cairo_get_user_data = cairo.cairo_get_user_data
cairo_set_user_data = cairo.cairo_set_user_data
cairo_save = cairo.cairo_save
cairo_restore = cairo.cairo_restore
cairo_push_group = cairo.cairo_push_group
cairo_push_group_with_content = cairo.cairo_push_group_with_content
cairo_pop_group = cairo.cairo_pop_group
cairo_pop_group_to_source = cairo.cairo_pop_group_to_source
cairo_operator_t = cairo.cairo_operator_t
cairo_set_operator = cairo.cairo_set_operator
cairo_set_source = cairo.cairo_set_source
cairo_set_source_rgb = cairo.cairo_set_source_rgb
cairo_set_source_rgba = cairo.cairo_set_source_rgba
cairo_set_source_surface = cairo.cairo_set_source_surface
cairo_set_tolerance = cairo.cairo_set_tolerance
cairo_antialias_t = cairo.cairo_antialias_t
cairo_set_antialias = cairo.cairo_set_antialias
cairo_fill_rule_t = cairo.cairo_fill_rule_t
cairo_set_fill_rule = cairo.cairo_set_fill_rule
cairo_set_line_width = cairo.cairo_set_line_width
cairo_line_cap_t = cairo.cairo_line_cap_t
cairo_set_line_cap = cairo.cairo_set_line_cap
cairo_line_join_t = cairo.cairo_line_join_t
cairo_set_line_join = cairo.cairo_set_line_join
cairo_set_dash = cairo.cairo_set_dash
cairo_set_miter_limit = cairo.cairo_set_miter_limit
cairo_translate = cairo.cairo_translate
cairo_scale = cairo.cairo_scale
cairo_rotate = cairo.cairo_rotate
cairo_transform = cairo.cairo_transform
cairo_set_matrix = cairo.cairo_set_matrix
cairo_identity_matrix = cairo.cairo_identity_matrix
cairo_user_to_device = cairo.cairo_user_to_device
cairo_user_to_device_distance = cairo.cairo_user_to_device_distance
cairo_device_to_user = cairo.cairo_device_to_user
cairo_device_to_user_distance = cairo.cairo_device_to_user_distance
cairo_new_path = cairo.cairo_new_path
cairo_move_to = cairo.cairo_move_to
cairo_new_sub_path = cairo.cairo_new_sub_path
cairo_line_to = cairo.cairo_line_to
cairo_curve_to = cairo.cairo_curve_to
cairo_arc = cairo.cairo_arc
cairo_arc_negative = cairo.cairo_arc_negative
cairo_rel_move_to = cairo.cairo_rel_move_to
cairo_rel_line_to = cairo.cairo_rel_line_to
cairo_rel_curve_to = cairo.cairo_rel_curve_to
cairo_rectangle = cairo.cairo_rectangle
cairo_close_path = cairo.cairo_close_path
cairo_path_extents = cairo.cairo_path_extents
cairo_paint = cairo.cairo_paint
cairo_paint_with_alpha = cairo.cairo_paint_with_alpha
cairo_mask = cairo.cairo_mask
cairo_mask_surface = cairo.cairo_mask_surface
cairo_stroke = cairo.cairo_stroke
cairo_stroke_preserve = cairo.cairo_stroke_preserve
cairo_fill = cairo.cairo_fill
cairo_fill_preserve = cairo.cairo_fill_preserve
cairo_copy_page = cairo.cairo_copy_page
cairo_show_page = cairo.cairo_show_page
cairo_in_stroke = cairo.cairo_in_stroke
cairo_in_fill = cairo.cairo_in_fill
cairo_stroke_extents = cairo.cairo_stroke_extents
cairo_fill_extents = cairo.cairo_fill_extents
cairo_reset_clip = cairo.cairo_reset_clip
cairo_clip = cairo.cairo_clip
cairo_clip_preserve = cairo.cairo_clip_preserve
cairo_clip_extents = cairo.cairo_clip_extents
cairo_rectangle_t = cairo.cairo_rectangle_t
cairo_rectangle_list_t = cairo.cairo_rectangle_list_t
cairo_copy_clip_rectangle_list = cairo.cairo_copy_clip_rectangle_list
cairo_rectangle_list_destroy = cairo.cairo_rectangle_list_destroy
cairo_scaled_font_t = cairo.cairo_scaled_font_t
cairo_font_face_t = cairo.cairo_font_face_t
cairo_glyph_t = cairo.cairo_glyph_t
cairo_glyph_allocate = cairo.cairo_glyph_allocate
cairo_glyph_free = cairo.cairo_glyph_free
cairo_text_cluster_t = cairo.cairo_text_cluster_t
cairo_text_cluster_allocate = cairo.cairo_text_cluster_allocate
cairo_text_cluster_free = cairo.cairo_text_cluster_free
cairo_text_cluster_flags_t = cairo.cairo_text_cluster_flags_t
cairo_text_extents_t = cairo.cairo_text_extents_t
cairo_font_extents_t = cairo.cairo_font_extents_t
cairo_font_slant_t = cairo.cairo_font_slant_t
cairo_font_weight_t = cairo.cairo_font_weight_t
cairo_subpixel_order_t = cairo.cairo_subpixel_order_t
cairo_hint_style_t = cairo.cairo_hint_style_t
cairo_hint_metrics_t = cairo.cairo_hint_metrics_t
cairo_font_options_t = cairo.cairo_font_options_t
cairo_font_options_create = cairo.cairo_font_options_create
cairo_font_options_copy = cairo.cairo_font_options_copy
cairo_font_options_destroy = cairo.cairo_font_options_destroy
cairo_font_options_status = cairo.cairo_font_options_status
cairo_font_options_merge = cairo.cairo_font_options_merge
cairo_font_options_equal = cairo.cairo_font_options_equal
cairo_font_options_hash = cairo.cairo_font_options_hash
cairo_font_options_set_antialias = cairo.cairo_font_options_set_antialias
cairo_font_options_get_antialias = cairo.cairo_font_options_get_antialias
cairo_font_options_set_subpixel_order = cairo.cairo_font_options_set_subpixel_order
cairo_font_options_get_subpixel_order = cairo.cairo_font_options_get_subpixel_order
cairo_font_options_set_hint_style = cairo.cairo_font_options_set_hint_style
cairo_font_options_get_hint_style = cairo.cairo_font_options_get_hint_style
cairo_font_options_set_hint_metrics = cairo.cairo_font_options_set_hint_metrics
cairo_font_options_get_hint_metrics = cairo.cairo_font_options_get_hint_metrics
cairo_select_font_face = cairo.cairo_select_font_face
cairo_set_font_size = cairo.cairo_set_font_size
cairo_set_font_matrix = cairo.cairo_set_font_matrix
cairo_get_font_matrix = cairo.cairo_get_font_matrix
cairo_set_font_options = cairo.cairo_set_font_options
cairo_get_font_options = cairo.cairo_get_font_options
cairo_set_font_face = cairo.cairo_set_font_face
cairo_get_font_face = cairo.cairo_get_font_face
cairo_set_scaled_font = cairo.cairo_set_scaled_font
cairo_get_scaled_font = cairo.cairo_get_scaled_font
cairo_show_text = cairo.cairo_show_text
cairo_show_glyphs = cairo.cairo_show_glyphs
cairo_show_text_glyphs = cairo.cairo_show_text_glyphs
cairo_text_path = cairo.cairo_text_path
cairo_glyph_path = cairo.cairo_glyph_path
cairo_text_extents = cairo.cairo_text_extents
cairo_glyph_extents = cairo.cairo_glyph_extents
cairo_font_extents = cairo.cairo_font_extents
cairo_font_face_reference = cairo.cairo_font_face_reference
cairo_font_face_destroy = cairo.cairo_font_face_destroy
cairo_font_face_get_reference_count = cairo.cairo_font_face_get_reference_count
cairo_font_face_status = cairo.cairo_font_face_status
cairo_font_type_t = cairo.cairo_font_type_t
cairo_font_face_get_type = cairo.cairo_font_face_get_type
cairo_font_face_get_user_data = cairo.cairo_font_face_get_user_data
cairo_font_face_set_user_data = cairo.cairo_font_face_set_user_data
cairo_scaled_font_create = cairo.cairo_scaled_font_create
cairo_scaled_font_reference = cairo.cairo_scaled_font_reference
cairo_scaled_font_destroy = cairo.cairo_scaled_font_destroy
cairo_scaled_font_get_reference_count = cairo.cairo_scaled_font_get_reference_count
cairo_scaled_font_status = cairo.cairo_scaled_font_status
cairo_scaled_font_get_type = cairo.cairo_scaled_font_get_type
cairo_scaled_font_get_user_data = cairo.cairo_scaled_font_get_user_data
cairo_scaled_font_set_user_data = cairo.cairo_scaled_font_set_user_data
cairo_scaled_font_extents = cairo.cairo_scaled_font_extents
cairo_scaled_font_text_extents = cairo.cairo_scaled_font_text_extents
cairo_scaled_font_glyph_extents = cairo.cairo_scaled_font_glyph_extents
cairo_scaled_font_text_to_glyphs = cairo.cairo_scaled_font_text_to_glyphs
cairo_scaled_font_get_font_face = cairo.cairo_scaled_font_get_font_face
cairo_scaled_font_get_font_matrix = cairo.cairo_scaled_font_get_font_matrix
cairo_scaled_font_get_ctm = cairo.cairo_scaled_font_get_ctm
cairo_scaled_font_get_scale_matrix = cairo.cairo_scaled_font_get_scale_matrix
cairo_scaled_font_get_font_options = cairo.cairo_scaled_font_get_font_options
cairo_toy_font_face_create = cairo.cairo_toy_font_face_create
cairo_toy_font_face_get_family = cairo.cairo_toy_font_face_get_family
cairo_toy_font_face_get_slant = cairo.cairo_toy_font_face_get_slant
cairo_toy_font_face_get_weight = cairo.cairo_toy_font_face_get_weight
cairo_user_font_face_create = cairo.cairo_user_font_face_create
cairo_user_scaled_font_init_func_t = cairo.cairo_user_scaled_font_init_func_t
cairo_user_scaled_font_render_glyph_func_t = cairo.cairo_user_scaled_font_render_glyph_func_t
cairo_user_scaled_font_text_to_glyphs_func_t = cairo.cairo_user_scaled_font_text_to_glyphs_func_t
cairo_user_scaled_font_unicode_to_glyph_func_t = cairo.cairo_user_scaled_font_unicode_to_glyph_func_t
cairo_user_font_face_set_init_func = cairo.cairo_user_font_face_set_init_func
cairo_user_font_face_set_render_glyph_func = cairo.cairo_user_font_face_set_render_glyph_func
cairo_user_font_face_set_text_to_glyphs_func = cairo.cairo_user_font_face_set_text_to_glyphs_func
cairo_user_font_face_set_unicode_to_glyph_func = cairo.cairo_user_font_face_set_unicode_to_glyph_func
cairo_user_font_face_get_init_func = cairo.cairo_user_font_face_get_init_func
cairo_user_font_face_get_render_glyph_func = cairo.cairo_user_font_face_get_render_glyph_func
cairo_user_font_face_get_text_to_glyphs_func = cairo.cairo_user_font_face_get_text_to_glyphs_func
cairo_user_font_face_get_unicode_to_glyph_func = cairo.cairo_user_font_face_get_unicode_to_glyph_func
cairo_get_operator = cairo.cairo_get_operator
cairo_get_source = cairo.cairo_get_source
cairo_get_tolerance = cairo.cairo_get_tolerance
cairo_get_antialias = cairo.cairo_get_antialias
cairo_has_current_point = cairo.cairo_has_current_point
cairo_get_current_point = cairo.cairo_get_current_point
cairo_get_fill_rule = cairo.cairo_get_fill_rule
cairo_get_line_width = cairo.cairo_get_line_width
cairo_get_line_cap = cairo.cairo_get_line_cap
cairo_get_line_join = cairo.cairo_get_line_join
cairo_get_miter_limit = cairo.cairo_get_miter_limit
cairo_get_dash_count = cairo.cairo_get_dash_count
cairo_get_dash = cairo.cairo_get_dash
cairo_get_matrix = cairo.cairo_get_matrix
cairo_get_target = cairo.cairo_get_target
cairo_get_group_target = cairo.cairo_get_group_target
cairo_path_data_type_t = cairo.cairo_path_data_type_t
cairo_path_data_t = cairo.cairo_path_data_t
cairo_path_t = cairo.cairo_path_t
cairo_copy_path = cairo.cairo_copy_path
cairo_copy_path_flat = cairo.cairo_copy_path_flat
cairo_append_path = cairo.cairo_append_path
cairo_path_destroy = cairo.cairo_path_destroy
cairo_status = cairo.cairo_status
cairo_status_to_string = cairo.cairo_status_to_string
cairo_surface_create_similar = cairo.cairo_surface_create_similar
cairo_surface_reference = cairo.cairo_surface_reference
cairo_surface_finish = cairo.cairo_surface_finish
cairo_surface_destroy = cairo.cairo_surface_destroy
cairo_surface_get_reference_count = cairo.cairo_surface_get_reference_count
cairo_surface_status = cairo.cairo_surface_status
cairo_surface_type_t = cairo.cairo_surface_type_t
cairo_surface_get_type = cairo.cairo_surface_get_type
cairo_surface_get_content = cairo.cairo_surface_get_content
cairo_surface_write_to_png = cairo.cairo_surface_write_to_png
cairo_surface_write_to_png_stream = cairo.cairo_surface_write_to_png_stream
cairo_surface_get_user_data = cairo.cairo_surface_get_user_data
cairo_surface_set_user_data = cairo.cairo_surface_set_user_data
cairo_surface_get_font_options = cairo.cairo_surface_get_font_options
cairo_surface_flush = cairo.cairo_surface_flush
cairo_surface_mark_dirty = cairo.cairo_surface_mark_dirty
cairo_surface_mark_dirty_rectangle = cairo.cairo_surface_mark_dirty_rectangle
cairo_surface_set_device_offset = cairo.cairo_surface_set_device_offset
cairo_surface_get_device_offset = cairo.cairo_surface_get_device_offset
cairo_surface_set_fallback_resolution = cairo.cairo_surface_set_fallback_resolution
cairo_surface_get_fallback_resolution = cairo.cairo_surface_get_fallback_resolution
cairo_surface_copy_page = cairo.cairo_surface_copy_page
cairo_surface_show_page = cairo.cairo_surface_show_page
cairo_surface_has_show_text_glyphs = cairo.cairo_surface_has_show_text_glyphs
cairo_format_t = cairo.cairo_format_t
cairo_image_surface_create = cairo.cairo_image_surface_create
cairo_format_stride_for_width = cairo.cairo_format_stride_for_width
cairo_image_surface_create_for_data = cairo.cairo_image_surface_create_for_data
cairo_image_surface_get_data = cairo.cairo_image_surface_get_data
cairo_image_surface_get_format = cairo.cairo_image_surface_get_format
cairo_image_surface_get_width = cairo.cairo_image_surface_get_width
cairo_image_surface_get_height = cairo.cairo_image_surface_get_height
cairo_image_surface_get_stride = cairo.cairo_image_surface_get_stride
cairo_image_surface_create_from_png = cairo.cairo_image_surface_create_from_png
cairo_image_surface_create_from_png_stream = cairo.cairo_image_surface_create_from_png_stream
cairo_pattern_create_rgb = cairo.cairo_pattern_create_rgb
cairo_pattern_create_rgba = cairo.cairo_pattern_create_rgba
cairo_pattern_create_for_surface = cairo.cairo_pattern_create_for_surface
cairo_pattern_create_linear = cairo.cairo_pattern_create_linear
cairo_pattern_create_radial = cairo.cairo_pattern_create_radial
cairo_pattern_reference = cairo.cairo_pattern_reference
cairo_pattern_destroy = cairo.cairo_pattern_destroy
cairo_pattern_get_reference_count = cairo.cairo_pattern_get_reference_count
cairo_pattern_status = cairo.cairo_pattern_status
cairo_pattern_get_user_data = cairo.cairo_pattern_get_user_data
cairo_pattern_set_user_data = cairo.cairo_pattern_set_user_data
cairo_pattern_type_t = cairo.cairo_pattern_type_t
cairo_pattern_get_type = cairo.cairo_pattern_get_type
cairo_pattern_add_color_stop_rgb = cairo.cairo_pattern_add_color_stop_rgb
cairo_pattern_add_color_stop_rgba = cairo.cairo_pattern_add_color_stop_rgba
cairo_pattern_set_matrix = cairo.cairo_pattern_set_matrix
cairo_pattern_get_matrix = cairo.cairo_pattern_get_matrix
cairo_extend_t = cairo.cairo_extend_t
cairo_pattern_set_extend = cairo.cairo_pattern_set_extend
cairo_pattern_get_extend = cairo.cairo_pattern_get_extend
cairo_filter_t = cairo.cairo_filter_t
cairo_pattern_set_filter = cairo.cairo_pattern_set_filter
cairo_pattern_get_filter = cairo.cairo_pattern_get_filter
cairo_pattern_get_rgba = cairo.cairo_pattern_get_rgba
cairo_pattern_get_surface = cairo.cairo_pattern_get_surface
cairo_pattern_get_color_stop_rgba = cairo.cairo_pattern_get_color_stop_rgba
cairo_pattern_get_color_stop_count = cairo.cairo_pattern_get_color_stop_count
cairo_pattern_get_linear_points = cairo.cairo_pattern_get_linear_points
cairo_pattern_get_radial_circles = cairo.cairo_pattern_get_radial_circles
cairo_matrix_init = cairo.cairo_matrix_init
cairo_matrix_init_identity = cairo.cairo_matrix_init_identity
cairo_matrix_init_translate = cairo.cairo_matrix_init_translate
cairo_matrix_init_scale = cairo.cairo_matrix_init_scale
cairo_matrix_init_rotate = cairo.cairo_matrix_init_rotate
cairo_matrix_translate = cairo.cairo_matrix_translate
cairo_matrix_scale = cairo.cairo_matrix_scale
cairo_matrix_rotate = cairo.cairo_matrix_rotate
cairo_matrix_invert = cairo.cairo_matrix_invert
cairo_matrix_multiply = cairo.cairo_matrix_multiply
cairo_matrix_transform_distance = cairo.cairo_matrix_transform_distance
cairo_matrix_transform_point = cairo.cairo_matrix_transform_point
cairo_debug_reset_static_data = cairo.cairo_debug_reset_static_data
class struct__PangoCairoFont(Structure):
    __slots__ = [
    ]
struct__PangoCairoFont._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoCairoFont(Structure):
    __slots__ = [
    ]
struct__PangoCairoFont._fields_ = [
    ('_opaque_struct', c_int)
]

PangoCairoFont = struct__PangoCairoFont 	# pango-new.h:2927
class struct__PangoCairoFontMap(Structure):
    __slots__ = [
    ]
struct__PangoCairoFontMap._fields_ = [
    ('_opaque_struct', c_int)
]

class struct__PangoCairoFontMap(Structure):
    __slots__ = [
    ]
struct__PangoCairoFontMap._fields_ = [
    ('_opaque_struct', c_int)
]

PangoCairoFontMap = struct__PangoCairoFontMap 	# pango-new.h:2928
# pango-new.h:2943
pango_cairo_font_map_new = _lib.pango_cairo_font_map_new
pango_cairo_font_map_new.restype = POINTER(PangoFontMap)
pango_cairo_font_map_new.argtypes = []

# pango-new.h:2944
pango_cairo_font_map_new_for_font_type = _lib.pango_cairo_font_map_new_for_font_type
pango_cairo_font_map_new_for_font_type.restype = POINTER(PangoFontMap)
pango_cairo_font_map_new_for_font_type.argtypes = [cairo_font_type_t]

# pango-new.h:2945
pango_cairo_font_map_get_default = _lib.pango_cairo_font_map_get_default
pango_cairo_font_map_get_default.restype = POINTER(PangoFontMap)
pango_cairo_font_map_get_default.argtypes = []

# pango-new.h:2946
pango_cairo_font_map_set_default = _lib.pango_cairo_font_map_set_default
pango_cairo_font_map_set_default.restype = None
pango_cairo_font_map_set_default.argtypes = [POINTER(PangoCairoFontMap)]

# pango-new.h:2947
pango_cairo_font_map_get_font_type = _lib.pango_cairo_font_map_get_font_type
pango_cairo_font_map_get_font_type.restype = cairo_font_type_t
pango_cairo_font_map_get_font_type.argtypes = [POINTER(PangoCairoFontMap)]

# pango-new.h:2949
pango_cairo_font_map_set_resolution = _lib.pango_cairo_font_map_set_resolution
pango_cairo_font_map_set_resolution.restype = None
pango_cairo_font_map_set_resolution.argtypes = [POINTER(PangoCairoFontMap), c_double]

# pango-new.h:2951
pango_cairo_font_map_get_resolution = _lib.pango_cairo_font_map_get_resolution
pango_cairo_font_map_get_resolution.restype = c_double
pango_cairo_font_map_get_resolution.argtypes = [POINTER(PangoCairoFontMap)]

# pango-new.h:2953
pango_cairo_font_map_create_context = _lib.pango_cairo_font_map_create_context
pango_cairo_font_map_create_context.restype = POINTER(PangoContext)
pango_cairo_font_map_create_context.argtypes = [POINTER(PangoCairoFontMap)]

# pango-new.h:2961
pango_cairo_font_get_scaled_font = _lib.pango_cairo_font_get_scaled_font
pango_cairo_font_get_scaled_font.restype = POINTER(cairo_scaled_font_t)
pango_cairo_font_get_scaled_font.argtypes = [POINTER(PangoCairoFont)]

# pango-new.h:2965
pango_cairo_update_context = _lib.pango_cairo_update_context
pango_cairo_update_context.restype = None
pango_cairo_update_context.argtypes = [POINTER(cairo_t), POINTER(PangoContext)]

_pango_cairo_update_context = pango_cairo_update_context
pango_cairo_update_context = lambda arg0, arg1: _pango_cairo_update_context(arg0._internal, arg1._internal)

# pango-new.h:2968
pango_cairo_context_set_font_options = _lib.pango_cairo_context_set_font_options
pango_cairo_context_set_font_options.restype = None
pango_cairo_context_set_font_options.argtypes = [POINTER(PangoContext), POINTER(cairo_font_options_t)]

_pango_cairo_context_set_font_options = pango_cairo_context_set_font_options
pango_cairo_context_set_font_options = lambda arg0, arg1: _pango_cairo_context_set_font_options(arg0._internal, arg1)

# pango-new.h:2970
pango_cairo_context_get_font_options = _lib.pango_cairo_context_get_font_options
pango_cairo_context_get_font_options.restype = POINTER(cairo_font_options_t)
pango_cairo_context_get_font_options.argtypes = [POINTER(PangoContext)]

_pango_cairo_context_get_font_options = pango_cairo_context_get_font_options
pango_cairo_context_get_font_options = lambda arg0: _pango_cairo_context_get_font_options(arg0._internal)

# pango-new.h:2972
pango_cairo_context_set_resolution = _lib.pango_cairo_context_set_resolution
pango_cairo_context_set_resolution.restype = None
pango_cairo_context_set_resolution.argtypes = [POINTER(PangoContext), c_double]

_pango_cairo_context_set_resolution = pango_cairo_context_set_resolution
pango_cairo_context_set_resolution = lambda arg0, arg1: _pango_cairo_context_set_resolution(arg0._internal, arg1)

# pango-new.h:2974
pango_cairo_context_get_resolution = _lib.pango_cairo_context_get_resolution
pango_cairo_context_get_resolution.restype = c_double
pango_cairo_context_get_resolution.argtypes = [POINTER(PangoContext)]

_pango_cairo_context_get_resolution = pango_cairo_context_get_resolution
pango_cairo_context_get_resolution = lambda arg0: _pango_cairo_context_get_resolution(arg0._internal)

# pango-new.h:2985
pango_cairo_create_context = _lib.pango_cairo_create_context
pango_cairo_create_context.restype = POINTER(PangoContext)
pango_cairo_create_context.argtypes = [POINTER(cairo_t)]

_pango_cairo_create_context = pango_cairo_create_context
pango_cairo_create_context = lambda arg0: Context._from_internal(_pango_cairo_create_context(arg0._internal))

# pango-new.h:2986
pango_cairo_create_layout = _lib.pango_cairo_create_layout
pango_cairo_create_layout.restype = POINTER(PangoLayout)
pango_cairo_create_layout.argtypes = [POINTER(cairo_t)]

_pango_cairo_create_layout = pango_cairo_create_layout
pango_cairo_create_layout = lambda arg0: Layout._from_internal(_pango_cairo_create_layout(arg0._internal))

# pango-new.h:2987
pango_cairo_update_layout = _lib.pango_cairo_update_layout
pango_cairo_update_layout.restype = None
pango_cairo_update_layout.argtypes = [POINTER(cairo_t), POINTER(PangoLayout)]

_pango_cairo_update_layout = pango_cairo_update_layout
pango_cairo_update_layout = lambda arg0, arg1: _pango_cairo_update_layout(arg0._internal, arg1._internal)

# pango-new.h:2993
pango_cairo_show_glyph_string = _lib.pango_cairo_show_glyph_string
pango_cairo_show_glyph_string.restype = None
pango_cairo_show_glyph_string.argtypes = [POINTER(cairo_t), POINTER(PangoFont), POINTER(PangoGlyphString)]

_pango_cairo_show_glyph_string = pango_cairo_show_glyph_string
pango_cairo_show_glyph_string = lambda arg0, arg1, arg2: _pango_cairo_show_glyph_string(arg0._internal, arg1, arg2)

# pango-new.h:2996
pango_cairo_show_glyph_item = _lib.pango_cairo_show_glyph_item
pango_cairo_show_glyph_item.restype = None
pango_cairo_show_glyph_item.argtypes = [POINTER(cairo_t), c_char_p, POINTER(PangoGlyphItem)]

_pango_cairo_show_glyph_item = pango_cairo_show_glyph_item
pango_cairo_show_glyph_item = lambda arg0, arg1, arg2: _pango_cairo_show_glyph_item(arg0._internal, arg1, arg2)

# pango-new.h:2999
pango_cairo_show_layout_line = _lib.pango_cairo_show_layout_line
pango_cairo_show_layout_line.restype = None
pango_cairo_show_layout_line.argtypes = [POINTER(cairo_t), POINTER(PangoLayoutLine)]

_pango_cairo_show_layout_line = pango_cairo_show_layout_line
pango_cairo_show_layout_line = lambda arg0, arg1: _pango_cairo_show_layout_line(arg0._internal, arg1)

# pango-new.h:3001
pango_cairo_show_layout = _lib.pango_cairo_show_layout
pango_cairo_show_layout.restype = None
pango_cairo_show_layout.argtypes = [POINTER(cairo_t), POINTER(PangoLayout)]

_pango_cairo_show_layout = pango_cairo_show_layout
pango_cairo_show_layout = lambda arg0, arg1: _pango_cairo_show_layout(arg0._internal, arg1._internal)

# pango-new.h:3004
pango_cairo_show_error_underline = _lib.pango_cairo_show_error_underline
pango_cairo_show_error_underline.restype = None
pango_cairo_show_error_underline.argtypes = [POINTER(cairo_t), c_double, c_double, c_double, c_double]

_pango_cairo_show_error_underline = pango_cairo_show_error_underline
pango_cairo_show_error_underline = lambda arg0, arg1, arg2, arg3, arg4: _pango_cairo_show_error_underline(arg0._internal, arg1, arg2, arg3, arg4)

# pango-new.h:3013
pango_cairo_glyph_string_path = _lib.pango_cairo_glyph_string_path
pango_cairo_glyph_string_path.restype = None
pango_cairo_glyph_string_path.argtypes = [POINTER(cairo_t), POINTER(PangoFont), POINTER(PangoGlyphString)]

_pango_cairo_glyph_string_path = pango_cairo_glyph_string_path
pango_cairo_glyph_string_path = lambda arg0, arg1, arg2: _pango_cairo_glyph_string_path(arg0._internal, arg1, arg2)

# pango-new.h:3016
pango_cairo_layout_line_path = _lib.pango_cairo_layout_line_path
pango_cairo_layout_line_path.restype = None
pango_cairo_layout_line_path.argtypes = [POINTER(cairo_t), POINTER(PangoLayoutLine)]

_pango_cairo_layout_line_path = pango_cairo_layout_line_path
pango_cairo_layout_line_path = lambda arg0, arg1: _pango_cairo_layout_line_path(arg0._internal, arg1)

# pango-new.h:3018
pango_cairo_layout_path = _lib.pango_cairo_layout_path
pango_cairo_layout_path.restype = None
pango_cairo_layout_path.argtypes = [POINTER(cairo_t), POINTER(PangoLayout)]

_pango_cairo_layout_path = pango_cairo_layout_path
pango_cairo_layout_path = lambda arg0, arg1: _pango_cairo_layout_path(arg0._internal, arg1._internal)

# pango-new.h:3021
pango_cairo_error_underline_path = _lib.pango_cairo_error_underline_path
pango_cairo_error_underline_path.restype = None
pango_cairo_error_underline_path.argtypes = [POINTER(cairo_t), c_double, c_double, c_double, c_double]

_pango_cairo_error_underline_path = pango_cairo_error_underline_path
pango_cairo_error_underline_path = lambda arg0, arg1, arg2, arg3, arg4: _pango_cairo_error_underline_path(arg0._internal, arg1, arg2, arg3, arg4)

class _Wrapper(object):
    @classmethod
    def _from_internal(cls, internal):
        self = object.__new__(cls)
        self._internal = internal
        return self

class Context(_Wrapper):
    @classmethod
    def new(self):
        return Context._from_internal(pango_context_new())

    def set_font_map(self, arg1):
        return pango_context_set_font_map(self._internal, arg1._internal)

    def get_font_map(self):
        return FontMap._from_internal(pango_context_get_font_map(self._internal))

    def list_families(self, arg1, arg2):
        return pango_context_list_families(self._internal, arg1, arg2)

    def load_font(self, arg1):
        return pango_context_load_font(self._internal, arg1._internal)

    def load_fontset(self, arg1, arg2):
        return pango_context_load_fontset(self._internal, arg1._internal, arg2)

    def get_metrics(self, arg1, arg2):
        return pango_context_get_metrics(self._internal, arg1._internal, arg2)

    def set_font_description(self, arg1):
        return pango_context_set_font_description(self._internal, arg1._internal)

    def get_font_description(self):
        return FontDescription._from_internal(pango_context_get_font_description(self._internal))

    def get_language(self):
        return pango_context_get_language(self._internal)

    def set_language(self, arg1):
        return pango_context_set_language(self._internal, arg1)

    def set_base_dir(self, arg1):
        return pango_context_set_base_dir(self._internal, arg1)

    def get_base_dir(self):
        return pango_context_get_base_dir(self._internal)

    def set_base_gravity(self, arg1):
        return pango_context_set_base_gravity(self._internal, arg1)

    def get_base_gravity(self):
        return pango_context_get_base_gravity(self._internal)

    def get_gravity(self):
        return pango_context_get_gravity(self._internal)

    def set_gravity_hint(self, arg1):
        return pango_context_set_gravity_hint(self._internal, arg1)

    def get_gravity_hint(self):
        return pango_context_get_gravity_hint(self._internal)

    def set_matrix(self, arg1):
        return pango_context_set_matrix(self._internal, arg1)

    def get_matrix(self):
        return pango_context_get_matrix(self._internal)

    def __init__(self, *args, **kwargs):
        self._internal = Context.new(*args, **kwargs)._internal

    font_map = property(get_font_map, set_font_map)
    font_description = property(get_font_description, set_font_description)
    language = property(get_language, set_language)
    base_dir = property(get_base_dir, set_base_dir)
    base_gravity = property(get_base_gravity, set_base_gravity)
    gravity = property(get_gravity)
    gravity_hint = property(get_gravity_hint, set_gravity_hint)
    matrix = property(get_matrix, set_matrix)

class Layout(_Wrapper):
    def get_size(self):
        width ,height =c_int (),c_int ()
        pango_layout_get_size (self ._internal ,byref (width ),byref (height ))
        return (width .value ,height .value )

    @classmethod
    def new(self, arg0):
        return Layout._from_internal(pango_layout_new(arg0._internal))

    def copy(self):
        return Layout._from_internal(pango_layout_copy(self._internal))

    def get_context(self):
        return Context._from_internal(pango_layout_get_context(self._internal))

    def set_attributes(self, arg1):
        return pango_layout_set_attributes(self._internal, arg1)

    def get_attributes(self):
        return pango_layout_get_attributes(self._internal)

    def set_text(self, arg1, arg2):
        return pango_layout_set_text(self._internal, arg1, arg2)

    def get_text(self):
        return pango_layout_get_text(self._internal)

    def set_markup(self, arg1, arg2):
        return pango_layout_set_markup(self._internal, arg1, arg2)

    def set_font_description(self, arg1):
        return pango_layout_set_font_description(self._internal, arg1._internal)

    def get_font_description(self):
        return FontDescription._from_internal(pango_layout_get_font_description(self._internal))

    def set_width(self, arg1):
        return pango_layout_set_width(self._internal, arg1)

    def get_width(self):
        return pango_layout_get_width(self._internal)

    def set_height(self, arg1):
        return pango_layout_set_height(self._internal, arg1)

    def get_height(self):
        return pango_layout_get_height(self._internal)

    def set_wrap(self, arg1):
        return pango_layout_set_wrap(self._internal, arg1)

    def get_wrap(self):
        return pango_layout_get_wrap(self._internal)

    def set_indent(self, arg1):
        return pango_layout_set_indent(self._internal, arg1)

    def get_indent(self):
        return pango_layout_get_indent(self._internal)

    def set_spacing(self, arg1):
        return pango_layout_set_spacing(self._internal, arg1)

    def get_spacing(self):
        return pango_layout_get_spacing(self._internal)

    def set_alignment(self, arg1):
        return pango_layout_set_alignment(self._internal, arg1)

    def get_alignment(self):
        return pango_layout_get_alignment(self._internal)

    def set_tabs(self, arg1):
        return pango_layout_set_tabs(self._internal, arg1)

    def get_tabs(self):
        return pango_layout_get_tabs(self._internal)

    def set_ellipsize(self, arg1):
        return pango_layout_set_ellipsize(self._internal, arg1)

    def get_ellipsize(self):
        return pango_layout_get_ellipsize(self._internal)

    def get_unknown_glyphs_count(self):
        return pango_layout_get_unknown_glyphs_count(self._internal)

    def context_changed(self):
        return pango_layout_context_changed(self._internal)

    def index_to_pos(self, arg1, arg2):
        return pango_layout_index_to_pos(self._internal, arg1, arg2)

    def get_cursor_pos(self, arg1, arg2, arg3):
        return pango_layout_get_cursor_pos(self._internal, arg1, arg2, arg3)

    def get_extents(self, arg1, arg2):
        return pango_layout_get_extents(self._internal, arg1, arg2)

    def get_pixel_extents(self, arg1, arg2):
        return pango_layout_get_pixel_extents(self._internal, arg1, arg2)

    def get_pixel_size(self, arg1, arg2):
        return pango_layout_get_pixel_size(self._internal, arg1, arg2)

    def get_baseline(self):
        return pango_layout_get_baseline(self._internal)

    def get_line_count(self):
        return pango_layout_get_line_count(self._internal)

    def get_line(self, arg1):
        return pango_layout_get_line(self._internal, arg1)

    def get_line_readonly(self, arg1):
        return pango_layout_get_line_readonly(self._internal, arg1)

    def line_ref(self):
        return pango_layout_line_ref(self._internal)

    def line_unref(self):
        return pango_layout_line_unref(self._internal)

    def line_get_x_ranges(self, arg1, arg2, arg3, arg4):
        return pango_layout_line_get_x_ranges(self._internal, arg1, arg2, arg3, arg4)

    def line_get_extents(self, arg1, arg2):
        return pango_layout_line_get_extents(self._internal, arg1, arg2)

    def line_get_pixel_extents(self, arg1, arg2):
        return pango_layout_line_get_pixel_extents(self._internal, arg1, arg2)

    def get_iter(self):
        return pango_layout_get_iter(self._internal)

    def iter_copy(self):
        return pango_layout_iter_copy(self._internal)

    def iter_free(self):
        return pango_layout_iter_free(self._internal)

    def iter_get_index(self):
        return pango_layout_iter_get_index(self._internal)

    def iter_get_run(self):
        return pango_layout_iter_get_run(self._internal)

    def iter_get_run_readonly(self):
        return pango_layout_iter_get_run_readonly(self._internal)

    def iter_get_line(self):
        return pango_layout_iter_get_line(self._internal)

    def iter_get_line_readonly(self):
        return pango_layout_iter_get_line_readonly(self._internal)

    def iter_get_layout(self):
        return Layout._from_internal(pango_layout_iter_get_layout(self._internal))

    def iter_get_char_extents(self, arg1):
        return pango_layout_iter_get_char_extents(self._internal, arg1)

    def iter_get_cluster_extents(self, arg1, arg2):
        return pango_layout_iter_get_cluster_extents(self._internal, arg1, arg2)

    def iter_get_run_extents(self, arg1, arg2):
        return pango_layout_iter_get_run_extents(self._internal, arg1, arg2)

    def iter_get_line_extents(self, arg1, arg2):
        return pango_layout_iter_get_line_extents(self._internal, arg1, arg2)

    def iter_get_line_yrange(self, arg1, arg2):
        return pango_layout_iter_get_line_yrange(self._internal, arg1, arg2)

    def iter_get_layout_extents(self, arg1, arg2):
        return pango_layout_iter_get_layout_extents(self._internal, arg1, arg2)

    def iter_get_baseline(self):
        return pango_layout_iter_get_baseline(self._internal)

    def __init__(self, *args, **kwargs):
        self._internal = Layout.new(*args, **kwargs)._internal

    size = property(get_size)
    context = property(get_context)
    attributes = property(get_attributes, set_attributes)
    font_description = property(get_font_description, set_font_description)
    width = property(get_width, set_width)
    height = property(get_height, set_height)
    wrap = property(get_wrap, set_wrap)
    indent = property(get_indent, set_indent)
    spacing = property(get_spacing, set_spacing)
    alignment = property(get_alignment, set_alignment)
    tabs = property(get_tabs, set_tabs)
    ellipsize = property(get_ellipsize, set_ellipsize)
    unknown_glyphs_count = property(get_unknown_glyphs_count)
    baseline = property(get_baseline)
    line_count = property(get_line_count)
    iter = property(get_iter)

class FontDescription(_Wrapper):
    @classmethod
    def new(self):
        return FontDescription._from_internal(pango_font_description_new())

    def copy(self):
        return FontDescription._from_internal(pango_font_description_copy(self._internal))

    def copy_static(self):
        return FontDescription._from_internal(pango_font_description_copy_static(self._internal))

    def free(self):
        return pango_font_description_free(self._internal)

    def set_family(self, arg1):
        return pango_font_description_set_family(self._internal, arg1)

    def set_family_static(self, arg1):
        return pango_font_description_set_family_static(self._internal, arg1)

    def get_family(self):
        return pango_font_description_get_family(self._internal)

    def set_style(self, arg1):
        return pango_font_description_set_style(self._internal, arg1)

    def get_style(self):
        return pango_font_description_get_style(self._internal)

    def set_variant(self, arg1):
        return pango_font_description_set_variant(self._internal, arg1)

    def get_variant(self):
        return pango_font_description_get_variant(self._internal)

    def set_weight(self, arg1):
        return pango_font_description_set_weight(self._internal, arg1)

    def get_weight(self):
        return pango_font_description_get_weight(self._internal)

    def set_stretch(self, arg1):
        return pango_font_description_set_stretch(self._internal, arg1)

    def get_stretch(self):
        return pango_font_description_get_stretch(self._internal)

    def set_absolute_size(self, arg1):
        return pango_font_description_set_absolute_size(self._internal, arg1)

    def set_gravity(self, arg1):
        return pango_font_description_set_gravity(self._internal, arg1)

    def get_gravity(self):
        return pango_font_description_get_gravity(self._internal)

    def get_set_fields(self):
        return pango_font_description_get_set_fields(self._internal)

    def unset_fields(self, arg1):
        return pango_font_description_unset_fields(self._internal, arg1)

    @classmethod
    def from_string(self, arg0):
        return FontDescription._from_internal(pango_font_description_from_string(arg0))

    def to_string(self):
        return pango_font_description_to_string(self._internal)

    def to_filename(self):
        return pango_font_description_to_filename(self._internal)

    def __init__(self, *args, **kwargs):
        self._internal = FontDescription.new(*args, **kwargs)._internal

    family = property(get_family, set_family)
    family_static = property(None, set_family_static)
    style = property(get_style, set_style)
    variant = property(get_variant, set_variant)
    weight = property(get_weight, set_weight)
    stretch = property(get_stretch, set_stretch)
    absolute_size = property(None, set_absolute_size)
    gravity = property(get_gravity, set_gravity)
    set_fields = property(get_set_fields)

class FontMap(_Wrapper):
    def create_context(self):
        return Context._from_internal(pango_font_map_create_context(self._internal))

    def load_font(self, arg1, arg2):
        return pango_font_map_load_font(self._internal, arg1._internal, arg2._internal)

    def load_fontset(self, arg1, arg2, arg3):
        return pango_font_map_load_fontset(self._internal, arg1._internal, arg2._internal, arg3)

    def list_families(self, arg1, arg2):
        return pango_font_map_list_families(self._internal, arg1, arg2)

class CairoFontMap(FontMap):
    @classmethod
    def new(self):
        return CairoFontMap._from_internal(pango_cairo_font_map_new())

    @classmethod
    def new_for_font_type(self, arg0):
        return CairoFontMap._from_internal(pango_cairo_font_map_new_for_font_type(arg0))

    def get_default(self):
        return FontMap._from_internal(pango_cairo_font_map_get_default())

    def set_default(self):
        return pango_cairo_font_map_set_default(self._internal)

    def get_font_type(self):
        return pango_cairo_font_map_get_font_type(self._internal)

    def set_resolution(self, arg1):
        return pango_cairo_font_map_set_resolution(self._internal, arg1)

    def get_resolution(self):
        return pango_cairo_font_map_get_resolution(self._internal)

    def create_context(self):
        return Context._from_internal(pango_cairo_font_map_create_context(self._internal))

    def __init__(self, *args, **kwargs):
        self._internal = CairoFontMap.new(*args, **kwargs)._internal

    font_type = property(get_font_type)
    resolution = property(get_resolution, set_resolution)


COVERAGE_NONE = PANGO_COVERAGE_NONE
COVERAGE_FALLBACK = PANGO_COVERAGE_FALLBACK
COVERAGE_APPROXIMATE = PANGO_COVERAGE_APPROXIMATE
COVERAGE_EXACT = PANGO_COVERAGE_EXACT
coverage_new = pango_coverage_new
coverage_ref = pango_coverage_ref
coverage_unref = pango_coverage_unref
coverage_copy = pango_coverage_copy
coverage_get = pango_coverage_get
coverage_set = pango_coverage_set
coverage_max = pango_coverage_max
units_from_double = pango_units_from_double
units_to_double = pango_units_to_double
extents_to_pixels = pango_extents_to_pixels
GRAVITY_SOUTH = PANGO_GRAVITY_SOUTH
GRAVITY_EAST = PANGO_GRAVITY_EAST
GRAVITY_NORTH = PANGO_GRAVITY_NORTH
GRAVITY_WEST = PANGO_GRAVITY_WEST
GRAVITY_AUTO = PANGO_GRAVITY_AUTO
GRAVITY_HINT_NATURAL = PANGO_GRAVITY_HINT_NATURAL
GRAVITY_HINT_STRONG = PANGO_GRAVITY_HINT_STRONG
GRAVITY_HINT_LINE = PANGO_GRAVITY_HINT_LINE
matrix_copy = pango_matrix_copy
matrix_free = pango_matrix_free
matrix_translate = pango_matrix_translate
matrix_scale = pango_matrix_scale
matrix_rotate = pango_matrix_rotate
matrix_concat = pango_matrix_concat
matrix_transform_point = pango_matrix_transform_point
matrix_transform_distance = pango_matrix_transform_distance
matrix_transform_rectangle = pango_matrix_transform_rectangle
matrix_transform_pixel_rectangle = pango_matrix_transform_pixel_rectangle
matrix_get_font_scale_factor = pango_matrix_get_font_scale_factor
SCRIPT_INVALID_CODE = PANGO_SCRIPT_INVALID_CODE
SCRIPT_COMMON = PANGO_SCRIPT_COMMON
SCRIPT_INHERITED = PANGO_SCRIPT_INHERITED
SCRIPT_ARABIC = PANGO_SCRIPT_ARABIC
SCRIPT_ARMENIAN = PANGO_SCRIPT_ARMENIAN
SCRIPT_BENGALI = PANGO_SCRIPT_BENGALI
SCRIPT_BOPOMOFO = PANGO_SCRIPT_BOPOMOFO
SCRIPT_CHEROKEE = PANGO_SCRIPT_CHEROKEE
SCRIPT_COPTIC = PANGO_SCRIPT_COPTIC
SCRIPT_CYRILLIC = PANGO_SCRIPT_CYRILLIC
SCRIPT_DESERET = PANGO_SCRIPT_DESERET
SCRIPT_DEVANAGARI = PANGO_SCRIPT_DEVANAGARI
SCRIPT_ETHIOPIC = PANGO_SCRIPT_ETHIOPIC
SCRIPT_GEORGIAN = PANGO_SCRIPT_GEORGIAN
SCRIPT_GOTHIC = PANGO_SCRIPT_GOTHIC
SCRIPT_GREEK = PANGO_SCRIPT_GREEK
SCRIPT_GUJARATI = PANGO_SCRIPT_GUJARATI
SCRIPT_GURMUKHI = PANGO_SCRIPT_GURMUKHI
SCRIPT_HAN = PANGO_SCRIPT_HAN
SCRIPT_HANGUL = PANGO_SCRIPT_HANGUL
SCRIPT_HEBREW = PANGO_SCRIPT_HEBREW
SCRIPT_HIRAGANA = PANGO_SCRIPT_HIRAGANA
SCRIPT_KANNADA = PANGO_SCRIPT_KANNADA
SCRIPT_KATAKANA = PANGO_SCRIPT_KATAKANA
SCRIPT_KHMER = PANGO_SCRIPT_KHMER
SCRIPT_LAO = PANGO_SCRIPT_LAO
SCRIPT_LATIN = PANGO_SCRIPT_LATIN
SCRIPT_MALAYALAM = PANGO_SCRIPT_MALAYALAM
SCRIPT_MONGOLIAN = PANGO_SCRIPT_MONGOLIAN
SCRIPT_MYANMAR = PANGO_SCRIPT_MYANMAR
SCRIPT_OGHAM = PANGO_SCRIPT_OGHAM
SCRIPT_OLD_ITALIC = PANGO_SCRIPT_OLD_ITALIC
SCRIPT_ORIYA = PANGO_SCRIPT_ORIYA
SCRIPT_RUNIC = PANGO_SCRIPT_RUNIC
SCRIPT_SINHALA = PANGO_SCRIPT_SINHALA
SCRIPT_SYRIAC = PANGO_SCRIPT_SYRIAC
SCRIPT_TAMIL = PANGO_SCRIPT_TAMIL
SCRIPT_TELUGU = PANGO_SCRIPT_TELUGU
SCRIPT_THAANA = PANGO_SCRIPT_THAANA
SCRIPT_THAI = PANGO_SCRIPT_THAI
SCRIPT_TIBETAN = PANGO_SCRIPT_TIBETAN
SCRIPT_CANADIAN_ABORIGINAL = PANGO_SCRIPT_CANADIAN_ABORIGINAL
SCRIPT_YI = PANGO_SCRIPT_YI
SCRIPT_TAGALOG = PANGO_SCRIPT_TAGALOG
SCRIPT_HANUNOO = PANGO_SCRIPT_HANUNOO
SCRIPT_BUHID = PANGO_SCRIPT_BUHID
SCRIPT_TAGBANWA = PANGO_SCRIPT_TAGBANWA
SCRIPT_BRAILLE = PANGO_SCRIPT_BRAILLE
SCRIPT_CYPRIOT = PANGO_SCRIPT_CYPRIOT
SCRIPT_LIMBU = PANGO_SCRIPT_LIMBU
SCRIPT_OSMANYA = PANGO_SCRIPT_OSMANYA
SCRIPT_SHAVIAN = PANGO_SCRIPT_SHAVIAN
SCRIPT_LINEAR_B = PANGO_SCRIPT_LINEAR_B
SCRIPT_TAI_LE = PANGO_SCRIPT_TAI_LE
SCRIPT_UGARITIC = PANGO_SCRIPT_UGARITIC
SCRIPT_NEW_TAI_LUE = PANGO_SCRIPT_NEW_TAI_LUE
SCRIPT_BUGINESE = PANGO_SCRIPT_BUGINESE
SCRIPT_GLAGOLITIC = PANGO_SCRIPT_GLAGOLITIC
SCRIPT_TIFINAGH = PANGO_SCRIPT_TIFINAGH
SCRIPT_SYLOTI_NAGRI = PANGO_SCRIPT_SYLOTI_NAGRI
SCRIPT_OLD_PERSIAN = PANGO_SCRIPT_OLD_PERSIAN
SCRIPT_KHAROSHTHI = PANGO_SCRIPT_KHAROSHTHI
SCRIPT_UNKNOWN = PANGO_SCRIPT_UNKNOWN
SCRIPT_BALINESE = PANGO_SCRIPT_BALINESE
SCRIPT_CUNEIFORM = PANGO_SCRIPT_CUNEIFORM
SCRIPT_PHOENICIAN = PANGO_SCRIPT_PHOENICIAN
SCRIPT_PHAGS_PA = PANGO_SCRIPT_PHAGS_PA
SCRIPT_NKO = PANGO_SCRIPT_NKO
SCRIPT_KAYAH_LI = PANGO_SCRIPT_KAYAH_LI
SCRIPT_LEPCHA = PANGO_SCRIPT_LEPCHA
SCRIPT_REJANG = PANGO_SCRIPT_REJANG
SCRIPT_SUNDANESE = PANGO_SCRIPT_SUNDANESE
SCRIPT_SAURASHTRA = PANGO_SCRIPT_SAURASHTRA
SCRIPT_CHAM = PANGO_SCRIPT_CHAM
SCRIPT_OL_CHIKI = PANGO_SCRIPT_OL_CHIKI
SCRIPT_VAI = PANGO_SCRIPT_VAI
SCRIPT_CARIAN = PANGO_SCRIPT_CARIAN
SCRIPT_LYCIAN = PANGO_SCRIPT_LYCIAN
SCRIPT_LYDIAN = PANGO_SCRIPT_LYDIAN
script_iter_new = pango_script_iter_new
script_iter_get_range = pango_script_iter_get_range
script_iter_free = pango_script_iter_free
language_from_string = pango_language_from_string
language_to_string = pango_language_to_string
language_get_sample_string = pango_language_get_sample_string
language_get_default = pango_language_get_default
language_get_scripts = pango_language_get_scripts
script_get_sample_language = pango_script_get_sample_language
gravity_to_rotation = pango_gravity_to_rotation
gravity_get_for_matrix = pango_gravity_get_for_matrix
gravity_get_for_script = pango_gravity_get_for_script
BIDI_TYPE_L = PANGO_BIDI_TYPE_L
BIDI_TYPE_LRE = PANGO_BIDI_TYPE_LRE
BIDI_TYPE_LRO = PANGO_BIDI_TYPE_LRO
BIDI_TYPE_R = PANGO_BIDI_TYPE_R
BIDI_TYPE_AL = PANGO_BIDI_TYPE_AL
BIDI_TYPE_RLE = PANGO_BIDI_TYPE_RLE
BIDI_TYPE_RLO = PANGO_BIDI_TYPE_RLO
BIDI_TYPE_PDF = PANGO_BIDI_TYPE_PDF
BIDI_TYPE_EN = PANGO_BIDI_TYPE_EN
BIDI_TYPE_ES = PANGO_BIDI_TYPE_ES
BIDI_TYPE_ET = PANGO_BIDI_TYPE_ET
BIDI_TYPE_AN = PANGO_BIDI_TYPE_AN
BIDI_TYPE_CS = PANGO_BIDI_TYPE_CS
BIDI_TYPE_NSM = PANGO_BIDI_TYPE_NSM
BIDI_TYPE_BN = PANGO_BIDI_TYPE_BN
BIDI_TYPE_B = PANGO_BIDI_TYPE_B
BIDI_TYPE_S = PANGO_BIDI_TYPE_S
BIDI_TYPE_WS = PANGO_BIDI_TYPE_WS
BIDI_TYPE_ON = PANGO_BIDI_TYPE_ON
DIRECTION_LTR = PANGO_DIRECTION_LTR
DIRECTION_RTL = PANGO_DIRECTION_RTL
DIRECTION_TTB_LTR = PANGO_DIRECTION_TTB_LTR
DIRECTION_TTB_RTL = PANGO_DIRECTION_TTB_RTL
DIRECTION_WEAK_LTR = PANGO_DIRECTION_WEAK_LTR
DIRECTION_WEAK_RTL = PANGO_DIRECTION_WEAK_RTL
DIRECTION_NEUTRAL = PANGO_DIRECTION_NEUTRAL
STYLE_NORMAL = PANGO_STYLE_NORMAL
STYLE_OBLIQUE = PANGO_STYLE_OBLIQUE
STYLE_ITALIC = PANGO_STYLE_ITALIC
VARIANT_NORMAL = PANGO_VARIANT_NORMAL
VARIANT_SMALL_CAPS = PANGO_VARIANT_SMALL_CAPS
WEIGHT_THIN = PANGO_WEIGHT_THIN
WEIGHT_ULTRALIGHT = PANGO_WEIGHT_ULTRALIGHT
WEIGHT_LIGHT = PANGO_WEIGHT_LIGHT
WEIGHT_BOOK = PANGO_WEIGHT_BOOK
WEIGHT_NORMAL = PANGO_WEIGHT_NORMAL
WEIGHT_MEDIUM = PANGO_WEIGHT_MEDIUM
WEIGHT_SEMIBOLD = PANGO_WEIGHT_SEMIBOLD
WEIGHT_BOLD = PANGO_WEIGHT_BOLD
WEIGHT_ULTRABOLD = PANGO_WEIGHT_ULTRABOLD
WEIGHT_HEAVY = PANGO_WEIGHT_HEAVY
WEIGHT_ULTRAHEAVY = PANGO_WEIGHT_ULTRAHEAVY
STRETCH_ULTRA_CONDENSED = PANGO_STRETCH_ULTRA_CONDENSED
STRETCH_EXTRA_CONDENSED = PANGO_STRETCH_EXTRA_CONDENSED
STRETCH_CONDENSED = PANGO_STRETCH_CONDENSED
STRETCH_SEMI_CONDENSED = PANGO_STRETCH_SEMI_CONDENSED
STRETCH_NORMAL = PANGO_STRETCH_NORMAL
STRETCH_SEMI_EXPANDED = PANGO_STRETCH_SEMI_EXPANDED
STRETCH_EXPANDED = PANGO_STRETCH_EXPANDED
STRETCH_EXTRA_EXPANDED = PANGO_STRETCH_EXTRA_EXPANDED
STRETCH_ULTRA_EXPANDED = PANGO_STRETCH_ULTRA_EXPANDED
FONT_MASK_FAMILY = PANGO_FONT_MASK_FAMILY
FONT_MASK_STYLE = PANGO_FONT_MASK_STYLE
FONT_MASK_VARIANT = PANGO_FONT_MASK_VARIANT
FONT_MASK_WEIGHT = PANGO_FONT_MASK_WEIGHT
FONT_MASK_STRETCH = PANGO_FONT_MASK_STRETCH
FONT_MASK_SIZE = PANGO_FONT_MASK_SIZE
FONT_MASK_GRAVITY = PANGO_FONT_MASK_GRAVITY
font_description_new = pango_font_description_new
font_description_copy = pango_font_description_copy
font_description_copy_static = pango_font_description_copy_static
font_description_free = pango_font_description_free
font_descriptions_free = pango_font_descriptions_free
font_description_set_family = pango_font_description_set_family
font_description_set_family_static = pango_font_description_set_family_static
font_description_get_family = pango_font_description_get_family
font_description_set_style = pango_font_description_set_style
font_description_get_style = pango_font_description_get_style
font_description_set_variant = pango_font_description_set_variant
font_description_get_variant = pango_font_description_get_variant
font_description_set_weight = pango_font_description_set_weight
font_description_get_weight = pango_font_description_get_weight
font_description_set_stretch = pango_font_description_set_stretch
font_description_get_stretch = pango_font_description_get_stretch
font_description_set_absolute_size = pango_font_description_set_absolute_size
font_description_set_gravity = pango_font_description_set_gravity
font_description_get_gravity = pango_font_description_get_gravity
font_description_get_set_fields = pango_font_description_get_set_fields
font_description_unset_fields = pango_font_description_unset_fields
font_description_from_string = pango_font_description_from_string
font_description_to_string = pango_font_description_to_string
font_description_to_filename = pango_font_description_to_filename
font_metrics_ref = pango_font_metrics_ref
font_metrics_unref = pango_font_metrics_unref
font_metrics_get_ascent = pango_font_metrics_get_ascent
font_metrics_get_descent = pango_font_metrics_get_descent
font_metrics_get_approximate_char_width = pango_font_metrics_get_approximate_char_width
font_metrics_get_approximate_digit_width = pango_font_metrics_get_approximate_digit_width
font_metrics_get_underline_position = pango_font_metrics_get_underline_position
font_metrics_get_underline_thickness = pango_font_metrics_get_underline_thickness
font_metrics_get_strikethrough_position = pango_font_metrics_get_strikethrough_position
font_metrics_get_strikethrough_thickness = pango_font_metrics_get_strikethrough_thickness
font_family_list_faces = pango_font_family_list_faces
font_family_get_name = pango_font_family_get_name
font_face_describe = pango_font_face_describe
font_face_get_face_name = pango_font_face_get_face_name
font_face_list_sizes = pango_font_face_list_sizes
font_describe = pango_font_describe
font_describe_with_absolute_size = pango_font_describe_with_absolute_size
font_get_coverage = pango_font_get_coverage
font_find_shaper = pango_font_find_shaper
font_get_metrics = pango_font_get_metrics
font_get_glyph_extents = pango_font_get_glyph_extents
font_get_font_map = pango_font_get_font_map
color_copy = pango_color_copy
color_free = pango_color_free
ATTR_INVALID = PANGO_ATTR_INVALID
ATTR_LANGUAGE = PANGO_ATTR_LANGUAGE
ATTR_FAMILY = PANGO_ATTR_FAMILY
ATTR_STYLE = PANGO_ATTR_STYLE
ATTR_WEIGHT = PANGO_ATTR_WEIGHT
ATTR_VARIANT = PANGO_ATTR_VARIANT
ATTR_STRETCH = PANGO_ATTR_STRETCH
ATTR_SIZE = PANGO_ATTR_SIZE
ATTR_FONT_DESC = PANGO_ATTR_FONT_DESC
ATTR_FOREGROUND = PANGO_ATTR_FOREGROUND
ATTR_BACKGROUND = PANGO_ATTR_BACKGROUND
ATTR_UNDERLINE = PANGO_ATTR_UNDERLINE
ATTR_STRIKETHROUGH = PANGO_ATTR_STRIKETHROUGH
ATTR_RISE = PANGO_ATTR_RISE
ATTR_SHAPE = PANGO_ATTR_SHAPE
ATTR_SCALE = PANGO_ATTR_SCALE
ATTR_FALLBACK = PANGO_ATTR_FALLBACK
ATTR_LETTER_SPACING = PANGO_ATTR_LETTER_SPACING
ATTR_UNDERLINE_COLOR = PANGO_ATTR_UNDERLINE_COLOR
ATTR_STRIKETHROUGH_COLOR = PANGO_ATTR_STRIKETHROUGH_COLOR
ATTR_ABSOLUTE_SIZE = PANGO_ATTR_ABSOLUTE_SIZE
ATTR_GRAVITY = PANGO_ATTR_GRAVITY
ATTR_GRAVITY_HINT = PANGO_ATTR_GRAVITY_HINT
UNDERLINE_NONE = PANGO_UNDERLINE_NONE
UNDERLINE_SINGLE = PANGO_UNDERLINE_SINGLE
UNDERLINE_DOUBLE = PANGO_UNDERLINE_DOUBLE
UNDERLINE_LOW = PANGO_UNDERLINE_LOW
UNDERLINE_ERROR = PANGO_UNDERLINE_ERROR
attr_type_get_name = pango_attr_type_get_name
attribute_init = pango_attribute_init
attribute_copy = pango_attribute_copy
attribute_destroy = pango_attribute_destroy
attr_language_new = pango_attr_language_new
attr_family_new = pango_attr_family_new
attr_foreground_new = pango_attr_foreground_new
attr_background_new = pango_attr_background_new
attr_size_new = pango_attr_size_new
attr_size_new_absolute = pango_attr_size_new_absolute
attr_style_new = pango_attr_style_new
attr_weight_new = pango_attr_weight_new
attr_variant_new = pango_attr_variant_new
attr_stretch_new = pango_attr_stretch_new
attr_font_desc_new = pango_attr_font_desc_new
attr_underline_new = pango_attr_underline_new
attr_underline_color_new = pango_attr_underline_color_new
attr_strikethrough_color_new = pango_attr_strikethrough_color_new
attr_rise_new = pango_attr_rise_new
attr_scale_new = pango_attr_scale_new
attr_letter_spacing_new = pango_attr_letter_spacing_new
attr_shape_new = pango_attr_shape_new
attr_gravity_new = pango_attr_gravity_new
attr_gravity_hint_new = pango_attr_gravity_hint_new
attr_list_new = pango_attr_list_new
attr_list_ref = pango_attr_list_ref
attr_list_unref = pango_attr_list_unref
attr_list_copy = pango_attr_list_copy
attr_list_insert = pango_attr_list_insert
attr_list_insert_before = pango_attr_list_insert_before
attr_list_change = pango_attr_list_change
attr_list_get_iterator = pango_attr_list_get_iterator
attr_iterator_copy = pango_attr_iterator_copy
attr_iterator_destroy = pango_attr_iterator_destroy
attr_iterator_get = pango_attr_iterator_get
item_new = pango_item_new
item_copy = pango_item_copy
item_free = pango_item_free
item_split = pango_item_split
get_log_attrs = pango_get_log_attrs
fontset_get_metrics = pango_fontset_get_metrics
font_map_create_context = pango_font_map_create_context
font_map_load_font = pango_font_map_load_font
font_map_load_fontset = pango_font_map_load_fontset
font_map_list_families = pango_font_map_list_families
context_new = pango_context_new
context_set_font_map = pango_context_set_font_map
context_get_font_map = pango_context_get_font_map
context_list_families = pango_context_list_families
context_load_font = pango_context_load_font
context_load_fontset = pango_context_load_fontset
context_get_metrics = pango_context_get_metrics
context_set_font_description = pango_context_set_font_description
context_get_font_description = pango_context_get_font_description
context_get_language = pango_context_get_language
context_set_language = pango_context_set_language
context_set_base_dir = pango_context_set_base_dir
context_get_base_dir = pango_context_get_base_dir
context_set_base_gravity = pango_context_set_base_gravity
context_get_base_gravity = pango_context_get_base_gravity
context_get_gravity = pango_context_get_gravity
context_set_gravity_hint = pango_context_set_gravity_hint
context_get_gravity_hint = pango_context_get_gravity_hint
context_set_matrix = pango_context_set_matrix
context_get_matrix = pango_context_get_matrix
glyph_string_new = pango_glyph_string_new
glyph_string_copy = pango_glyph_string_copy
glyph_string_free = pango_glyph_string_free
glyph_string_extents = pango_glyph_string_extents
glyph_string_get_width = pango_glyph_string_get_width
glyph_string_extents_range = pango_glyph_string_extents_range
glyph_string_get_logical_widths = pango_glyph_string_get_logical_widths
glyph_string_x_to_index = pango_glyph_string_x_to_index
glyph_item_split = pango_glyph_item_split
glyph_item_copy = pango_glyph_item_copy
glyph_item_free = pango_glyph_item_free
glyph_item_letter_space = pango_glyph_item_letter_space
glyph_item_iter_copy = pango_glyph_item_iter_copy
glyph_item_iter_free = pango_glyph_item_iter_free
TAB_LEFT = PANGO_TAB_LEFT
tab_array_copy = pango_tab_array_copy
tab_array_free = pango_tab_array_free
ALIGN_LEFT = PANGO_ALIGN_LEFT
ALIGN_CENTER = PANGO_ALIGN_CENTER
ALIGN_RIGHT = PANGO_ALIGN_RIGHT
WRAP_WORD = PANGO_WRAP_WORD
WRAP_CHAR = PANGO_WRAP_CHAR
WRAP_WORD_CHAR = PANGO_WRAP_WORD_CHAR
ELLIPSIZE_NONE = PANGO_ELLIPSIZE_NONE
ELLIPSIZE_START = PANGO_ELLIPSIZE_START
ELLIPSIZE_MIDDLE = PANGO_ELLIPSIZE_MIDDLE
ELLIPSIZE_END = PANGO_ELLIPSIZE_END
layout_new = pango_layout_new
layout_copy = pango_layout_copy
layout_get_context = pango_layout_get_context
layout_set_attributes = pango_layout_set_attributes
layout_get_attributes = pango_layout_get_attributes
layout_set_text = pango_layout_set_text
layout_get_text = pango_layout_get_text
layout_set_markup = pango_layout_set_markup
layout_set_font_description = pango_layout_set_font_description
layout_get_font_description = pango_layout_get_font_description
layout_set_width = pango_layout_set_width
layout_get_width = pango_layout_get_width
layout_set_height = pango_layout_set_height
layout_get_height = pango_layout_get_height
layout_set_wrap = pango_layout_set_wrap
layout_get_wrap = pango_layout_get_wrap
layout_set_indent = pango_layout_set_indent
layout_get_indent = pango_layout_get_indent
layout_set_spacing = pango_layout_set_spacing
layout_get_spacing = pango_layout_get_spacing
layout_set_alignment = pango_layout_set_alignment
layout_get_alignment = pango_layout_get_alignment
layout_set_tabs = pango_layout_set_tabs
layout_get_tabs = pango_layout_get_tabs
layout_set_ellipsize = pango_layout_set_ellipsize
layout_get_ellipsize = pango_layout_get_ellipsize
layout_get_unknown_glyphs_count = pango_layout_get_unknown_glyphs_count
layout_context_changed = pango_layout_context_changed
layout_index_to_pos = pango_layout_index_to_pos
layout_get_cursor_pos = pango_layout_get_cursor_pos
layout_get_extents = pango_layout_get_extents
layout_get_pixel_extents = pango_layout_get_pixel_extents
layout_get_size = pango_layout_get_size
layout_get_pixel_size = pango_layout_get_pixel_size
layout_get_baseline = pango_layout_get_baseline
layout_get_line_count = pango_layout_get_line_count
layout_get_line = pango_layout_get_line
layout_get_line_readonly = pango_layout_get_line_readonly
layout_line_ref = pango_layout_line_ref
layout_line_unref = pango_layout_line_unref
layout_line_get_x_ranges = pango_layout_line_get_x_ranges
layout_line_get_extents = pango_layout_line_get_extents
layout_line_get_pixel_extents = pango_layout_line_get_pixel_extents
layout_get_iter = pango_layout_get_iter
layout_iter_copy = pango_layout_iter_copy
layout_iter_free = pango_layout_iter_free
layout_iter_get_index = pango_layout_iter_get_index
layout_iter_get_run = pango_layout_iter_get_run
layout_iter_get_run_readonly = pango_layout_iter_get_run_readonly
layout_iter_get_line = pango_layout_iter_get_line
layout_iter_get_line_readonly = pango_layout_iter_get_line_readonly
layout_iter_get_layout = pango_layout_iter_get_layout
layout_iter_get_char_extents = pango_layout_iter_get_char_extents
layout_iter_get_cluster_extents = pango_layout_iter_get_cluster_extents
layout_iter_get_run_extents = pango_layout_iter_get_run_extents
layout_iter_get_line_extents = pango_layout_iter_get_line_extents
layout_iter_get_line_yrange = pango_layout_iter_get_line_yrange
layout_iter_get_layout_extents = pango_layout_iter_get_layout_extents
layout_iter_get_baseline = pango_layout_iter_get_baseline
RENDER_PART_FOREGROUND = PANGO_RENDER_PART_FOREGROUND
RENDER_PART_BACKGROUND = PANGO_RENDER_PART_BACKGROUND
RENDER_PART_UNDERLINE = PANGO_RENDER_PART_UNDERLINE
RENDER_PART_STRIKETHROUGH = PANGO_RENDER_PART_STRIKETHROUGH
renderer_draw_layout = pango_renderer_draw_layout
renderer_draw_layout_line = pango_renderer_draw_layout_line
renderer_draw_glyphs = pango_renderer_draw_glyphs
renderer_draw_glyph_item = pango_renderer_draw_glyph_item
renderer_draw_rectangle = pango_renderer_draw_rectangle
renderer_draw_error_underline = pango_renderer_draw_error_underline
renderer_draw_trapezoid = pango_renderer_draw_trapezoid
renderer_draw_glyph = pango_renderer_draw_glyph
renderer_activate = pango_renderer_activate
renderer_deactivate = pango_renderer_deactivate
renderer_part_changed = pango_renderer_part_changed
renderer_set_color = pango_renderer_set_color
renderer_get_color = pango_renderer_get_color
renderer_set_matrix = pango_renderer_set_matrix
renderer_get_matrix = pango_renderer_get_matrix
renderer_get_layout = pango_renderer_get_layout
renderer_get_layout_line = pango_renderer_get_layout_line
split_file_list = pango_split_file_list
trim_string = pango_trim_string
quantize_line_geometry = pango_quantize_line_geometry
version = pango_version
version_string = pango_version_string
version_check = pango_version_check
cairo_font_map_new = pango_cairo_font_map_new
cairo_font_map_new_for_font_type = pango_cairo_font_map_new_for_font_type
cairo_font_map_get_default = pango_cairo_font_map_get_default
cairo_font_map_set_default = pango_cairo_font_map_set_default
cairo_font_map_get_font_type = pango_cairo_font_map_get_font_type
cairo_font_map_set_resolution = pango_cairo_font_map_set_resolution
cairo_font_map_get_resolution = pango_cairo_font_map_get_resolution
cairo_font_map_create_context = pango_cairo_font_map_create_context
cairo_font_get_scaled_font = pango_cairo_font_get_scaled_font
cairo_update_context = pango_cairo_update_context
cairo_context_set_font_options = pango_cairo_context_set_font_options
cairo_context_get_font_options = pango_cairo_context_get_font_options
cairo_context_set_resolution = pango_cairo_context_set_resolution
cairo_context_get_resolution = pango_cairo_context_get_resolution
cairo_create_context = pango_cairo_create_context
cairo_create_layout = pango_cairo_create_layout
cairo_update_layout = pango_cairo_update_layout
cairo_show_glyph_string = pango_cairo_show_glyph_string
cairo_show_glyph_item = pango_cairo_show_glyph_item
cairo_show_layout_line = pango_cairo_show_layout_line
cairo_show_layout = pango_cairo_show_layout
cairo_show_error_underline = pango_cairo_show_error_underline
cairo_glyph_string_path = pango_cairo_glyph_string_path
cairo_layout_line_path = pango_cairo_layout_line_path
cairo_layout_path = pango_cairo_layout_path
cairo_error_underline_path = pango_cairo_error_underline_path

__all__ = ['gint8', 'guint8', 'gint16', 'guint16', 'gint32', 'guint32',
'gint64', 'guint64', 'gssize', 'gsize', 'goffset', 'gintptr', 'guintptr',
'GStaticMutex', 'GSystemThread', 'GPid', 'PangoCoverage',
'PangoCoverageLevel', 'PANGO_COVERAGE_NONE', 'PANGO_COVERAGE_FALLBACK',
'PANGO_COVERAGE_APPROXIMATE', 'PANGO_COVERAGE_EXACT', 'pango_coverage_new',
'pango_coverage_ref', 'pango_coverage_unref', 'pango_coverage_copy',
'pango_coverage_get', 'pango_coverage_set', 'pango_coverage_max',
'PangoLogAttr', 'PangoEngineLang', 'PangoEngineShape', 'PangoFont',
'PangoFontMap', 'PangoRectangle', 'PangoGlyph', 'pango_units_from_double',
'pango_units_to_double', 'pango_extents_to_pixels', 'PangoGravity',
'PANGO_GRAVITY_SOUTH', 'PANGO_GRAVITY_EAST', 'PANGO_GRAVITY_NORTH',
'PANGO_GRAVITY_WEST', 'PANGO_GRAVITY_AUTO', 'PangoGravityHint',
'PANGO_GRAVITY_HINT_NATURAL', 'PANGO_GRAVITY_HINT_STRONG',
'PANGO_GRAVITY_HINT_LINE', 'PangoMatrix', 'pango_matrix_copy',
'pango_matrix_free', 'pango_matrix_translate', 'pango_matrix_scale',
'pango_matrix_rotate', 'pango_matrix_concat', 'pango_matrix_transform_point',
'pango_matrix_transform_distance', 'pango_matrix_transform_rectangle',
'pango_matrix_transform_pixel_rectangle',
'pango_matrix_get_font_scale_factor', 'PangoScriptIter', 'PangoScript',
'PANGO_SCRIPT_INVALID_CODE', 'PANGO_SCRIPT_COMMON', 'PANGO_SCRIPT_INHERITED',
'PANGO_SCRIPT_ARABIC', 'PANGO_SCRIPT_ARMENIAN', 'PANGO_SCRIPT_BENGALI',
'PANGO_SCRIPT_BOPOMOFO', 'PANGO_SCRIPT_CHEROKEE', 'PANGO_SCRIPT_COPTIC',
'PANGO_SCRIPT_CYRILLIC', 'PANGO_SCRIPT_DESERET', 'PANGO_SCRIPT_DEVANAGARI',
'PANGO_SCRIPT_ETHIOPIC', 'PANGO_SCRIPT_GEORGIAN', 'PANGO_SCRIPT_GOTHIC',
'PANGO_SCRIPT_GREEK', 'PANGO_SCRIPT_GUJARATI', 'PANGO_SCRIPT_GURMUKHI',
'PANGO_SCRIPT_HAN', 'PANGO_SCRIPT_HANGUL', 'PANGO_SCRIPT_HEBREW',
'PANGO_SCRIPT_HIRAGANA', 'PANGO_SCRIPT_KANNADA', 'PANGO_SCRIPT_KATAKANA',
'PANGO_SCRIPT_KHMER', 'PANGO_SCRIPT_LAO', 'PANGO_SCRIPT_LATIN',
'PANGO_SCRIPT_MALAYALAM', 'PANGO_SCRIPT_MONGOLIAN', 'PANGO_SCRIPT_MYANMAR',
'PANGO_SCRIPT_OGHAM', 'PANGO_SCRIPT_OLD_ITALIC', 'PANGO_SCRIPT_ORIYA',
'PANGO_SCRIPT_RUNIC', 'PANGO_SCRIPT_SINHALA', 'PANGO_SCRIPT_SYRIAC',
'PANGO_SCRIPT_TAMIL', 'PANGO_SCRIPT_TELUGU', 'PANGO_SCRIPT_THAANA',
'PANGO_SCRIPT_THAI', 'PANGO_SCRIPT_TIBETAN',
'PANGO_SCRIPT_CANADIAN_ABORIGINAL', 'PANGO_SCRIPT_YI', 'PANGO_SCRIPT_TAGALOG',
'PANGO_SCRIPT_HANUNOO', 'PANGO_SCRIPT_BUHID', 'PANGO_SCRIPT_TAGBANWA',
'PANGO_SCRIPT_BRAILLE', 'PANGO_SCRIPT_CYPRIOT', 'PANGO_SCRIPT_LIMBU',
'PANGO_SCRIPT_OSMANYA', 'PANGO_SCRIPT_SHAVIAN', 'PANGO_SCRIPT_LINEAR_B',
'PANGO_SCRIPT_TAI_LE', 'PANGO_SCRIPT_UGARITIC', 'PANGO_SCRIPT_NEW_TAI_LUE',
'PANGO_SCRIPT_BUGINESE', 'PANGO_SCRIPT_GLAGOLITIC', 'PANGO_SCRIPT_TIFINAGH',
'PANGO_SCRIPT_SYLOTI_NAGRI', 'PANGO_SCRIPT_OLD_PERSIAN',
'PANGO_SCRIPT_KHAROSHTHI', 'PANGO_SCRIPT_UNKNOWN', 'PANGO_SCRIPT_BALINESE',
'PANGO_SCRIPT_CUNEIFORM', 'PANGO_SCRIPT_PHOENICIAN', 'PANGO_SCRIPT_PHAGS_PA',
'PANGO_SCRIPT_NKO', 'PANGO_SCRIPT_KAYAH_LI', 'PANGO_SCRIPT_LEPCHA',
'PANGO_SCRIPT_REJANG', 'PANGO_SCRIPT_SUNDANESE', 'PANGO_SCRIPT_SAURASHTRA',
'PANGO_SCRIPT_CHAM', 'PANGO_SCRIPT_OL_CHIKI', 'PANGO_SCRIPT_VAI',
'PANGO_SCRIPT_CARIAN', 'PANGO_SCRIPT_LYCIAN', 'PANGO_SCRIPT_LYDIAN',
'pango_script_iter_new', 'pango_script_iter_get_range',
'pango_script_iter_free', 'PangoLanguage', 'pango_language_from_string',
'pango_language_to_string', 'pango_language_get_sample_string',
'pango_language_get_default', 'pango_language_get_scripts',
'pango_script_get_sample_language', 'pango_gravity_to_rotation',
'pango_gravity_get_for_matrix', 'pango_gravity_get_for_script',
'PangoBidiType', 'PANGO_BIDI_TYPE_L', 'PANGO_BIDI_TYPE_LRE',
'PANGO_BIDI_TYPE_LRO', 'PANGO_BIDI_TYPE_R', 'PANGO_BIDI_TYPE_AL',
'PANGO_BIDI_TYPE_RLE', 'PANGO_BIDI_TYPE_RLO', 'PANGO_BIDI_TYPE_PDF',
'PANGO_BIDI_TYPE_EN', 'PANGO_BIDI_TYPE_ES', 'PANGO_BIDI_TYPE_ET',
'PANGO_BIDI_TYPE_AN', 'PANGO_BIDI_TYPE_CS', 'PANGO_BIDI_TYPE_NSM',
'PANGO_BIDI_TYPE_BN', 'PANGO_BIDI_TYPE_B', 'PANGO_BIDI_TYPE_S',
'PANGO_BIDI_TYPE_WS', 'PANGO_BIDI_TYPE_ON', 'PangoDirection',
'PANGO_DIRECTION_LTR', 'PANGO_DIRECTION_RTL', 'PANGO_DIRECTION_TTB_LTR',
'PANGO_DIRECTION_TTB_RTL', 'PANGO_DIRECTION_WEAK_LTR',
'PANGO_DIRECTION_WEAK_RTL', 'PANGO_DIRECTION_NEUTRAL', 'PangoFontDescription',
'PangoFontMetrics', 'PangoStyle', 'PANGO_STYLE_NORMAL', 'PANGO_STYLE_OBLIQUE',
'PANGO_STYLE_ITALIC', 'PangoVariant', 'PANGO_VARIANT_NORMAL',
'PANGO_VARIANT_SMALL_CAPS', 'PangoWeight', 'PANGO_WEIGHT_THIN',
'PANGO_WEIGHT_ULTRALIGHT', 'PANGO_WEIGHT_LIGHT', 'PANGO_WEIGHT_BOOK',
'PANGO_WEIGHT_NORMAL', 'PANGO_WEIGHT_MEDIUM', 'PANGO_WEIGHT_SEMIBOLD',
'PANGO_WEIGHT_BOLD', 'PANGO_WEIGHT_ULTRABOLD', 'PANGO_WEIGHT_HEAVY',
'PANGO_WEIGHT_ULTRAHEAVY', 'PangoStretch', 'PANGO_STRETCH_ULTRA_CONDENSED',
'PANGO_STRETCH_EXTRA_CONDENSED', 'PANGO_STRETCH_CONDENSED',
'PANGO_STRETCH_SEMI_CONDENSED', 'PANGO_STRETCH_NORMAL',
'PANGO_STRETCH_SEMI_EXPANDED', 'PANGO_STRETCH_EXPANDED',
'PANGO_STRETCH_EXTRA_EXPANDED', 'PANGO_STRETCH_ULTRA_EXPANDED',
'PangoFontMask', 'PANGO_FONT_MASK_FAMILY', 'PANGO_FONT_MASK_STYLE',
'PANGO_FONT_MASK_VARIANT', 'PANGO_FONT_MASK_WEIGHT',
'PANGO_FONT_MASK_STRETCH', 'PANGO_FONT_MASK_SIZE', 'PANGO_FONT_MASK_GRAVITY',
'pango_font_description_new', 'pango_font_description_copy',
'pango_font_description_copy_static', 'pango_font_description_free',
'pango_font_descriptions_free', 'pango_font_description_set_family',
'pango_font_description_set_family_static',
'pango_font_description_get_family', 'pango_font_description_set_style',
'pango_font_description_get_style', 'pango_font_description_set_variant',
'pango_font_description_get_variant', 'pango_font_description_set_weight',
'pango_font_description_get_weight', 'pango_font_description_set_stretch',
'pango_font_description_get_stretch',
'pango_font_description_set_absolute_size',
'pango_font_description_set_gravity', 'pango_font_description_get_gravity',
'pango_font_description_get_set_fields',
'pango_font_description_unset_fields', 'pango_font_description_from_string',
'pango_font_description_to_string', 'pango_font_description_to_filename',
'pango_font_metrics_ref', 'pango_font_metrics_unref',
'pango_font_metrics_get_ascent', 'pango_font_metrics_get_descent',
'pango_font_metrics_get_approximate_char_width',
'pango_font_metrics_get_approximate_digit_width',
'pango_font_metrics_get_underline_position',
'pango_font_metrics_get_underline_thickness',
'pango_font_metrics_get_strikethrough_position',
'pango_font_metrics_get_strikethrough_thickness', 'PangoFontFamily',
'PangoFontFace', 'pango_font_family_list_faces', 'pango_font_family_get_name',
'pango_font_face_describe', 'pango_font_face_get_face_name',
'pango_font_face_list_sizes', 'pango_font_describe',
'pango_font_describe_with_absolute_size', 'pango_font_get_coverage',
'pango_font_find_shaper', 'pango_font_get_metrics',
'pango_font_get_glyph_extents', 'pango_font_get_font_map', 'PangoColor',
'pango_color_copy', 'pango_color_free', 'PangoAttribute', 'PangoAttrClass',
'PangoAttrString', 'PangoAttrLanguage', 'PangoAttrInt', 'PangoAttrSize',
'PangoAttrFloat', 'PangoAttrColor', 'PangoAttrFontDesc', 'PangoAttrShape',
'PangoAttrList', 'PangoAttrIterator', 'PangoAttrType', 'PANGO_ATTR_INVALID',
'PANGO_ATTR_LANGUAGE', 'PANGO_ATTR_FAMILY', 'PANGO_ATTR_STYLE',
'PANGO_ATTR_WEIGHT', 'PANGO_ATTR_VARIANT', 'PANGO_ATTR_STRETCH',
'PANGO_ATTR_SIZE', 'PANGO_ATTR_FONT_DESC', 'PANGO_ATTR_FOREGROUND',
'PANGO_ATTR_BACKGROUND', 'PANGO_ATTR_UNDERLINE', 'PANGO_ATTR_STRIKETHROUGH',
'PANGO_ATTR_RISE', 'PANGO_ATTR_SHAPE', 'PANGO_ATTR_SCALE',
'PANGO_ATTR_FALLBACK', 'PANGO_ATTR_LETTER_SPACING',
'PANGO_ATTR_UNDERLINE_COLOR', 'PANGO_ATTR_STRIKETHROUGH_COLOR',
'PANGO_ATTR_ABSOLUTE_SIZE', 'PANGO_ATTR_GRAVITY', 'PANGO_ATTR_GRAVITY_HINT',
'PangoUnderline', 'PANGO_UNDERLINE_NONE', 'PANGO_UNDERLINE_SINGLE',
'PANGO_UNDERLINE_DOUBLE', 'PANGO_UNDERLINE_LOW', 'PANGO_UNDERLINE_ERROR',
'pango_attr_type_get_name', 'pango_attribute_init', 'pango_attribute_copy',
'pango_attribute_destroy', 'pango_attr_language_new', 'pango_attr_family_new',
'pango_attr_foreground_new', 'pango_attr_background_new',
'pango_attr_size_new', 'pango_attr_size_new_absolute', 'pango_attr_style_new',
'pango_attr_weight_new', 'pango_attr_variant_new', 'pango_attr_stretch_new',
'pango_attr_font_desc_new', 'pango_attr_underline_new',
'pango_attr_underline_color_new', 'pango_attr_strikethrough_color_new',
'pango_attr_rise_new', 'pango_attr_scale_new',
'pango_attr_letter_spacing_new', 'pango_attr_shape_new',
'pango_attr_gravity_new', 'pango_attr_gravity_hint_new',
'pango_attr_list_new', 'pango_attr_list_ref', 'pango_attr_list_unref',
'pango_attr_list_copy', 'pango_attr_list_insert',
'pango_attr_list_insert_before', 'pango_attr_list_change',
'pango_attr_list_get_iterator', 'pango_attr_iterator_copy',
'pango_attr_iterator_destroy', 'pango_attr_iterator_get', 'PangoAnalysis',
'PangoItem', 'pango_item_new', 'pango_item_copy', 'pango_item_free',
'pango_item_split', 'pango_get_log_attrs', 'PangoFontset',
'pango_fontset_get_metrics', 'PangoContext', 'pango_font_map_create_context',
'pango_font_map_load_font', 'pango_font_map_load_fontset',
'pango_font_map_list_families', 'PangoContextClass', 'pango_context_new',
'pango_context_set_font_map', 'pango_context_get_font_map',
'pango_context_list_families', 'pango_context_load_font',
'pango_context_load_fontset', 'pango_context_get_metrics',
'pango_context_set_font_description', 'pango_context_get_font_description',
'pango_context_get_language', 'pango_context_set_language',
'pango_context_set_base_dir', 'pango_context_get_base_dir',
'pango_context_set_base_gravity', 'pango_context_get_base_gravity',
'pango_context_get_gravity', 'pango_context_set_gravity_hint',
'pango_context_get_gravity_hint', 'pango_context_set_matrix',
'pango_context_get_matrix', 'PangoGlyphGeometry', 'PangoGlyphVisAttr',
'PangoGlyphInfo', 'PangoGlyphString', 'PangoGlyphUnit',
'pango_glyph_string_new', 'pango_glyph_string_copy',
'pango_glyph_string_free', 'pango_glyph_string_extents',
'pango_glyph_string_get_width', 'pango_glyph_string_extents_range',
'pango_glyph_string_get_logical_widths', 'pango_glyph_string_x_to_index',
'PangoGlyphItem', 'pango_glyph_item_split', 'pango_glyph_item_copy',
'pango_glyph_item_free', 'pango_glyph_item_letter_space',
'PangoGlyphItemIter', 'pango_glyph_item_iter_copy',
'pango_glyph_item_iter_free', 'PangoTabArray', 'PangoTabAlign',
'PANGO_TAB_LEFT', 'pango_tab_array_copy', 'pango_tab_array_free',
'PangoLayout', 'PangoLayoutClass', 'PangoLayoutLine', 'PangoLayoutRun',
'PangoAlignment', 'PANGO_ALIGN_LEFT', 'PANGO_ALIGN_CENTER',
'PANGO_ALIGN_RIGHT', 'PangoWrapMode', 'PANGO_WRAP_WORD', 'PANGO_WRAP_CHAR',
'PANGO_WRAP_WORD_CHAR', 'PangoEllipsizeMode', 'PANGO_ELLIPSIZE_NONE',
'PANGO_ELLIPSIZE_START', 'PANGO_ELLIPSIZE_MIDDLE', 'PANGO_ELLIPSIZE_END',
'pango_layout_new', 'pango_layout_copy', 'pango_layout_get_context',
'pango_layout_set_attributes', 'pango_layout_get_attributes',
'pango_layout_set_text', 'pango_layout_get_text', 'pango_layout_set_markup',
'pango_layout_set_font_description', 'pango_layout_get_font_description',
'pango_layout_set_width', 'pango_layout_get_width', 'pango_layout_set_height',
'pango_layout_get_height', 'pango_layout_set_wrap', 'pango_layout_get_wrap',
'pango_layout_set_indent', 'pango_layout_get_indent',
'pango_layout_set_spacing', 'pango_layout_get_spacing',
'pango_layout_set_alignment', 'pango_layout_get_alignment',
'pango_layout_set_tabs', 'pango_layout_get_tabs',
'pango_layout_set_ellipsize', 'pango_layout_get_ellipsize',
'pango_layout_get_unknown_glyphs_count', 'pango_layout_context_changed',
'pango_layout_index_to_pos', 'pango_layout_get_cursor_pos',
'pango_layout_get_extents', 'pango_layout_get_pixel_extents',
'pango_layout_get_size', 'pango_layout_get_pixel_size',
'pango_layout_get_baseline', 'pango_layout_get_line_count',
'pango_layout_get_line', 'pango_layout_get_line_readonly',
'pango_layout_line_ref', 'pango_layout_line_unref',
'pango_layout_line_get_x_ranges', 'pango_layout_line_get_extents',
'pango_layout_line_get_pixel_extents', 'PangoLayoutIter',
'pango_layout_get_iter', 'pango_layout_iter_copy', 'pango_layout_iter_free',
'pango_layout_iter_get_index', 'pango_layout_iter_get_run',
'pango_layout_iter_get_run_readonly', 'pango_layout_iter_get_line',
'pango_layout_iter_get_line_readonly', 'pango_layout_iter_get_layout',
'pango_layout_iter_get_char_extents', 'pango_layout_iter_get_cluster_extents',
'pango_layout_iter_get_run_extents', 'pango_layout_iter_get_line_extents',
'pango_layout_iter_get_line_yrange', 'pango_layout_iter_get_layout_extents',
'pango_layout_iter_get_baseline', 'PangoRenderer', 'PangoRendererClass',
'PangoRendererPrivate', 'PangoRenderPart', 'PANGO_RENDER_PART_FOREGROUND',
'PANGO_RENDER_PART_BACKGROUND', 'PANGO_RENDER_PART_UNDERLINE',
'PANGO_RENDER_PART_STRIKETHROUGH', 'pango_renderer_draw_layout',
'pango_renderer_draw_layout_line', 'pango_renderer_draw_glyphs',
'pango_renderer_draw_glyph_item', 'pango_renderer_draw_rectangle',
'pango_renderer_draw_error_underline', 'pango_renderer_draw_trapezoid',
'pango_renderer_draw_glyph', 'pango_renderer_activate',
'pango_renderer_deactivate', 'pango_renderer_part_changed',
'pango_renderer_set_color', 'pango_renderer_get_color',
'pango_renderer_set_matrix', 'pango_renderer_get_matrix',
'pango_renderer_get_layout', 'pango_renderer_get_layout_line',
'pango_split_file_list', 'pango_trim_string', 'pango_quantize_line_geometry',
'pango_version', 'pango_version_string', 'pango_version_check',
'cairo_bool_t', 'cairo_t', 'cairo_surface_t', 'cairo_matrix_t',
'cairo_pattern_t', 'cairo_destroy_func_t', 'cairo_user_data_key_t',
'cairo_status_t', 'cairo_content_t', 'cairo_write_func_t',
'cairo_read_func_t', 'cairo_operator_t', 'cairo_antialias_t',
'cairo_fill_rule_t', 'cairo_line_cap_t', 'cairo_line_join_t',
'cairo_rectangle_t', 'cairo_rectangle_list_t', 'cairo_scaled_font_t',
'cairo_font_face_t', 'cairo_glyph_t', 'cairo_text_cluster_t',
'cairo_text_cluster_flags_t', 'cairo_text_extents_t', 'cairo_font_extents_t',
'cairo_font_slant_t', 'cairo_font_weight_t', 'cairo_subpixel_order_t',
'cairo_hint_style_t', 'cairo_hint_metrics_t', 'cairo_font_options_t',
'cairo_font_type_t', 'cairo_user_scaled_font_init_func_t',
'cairo_user_scaled_font_render_glyph_func_t',
'cairo_user_scaled_font_text_to_glyphs_func_t',
'cairo_user_scaled_font_unicode_to_glyph_func_t', 'cairo_path_data_type_t',
'cairo_path_data_t', 'cairo_path_t', 'cairo_surface_type_t', 'cairo_format_t',
'cairo_pattern_type_t', 'cairo_extend_t', 'cairo_filter_t', 'PangoCairoFont',
'PangoCairoFontMap', 'pango_cairo_font_map_new',
'pango_cairo_font_map_new_for_font_type', 'pango_cairo_font_map_get_default',
'pango_cairo_font_map_set_default', 'pango_cairo_font_map_get_font_type',
'pango_cairo_font_map_set_resolution', 'pango_cairo_font_map_get_resolution',
'pango_cairo_font_map_create_context', 'pango_cairo_font_get_scaled_font',
'pango_cairo_update_context', 'pango_cairo_context_set_font_options',
'pango_cairo_context_get_font_options', 'pango_cairo_context_set_resolution',
'pango_cairo_context_get_resolution', 'pango_cairo_create_context',
'pango_cairo_create_layout', 'pango_cairo_update_layout',
'pango_cairo_show_glyph_string', 'pango_cairo_show_glyph_item',
'pango_cairo_show_layout_line', 'pango_cairo_show_layout',
'pango_cairo_show_error_underline', 'pango_cairo_glyph_string_path',
'pango_cairo_layout_line_path', 'pango_cairo_layout_path',
'pango_cairo_error_underline_path', 'COVERAGE_NONE', 'COVERAGE_FALLBACK',
'COVERAGE_APPROXIMATE', 'COVERAGE_EXACT', 'coverage_new', 'coverage_ref',
'coverage_unref', 'coverage_copy', 'coverage_get', 'coverage_set',
'coverage_max', 'units_from_double', 'units_to_double', 'extents_to_pixels',
'GRAVITY_SOUTH', 'GRAVITY_EAST', 'GRAVITY_NORTH', 'GRAVITY_WEST',
'GRAVITY_AUTO', 'GRAVITY_HINT_NATURAL', 'GRAVITY_HINT_STRONG',
'GRAVITY_HINT_LINE', 'matrix_copy', 'matrix_free', 'matrix_translate',
'matrix_scale', 'matrix_rotate', 'matrix_concat', 'matrix_transform_point',
'matrix_transform_distance', 'matrix_transform_rectangle',
'matrix_transform_pixel_rectangle', 'matrix_get_font_scale_factor',
'SCRIPT_INVALID_CODE', 'SCRIPT_COMMON', 'SCRIPT_INHERITED', 'SCRIPT_ARABIC',
'SCRIPT_ARMENIAN', 'SCRIPT_BENGALI', 'SCRIPT_BOPOMOFO', 'SCRIPT_CHEROKEE',
'SCRIPT_COPTIC', 'SCRIPT_CYRILLIC', 'SCRIPT_DESERET', 'SCRIPT_DEVANAGARI',
'SCRIPT_ETHIOPIC', 'SCRIPT_GEORGIAN', 'SCRIPT_GOTHIC', 'SCRIPT_GREEK',
'SCRIPT_GUJARATI', 'SCRIPT_GURMUKHI', 'SCRIPT_HAN', 'SCRIPT_HANGUL',
'SCRIPT_HEBREW', 'SCRIPT_HIRAGANA', 'SCRIPT_KANNADA', 'SCRIPT_KATAKANA',
'SCRIPT_KHMER', 'SCRIPT_LAO', 'SCRIPT_LATIN', 'SCRIPT_MALAYALAM',
'SCRIPT_MONGOLIAN', 'SCRIPT_MYANMAR', 'SCRIPT_OGHAM', 'SCRIPT_OLD_ITALIC',
'SCRIPT_ORIYA', 'SCRIPT_RUNIC', 'SCRIPT_SINHALA', 'SCRIPT_SYRIAC',
'SCRIPT_TAMIL', 'SCRIPT_TELUGU', 'SCRIPT_THAANA', 'SCRIPT_THAI',
'SCRIPT_TIBETAN', 'SCRIPT_CANADIAN_ABORIGINAL', 'SCRIPT_YI', 'SCRIPT_TAGALOG',
'SCRIPT_HANUNOO', 'SCRIPT_BUHID', 'SCRIPT_TAGBANWA', 'SCRIPT_BRAILLE',
'SCRIPT_CYPRIOT', 'SCRIPT_LIMBU', 'SCRIPT_OSMANYA', 'SCRIPT_SHAVIAN',
'SCRIPT_LINEAR_B', 'SCRIPT_TAI_LE', 'SCRIPT_UGARITIC', 'SCRIPT_NEW_TAI_LUE',
'SCRIPT_BUGINESE', 'SCRIPT_GLAGOLITIC', 'SCRIPT_TIFINAGH',
'SCRIPT_SYLOTI_NAGRI', 'SCRIPT_OLD_PERSIAN', 'SCRIPT_KHAROSHTHI',
'SCRIPT_UNKNOWN', 'SCRIPT_BALINESE', 'SCRIPT_CUNEIFORM', 'SCRIPT_PHOENICIAN',
'SCRIPT_PHAGS_PA', 'SCRIPT_NKO', 'SCRIPT_KAYAH_LI', 'SCRIPT_LEPCHA',
'SCRIPT_REJANG', 'SCRIPT_SUNDANESE', 'SCRIPT_SAURASHTRA', 'SCRIPT_CHAM',
'SCRIPT_OL_CHIKI', 'SCRIPT_VAI', 'SCRIPT_CARIAN', 'SCRIPT_LYCIAN',
'SCRIPT_LYDIAN', 'script_iter_new', 'script_iter_get_range',
'script_iter_free', 'language_from_string', 'language_to_string',
'language_get_sample_string', 'language_get_default', 'language_get_scripts',
'script_get_sample_language', 'gravity_to_rotation', 'gravity_get_for_matrix',
'gravity_get_for_script', 'BIDI_TYPE_L', 'BIDI_TYPE_LRE', 'BIDI_TYPE_LRO',
'BIDI_TYPE_R', 'BIDI_TYPE_AL', 'BIDI_TYPE_RLE', 'BIDI_TYPE_RLO',
'BIDI_TYPE_PDF', 'BIDI_TYPE_EN', 'BIDI_TYPE_ES', 'BIDI_TYPE_ET',
'BIDI_TYPE_AN', 'BIDI_TYPE_CS', 'BIDI_TYPE_NSM', 'BIDI_TYPE_BN',
'BIDI_TYPE_B', 'BIDI_TYPE_S', 'BIDI_TYPE_WS', 'BIDI_TYPE_ON', 'DIRECTION_LTR',
'DIRECTION_RTL', 'DIRECTION_TTB_LTR', 'DIRECTION_TTB_RTL',
'DIRECTION_WEAK_LTR', 'DIRECTION_WEAK_RTL', 'DIRECTION_NEUTRAL',
'STYLE_NORMAL', 'STYLE_OBLIQUE', 'STYLE_ITALIC', 'VARIANT_NORMAL',
'VARIANT_SMALL_CAPS', 'WEIGHT_THIN', 'WEIGHT_ULTRALIGHT', 'WEIGHT_LIGHT',
'WEIGHT_BOOK', 'WEIGHT_NORMAL', 'WEIGHT_MEDIUM', 'WEIGHT_SEMIBOLD',
'WEIGHT_BOLD', 'WEIGHT_ULTRABOLD', 'WEIGHT_HEAVY', 'WEIGHT_ULTRAHEAVY',
'STRETCH_ULTRA_CONDENSED', 'STRETCH_EXTRA_CONDENSED', 'STRETCH_CONDENSED',
'STRETCH_SEMI_CONDENSED', 'STRETCH_NORMAL', 'STRETCH_SEMI_EXPANDED',
'STRETCH_EXPANDED', 'STRETCH_EXTRA_EXPANDED', 'STRETCH_ULTRA_EXPANDED',
'FONT_MASK_FAMILY', 'FONT_MASK_STYLE', 'FONT_MASK_VARIANT',
'FONT_MASK_WEIGHT', 'FONT_MASK_STRETCH', 'FONT_MASK_SIZE',
'FONT_MASK_GRAVITY', 'font_description_new', 'font_description_copy',
'font_description_copy_static', 'font_description_free',
'font_descriptions_free', 'font_description_set_family',
'font_description_set_family_static', 'font_description_get_family',
'font_description_set_style', 'font_description_get_style',
'font_description_set_variant', 'font_description_get_variant',
'font_description_set_weight', 'font_description_get_weight',
'font_description_set_stretch', 'font_description_get_stretch',
'font_description_set_absolute_size', 'font_description_set_gravity',
'font_description_get_gravity', 'font_description_get_set_fields',
'font_description_unset_fields', 'font_description_from_string',
'font_description_to_string', 'font_description_to_filename',
'font_metrics_ref', 'font_metrics_unref', 'font_metrics_get_ascent',
'font_metrics_get_descent', 'font_metrics_get_approximate_char_width',
'font_metrics_get_approximate_digit_width',
'font_metrics_get_underline_position', 'font_metrics_get_underline_thickness',
'font_metrics_get_strikethrough_position',
'font_metrics_get_strikethrough_thickness', 'font_family_list_faces',
'font_family_get_name', 'font_face_describe', 'font_face_get_face_name',
'font_face_list_sizes', 'font_describe', 'font_describe_with_absolute_size',
'font_get_coverage', 'font_find_shaper', 'font_get_metrics',
'font_get_glyph_extents', 'font_get_font_map', 'color_copy', 'color_free',
'ATTR_INVALID', 'ATTR_LANGUAGE', 'ATTR_FAMILY', 'ATTR_STYLE', 'ATTR_WEIGHT',
'ATTR_VARIANT', 'ATTR_STRETCH', 'ATTR_SIZE', 'ATTR_FONT_DESC',
'ATTR_FOREGROUND', 'ATTR_BACKGROUND', 'ATTR_UNDERLINE', 'ATTR_STRIKETHROUGH',
'ATTR_RISE', 'ATTR_SHAPE', 'ATTR_SCALE', 'ATTR_FALLBACK',
'ATTR_LETTER_SPACING', 'ATTR_UNDERLINE_COLOR', 'ATTR_STRIKETHROUGH_COLOR',
'ATTR_ABSOLUTE_SIZE', 'ATTR_GRAVITY', 'ATTR_GRAVITY_HINT', 'UNDERLINE_NONE',
'UNDERLINE_SINGLE', 'UNDERLINE_DOUBLE', 'UNDERLINE_LOW', 'UNDERLINE_ERROR',
'attr_type_get_name', 'attribute_init', 'attribute_copy', 'attribute_destroy',
'attr_language_new', 'attr_family_new', 'attr_foreground_new',
'attr_background_new', 'attr_size_new', 'attr_size_new_absolute',
'attr_style_new', 'attr_weight_new', 'attr_variant_new', 'attr_stretch_new',
'attr_font_desc_new', 'attr_underline_new', 'attr_underline_color_new',
'attr_strikethrough_color_new', 'attr_rise_new', 'attr_scale_new',
'attr_letter_spacing_new', 'attr_shape_new', 'attr_gravity_new',
'attr_gravity_hint_new', 'attr_list_new', 'attr_list_ref', 'attr_list_unref',
'attr_list_copy', 'attr_list_insert', 'attr_list_insert_before',
'attr_list_change', 'attr_list_get_iterator', 'attr_iterator_copy',
'attr_iterator_destroy', 'attr_iterator_get', 'item_new', 'item_copy',
'item_free', 'item_split', 'get_log_attrs', 'fontset_get_metrics',
'font_map_create_context', 'font_map_load_font', 'font_map_load_fontset',
'font_map_list_families', 'context_new', 'context_set_font_map',
'context_get_font_map', 'context_list_families', 'context_load_font',
'context_load_fontset', 'context_get_metrics', 'context_set_font_description',
'context_get_font_description', 'context_get_language',
'context_set_language', 'context_set_base_dir', 'context_get_base_dir',
'context_set_base_gravity', 'context_get_base_gravity', 'context_get_gravity',
'context_set_gravity_hint', 'context_get_gravity_hint', 'context_set_matrix',
'context_get_matrix', 'glyph_string_new', 'glyph_string_copy',
'glyph_string_free', 'glyph_string_extents', 'glyph_string_get_width',
'glyph_string_extents_range', 'glyph_string_get_logical_widths',
'glyph_string_x_to_index', 'glyph_item_split', 'glyph_item_copy',
'glyph_item_free', 'glyph_item_letter_space', 'glyph_item_iter_copy',
'glyph_item_iter_free', 'TAB_LEFT', 'tab_array_copy', 'tab_array_free',
'ALIGN_LEFT', 'ALIGN_CENTER', 'ALIGN_RIGHT', 'WRAP_WORD', 'WRAP_CHAR',
'WRAP_WORD_CHAR', 'ELLIPSIZE_NONE', 'ELLIPSIZE_START', 'ELLIPSIZE_MIDDLE',
'ELLIPSIZE_END', 'layout_new', 'layout_copy', 'layout_get_context',
'layout_set_attributes', 'layout_get_attributes', 'layout_set_text',
'layout_get_text', 'layout_set_markup', 'layout_set_font_description',
'layout_get_font_description', 'layout_set_width', 'layout_get_width',
'layout_set_height', 'layout_get_height', 'layout_set_wrap',
'layout_get_wrap', 'layout_set_indent', 'layout_get_indent',
'layout_set_spacing', 'layout_get_spacing', 'layout_set_alignment',
'layout_get_alignment', 'layout_set_tabs', 'layout_get_tabs',
'layout_set_ellipsize', 'layout_get_ellipsize',
'layout_get_unknown_glyphs_count', 'layout_context_changed',
'layout_index_to_pos', 'layout_get_cursor_pos', 'layout_get_extents',
'layout_get_pixel_extents', 'layout_get_size', 'layout_get_pixel_size',
'layout_get_baseline', 'layout_get_line_count', 'layout_get_line',
'layout_get_line_readonly', 'layout_line_ref', 'layout_line_unref',
'layout_line_get_x_ranges', 'layout_line_get_extents',
'layout_line_get_pixel_extents', 'layout_get_iter', 'layout_iter_copy',
'layout_iter_free', 'layout_iter_get_index', 'layout_iter_get_run',
'layout_iter_get_run_readonly', 'layout_iter_get_line',
'layout_iter_get_line_readonly', 'layout_iter_get_layout',
'layout_iter_get_char_extents', 'layout_iter_get_cluster_extents',
'layout_iter_get_run_extents', 'layout_iter_get_line_extents',
'layout_iter_get_line_yrange', 'layout_iter_get_layout_extents',
'layout_iter_get_baseline', 'RENDER_PART_FOREGROUND',
'RENDER_PART_BACKGROUND', 'RENDER_PART_UNDERLINE',
'RENDER_PART_STRIKETHROUGH', 'renderer_draw_layout',
'renderer_draw_layout_line', 'renderer_draw_glyphs',
'renderer_draw_glyph_item', 'renderer_draw_rectangle',
'renderer_draw_error_underline', 'renderer_draw_trapezoid',
'renderer_draw_glyph', 'renderer_activate', 'renderer_deactivate',
'renderer_part_changed', 'renderer_set_color', 'renderer_get_color',
'renderer_set_matrix', 'renderer_get_matrix', 'renderer_get_layout',
'renderer_get_layout_line', 'split_file_list', 'trim_string',
'quantize_line_geometry', 'version', 'version_string', 'version_check',
'cairo_font_map_new', 'cairo_font_map_new_for_font_type',
'cairo_font_map_get_default', 'cairo_font_map_set_default',
'cairo_font_map_get_font_type', 'cairo_font_map_set_resolution',
'cairo_font_map_get_resolution', 'cairo_font_map_create_context',
'cairo_font_get_scaled_font', 'cairo_update_context',
'cairo_context_set_font_options', 'cairo_context_get_font_options',
'cairo_context_set_resolution', 'cairo_context_get_resolution',
'cairo_create_context', 'cairo_create_layout', 'cairo_update_layout',
'cairo_show_glyph_string', 'cairo_show_glyph_item', 'cairo_show_layout_line',
'cairo_show_layout', 'cairo_show_error_underline', 'cairo_glyph_string_path',
'cairo_layout_line_path', 'cairo_layout_path', 'cairo_error_underline_path',
'Context', 'Layout', 'FontDescription', 'FontMap', 'CairoFontMap']
