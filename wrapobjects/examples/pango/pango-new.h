


typedef struct _PangoCoverage PangoCoverage;

typedef enum {
  PANGO_COVERAGE_NONE,
  PANGO_COVERAGE_FALLBACK,
  PANGO_COVERAGE_APPROXIMATE,
  PANGO_COVERAGE_EXACT
} PangoCoverageLevel;

PangoCoverage * pango_coverage_new (void);
PangoCoverage * pango_coverage_ref (PangoCoverage *coverage);
void pango_coverage_unref (PangoCoverage *coverage);
PangoCoverage * pango_coverage_copy (PangoCoverage *coverage);
PangoCoverageLevel pango_coverage_get (PangoCoverage *coverage,
        int index_);
void pango_coverage_set (PangoCoverage *coverage,
        int index_,
        PangoCoverageLevel level);
void pango_coverage_max (PangoCoverage *coverage,
        PangoCoverage *other);

void pango_coverage_to_bytes (PangoCoverage *coverage,
       guchar **bytes,
       int *n_bytes);
PangoCoverage *pango_coverage_from_bytes (guchar *bytes,
       int n_bytes);





typedef struct _PangoLogAttr PangoLogAttr;

typedef struct _PangoEngineLang PangoEngineLang;
typedef struct _PangoEngineShape PangoEngineShape;

typedef struct _PangoFont PangoFont;
typedef struct _PangoFontMap PangoFontMap;

typedef struct _PangoRectangle PangoRectangle;




typedef guint32 PangoGlyph;
int pango_units_from_double (double d) ;
double pango_units_to_double (int i) ;






struct _PangoRectangle
{
  int x;
  int y;
  int width;
  int height;
};
void pango_extents_to_pixels (PangoRectangle *inclusive,
         PangoRectangle *nearest);



typedef enum {
  PANGO_GRAVITY_SOUTH,
  PANGO_GRAVITY_EAST,
  PANGO_GRAVITY_NORTH,
  PANGO_GRAVITY_WEST,
  PANGO_GRAVITY_AUTO
} PangoGravity;
typedef enum {
  PANGO_GRAVITY_HINT_NATURAL,
  PANGO_GRAVITY_HINT_STRONG,
  PANGO_GRAVITY_HINT_LINE
} PangoGravityHint;


typedef struct _PangoMatrix PangoMatrix;
struct _PangoMatrix
{
  double xx;
  double xy;
  double yx;
  double yy;
  double x0;
  double y0;
};

GType pango_matrix_get_type (void) ;

PangoMatrix *pango_matrix_copy (const PangoMatrix *matrix);
void pango_matrix_free (PangoMatrix *matrix);

void pango_matrix_translate (PangoMatrix *matrix,
        double tx,
        double ty);
void pango_matrix_scale (PangoMatrix *matrix,
        double scale_x,
        double scale_y);
void pango_matrix_rotate (PangoMatrix *matrix,
        double degrees);
void pango_matrix_concat (PangoMatrix *matrix,
        const PangoMatrix *new_matrix);
void pango_matrix_transform_point (const PangoMatrix *matrix,
          double *x,
          double *y);
void pango_matrix_transform_distance (const PangoMatrix *matrix,
          double *dx,
          double *dy);
void pango_matrix_transform_rectangle (const PangoMatrix *matrix,
           PangoRectangle *rect);
void pango_matrix_transform_pixel_rectangle (const PangoMatrix *matrix,
          PangoRectangle *rect);
double pango_matrix_get_font_scale_factor (const PangoMatrix *matrix) ;











typedef struct _PangoScriptIter PangoScriptIter;

typedef enum {
      PANGO_SCRIPT_INVALID_CODE = -1,
      PANGO_SCRIPT_COMMON = 0,
      PANGO_SCRIPT_INHERITED,
      PANGO_SCRIPT_ARABIC,
      PANGO_SCRIPT_ARMENIAN,
      PANGO_SCRIPT_BENGALI,
      PANGO_SCRIPT_BOPOMOFO,
      PANGO_SCRIPT_CHEROKEE,
      PANGO_SCRIPT_COPTIC,
      PANGO_SCRIPT_CYRILLIC,
      PANGO_SCRIPT_DESERET,
      PANGO_SCRIPT_DEVANAGARI,
      PANGO_SCRIPT_ETHIOPIC,
      PANGO_SCRIPT_GEORGIAN,
      PANGO_SCRIPT_GOTHIC,
      PANGO_SCRIPT_GREEK,
      PANGO_SCRIPT_GUJARATI,
      PANGO_SCRIPT_GURMUKHI,
      PANGO_SCRIPT_HAN,
      PANGO_SCRIPT_HANGUL,
      PANGO_SCRIPT_HEBREW,
      PANGO_SCRIPT_HIRAGANA,
      PANGO_SCRIPT_KANNADA,
      PANGO_SCRIPT_KATAKANA,
      PANGO_SCRIPT_KHMER,
      PANGO_SCRIPT_LAO,
      PANGO_SCRIPT_LATIN,
      PANGO_SCRIPT_MALAYALAM,
      PANGO_SCRIPT_MONGOLIAN,
      PANGO_SCRIPT_MYANMAR,
      PANGO_SCRIPT_OGHAM,
      PANGO_SCRIPT_OLD_ITALIC,
      PANGO_SCRIPT_ORIYA,
      PANGO_SCRIPT_RUNIC,
      PANGO_SCRIPT_SINHALA,
      PANGO_SCRIPT_SYRIAC,
      PANGO_SCRIPT_TAMIL,
      PANGO_SCRIPT_TELUGU,
      PANGO_SCRIPT_THAANA,
      PANGO_SCRIPT_THAI,
      PANGO_SCRIPT_TIBETAN,
      PANGO_SCRIPT_CANADIAN_ABORIGINAL,
      PANGO_SCRIPT_YI,
      PANGO_SCRIPT_TAGALOG,
      PANGO_SCRIPT_HANUNOO,
      PANGO_SCRIPT_BUHID,
      PANGO_SCRIPT_TAGBANWA,


      PANGO_SCRIPT_BRAILLE,
      PANGO_SCRIPT_CYPRIOT,
      PANGO_SCRIPT_LIMBU,
      PANGO_SCRIPT_OSMANYA,
      PANGO_SCRIPT_SHAVIAN,
      PANGO_SCRIPT_LINEAR_B,
      PANGO_SCRIPT_TAI_LE,
      PANGO_SCRIPT_UGARITIC,


      PANGO_SCRIPT_NEW_TAI_LUE,
      PANGO_SCRIPT_BUGINESE,
      PANGO_SCRIPT_GLAGOLITIC,
      PANGO_SCRIPT_TIFINAGH,
      PANGO_SCRIPT_SYLOTI_NAGRI,
      PANGO_SCRIPT_OLD_PERSIAN,
      PANGO_SCRIPT_KHAROSHTHI,


      PANGO_SCRIPT_UNKNOWN,
      PANGO_SCRIPT_BALINESE,
      PANGO_SCRIPT_CUNEIFORM,
      PANGO_SCRIPT_PHOENICIAN,
      PANGO_SCRIPT_PHAGS_PA,
      PANGO_SCRIPT_NKO,


      PANGO_SCRIPT_KAYAH_LI,
      PANGO_SCRIPT_LEPCHA,
      PANGO_SCRIPT_REJANG,
      PANGO_SCRIPT_SUNDANESE,
      PANGO_SCRIPT_SAURASHTRA,
      PANGO_SCRIPT_CHAM,
      PANGO_SCRIPT_OL_CHIKI,
      PANGO_SCRIPT_VAI,
      PANGO_SCRIPT_CARIAN,
      PANGO_SCRIPT_LYCIAN,
      PANGO_SCRIPT_LYDIAN
} PangoScript;

PangoScript pango_script_for_unichar (gunichar ch) ;

PangoScriptIter *pango_script_iter_new (const char *text,
           int length);
void pango_script_iter_get_range (PangoScriptIter *iter,
           const char **start,
           const char **end,
           PangoScript *script);
gboolean pango_script_iter_next (PangoScriptIter *iter);
void pango_script_iter_free (PangoScriptIter *iter);



typedef struct _PangoLanguage PangoLanguage;



GType pango_language_get_type (void) ;
PangoLanguage *pango_language_from_string (const char *language);

const char *pango_language_to_string (PangoLanguage *language) ;



const char *pango_language_get_sample_string (PangoLanguage *language) ;
PangoLanguage *pango_language_get_default (void) ;

gboolean pango_language_matches (PangoLanguage *language,
           const char *range_list) ;


gboolean pango_language_includes_script (PangoLanguage *language,
           PangoScript script) ;
const PangoScript *pango_language_get_scripts (PangoLanguage *language,
           int *num_scripts);



PangoLanguage *pango_script_get_sample_language (PangoScript script) ;



double pango_gravity_to_rotation (PangoGravity gravity) ;
PangoGravity pango_gravity_get_for_matrix (const PangoMatrix *matrix) ;
PangoGravity pango_gravity_get_for_script (PangoScript script,
        PangoGravity base_gravity,
        PangoGravityHint hint) ;







typedef enum {

  PANGO_BIDI_TYPE_L,
  PANGO_BIDI_TYPE_LRE,
  PANGO_BIDI_TYPE_LRO,
  PANGO_BIDI_TYPE_R,
  PANGO_BIDI_TYPE_AL,
  PANGO_BIDI_TYPE_RLE,
  PANGO_BIDI_TYPE_RLO,


  PANGO_BIDI_TYPE_PDF,
  PANGO_BIDI_TYPE_EN,
  PANGO_BIDI_TYPE_ES,
  PANGO_BIDI_TYPE_ET,
  PANGO_BIDI_TYPE_AN,
  PANGO_BIDI_TYPE_CS,
  PANGO_BIDI_TYPE_NSM,
  PANGO_BIDI_TYPE_BN,


  PANGO_BIDI_TYPE_B,
  PANGO_BIDI_TYPE_S,
  PANGO_BIDI_TYPE_WS,
  PANGO_BIDI_TYPE_ON
} PangoBidiType;

PangoBidiType pango_bidi_type_for_unichar (gunichar ch) ;
typedef enum {
  PANGO_DIRECTION_LTR,
  PANGO_DIRECTION_RTL,
  PANGO_DIRECTION_TTB_LTR,
  PANGO_DIRECTION_TTB_RTL,
  PANGO_DIRECTION_WEAK_LTR,
  PANGO_DIRECTION_WEAK_RTL,
  PANGO_DIRECTION_NEUTRAL
} PangoDirection;

PangoDirection pango_unichar_direction (gunichar ch) ;
PangoDirection pango_find_base_dir (const gchar *text,
          gint length);


gboolean pango_get_mirror_char (gunichar ch,
          gunichar *mirrored_ch);











typedef struct _PangoFontDescription PangoFontDescription;
typedef struct _PangoFontMetrics PangoFontMetrics;
typedef enum {
  PANGO_STYLE_NORMAL,
  PANGO_STYLE_OBLIQUE,
  PANGO_STYLE_ITALIC
} PangoStyle;

typedef enum {
  PANGO_VARIANT_NORMAL,
  PANGO_VARIANT_SMALL_CAPS
} PangoVariant;

typedef enum {
  PANGO_WEIGHT_THIN = 100,
  PANGO_WEIGHT_ULTRALIGHT = 200,
  PANGO_WEIGHT_LIGHT = 300,
  PANGO_WEIGHT_BOOK = 380,
  PANGO_WEIGHT_NORMAL = 400,
  PANGO_WEIGHT_MEDIUM = 500,
  PANGO_WEIGHT_SEMIBOLD = 600,
  PANGO_WEIGHT_BOLD = 700,
  PANGO_WEIGHT_ULTRABOLD = 800,
  PANGO_WEIGHT_HEAVY = 900,
  PANGO_WEIGHT_ULTRAHEAVY = 1000
} PangoWeight;

typedef enum {
  PANGO_STRETCH_ULTRA_CONDENSED,
  PANGO_STRETCH_EXTRA_CONDENSED,
  PANGO_STRETCH_CONDENSED,
  PANGO_STRETCH_SEMI_CONDENSED,
  PANGO_STRETCH_NORMAL,
  PANGO_STRETCH_SEMI_EXPANDED,
  PANGO_STRETCH_EXPANDED,
  PANGO_STRETCH_EXTRA_EXPANDED,
  PANGO_STRETCH_ULTRA_EXPANDED
} PangoStretch;

typedef enum {
  PANGO_FONT_MASK_FAMILY = 1 << 0,
  PANGO_FONT_MASK_STYLE = 1 << 1,
  PANGO_FONT_MASK_VARIANT = 1 << 2,
  PANGO_FONT_MASK_WEIGHT = 1 << 3,
  PANGO_FONT_MASK_STRETCH = 1 << 4,
  PANGO_FONT_MASK_SIZE = 1 << 5,
  PANGO_FONT_MASK_GRAVITY = 1 << 6
} PangoFontMask;
GType pango_font_description_get_type (void) ;
PangoFontDescription *pango_font_description_new (void);
PangoFontDescription *pango_font_description_copy (const PangoFontDescription *desc);
PangoFontDescription *pango_font_description_copy_static (const PangoFontDescription *desc);
guint pango_font_description_hash (const PangoFontDescription *desc) ;
gboolean pango_font_description_equal (const PangoFontDescription *desc1,
         const PangoFontDescription *desc2) ;
void pango_font_description_free (PangoFontDescription *desc);
void pango_font_descriptions_free (PangoFontDescription **descs,
         int n_descs);

void pango_font_description_set_family (PangoFontDescription *desc,
              const char *family);
void pango_font_description_set_family_static (PangoFontDescription *desc,
              const char *family);
const char *pango_font_description_get_family (const PangoFontDescription *desc) ;
void pango_font_description_set_style (PangoFontDescription *desc,
              PangoStyle style);
PangoStyle pango_font_description_get_style (const PangoFontDescription *desc) ;
void pango_font_description_set_variant (PangoFontDescription *desc,
              PangoVariant variant);
PangoVariant pango_font_description_get_variant (const PangoFontDescription *desc) ;
void pango_font_description_set_weight (PangoFontDescription *desc,
              PangoWeight weight);
PangoWeight pango_font_description_get_weight (const PangoFontDescription *desc) ;
void pango_font_description_set_stretch (PangoFontDescription *desc,
              PangoStretch stretch);
PangoStretch pango_font_description_get_stretch (const PangoFontDescription *desc) ;
void pango_font_description_set_size (PangoFontDescription *desc,
              gint size);
gint pango_font_description_get_size (const PangoFontDescription *desc) ;
void pango_font_description_set_absolute_size (PangoFontDescription *desc,
              double size);
gboolean pango_font_description_get_size_is_absolute (const PangoFontDescription *desc) ;
void pango_font_description_set_gravity (PangoFontDescription *desc,
              PangoGravity gravity);
PangoGravity pango_font_description_get_gravity (const PangoFontDescription *desc) ;

PangoFontMask pango_font_description_get_set_fields (const PangoFontDescription *desc) ;
void pango_font_description_unset_fields (PangoFontDescription *desc,
           PangoFontMask to_unset);

void pango_font_description_merge (PangoFontDescription *desc,
       const PangoFontDescription *desc_to_merge,
       gboolean replace_existing);
void pango_font_description_merge_static (PangoFontDescription *desc,
       const PangoFontDescription *desc_to_merge,
       gboolean replace_existing);

gboolean pango_font_description_better_match (const PangoFontDescription *desc,
           const PangoFontDescription *old_match,
           const PangoFontDescription *new_match) ;

PangoFontDescription *pango_font_description_from_string (const char *str);
char * pango_font_description_to_string (const PangoFontDescription *desc);
char * pango_font_description_to_filename (const PangoFontDescription *desc);






GType pango_font_metrics_get_type (void) ;
PangoFontMetrics *pango_font_metrics_ref (PangoFontMetrics *metrics);
void pango_font_metrics_unref (PangoFontMetrics *metrics);
int pango_font_metrics_get_ascent (PangoFontMetrics *metrics) ;
int pango_font_metrics_get_descent (PangoFontMetrics *metrics) ;
int pango_font_metrics_get_approximate_char_width (PangoFontMetrics *metrics) ;
int pango_font_metrics_get_approximate_digit_width (PangoFontMetrics *metrics) ;
int pango_font_metrics_get_underline_position (PangoFontMetrics *metrics) ;
int pango_font_metrics_get_underline_thickness (PangoFontMetrics *metrics) ;
int pango_font_metrics_get_strikethrough_position (PangoFontMetrics *metrics) ;
int pango_font_metrics_get_strikethrough_thickness (PangoFontMetrics *metrics) ;
typedef struct _PangoFontFamily PangoFontFamily;
typedef struct _PangoFontFace PangoFontFace;

GType pango_font_family_get_type (void) ;

void pango_font_family_list_faces (PangoFontFamily *family,
         PangoFontFace ***faces,
         int *n_faces);
const char *pango_font_family_get_name (PangoFontFamily *family) ;
gboolean pango_font_family_is_monospace (PangoFontFamily *family) ;
GType pango_font_face_get_type (void) ;

PangoFontDescription *pango_font_face_describe (PangoFontFace *face);
const char *pango_font_face_get_face_name (PangoFontFace *face) ;
void pango_font_face_list_sizes (PangoFontFace *face,
            int **sizes,
            int *n_sizes);
gboolean pango_font_face_is_synthesized (PangoFontFace *face) ;
GType pango_font_get_type (void) ;

PangoFontDescription *pango_font_describe (PangoFont *font);
PangoFontDescription *pango_font_describe_with_absolute_size (PangoFont *font);
PangoCoverage * pango_font_get_coverage (PangoFont *font,
          PangoLanguage *language);
PangoEngineShape * pango_font_find_shaper (PangoFont *font,
          PangoLanguage *language,
          guint32 ch);
PangoFontMetrics * pango_font_get_metrics (PangoFont *font,
          PangoLanguage *language);
void pango_font_get_glyph_extents (PangoFont *font,
          PangoGlyph glyph,
          PangoRectangle *ink_rect,
          PangoRectangle *logical_rect);
PangoFontMap *pango_font_get_font_map (PangoFont *font);







typedef struct _PangoColor PangoColor;

struct _PangoColor
{
  guint16 red;
  guint16 green;
  guint16 blue;
};


GType pango_color_get_type (void) ;

PangoColor *pango_color_copy (const PangoColor *src);
void pango_color_free (PangoColor *color);
gboolean pango_color_parse (PangoColor *color,
      const char *spec);
gchar *pango_color_to_string(const PangoColor *color);




typedef struct _PangoAttribute PangoAttribute;
typedef struct _PangoAttrClass PangoAttrClass;

typedef struct _PangoAttrString PangoAttrString;
typedef struct _PangoAttrLanguage PangoAttrLanguage;
typedef struct _PangoAttrInt PangoAttrInt;
typedef struct _PangoAttrSize PangoAttrSize;
typedef struct _PangoAttrFloat PangoAttrFloat;
typedef struct _PangoAttrColor PangoAttrColor;
typedef struct _PangoAttrFontDesc PangoAttrFontDesc;
typedef struct _PangoAttrShape PangoAttrShape;


typedef struct _PangoAttrList PangoAttrList;
typedef struct _PangoAttrIterator PangoAttrIterator;

typedef enum
{
  PANGO_ATTR_INVALID,
  PANGO_ATTR_LANGUAGE,
  PANGO_ATTR_FAMILY,
  PANGO_ATTR_STYLE,
  PANGO_ATTR_WEIGHT,
  PANGO_ATTR_VARIANT,
  PANGO_ATTR_STRETCH,
  PANGO_ATTR_SIZE,
  PANGO_ATTR_FONT_DESC,
  PANGO_ATTR_FOREGROUND,
  PANGO_ATTR_BACKGROUND,
  PANGO_ATTR_UNDERLINE,
  PANGO_ATTR_STRIKETHROUGH,
  PANGO_ATTR_RISE,
  PANGO_ATTR_SHAPE,
  PANGO_ATTR_SCALE,
  PANGO_ATTR_FALLBACK,
  PANGO_ATTR_LETTER_SPACING,
  PANGO_ATTR_UNDERLINE_COLOR,
  PANGO_ATTR_STRIKETHROUGH_COLOR,
  PANGO_ATTR_ABSOLUTE_SIZE,
  PANGO_ATTR_GRAVITY,
  PANGO_ATTR_GRAVITY_HINT
} PangoAttrType;

typedef enum {
  PANGO_UNDERLINE_NONE,
  PANGO_UNDERLINE_SINGLE,
  PANGO_UNDERLINE_DOUBLE,
  PANGO_UNDERLINE_LOW,
  PANGO_UNDERLINE_ERROR
} PangoUnderline;




struct _PangoAttribute
{
  const PangoAttrClass *klass;
  guint start_index;
  guint end_index;
};

typedef gboolean (*PangoAttrFilterFunc) (PangoAttribute *attribute,
      gpointer data);

typedef gpointer (*PangoAttrDataCopyFunc) (gconstpointer data);

struct _PangoAttrClass
{

  PangoAttrType type;
  PangoAttribute * (*copy) (const PangoAttribute *attr);
  void (*destroy) (PangoAttribute *attr);
  gboolean (*equal) (const PangoAttribute *attr1, const PangoAttribute *attr2);
};

struct _PangoAttrString
{
  PangoAttribute attr;
  char *value;
};

struct _PangoAttrLanguage
{
  PangoAttribute attr;
  PangoLanguage *value;
};

struct _PangoAttrInt
{
  PangoAttribute attr;
  int value;
};

struct _PangoAttrFloat
{
  PangoAttribute attr;
  double value;
};

struct _PangoAttrColor
{
  PangoAttribute attr;
  PangoColor color;
};

struct _PangoAttrSize
{
  PangoAttribute attr;
  int size;
  guint absolute : 1;
};

struct _PangoAttrShape
{
  PangoAttribute attr;
  PangoRectangle ink_rect;
  PangoRectangle logical_rect;

  gpointer data;
  PangoAttrDataCopyFunc copy_func;
  GDestroyNotify destroy_func;
};

struct _PangoAttrFontDesc
{
  PangoAttribute attr;
  PangoFontDescription *desc;
};

PangoAttrType pango_attr_type_register (const gchar *name);
const char * pango_attr_type_get_name (PangoAttrType type) ;

void pango_attribute_init (PangoAttribute *attr,
           const PangoAttrClass *klass);
PangoAttribute * pango_attribute_copy (const PangoAttribute *attr);
void pango_attribute_destroy (PangoAttribute *attr);
gboolean pango_attribute_equal (const PangoAttribute *attr1,
           const PangoAttribute *attr2) ;

PangoAttribute *pango_attr_language_new (PangoLanguage *language);
PangoAttribute *pango_attr_family_new (const char *family);
PangoAttribute *pango_attr_foreground_new (guint16 red,
           guint16 green,
           guint16 blue);
PangoAttribute *pango_attr_background_new (guint16 red,
           guint16 green,
           guint16 blue);
PangoAttribute *pango_attr_size_new (int size);
PangoAttribute *pango_attr_size_new_absolute (int size);
PangoAttribute *pango_attr_style_new (PangoStyle style);
PangoAttribute *pango_attr_weight_new (PangoWeight weight);
PangoAttribute *pango_attr_variant_new (PangoVariant variant);
PangoAttribute *pango_attr_stretch_new (PangoStretch stretch);
PangoAttribute *pango_attr_font_desc_new (const PangoFontDescription *desc);

PangoAttribute *pango_attr_underline_new (PangoUnderline underline);
PangoAttribute *pango_attr_underline_color_new (guint16 red,
          guint16 green,
          guint16 blue);
PangoAttribute *pango_attr_strikethrough_new (gboolean strikethrough);
PangoAttribute *pango_attr_strikethrough_color_new (guint16 red,
          guint16 green,
          guint16 blue);

PangoAttribute *pango_attr_rise_new (int rise);
PangoAttribute *pango_attr_scale_new (double scale_factor);
PangoAttribute *pango_attr_fallback_new (gboolean enable_fallback);
PangoAttribute *pango_attr_letter_spacing_new (int letter_spacing);

PangoAttribute *pango_attr_shape_new (const PangoRectangle *ink_rect,
      const PangoRectangle *logical_rect);
PangoAttribute *pango_attr_shape_new_with_data (const PangoRectangle *ink_rect,
      const PangoRectangle *logical_rect,
      gpointer data,
      PangoAttrDataCopyFunc copy_func,
      GDestroyNotify destroy_func);

PangoAttribute *pango_attr_gravity_new (PangoGravity gravity);
PangoAttribute *pango_attr_gravity_hint_new (PangoGravityHint hint);

GType pango_attr_list_get_type (void) ;
PangoAttrList * pango_attr_list_new (void);
PangoAttrList * pango_attr_list_ref (PangoAttrList *list);
void pango_attr_list_unref (PangoAttrList *list);
PangoAttrList * pango_attr_list_copy (PangoAttrList *list);
void pango_attr_list_insert (PangoAttrList *list,
        PangoAttribute *attr);
void pango_attr_list_insert_before (PangoAttrList *list,
        PangoAttribute *attr);
void pango_attr_list_change (PangoAttrList *list,
        PangoAttribute *attr);
void pango_attr_list_splice (PangoAttrList *list,
        PangoAttrList *other,
        gint pos,
        gint len);

PangoAttrList *pango_attr_list_filter (PangoAttrList *list,
           PangoAttrFilterFunc func,
           gpointer data);

PangoAttrIterator *pango_attr_list_get_iterator (PangoAttrList *list);

void pango_attr_iterator_range (PangoAttrIterator *iterator,
       gint *start,
       gint *end);
gboolean pango_attr_iterator_next (PangoAttrIterator *iterator);
PangoAttrIterator *pango_attr_iterator_copy (PangoAttrIterator *iterator);
void pango_attr_iterator_destroy (PangoAttrIterator *iterator);
PangoAttribute * pango_attr_iterator_get (PangoAttrIterator *iterator,
       PangoAttrType type);
void pango_attr_iterator_get_font (PangoAttrIterator *iterator,
       PangoFontDescription *desc,
       PangoLanguage **language,
       GSList **extra_attrs);
GSList * pango_attr_iterator_get_attrs (PangoAttrIterator *iterator);


gboolean pango_parse_markup (const char *markup_text,
        int length,
        gunichar accel_marker,
        PangoAttrList **attr_list,
        char **text,
        gunichar *accel_char,
        GError **error);







typedef struct _PangoAnalysis PangoAnalysis;
typedef struct _PangoItem PangoItem;




struct _PangoAnalysis
{
  PangoEngineShape *shape_engine;
  PangoEngineLang *lang_engine;
  PangoFont *font;

  guint8 level;
  guint8 gravity;
  guint8 flags;

  guint8 script;
  PangoLanguage *language;

  GSList *extra_attrs;
};

struct _PangoItem
{
  gint offset;
  gint length;
  gint num_chars;
  PangoAnalysis analysis;
};



GType pango_item_get_type (void) ;

PangoItem *pango_item_new (void);
PangoItem *pango_item_copy (PangoItem *item);
void pango_item_free (PangoItem *item);
PangoItem *pango_item_split (PangoItem *orig,
        int split_index,
        int split_offset);





struct _PangoLogAttr
{
  guint is_line_break : 1;

  guint is_mandatory_break : 1;

  guint is_char_break : 1;

  guint is_white : 1;




  guint is_cursor_position : 1;






  guint is_word_start : 1;
  guint is_word_end : 1;
  guint is_sentence_boundary : 1;
  guint is_sentence_start : 1;
  guint is_sentence_end : 1;




  guint backspace_deletes_character : 1;




  guint is_expandable_space : 1;


  guint is_word_boundary : 1;
};




void pango_break (const gchar *text,
    int length,
    PangoAnalysis *analysis,
    PangoLogAttr *attrs,
    int attrs_len);

void pango_find_paragraph_boundary (const gchar *text,
        gint length,
        gint *paragraph_delimiter_index,
        gint *next_paragraph_start);

void pango_get_log_attrs (const char *text,
     int length,
     int level,
     PangoLanguage *language,
     PangoLogAttr *log_attrs,
     int attrs_len);


GType pango_fontset_get_type (void) ;

typedef struct _PangoFontset PangoFontset;
typedef gboolean (*PangoFontsetForeachFunc) (PangoFontset *fontset,
          PangoFont *font,
          gpointer data);

PangoFont * pango_fontset_get_font (PangoFontset *fontset,
          guint wc);
PangoFontMetrics *pango_fontset_get_metrics (PangoFontset *fontset);
void pango_fontset_foreach (PangoFontset *fontset,
          PangoFontsetForeachFunc func,
          gpointer data);








typedef struct _PangoContext PangoContext;

GType pango_font_map_get_type (void) ;
PangoContext * pango_font_map_create_context (PangoFontMap *fontmap);
PangoFont * pango_font_map_load_font (PangoFontMap *fontmap,
         PangoContext *context,
         const PangoFontDescription *desc);
PangoFontset *pango_font_map_load_fontset (PangoFontMap *fontmap,
         PangoContext *context,
         const PangoFontDescription *desc,
         PangoLanguage *language);
void pango_font_map_list_families (PangoFontMap *fontmap,
         PangoFontFamily ***families,
         int *n_families);










typedef struct _PangoContextClass PangoContextClass;
GType pango_context_get_type (void) ;

PangoContext *pango_context_new (void);
void pango_context_set_font_map (PangoContext *context,
        PangoFontMap *font_map);
PangoFontMap *pango_context_get_font_map (PangoContext *context);

void pango_context_list_families (PangoContext *context,
        PangoFontFamily ***families,
        int *n_families);
PangoFont * pango_context_load_font (PangoContext *context,
        const PangoFontDescription *desc);
PangoFontset *pango_context_load_fontset (PangoContext *context,
        const PangoFontDescription *desc,
        PangoLanguage *language);

PangoFontMetrics *pango_context_get_metrics (PangoContext *context,
            const PangoFontDescription *desc,
            PangoLanguage *language);

void pango_context_set_font_description (PangoContext *context,
             const PangoFontDescription *desc);
PangoFontDescription * pango_context_get_font_description (PangoContext *context);
PangoLanguage *pango_context_get_language (PangoContext *context);
void pango_context_set_language (PangoContext *context,
             PangoLanguage *language);
void pango_context_set_base_dir (PangoContext *context,
             PangoDirection direction);
PangoDirection pango_context_get_base_dir (PangoContext *context);
void pango_context_set_base_gravity (PangoContext *context,
             PangoGravity gravity);
PangoGravity pango_context_get_base_gravity (PangoContext *context);
PangoGravity pango_context_get_gravity (PangoContext *context);
void pango_context_set_gravity_hint (PangoContext *context,
             PangoGravityHint hint);
PangoGravityHint pango_context_get_gravity_hint (PangoContext *context);

void pango_context_set_matrix (PangoContext *context,
            const PangoMatrix *matrix);
const PangoMatrix *pango_context_get_matrix (PangoContext *context);





GList *pango_itemize (PangoContext *context,
         const char *text,
         int start_index,
         int length,
         PangoAttrList *attrs,
         PangoAttrIterator *cached_iter);
GList *pango_itemize_with_base_dir (PangoContext *context,
         PangoDirection base_dir,
         const char *text,
         int start_index,
         int length,
         PangoAttrList *attrs,
         PangoAttrIterator *cached_iter);





typedef struct _PangoGlyphGeometry PangoGlyphGeometry;
typedef struct _PangoGlyphVisAttr PangoGlyphVisAttr;
typedef struct _PangoGlyphInfo PangoGlyphInfo;
typedef struct _PangoGlyphString PangoGlyphString;


typedef gint32 PangoGlyphUnit;



struct _PangoGlyphGeometry
{
  PangoGlyphUnit width;
  PangoGlyphUnit x_offset;
  PangoGlyphUnit y_offset;
};



struct _PangoGlyphVisAttr
{
  guint is_cluster_start : 1;
};



struct _PangoGlyphInfo
{
  PangoGlyph glyph;
  PangoGlyphGeometry geometry;
  PangoGlyphVisAttr attr;
};




struct _PangoGlyphString {
  gint num_glyphs;

  PangoGlyphInfo *glyphs;






  gint *log_clusters;


  gint space;
};



PangoGlyphString *pango_glyph_string_new (void);
void pango_glyph_string_set_size (PangoGlyphString *string,
            gint new_len);
GType pango_glyph_string_get_type (void) ;
PangoGlyphString *pango_glyph_string_copy (PangoGlyphString *string);
void pango_glyph_string_free (PangoGlyphString *string);
void pango_glyph_string_extents (PangoGlyphString *glyphs,
            PangoFont *font,
            PangoRectangle *ink_rect,
            PangoRectangle *logical_rect);
int pango_glyph_string_get_width(PangoGlyphString *glyphs) ;

void pango_glyph_string_extents_range (PangoGlyphString *glyphs,
           int start,
           int end,
           PangoFont *font,
           PangoRectangle *ink_rect,
           PangoRectangle *logical_rect);

void pango_glyph_string_get_logical_widths (PangoGlyphString *glyphs,
         const char *text,
         int length,
         int embedding_level,
         int *logical_widths);

void pango_glyph_string_index_to_x (PangoGlyphString *glyphs,
        char *text,
        int length,
        PangoAnalysis *analysis,
        int index_,
        gboolean trailing,
        int *x_pos);
void pango_glyph_string_x_to_index (PangoGlyphString *glyphs,
        char *text,
        int length,
        PangoAnalysis *analysis,
        int x_pos,
        int *index_,
        int *trailing);



void pango_shape (const gchar *text,
    gint length,
    const PangoAnalysis *analysis,
    PangoGlyphString *glyphs);

GList *pango_reorder_items (GList *logical_items);








GType pango_attr_type_get_type (void);

GType pango_underline_get_type (void);


GType pango_bidi_type_get_type (void);

GType pango_direction_get_type (void);


GType pango_coverage_level_get_type (void);


GType pango_style_get_type (void);

GType pango_variant_get_type (void);

GType pango_weight_get_type (void);

GType pango_stretch_get_type (void);

GType pango_font_mask_get_type (void);


GType pango_gravity_get_type (void);

GType pango_gravity_hint_get_type (void);


GType pango_alignment_get_type (void);

GType pango_wrap_mode_get_type (void);

GType pango_ellipsize_mode_get_type (void);


GType pango_render_part_get_type (void);


GType pango_script_get_type (void);


GType pango_tab_align_get_type (void);








typedef struct _PangoGlyphItem PangoGlyphItem;

struct _PangoGlyphItem
{
  PangoItem *item;
  PangoGlyphString *glyphs;
};



GType pango_glyph_item_get_type (void) ;

PangoGlyphItem *pango_glyph_item_split (PangoGlyphItem *orig,
            const char *text,
            int split_index);
PangoGlyphItem *pango_glyph_item_copy (PangoGlyphItem *orig);
void pango_glyph_item_free (PangoGlyphItem *glyph_item);
GSList * pango_glyph_item_apply_attrs (PangoGlyphItem *glyph_item,
            const char *text,
            PangoAttrList *list);
void pango_glyph_item_letter_space (PangoGlyphItem *glyph_item,
            const char *text,
            PangoLogAttr *log_attrs,
            int letter_spacing);


typedef struct _PangoGlyphItemIter PangoGlyphItemIter;

struct _PangoGlyphItemIter
{
  PangoGlyphItem *glyph_item;
  const gchar *text;

  int start_glyph;
  int start_index;
  int start_char;

  int end_glyph;
  int end_index;
  int end_char;
};



GType pango_glyph_item_iter_get_type (void) ;
PangoGlyphItemIter *pango_glyph_item_iter_copy (PangoGlyphItemIter *orig);
void pango_glyph_item_iter_free (PangoGlyphItemIter *iter);

gboolean pango_glyph_item_iter_init_start (PangoGlyphItemIter *iter,
          PangoGlyphItem *glyph_item,
          const char *text);
gboolean pango_glyph_item_iter_init_end (PangoGlyphItemIter *iter,
          PangoGlyphItem *glyph_item,
          const char *text);
gboolean pango_glyph_item_iter_next_cluster (PangoGlyphItemIter *iter);
gboolean pango_glyph_item_iter_prev_cluster (PangoGlyphItemIter *iter);






typedef struct _PangoTabArray PangoTabArray;

typedef enum
{
  PANGO_TAB_LEFT
} PangoTabAlign;



PangoTabArray *pango_tab_array_new (gint initial_size,
           gboolean positions_in_pixels);
PangoTabArray *pango_tab_array_new_with_positions (gint size,
           gboolean positions_in_pixels,
           PangoTabAlign first_alignment,
           gint first_position,
           ...);
GType pango_tab_array_get_type (void) ;
PangoTabArray *pango_tab_array_copy (PangoTabArray *src);
void pango_tab_array_free (PangoTabArray *tab_array);
gint pango_tab_array_get_size (PangoTabArray *tab_array);
void pango_tab_array_resize (PangoTabArray *tab_array,
           gint new_size);
void pango_tab_array_set_tab (PangoTabArray *tab_array,
           gint tab_index,
           PangoTabAlign alignment,
           gint location);
void pango_tab_array_get_tab (PangoTabArray *tab_array,
           gint tab_index,
           PangoTabAlign *alignment,
           gint *location);
void pango_tab_array_get_tabs (PangoTabArray *tab_array,
           PangoTabAlign **alignments,
           gint **locations);

gboolean pango_tab_array_get_positions_in_pixels (PangoTabArray *tab_array);






typedef struct _PangoLayout PangoLayout;
typedef struct _PangoLayoutClass PangoLayoutClass;
typedef struct _PangoLayoutLine PangoLayoutLine;

typedef PangoGlyphItem PangoLayoutRun;

typedef enum {
  PANGO_ALIGN_LEFT,
  PANGO_ALIGN_CENTER,
  PANGO_ALIGN_RIGHT
} PangoAlignment;

typedef enum {
  PANGO_WRAP_WORD,
  PANGO_WRAP_CHAR,
  PANGO_WRAP_WORD_CHAR
} PangoWrapMode;
typedef enum {
  PANGO_ELLIPSIZE_NONE,
  PANGO_ELLIPSIZE_START,
  PANGO_ELLIPSIZE_MIDDLE,
  PANGO_ELLIPSIZE_END
} PangoEllipsizeMode;

struct _PangoLayoutLine
{
  PangoLayout *layout;
  gint start_index;
  gint length;
  GSList *runs;
  guint is_paragraph_start : 1;
  guint resolved_dir : 3;
};
GType pango_layout_get_type (void) ;
PangoLayout *pango_layout_new (PangoContext *context);
PangoLayout *pango_layout_copy (PangoLayout *src);

PangoContext *pango_layout_get_context (PangoLayout *layout);

void pango_layout_set_attributes (PangoLayout *layout,
         PangoAttrList *attrs);
PangoAttrList *pango_layout_get_attributes (PangoLayout *layout);

void pango_layout_set_text (PangoLayout *layout,
         const char *text,
         int length);
const char *pango_layout_get_text (PangoLayout *layout);

void pango_layout_set_markup (PangoLayout *layout,
         const char *markup,
         int length);

void pango_layout_set_markup_with_accel (PangoLayout *layout,
         const char *markup,
         int length,
         gunichar accel_marker,
         gunichar *accel_char);

void pango_layout_set_font_description (PangoLayout *layout,
        const PangoFontDescription *desc);

const PangoFontDescription *pango_layout_get_font_description (PangoLayout *layout);

void pango_layout_set_width (PangoLayout *layout,
        int width);
int pango_layout_get_width (PangoLayout *layout);
void pango_layout_set_height (PangoLayout *layout,
        int height);
int pango_layout_get_height (PangoLayout *layout);
void pango_layout_set_wrap (PangoLayout *layout,
        PangoWrapMode wrap);
PangoWrapMode pango_layout_get_wrap (PangoLayout *layout);
gboolean pango_layout_is_wrapped (PangoLayout *layout);
void pango_layout_set_indent (PangoLayout *layout,
        int indent);
int pango_layout_get_indent (PangoLayout *layout);
void pango_layout_set_spacing (PangoLayout *layout,
        int spacing);
int pango_layout_get_spacing (PangoLayout *layout);
void pango_layout_set_justify (PangoLayout *layout,
        gboolean justify);
gboolean pango_layout_get_justify (PangoLayout *layout);
void pango_layout_set_auto_dir (PangoLayout *layout,
        gboolean auto_dir);
gboolean pango_layout_get_auto_dir (PangoLayout *layout);
void pango_layout_set_alignment (PangoLayout *layout,
        PangoAlignment alignment);
PangoAlignment pango_layout_get_alignment (PangoLayout *layout);

void pango_layout_set_tabs (PangoLayout *layout,
        PangoTabArray *tabs);

PangoTabArray* pango_layout_get_tabs (PangoLayout *layout);

void pango_layout_set_single_paragraph_mode (PangoLayout *layout,
             gboolean setting);
gboolean pango_layout_get_single_paragraph_mode (PangoLayout *layout);

void pango_layout_set_ellipsize (PangoLayout *layout,
            PangoEllipsizeMode ellipsize);
PangoEllipsizeMode pango_layout_get_ellipsize (PangoLayout *layout);
gboolean pango_layout_is_ellipsized (PangoLayout *layout);

int pango_layout_get_unknown_glyphs_count (PangoLayout *layout);

void pango_layout_context_changed (PangoLayout *layout);

void pango_layout_get_log_attrs (PangoLayout *layout,
         PangoLogAttr **attrs,
         gint *n_attrs);

void pango_layout_index_to_pos (PangoLayout *layout,
         int index_,
         PangoRectangle *pos);
void pango_layout_index_to_line_x (PangoLayout *layout,
         int index_,
         gboolean trailing,
         int *line,
         int *x_pos);
void pango_layout_get_cursor_pos (PangoLayout *layout,
         int index_,
         PangoRectangle *strong_pos,
         PangoRectangle *weak_pos);
void pango_layout_move_cursor_visually (PangoLayout *layout,
         gboolean strong,
         int old_index,
         int old_trailing,
         int direction,
         int *new_index,
         int *new_trailing);
gboolean pango_layout_xy_to_index (PangoLayout *layout,
         int x,
         int y,
         int *index_,
         int *trailing);
void pango_layout_get_extents (PangoLayout *layout,
         PangoRectangle *ink_rect,
         PangoRectangle *logical_rect);
void pango_layout_get_pixel_extents (PangoLayout *layout,
         PangoRectangle *ink_rect,
         PangoRectangle *logical_rect);
void pango_layout_get_size (PangoLayout *layout,
         int *width,
         int *height);
void pango_layout_get_pixel_size (PangoLayout *layout,
         int *width,
         int *height);
int pango_layout_get_baseline (PangoLayout *layout);

int pango_layout_get_line_count (PangoLayout *layout);
PangoLayoutLine *pango_layout_get_line (PangoLayout *layout,
          int line);
PangoLayoutLine *pango_layout_get_line_readonly (PangoLayout *layout,
          int line);
GSList * pango_layout_get_lines (PangoLayout *layout);
GSList * pango_layout_get_lines_readonly (PangoLayout *layout);




GType pango_layout_line_get_type (void) ;

PangoLayoutLine *pango_layout_line_ref (PangoLayoutLine *line);
void pango_layout_line_unref (PangoLayoutLine *line);

gboolean pango_layout_line_x_to_index (PangoLayoutLine *line,
      int x_pos,
      int *index_,
      int *trailing);
void pango_layout_line_index_to_x (PangoLayoutLine *line,
      int index_,
      gboolean trailing,
      int *x_pos);
void pango_layout_line_get_x_ranges (PangoLayoutLine *line,
      int start_index,
      int end_index,
      int **ranges,
      int *n_ranges);
void pango_layout_line_get_extents (PangoLayoutLine *line,
      PangoRectangle *ink_rect,
      PangoRectangle *logical_rect);
void pango_layout_line_get_pixel_extents (PangoLayoutLine *layout_line,
           PangoRectangle *ink_rect,
           PangoRectangle *logical_rect);

typedef struct _PangoLayoutIter PangoLayoutIter;



GType pango_layout_iter_get_type (void) ;

PangoLayoutIter *pango_layout_get_iter (PangoLayout *layout);
PangoLayoutIter *pango_layout_iter_copy (PangoLayoutIter *iter);
void pango_layout_iter_free (PangoLayoutIter *iter);

int pango_layout_iter_get_index (PangoLayoutIter *iter);
PangoLayoutRun *pango_layout_iter_get_run (PangoLayoutIter *iter);
PangoLayoutRun *pango_layout_iter_get_run_readonly (PangoLayoutIter *iter);
PangoLayoutLine *pango_layout_iter_get_line (PangoLayoutIter *iter);
PangoLayoutLine *pango_layout_iter_get_line_readonly (PangoLayoutIter *iter);
gboolean pango_layout_iter_at_last_line (PangoLayoutIter *iter);
PangoLayout *pango_layout_iter_get_layout (PangoLayoutIter *iter);

gboolean pango_layout_iter_next_char (PangoLayoutIter *iter);
gboolean pango_layout_iter_next_cluster (PangoLayoutIter *iter);
gboolean pango_layout_iter_next_run (PangoLayoutIter *iter);
gboolean pango_layout_iter_next_line (PangoLayoutIter *iter);

void pango_layout_iter_get_char_extents (PangoLayoutIter *iter,
         PangoRectangle *logical_rect);
void pango_layout_iter_get_cluster_extents (PangoLayoutIter *iter,
         PangoRectangle *ink_rect,
         PangoRectangle *logical_rect);
void pango_layout_iter_get_run_extents (PangoLayoutIter *iter,
         PangoRectangle *ink_rect,
         PangoRectangle *logical_rect);
void pango_layout_iter_get_line_extents (PangoLayoutIter *iter,
         PangoRectangle *ink_rect,
         PangoRectangle *logical_rect);



void pango_layout_iter_get_line_yrange (PangoLayoutIter *iter,
         int *y0_,
         int *y1_);
void pango_layout_iter_get_layout_extents (PangoLayoutIter *iter,
         PangoRectangle *ink_rect,
         PangoRectangle *logical_rect);
int pango_layout_iter_get_baseline (PangoLayoutIter *iter);




typedef struct _PangoRenderer PangoRenderer;
typedef struct _PangoRendererClass PangoRendererClass;
typedef struct _PangoRendererPrivate PangoRendererPrivate;
typedef enum
{
  PANGO_RENDER_PART_FOREGROUND,
  PANGO_RENDER_PART_BACKGROUND,
  PANGO_RENDER_PART_UNDERLINE,
  PANGO_RENDER_PART_STRIKETHROUGH
} PangoRenderPart;
struct _PangoRenderer
{

  GObject parent_instance;

  PangoUnderline underline;
  gboolean strikethrough;
  int active_count;


  PangoMatrix *matrix;


  PangoRendererPrivate *priv;
};
struct _PangoRendererClass
{

  GObjectClass parent_class;







  void (*draw_glyphs) (PangoRenderer *renderer,
         PangoFont *font,
         PangoGlyphString *glyphs,
         int x,
         int y);
  void (*draw_rectangle) (PangoRenderer *renderer,
     PangoRenderPart part,
     int x,
     int y,
     int width,
     int height);
  void (*draw_error_underline) (PangoRenderer *renderer,
    int x,
    int y,
    int width,
    int height);


  void (*draw_shape) (PangoRenderer *renderer,
        PangoAttrShape *attr,
        int x,
        int y);




  void (*draw_trapezoid) (PangoRenderer *renderer,
     PangoRenderPart part,
     double y1_,
     double x11,
     double x21,
     double y2,
     double x12,
     double x22);
  void (*draw_glyph) (PangoRenderer *renderer,
        PangoFont *font,
        PangoGlyph glyph,
        double x,
        double y);



  void (*part_changed) (PangoRenderer *renderer,
   PangoRenderPart part);



  void (*begin) (PangoRenderer *renderer);
  void (*end) (PangoRenderer *renderer);



  void (*prepare_run) (PangoRenderer *renderer,
         PangoLayoutRun *run);




  void (*draw_glyph_item) (PangoRenderer *renderer,
      const char *text,
      PangoGlyphItem *glyph_item,
      int x,
      int y);




  void (*_pango_reserved2) (void);
  void (*_pango_reserved3) (void);
  void (*_pango_reserved4) (void);
};

GType pango_renderer_get_type (void) ;

void pango_renderer_draw_layout (PangoRenderer *renderer,
       PangoLayout *layout,
       int x,
       int y);
void pango_renderer_draw_layout_line (PangoRenderer *renderer,
       PangoLayoutLine *line,
       int x,
       int y);
void pango_renderer_draw_glyphs (PangoRenderer *renderer,
       PangoFont *font,
       PangoGlyphString *glyphs,
       int x,
       int y);
void pango_renderer_draw_glyph_item (PangoRenderer *renderer,
       const char *text,
       PangoGlyphItem *glyph_item,
       int x,
       int y);
void pango_renderer_draw_rectangle (PangoRenderer *renderer,
       PangoRenderPart part,
       int x,
       int y,
       int width,
       int height);
void pango_renderer_draw_error_underline (PangoRenderer *renderer,
       int x,
       int y,
       int width,
       int height);
void pango_renderer_draw_trapezoid (PangoRenderer *renderer,
       PangoRenderPart part,
       double y1_,
       double x11,
       double x21,
       double y2,
       double x12,
       double x22);
void pango_renderer_draw_glyph (PangoRenderer *renderer,
       PangoFont *font,
       PangoGlyph glyph,
       double x,
       double y);

void pango_renderer_activate (PangoRenderer *renderer);
void pango_renderer_deactivate (PangoRenderer *renderer);

void pango_renderer_part_changed (PangoRenderer *renderer,
      PangoRenderPart part);

void pango_renderer_set_color (PangoRenderer *renderer,
          PangoRenderPart part,
          const PangoColor *color);
PangoColor *pango_renderer_get_color (PangoRenderer *renderer,
          PangoRenderPart part);

void pango_renderer_set_matrix (PangoRenderer *renderer,
             const PangoMatrix *matrix);
const PangoMatrix *pango_renderer_get_matrix (PangoRenderer *renderer);

PangoLayout *pango_renderer_get_layout (PangoRenderer *renderer);
PangoLayoutLine *pango_renderer_get_layout_line (PangoRenderer *renderer);










char ** pango_split_file_list (const char *str);

char *pango_trim_string (const char *str);
gint pango_read_line (FILE *stream,
          GString *str);
gboolean pango_skip_space (const char **pos);
gboolean pango_scan_word (const char **pos,
          GString *out);
gboolean pango_scan_string (const char **pos,
          GString *out);
gboolean pango_scan_int (const char **pos,
          int *out);
gboolean pango_parse_enum (GType type,
          const char *str,
          int *value,
          gboolean warn,
          char **possible_values);
gboolean pango_parse_style (const char *str,
         PangoStyle *style,
         gboolean warn);
gboolean pango_parse_variant (const char *str,
         PangoVariant *variant,
         gboolean warn);
gboolean pango_parse_weight (const char *str,
         PangoWeight *weight,
         gboolean warn);
gboolean pango_parse_stretch (const char *str,
         PangoStretch *stretch,
         gboolean warn);
void pango_quantize_line_geometry (int *thickness,
       int *position);



guint8 * pango_log2vis_get_embedding_levels (const gchar *text,
          int length,
          PangoDirection *pbase_dir);




gboolean pango_is_zero_width (gunichar ch) ;
int pango_version (void) ;


const char * pango_version_string (void) ;


const char * pango_version_check (int required_major,
        int required_minor,
        int required_micro) ;



 int
cairo_version (void);

 const char*
cairo_version_string (void);
typedef int cairo_bool_t;
typedef struct _cairo cairo_t;
typedef struct _cairo_surface cairo_surface_t;
typedef struct _cairo_matrix {
    double xx; double yx;
    double xy; double yy;
    double x0; double y0;
} cairo_matrix_t;
typedef struct _cairo_pattern cairo_pattern_t;
typedef void (*cairo_destroy_func_t) (void *data);
typedef struct _cairo_user_data_key {
    int unused;
} cairo_user_data_key_t;
typedef enum _cairo_status {
    CAIRO_STATUS_SUCCESS = 0,
    CAIRO_STATUS_NO_MEMORY,
    CAIRO_STATUS_INVALID_RESTORE,
    CAIRO_STATUS_INVALID_POP_GROUP,
    CAIRO_STATUS_NO_CURRENT_POINT,
    CAIRO_STATUS_INVALID_MATRIX,
    CAIRO_STATUS_INVALID_STATUS,
    CAIRO_STATUS_NULL_POINTER,
    CAIRO_STATUS_INVALID_STRING,
    CAIRO_STATUS_INVALID_PATH_DATA,
    CAIRO_STATUS_READ_ERROR,
    CAIRO_STATUS_WRITE_ERROR,
    CAIRO_STATUS_SURFACE_FINISHED,
    CAIRO_STATUS_SURFACE_TYPE_MISMATCH,
    CAIRO_STATUS_PATTERN_TYPE_MISMATCH,
    CAIRO_STATUS_INVALID_CONTENT,
    CAIRO_STATUS_INVALID_FORMAT,
    CAIRO_STATUS_INVALID_VISUAL,
    CAIRO_STATUS_FILE_NOT_FOUND,
    CAIRO_STATUS_INVALID_DASH,
    CAIRO_STATUS_INVALID_DSC_COMMENT,
    CAIRO_STATUS_INVALID_INDEX,
    CAIRO_STATUS_CLIP_NOT_REPRESENTABLE,
    CAIRO_STATUS_TEMP_FILE_ERROR,
    CAIRO_STATUS_INVALID_STRIDE,
    CAIRO_STATUS_FONT_TYPE_MISMATCH,
    CAIRO_STATUS_USER_FONT_IMMUTABLE,
    CAIRO_STATUS_USER_FONT_ERROR,
    CAIRO_STATUS_NEGATIVE_COUNT,
    CAIRO_STATUS_INVALID_CLUSTERS,
    CAIRO_STATUS_INVALID_SLANT,
    CAIRO_STATUS_INVALID_WEIGHT

} cairo_status_t;
typedef enum _cairo_content {
    CAIRO_CONTENT_COLOR = 0x1000,
    CAIRO_CONTENT_ALPHA = 0x2000,
    CAIRO_CONTENT_COLOR_ALPHA = 0x3000
} cairo_content_t;
typedef cairo_status_t (*cairo_write_func_t) (void *closure,
           const unsigned char *data,
           unsigned int length);
typedef cairo_status_t (*cairo_read_func_t) (void *closure,
          unsigned char *data,
          unsigned int length);


 cairo_t *
cairo_create (cairo_surface_t *target);

 cairo_t *
cairo_reference (cairo_t *cr);

 void
cairo_destroy (cairo_t *cr);

 unsigned int
cairo_get_reference_count (cairo_t *cr);

 void *
cairo_get_user_data (cairo_t *cr,
       const cairo_user_data_key_t *key);

 cairo_status_t
cairo_set_user_data (cairo_t *cr,
       const cairo_user_data_key_t *key,
       void *user_data,
       cairo_destroy_func_t destroy);

 void
cairo_save (cairo_t *cr);

 void
cairo_restore (cairo_t *cr);

 void
cairo_push_group (cairo_t *cr);

 void
cairo_push_group_with_content (cairo_t *cr, cairo_content_t content);

 cairo_pattern_t *
cairo_pop_group (cairo_t *cr);

 void
cairo_pop_group_to_source (cairo_t *cr);
typedef enum _cairo_operator {
    CAIRO_OPERATOR_CLEAR,

    CAIRO_OPERATOR_SOURCE,
    CAIRO_OPERATOR_OVER,
    CAIRO_OPERATOR_IN,
    CAIRO_OPERATOR_OUT,
    CAIRO_OPERATOR_ATOP,

    CAIRO_OPERATOR_DEST,
    CAIRO_OPERATOR_DEST_OVER,
    CAIRO_OPERATOR_DEST_IN,
    CAIRO_OPERATOR_DEST_OUT,
    CAIRO_OPERATOR_DEST_ATOP,

    CAIRO_OPERATOR_XOR,
    CAIRO_OPERATOR_ADD,
    CAIRO_OPERATOR_SATURATE
} cairo_operator_t;

 void
cairo_set_operator (cairo_t *cr, cairo_operator_t op);

 void
cairo_set_source (cairo_t *cr, cairo_pattern_t *source);

 void
cairo_set_source_rgb (cairo_t *cr, double red, double green, double blue);

 void
cairo_set_source_rgba (cairo_t *cr,
         double red, double green, double blue,
         double alpha);

 void
cairo_set_source_surface (cairo_t *cr,
     cairo_surface_t *surface,
     double x,
     double y);

 void
cairo_set_tolerance (cairo_t *cr, double tolerance);
typedef enum _cairo_antialias {
    CAIRO_ANTIALIAS_DEFAULT,
    CAIRO_ANTIALIAS_NONE,
    CAIRO_ANTIALIAS_GRAY,
    CAIRO_ANTIALIAS_SUBPIXEL
} cairo_antialias_t;

 void
cairo_set_antialias (cairo_t *cr, cairo_antialias_t antialias);
typedef enum _cairo_fill_rule {
    CAIRO_FILL_RULE_WINDING,
    CAIRO_FILL_RULE_EVEN_ODD
} cairo_fill_rule_t;

 void
cairo_set_fill_rule (cairo_t *cr, cairo_fill_rule_t fill_rule);

 void
cairo_set_line_width (cairo_t *cr, double width);
typedef enum _cairo_line_cap {
    CAIRO_LINE_CAP_BUTT,
    CAIRO_LINE_CAP_ROUND,
    CAIRO_LINE_CAP_SQUARE
} cairo_line_cap_t;

 void
cairo_set_line_cap (cairo_t *cr, cairo_line_cap_t line_cap);
typedef enum _cairo_line_join {
    CAIRO_LINE_JOIN_MITER,
    CAIRO_LINE_JOIN_ROUND,
    CAIRO_LINE_JOIN_BEVEL
} cairo_line_join_t;

 void
cairo_set_line_join (cairo_t *cr, cairo_line_join_t line_join);

 void
cairo_set_dash (cairo_t *cr,
  const double *dashes,
  int num_dashes,
  double offset);

 void
cairo_set_miter_limit (cairo_t *cr, double limit);

 void
cairo_translate (cairo_t *cr, double tx, double ty);

 void
cairo_scale (cairo_t *cr, double sx, double sy);

 void
cairo_rotate (cairo_t *cr, double angle);

 void
cairo_transform (cairo_t *cr,
   const cairo_matrix_t *matrix);

 void
cairo_set_matrix (cairo_t *cr,
    const cairo_matrix_t *matrix);

 void
cairo_identity_matrix (cairo_t *cr);

 void
cairo_user_to_device (cairo_t *cr, double *x, double *y);

 void
cairo_user_to_device_distance (cairo_t *cr, double *dx, double *dy);

 void
cairo_device_to_user (cairo_t *cr, double *x, double *y);

 void
cairo_device_to_user_distance (cairo_t *cr, double *dx, double *dy);


 void
cairo_new_path (cairo_t *cr);

 void
cairo_move_to (cairo_t *cr, double x, double y);

 void
cairo_new_sub_path (cairo_t *cr);

 void
cairo_line_to (cairo_t *cr, double x, double y);

 void
cairo_curve_to (cairo_t *cr,
  double x1, double y1,
  double x2, double y2,
  double x3, double y3);

 void
cairo_arc (cairo_t *cr,
    double xc, double yc,
    double radius,
    double angle1, double angle2);

 void
cairo_arc_negative (cairo_t *cr,
      double xc, double yc,
      double radius,
      double angle1, double angle2);
 void
cairo_rel_move_to (cairo_t *cr, double dx, double dy);

 void
cairo_rel_line_to (cairo_t *cr, double dx, double dy);

 void
cairo_rel_curve_to (cairo_t *cr,
      double dx1, double dy1,
      double dx2, double dy2,
      double dx3, double dy3);

 void
cairo_rectangle (cairo_t *cr,
   double x, double y,
   double width, double height);






 void
cairo_close_path (cairo_t *cr);

 void
cairo_path_extents (cairo_t *cr,
      double *x1, double *y1,
      double *x2, double *y2);


 void
cairo_paint (cairo_t *cr);

 void
cairo_paint_with_alpha (cairo_t *cr,
   double alpha);

 void
cairo_mask (cairo_t *cr,
     cairo_pattern_t *pattern);

 void
cairo_mask_surface (cairo_t *cr,
      cairo_surface_t *surface,
      double surface_x,
      double surface_y);

 void
cairo_stroke (cairo_t *cr);

 void
cairo_stroke_preserve (cairo_t *cr);

 void
cairo_fill (cairo_t *cr);

 void
cairo_fill_preserve (cairo_t *cr);

 void
cairo_copy_page (cairo_t *cr);

 void
cairo_show_page (cairo_t *cr);


 cairo_bool_t
cairo_in_stroke (cairo_t *cr, double x, double y);

 cairo_bool_t
cairo_in_fill (cairo_t *cr, double x, double y);


 void
cairo_stroke_extents (cairo_t *cr,
        double *x1, double *y1,
        double *x2, double *y2);

 void
cairo_fill_extents (cairo_t *cr,
      double *x1, double *y1,
      double *x2, double *y2);


 void
cairo_reset_clip (cairo_t *cr);

 void
cairo_clip (cairo_t *cr);

 void
cairo_clip_preserve (cairo_t *cr);

 void
cairo_clip_extents (cairo_t *cr,
      double *x1, double *y1,
      double *x2, double *y2);
typedef struct _cairo_rectangle {
    double x, y, width, height;
} cairo_rectangle_t;
typedef struct _cairo_rectangle_list {
    cairo_status_t status;
    cairo_rectangle_t *rectangles;
    int num_rectangles;
} cairo_rectangle_list_t;

 cairo_rectangle_list_t *
cairo_copy_clip_rectangle_list (cairo_t *cr);

 void
cairo_rectangle_list_destroy (cairo_rectangle_list_t *rectangle_list);
typedef struct _cairo_scaled_font cairo_scaled_font_t;
typedef struct _cairo_font_face cairo_font_face_t;
typedef struct {
    unsigned long index;
    double x;
    double y;
} cairo_glyph_t;

 cairo_glyph_t *
cairo_glyph_allocate (int num_glyphs);

 void
cairo_glyph_free (cairo_glyph_t *glyphs);
typedef struct {
    int num_bytes;
    int num_glyphs;
} cairo_text_cluster_t;

 cairo_text_cluster_t *
cairo_text_cluster_allocate (int num_clusters);

 void
cairo_text_cluster_free (cairo_text_cluster_t *clusters);
typedef enum _cairo_text_cluster_flags {
    CAIRO_TEXT_CLUSTER_FLAG_BACKWARD = 0x00000001
} cairo_text_cluster_flags_t;
typedef struct {
    double x_bearing;
    double y_bearing;
    double width;
    double height;
    double x_advance;
    double y_advance;
} cairo_text_extents_t;
typedef struct {
    double ascent;
    double descent;
    double height;
    double max_x_advance;
    double max_y_advance;
} cairo_font_extents_t;
typedef enum _cairo_font_slant {
    CAIRO_FONT_SLANT_NORMAL,
    CAIRO_FONT_SLANT_ITALIC,
    CAIRO_FONT_SLANT_OBLIQUE
} cairo_font_slant_t;
typedef enum _cairo_font_weight {
    CAIRO_FONT_WEIGHT_NORMAL,
    CAIRO_FONT_WEIGHT_BOLD
} cairo_font_weight_t;
typedef enum _cairo_subpixel_order {
    CAIRO_SUBPIXEL_ORDER_DEFAULT,
    CAIRO_SUBPIXEL_ORDER_RGB,
    CAIRO_SUBPIXEL_ORDER_BGR,
    CAIRO_SUBPIXEL_ORDER_VRGB,
    CAIRO_SUBPIXEL_ORDER_VBGR
} cairo_subpixel_order_t;
typedef enum _cairo_hint_style {
    CAIRO_HINT_STYLE_DEFAULT,
    CAIRO_HINT_STYLE_NONE,
    CAIRO_HINT_STYLE_SLIGHT,
    CAIRO_HINT_STYLE_MEDIUM,
    CAIRO_HINT_STYLE_FULL
} cairo_hint_style_t;
typedef enum _cairo_hint_metrics {
    CAIRO_HINT_METRICS_DEFAULT,
    CAIRO_HINT_METRICS_OFF,
    CAIRO_HINT_METRICS_ON
} cairo_hint_metrics_t;
typedef struct _cairo_font_options cairo_font_options_t;

 cairo_font_options_t *
cairo_font_options_create (void);

 cairo_font_options_t *
cairo_font_options_copy (const cairo_font_options_t *original);

 void
cairo_font_options_destroy (cairo_font_options_t *options);

 cairo_status_t
cairo_font_options_status (cairo_font_options_t *options);

 void
cairo_font_options_merge (cairo_font_options_t *options,
     const cairo_font_options_t *other);
 cairo_bool_t
cairo_font_options_equal (const cairo_font_options_t *options,
     const cairo_font_options_t *other);

 unsigned long
cairo_font_options_hash (const cairo_font_options_t *options);

 void
cairo_font_options_set_antialias (cairo_font_options_t *options,
      cairo_antialias_t antialias);
 cairo_antialias_t
cairo_font_options_get_antialias (const cairo_font_options_t *options);

 void
cairo_font_options_set_subpixel_order (cairo_font_options_t *options,
           cairo_subpixel_order_t subpixel_order);
 cairo_subpixel_order_t
cairo_font_options_get_subpixel_order (const cairo_font_options_t *options);

 void
cairo_font_options_set_hint_style (cairo_font_options_t *options,
       cairo_hint_style_t hint_style);
 cairo_hint_style_t
cairo_font_options_get_hint_style (const cairo_font_options_t *options);

 void
cairo_font_options_set_hint_metrics (cairo_font_options_t *options,
         cairo_hint_metrics_t hint_metrics);
 cairo_hint_metrics_t
cairo_font_options_get_hint_metrics (const cairo_font_options_t *options);




 void
cairo_select_font_face (cairo_t *cr,
   const char *family,
   cairo_font_slant_t slant,
   cairo_font_weight_t weight);

 void
cairo_set_font_size (cairo_t *cr, double size);

 void
cairo_set_font_matrix (cairo_t *cr,
         const cairo_matrix_t *matrix);

 void
cairo_get_font_matrix (cairo_t *cr,
         cairo_matrix_t *matrix);

 void
cairo_set_font_options (cairo_t *cr,
   const cairo_font_options_t *options);

 void
cairo_get_font_options (cairo_t *cr,
   cairo_font_options_t *options);

 void
cairo_set_font_face (cairo_t *cr, cairo_font_face_t *font_face);

 cairo_font_face_t *
cairo_get_font_face (cairo_t *cr);

 void
cairo_set_scaled_font (cairo_t *cr,
         const cairo_scaled_font_t *scaled_font);

 cairo_scaled_font_t *
cairo_get_scaled_font (cairo_t *cr);

 void
cairo_show_text (cairo_t *cr, const char *utf8);

 void
cairo_show_glyphs (cairo_t *cr, const cairo_glyph_t *glyphs, int num_glyphs);

 void
cairo_show_text_glyphs (cairo_t *cr,
   const char *utf8,
   int utf8_len,
   const cairo_glyph_t *glyphs,
   int num_glyphs,
   const cairo_text_cluster_t *clusters,
   int num_clusters,
   cairo_text_cluster_flags_t cluster_flags);

 void
cairo_text_path (cairo_t *cr, const char *utf8);

 void
cairo_glyph_path (cairo_t *cr, const cairo_glyph_t *glyphs, int num_glyphs);

 void
cairo_text_extents (cairo_t *cr,
      const char *utf8,
      cairo_text_extents_t *extents);

 void
cairo_glyph_extents (cairo_t *cr,
       const cairo_glyph_t *glyphs,
       int num_glyphs,
       cairo_text_extents_t *extents);

 void
cairo_font_extents (cairo_t *cr,
      cairo_font_extents_t *extents);



 cairo_font_face_t *
cairo_font_face_reference (cairo_font_face_t *font_face);

 void
cairo_font_face_destroy (cairo_font_face_t *font_face);

 unsigned int
cairo_font_face_get_reference_count (cairo_font_face_t *font_face);

 cairo_status_t
cairo_font_face_status (cairo_font_face_t *font_face);
typedef enum _cairo_font_type {
    CAIRO_FONT_TYPE_TOY,
    CAIRO_FONT_TYPE_FT,
    CAIRO_FONT_TYPE_WIN32,
    CAIRO_FONT_TYPE_QUARTZ,
    CAIRO_FONT_TYPE_USER
} cairo_font_type_t;

 cairo_font_type_t
cairo_font_face_get_type (cairo_font_face_t *font_face);

 void *
cairo_font_face_get_user_data (cairo_font_face_t *font_face,
          const cairo_user_data_key_t *key);

 cairo_status_t
cairo_font_face_set_user_data (cairo_font_face_t *font_face,
          const cairo_user_data_key_t *key,
          void *user_data,
          cairo_destroy_func_t destroy);



 cairo_scaled_font_t *
cairo_scaled_font_create (cairo_font_face_t *font_face,
     const cairo_matrix_t *font_matrix,
     const cairo_matrix_t *ctm,
     const cairo_font_options_t *options);

 cairo_scaled_font_t *
cairo_scaled_font_reference (cairo_scaled_font_t *scaled_font);

 void
cairo_scaled_font_destroy (cairo_scaled_font_t *scaled_font);

 unsigned int
cairo_scaled_font_get_reference_count (cairo_scaled_font_t *scaled_font);

 cairo_status_t
cairo_scaled_font_status (cairo_scaled_font_t *scaled_font);

 cairo_font_type_t
cairo_scaled_font_get_type (cairo_scaled_font_t *scaled_font);

 void *
cairo_scaled_font_get_user_data (cairo_scaled_font_t *scaled_font,
     const cairo_user_data_key_t *key);

 cairo_status_t
cairo_scaled_font_set_user_data (cairo_scaled_font_t *scaled_font,
     const cairo_user_data_key_t *key,
     void *user_data,
     cairo_destroy_func_t destroy);

 void
cairo_scaled_font_extents (cairo_scaled_font_t *scaled_font,
      cairo_font_extents_t *extents);

 void
cairo_scaled_font_text_extents (cairo_scaled_font_t *scaled_font,
    const char *utf8,
    cairo_text_extents_t *extents);

 void
cairo_scaled_font_glyph_extents (cairo_scaled_font_t *scaled_font,
     const cairo_glyph_t *glyphs,
     int num_glyphs,
     cairo_text_extents_t *extents);

 cairo_status_t
cairo_scaled_font_text_to_glyphs (cairo_scaled_font_t *scaled_font,
      double x,
      double y,
      const char *utf8,
      int utf8_len,
      cairo_glyph_t **glyphs,
      int *num_glyphs,
      cairo_text_cluster_t **clusters,
      int *num_clusters,
      cairo_text_cluster_flags_t *cluster_flags);

 cairo_font_face_t *
cairo_scaled_font_get_font_face (cairo_scaled_font_t *scaled_font);

 void
cairo_scaled_font_get_font_matrix (cairo_scaled_font_t *scaled_font,
       cairo_matrix_t *font_matrix);

 void
cairo_scaled_font_get_ctm (cairo_scaled_font_t *scaled_font,
      cairo_matrix_t *ctm);

 void
cairo_scaled_font_get_scale_matrix (cairo_scaled_font_t *scaled_font,
        cairo_matrix_t *scale_matrix);

 void
cairo_scaled_font_get_font_options (cairo_scaled_font_t *scaled_font,
        cairo_font_options_t *options);




 cairo_font_face_t *
cairo_toy_font_face_create (const char *family,
       cairo_font_slant_t slant,
       cairo_font_weight_t weight);

 const char *
cairo_toy_font_face_get_family (cairo_font_face_t *font_face);

 cairo_font_slant_t
cairo_toy_font_face_get_slant (cairo_font_face_t *font_face);

 cairo_font_weight_t
cairo_toy_font_face_get_weight (cairo_font_face_t *font_face);




 cairo_font_face_t *
cairo_user_font_face_create (void);
typedef cairo_status_t (*cairo_user_scaled_font_init_func_t) (cairo_scaled_font_t *scaled_font,
             cairo_t *cr,
             cairo_font_extents_t *extents);
typedef cairo_status_t (*cairo_user_scaled_font_render_glyph_func_t) (cairo_scaled_font_t *scaled_font,
              unsigned long glyph,
              cairo_t *cr,
              cairo_text_extents_t *extents);
typedef cairo_status_t (*cairo_user_scaled_font_text_to_glyphs_func_t) (cairo_scaled_font_t *scaled_font,
         const char *utf8,
         int utf8_len,
         cairo_glyph_t **glyphs,
         int *num_glyphs,
         cairo_text_cluster_t **clusters,
         int *num_clusters,
         cairo_text_cluster_flags_t *cluster_flags);
typedef cairo_status_t (*cairo_user_scaled_font_unicode_to_glyph_func_t) (cairo_scaled_font_t *scaled_font,
           unsigned long unicode,
           unsigned long *glyph_index);



 void
cairo_user_font_face_set_init_func (cairo_font_face_t *font_face,
        cairo_user_scaled_font_init_func_t init_func);

 void
cairo_user_font_face_set_render_glyph_func (cairo_font_face_t *font_face,
         cairo_user_scaled_font_render_glyph_func_t render_glyph_func);

 void
cairo_user_font_face_set_text_to_glyphs_func (cairo_font_face_t *font_face,
           cairo_user_scaled_font_text_to_glyphs_func_t text_to_glyphs_func);

 void
cairo_user_font_face_set_unicode_to_glyph_func (cairo_font_face_t *font_face,
             cairo_user_scaled_font_unicode_to_glyph_func_t unicode_to_glyph_func);



 cairo_user_scaled_font_init_func_t
cairo_user_font_face_get_init_func (cairo_font_face_t *font_face);

 cairo_user_scaled_font_render_glyph_func_t
cairo_user_font_face_get_render_glyph_func (cairo_font_face_t *font_face);

 cairo_user_scaled_font_text_to_glyphs_func_t
cairo_user_font_face_get_text_to_glyphs_func (cairo_font_face_t *font_face);

 cairo_user_scaled_font_unicode_to_glyph_func_t
cairo_user_font_face_get_unicode_to_glyph_func (cairo_font_face_t *font_face);




 cairo_operator_t
cairo_get_operator (cairo_t *cr);

 cairo_pattern_t *
cairo_get_source (cairo_t *cr);

 double
cairo_get_tolerance (cairo_t *cr);

 cairo_antialias_t
cairo_get_antialias (cairo_t *cr);

 cairo_bool_t
cairo_has_current_point (cairo_t *cr);

 void
cairo_get_current_point (cairo_t *cr, double *x, double *y);

 cairo_fill_rule_t
cairo_get_fill_rule (cairo_t *cr);

 double
cairo_get_line_width (cairo_t *cr);

 cairo_line_cap_t
cairo_get_line_cap (cairo_t *cr);

 cairo_line_join_t
cairo_get_line_join (cairo_t *cr);

 double
cairo_get_miter_limit (cairo_t *cr);

 int
cairo_get_dash_count (cairo_t *cr);

 void
cairo_get_dash (cairo_t *cr, double *dashes, double *offset);

 void
cairo_get_matrix (cairo_t *cr, cairo_matrix_t *matrix);

 cairo_surface_t *
cairo_get_target (cairo_t *cr);

 cairo_surface_t *
cairo_get_group_target (cairo_t *cr);
typedef enum _cairo_path_data_type {
    CAIRO_PATH_MOVE_TO,
    CAIRO_PATH_LINE_TO,
    CAIRO_PATH_CURVE_TO,
    CAIRO_PATH_CLOSE_PATH
} cairo_path_data_type_t;
typedef union _cairo_path_data_t cairo_path_data_t;
union _cairo_path_data_t {
    struct {
 cairo_path_data_type_t type;
 int length;
    } header;
    struct {
 double x, y;
    } point;
};
typedef struct cairo_path {
    cairo_status_t status;
    cairo_path_data_t *data;
    int num_data;
} cairo_path_t;

 cairo_path_t *
cairo_copy_path (cairo_t *cr);

 cairo_path_t *
cairo_copy_path_flat (cairo_t *cr);

 void
cairo_append_path (cairo_t *cr,
     const cairo_path_t *path);

 void
cairo_path_destroy (cairo_path_t *path);



 cairo_status_t
cairo_status (cairo_t *cr);

 const char *
cairo_status_to_string (cairo_status_t status);



 cairo_surface_t *
cairo_surface_create_similar (cairo_surface_t *other,
         cairo_content_t content,
         int width,
         int height);

 cairo_surface_t *
cairo_surface_reference (cairo_surface_t *surface);

 void
cairo_surface_finish (cairo_surface_t *surface);

 void
cairo_surface_destroy (cairo_surface_t *surface);

 unsigned int
cairo_surface_get_reference_count (cairo_surface_t *surface);

 cairo_status_t
cairo_surface_status (cairo_surface_t *surface);
typedef enum _cairo_surface_type {
    CAIRO_SURFACE_TYPE_IMAGE,
    CAIRO_SURFACE_TYPE_PDF,
    CAIRO_SURFACE_TYPE_PS,
    CAIRO_SURFACE_TYPE_XLIB,
    CAIRO_SURFACE_TYPE_XCB,
    CAIRO_SURFACE_TYPE_GLITZ,
    CAIRO_SURFACE_TYPE_QUARTZ,
    CAIRO_SURFACE_TYPE_WIN32,
    CAIRO_SURFACE_TYPE_BEOS,
    CAIRO_SURFACE_TYPE_DIRECTFB,
    CAIRO_SURFACE_TYPE_SVG,
    CAIRO_SURFACE_TYPE_OS2,
    CAIRO_SURFACE_TYPE_WIN32_PRINTING,
    CAIRO_SURFACE_TYPE_QUARTZ_IMAGE
} cairo_surface_type_t;

 cairo_surface_type_t
cairo_surface_get_type (cairo_surface_t *surface);

 cairo_content_t
cairo_surface_get_content (cairo_surface_t *surface);



 cairo_status_t
cairo_surface_write_to_png (cairo_surface_t *surface,
       const char *filename);

 cairo_status_t
cairo_surface_write_to_png_stream (cairo_surface_t *surface,
       cairo_write_func_t write_func,
       void *closure);



 void *
cairo_surface_get_user_data (cairo_surface_t *surface,
        const cairo_user_data_key_t *key);

 cairo_status_t
cairo_surface_set_user_data (cairo_surface_t *surface,
        const cairo_user_data_key_t *key,
        void *user_data,
        cairo_destroy_func_t destroy);

 void
cairo_surface_get_font_options (cairo_surface_t *surface,
    cairo_font_options_t *options);

 void
cairo_surface_flush (cairo_surface_t *surface);

 void
cairo_surface_mark_dirty (cairo_surface_t *surface);

 void
cairo_surface_mark_dirty_rectangle (cairo_surface_t *surface,
        int x,
        int y,
        int width,
        int height);

 void
cairo_surface_set_device_offset (cairo_surface_t *surface,
     double x_offset,
     double y_offset);

 void
cairo_surface_get_device_offset (cairo_surface_t *surface,
     double *x_offset,
     double *y_offset);

 void
cairo_surface_set_fallback_resolution (cairo_surface_t *surface,
           double x_pixels_per_inch,
           double y_pixels_per_inch);

 void
cairo_surface_get_fallback_resolution (cairo_surface_t *surface,
           double *x_pixels_per_inch,
           double *y_pixels_per_inch);

 void
cairo_surface_copy_page (cairo_surface_t *surface);

 void
cairo_surface_show_page (cairo_surface_t *surface);

 cairo_bool_t
cairo_surface_has_show_text_glyphs (cairo_surface_t *surface);
typedef enum _cairo_format {
    CAIRO_FORMAT_ARGB32,
    CAIRO_FORMAT_RGB24,
    CAIRO_FORMAT_A8,
    CAIRO_FORMAT_A1




} cairo_format_t;

 cairo_surface_t *
cairo_image_surface_create (cairo_format_t format,
       int width,
       int height);

 int
cairo_format_stride_for_width (cairo_format_t format,
          int width);

 cairo_surface_t *
cairo_image_surface_create_for_data (unsigned char *data,
         cairo_format_t format,
         int width,
         int height,
         int stride);

 unsigned char *
cairo_image_surface_get_data (cairo_surface_t *surface);

 cairo_format_t
cairo_image_surface_get_format (cairo_surface_t *surface);

 int
cairo_image_surface_get_width (cairo_surface_t *surface);

 int
cairo_image_surface_get_height (cairo_surface_t *surface);

 int
cairo_image_surface_get_stride (cairo_surface_t *surface);



 cairo_surface_t *
cairo_image_surface_create_from_png (const char *filename);

 cairo_surface_t *
cairo_image_surface_create_from_png_stream (cairo_read_func_t read_func,
         void *closure);





 cairo_pattern_t *
cairo_pattern_create_rgb (double red, double green, double blue);

 cairo_pattern_t *
cairo_pattern_create_rgba (double red, double green, double blue,
      double alpha);

 cairo_pattern_t *
cairo_pattern_create_for_surface (cairo_surface_t *surface);

 cairo_pattern_t *
cairo_pattern_create_linear (double x0, double y0,
        double x1, double y1);

 cairo_pattern_t *
cairo_pattern_create_radial (double cx0, double cy0, double radius0,
        double cx1, double cy1, double radius1);

 cairo_pattern_t *
cairo_pattern_reference (cairo_pattern_t *pattern);

 void
cairo_pattern_destroy (cairo_pattern_t *pattern);

 unsigned int
cairo_pattern_get_reference_count (cairo_pattern_t *pattern);

 cairo_status_t
cairo_pattern_status (cairo_pattern_t *pattern);

 void *
cairo_pattern_get_user_data (cairo_pattern_t *pattern,
        const cairo_user_data_key_t *key);

 cairo_status_t
cairo_pattern_set_user_data (cairo_pattern_t *pattern,
        const cairo_user_data_key_t *key,
        void *user_data,
        cairo_destroy_func_t destroy);
typedef enum _cairo_pattern_type {
    CAIRO_PATTERN_TYPE_SOLID,
    CAIRO_PATTERN_TYPE_SURFACE,
    CAIRO_PATTERN_TYPE_LINEAR,
    CAIRO_PATTERN_TYPE_RADIAL
} cairo_pattern_type_t;

 cairo_pattern_type_t
cairo_pattern_get_type (cairo_pattern_t *pattern);

 void
cairo_pattern_add_color_stop_rgb (cairo_pattern_t *pattern,
      double offset,
      double red, double green, double blue);

 void
cairo_pattern_add_color_stop_rgba (cairo_pattern_t *pattern,
       double offset,
       double red, double green, double blue,
       double alpha);

 void
cairo_pattern_set_matrix (cairo_pattern_t *pattern,
     const cairo_matrix_t *matrix);

 void
cairo_pattern_get_matrix (cairo_pattern_t *pattern,
     cairo_matrix_t *matrix);
typedef enum _cairo_extend {
    CAIRO_EXTEND_NONE,
    CAIRO_EXTEND_REPEAT,
    CAIRO_EXTEND_REFLECT,
    CAIRO_EXTEND_PAD
} cairo_extend_t;

 void
cairo_pattern_set_extend (cairo_pattern_t *pattern, cairo_extend_t extend);

 cairo_extend_t
cairo_pattern_get_extend (cairo_pattern_t *pattern);
typedef enum _cairo_filter {
    CAIRO_FILTER_FAST,
    CAIRO_FILTER_GOOD,
    CAIRO_FILTER_BEST,
    CAIRO_FILTER_NEAREST,
    CAIRO_FILTER_BILINEAR,
    CAIRO_FILTER_GAUSSIAN
} cairo_filter_t;

 void
cairo_pattern_set_filter (cairo_pattern_t *pattern, cairo_filter_t filter);

 cairo_filter_t
cairo_pattern_get_filter (cairo_pattern_t *pattern);

 cairo_status_t
cairo_pattern_get_rgba (cairo_pattern_t *pattern,
   double *red, double *green,
   double *blue, double *alpha);

 cairo_status_t
cairo_pattern_get_surface (cairo_pattern_t *pattern,
      cairo_surface_t **surface);


 cairo_status_t
cairo_pattern_get_color_stop_rgba (cairo_pattern_t *pattern,
       int index, double *offset,
       double *red, double *green,
       double *blue, double *alpha);

 cairo_status_t
cairo_pattern_get_color_stop_count (cairo_pattern_t *pattern,
        int *count);

 cairo_status_t
cairo_pattern_get_linear_points (cairo_pattern_t *pattern,
     double *x0, double *y0,
     double *x1, double *y1);

 cairo_status_t
cairo_pattern_get_radial_circles (cairo_pattern_t *pattern,
      double *x0, double *y0, double *r0,
      double *x1, double *y1, double *r1);



 void
cairo_matrix_init (cairo_matrix_t *matrix,
     double xx, double yx,
     double xy, double yy,
     double x0, double y0);

 void
cairo_matrix_init_identity (cairo_matrix_t *matrix);

 void
cairo_matrix_init_translate (cairo_matrix_t *matrix,
        double tx, double ty);

 void
cairo_matrix_init_scale (cairo_matrix_t *matrix,
    double sx, double sy);

 void
cairo_matrix_init_rotate (cairo_matrix_t *matrix,
     double radians);

 void
cairo_matrix_translate (cairo_matrix_t *matrix, double tx, double ty);

 void
cairo_matrix_scale (cairo_matrix_t *matrix, double sx, double sy);

 void
cairo_matrix_rotate (cairo_matrix_t *matrix, double radians);

 cairo_status_t
cairo_matrix_invert (cairo_matrix_t *matrix);

 void
cairo_matrix_multiply (cairo_matrix_t *result,
         const cairo_matrix_t *a,
         const cairo_matrix_t *b);

 void
cairo_matrix_transform_distance (const cairo_matrix_t *matrix,
     double *dx, double *dy);

 void
cairo_matrix_transform_point (const cairo_matrix_t *matrix,
         double *x, double *y);


 void
cairo_debug_reset_static_data (void);




typedef struct _PangoCairoFont PangoCairoFont;
typedef struct _PangoCairoFontMap PangoCairoFontMap;




typedef void (* PangoCairoShapeRendererFunc) (cairo_t *cr,
           PangoAttrShape *attr,
           gboolean do_path,
           gpointer data);




GType pango_cairo_font_map_get_type (void) ;

PangoFontMap *pango_cairo_font_map_new (void);
PangoFontMap *pango_cairo_font_map_new_for_font_type (cairo_font_type_t fonttype);
PangoFontMap *pango_cairo_font_map_get_default (void);
void pango_cairo_font_map_set_default (PangoCairoFontMap *fontmap);
cairo_font_type_t pango_cairo_font_map_get_font_type (PangoCairoFontMap *fontmap);

void pango_cairo_font_map_set_resolution (PangoCairoFontMap *fontmap,
         double dpi);
double pango_cairo_font_map_get_resolution (PangoCairoFontMap *fontmap);

PangoContext *pango_cairo_font_map_create_context (PangoCairoFontMap *fontmap);





GType pango_cairo_font_get_type (void) ;

cairo_scaled_font_t *pango_cairo_font_get_scaled_font (PangoCairoFont *font);



void pango_cairo_update_context (cairo_t *cr,
      PangoContext *context);

void pango_cairo_context_set_font_options (PangoContext *context,
          const cairo_font_options_t *options);
const cairo_font_options_t *pango_cairo_context_get_font_options (PangoContext *context);

void pango_cairo_context_set_resolution (PangoContext *context,
          double dpi);
double pango_cairo_context_get_resolution (PangoContext *context);

void pango_cairo_context_set_shape_renderer (PangoContext *context,
            PangoCairoShapeRendererFunc func,
            gpointer data,
            GDestroyNotify dnotify);
PangoCairoShapeRendererFunc pango_cairo_context_get_shape_renderer (PangoContext *context,
            gpointer *data);



PangoContext *pango_cairo_create_context (cairo_t *cr);
PangoLayout *pango_cairo_create_layout (cairo_t *cr);
void pango_cairo_update_layout (cairo_t *cr,
     PangoLayout *layout);




void pango_cairo_show_glyph_string (cairo_t *cr,
        PangoFont *font,
        PangoGlyphString *glyphs);
void pango_cairo_show_glyph_item (cairo_t *cr,
        const char *text,
        PangoGlyphItem *glyph_item);
void pango_cairo_show_layout_line (cairo_t *cr,
        PangoLayoutLine *line);
void pango_cairo_show_layout (cairo_t *cr,
        PangoLayout *layout);

void pango_cairo_show_error_underline (cairo_t *cr,
           double x,
           double y,
           double width,
           double height);




void pango_cairo_glyph_string_path (cairo_t *cr,
        PangoFont *font,
        PangoGlyphString *glyphs);
void pango_cairo_layout_line_path (cairo_t *cr,
        PangoLayoutLine *line);
void pango_cairo_layout_path (cairo_t *cr,
        PangoLayout *layout);

void pango_cairo_error_underline_path (cairo_t *cr,
           double x,
           double y,
           double width,
           double height);


