from . import keysymdef
from .util import cached_property

NO_SYMBOL = 0

def convert_case(sym):
    """ return lower, upper """
    lower = sym
    upper = sym

#    switch(sym >> 8)
#    {
    def latin1():
        if ((sym >= keysymdef.XK_A) and (sym <= keysymdef.XK_Z)):
            lower += (keysymdef.XK_a - keysymdef.XK_A)
        elif ((sym >= keysymdef.XK_a) and (sym <= keysymdef.XK_z)):
            upper -= (keysymdef.XK_a - keysymdef.XK_A)
        elif ((sym >= keysymdef.XK_Agrave) and (sym <= keysymdef.XK_Odiaeresis)):
            lower += (keysymdef.XK_agrave - keysymdef.XK_Agrave)
        elif ((sym >= keysymdef.XK_agrave) and (sym <= keysymdef.XK_odiaeresis)):
            upper -= (keysymdef.XK_agrave - keysymdef.XK_Agrave)
        elif ((sym >= keysymdef.XK_Ooblique) and (sym <= keysymdef.XK_Thorn)):
            lower += (keysymdef.XK_oslash - keysymdef.XK_Ooblique)
        elif ((sym >= keysymdef.XK_oslash) and (sym <= keysymdef.XK_thorn)):
            upper -= (keysymdef.XK_oslash - keysymdef.XK_Ooblique)
        
    def latin2():
        # Assume the KeySym is a legal value (ignore discontinuities)
        if (sym == keysymdef.XK_Aogonek):
            lower = keysymdef.XK_aogonek
        elif (sym >= keysymdef.XK_Lstroke and sym <= keysymdef.XK_Sacute):
            lower += (keysymdef.XK_lstroke - keysymdef.XK_Lstroke)
        elif (sym >= keysymdef.XK_Scaron and sym <= keysymdef.XK_Zacute):
            lower += (keysymdef.XK_scaron - keysymdef.XK_Scaron)
        elif (sym >= keysymdef.XK_Zcaron and sym <= keysymdef.XK_Zabovedot):
            lower += (keysymdef.XK_zcaron - keysymdef.XK_Zcaron)
        elif (sym == keysymdef.XK_aogonek):
            upper = keysymdef.XK_Aogonek
        elif (sym >= keysymdef.XK_lstroke and sym <= keysymdef.XK_sacute):
            upper -= (keysymdef.XK_lstroke - keysymdef.XK_Lstroke)
        elif (sym >= keysymdef.XK_scaron and sym <= keysymdef.XK_zacute):
            upper -= (keysymdef.XK_scaron - keysymdef.XK_Scaron)
        elif (sym >= keysymdef.XK_zcaron and sym <= keysymdef.XK_zabovedot):
            upper -= (keysymdef.XK_zcaron - keysymdef.XK_Zcaron)
        elif (sym >= keysymdef.XK_Racute and sym <= keysymdef.XK_Tcedilla):
            lower += (keysymdef.XK_racute - keysymdef.XK_Racute)
        elif (sym >= keysymdef.XK_racute and sym <= keysymdef.XK_tcedilla):
            upper -= (keysymdef.XK_racute - keysymdef.XK_Racute)

    def latin3():
        # Assume the KeySym is a legal value (ignore discontinuities)
        if (sym >= keysymdef.XK_Hstroke and sym <= keysymdef.XK_Hcircumflex):
            lower += (keysymdef.XK_hstroke - keysymdef.XK_Hstroke)
        elif (sym >= keysymdef.XK_Gbreve and sym <= keysymdef.XK_Jcircumflex):
            lower += (keysymdef.XK_gbreve - keysymdef.XK_Gbreve)
        elif (sym >= keysymdef.XK_hstroke and sym <= keysymdef.XK_hcircumflex):
            upper -= (keysymdef.XK_hstroke - keysymdef.XK_Hstroke)
        elif (sym >= keysymdef.XK_gbreve and sym <= keysymdef.XK_jcircumflex):
            upper -= (keysymdef.XK_gbreve - keysymdef.XK_Gbreve)
        elif (sym >= keysymdef.XK_Cabovedot and sym <= keysymdef.XK_Scircumflex):
            lower += (keysymdef.XK_cabovedot - keysymdef.XK_Cabovedot)
        elif (sym >= keysymdef.XK_cabovedot and sym <= keysymdef.XK_scircumflex):
            upper -= (keysymdef.XK_cabovedot - keysymdef.XK_Cabovedot)
        
    def latin4():
        # Assume the KeySym is a legal value (ignore discontinuities)
        if (sym >= keysymdef.XK_Rcedilla and sym <= keysymdef.XK_Tslash):
            lower += (keysymdef.XK_rcedilla - keysymdef.XK_Rcedilla)
        elif (sym >= keysymdef.XK_rcedilla and sym <= keysymdef.XK_tslash):
            upper -= (keysymdef.XK_rcedilla - keysymdef.XK_Rcedilla)
        elif (sym == keysymdef.XK_ENG):
            lower = keysymdef.XK_eng
        elif (sym == keysymdef.XK_eng):
            upper = keysymdef.XK_ENG
        elif (sym >= keysymdef.XK_Amacron and sym <= keysymdef.XK_Umacron):
            lower += (keysymdef.XK_amacron - keysymdef.XK_Amacron)
        elif (sym >= keysymdef.XK_amacron and sym <= keysymdef.XK_umacron):
            upper -= (keysymdef.XK_amacron - keysymdef.XK_Amacron)

    def cyrillic():
        # Assume the KeySym is a legal value (ignore discontinuities)
        if (sym >= keysymdef.XK_Serbian_DJE and sym <= keysymdef.XK_Serbian_DZE):
            lower -= (keysymdef.XK_Serbian_DJE - keysymdef.XK_Serbian_dje)
        elif (sym >= keysymdef.XK_Serbian_dje and sym <= keysymdef.XK_Serbian_dze):
            upper += (keysymdef.XK_Serbian_DJE - keysymdef.XK_Serbian_dje)
        elif (sym >= keysymdef.XK_Cyrillic_YU and sym <= keysymdef.XK_Cyrillic_HARDSIGN):
            lower -= (keysymdef.XK_Cyrillic_YU - keysymdef.XK_Cyrillic_yu)
        elif (sym >= keysymdef.XK_Cyrillic_yu and sym <= keysymdef.XK_Cyrillic_hardsign):
            upper += (keysymdef.XK_Cyrillic_YU - keysymdef.XK_Cyrillic_yu)
    
    def greek():
        if (sym >= keysymdef.XK_Greek_ALPHAaccent and sym <= keysymdef.XK_Greek_OMEGAaccent):
            lower += (keysymdef.XK_Greek_alphaaccent - keysymdef.XK_Greek_ALPHAaccent)
        elif (sym >= keysymdef.XK_Greek_alphaaccent and sym <= keysymdef.XK_Greek_omegaaccent and
            sym != keysymdef.XK_Greek_iotaaccentdieresis and
            sym != keysymdef.XK_Greek_upsilonaccentdieresis):
            upper -= (keysymdef.XK_Greek_alphaaccent - keysymdef.XK_Greek_ALPHAaccent)
        elif (sym >= keysymdef.XK_Greek_ALPHA and sym <= keysymdef.XK_Greek_OMEGA):
            lower += (keysymdef.XK_Greek_alpha - keysymdef.XK_Greek_ALPHA)
        elif (sym >= keysymdef.XK_Greek_alpha and sym <= keysymdef.XK_Greek_omega and
                sym != keysymdef.XK_Greek_finalsmallsigma):
            upper -= (keysymdef.XK_Greek_alpha - keysymdef.XK_Greek_ALPHA)
        
    def armenian(): 
        if (sym >= keysymdef.XK_Armenian_AYB and sym <= keysymdef.XK_Armenian_fe):
            lower = sym | 1
            upper = sym & ~1

    encmap = {0: latin1,
            1: latin2,
            2: latin3,
            3: latin4,
            6: cyrillic,
            7: greek,
            0x14: armenian}
    try:
        encmap[sym >> 8]()
    except KeyError:
        pass
    return lower, upper


class Keysyms(object):
    """
        a simple helper for keycodes and keysyms.

        :todo: wrap `xcb-keysmys` from xcb-util?
    """
    def __init__(self, conn):
        self.conn = conn
        
    @cached_property
    def _cookie(self):
        min_keycode = self.conn.get_setup().min_keycode
        max_keycode = self.conn.get_setup().max_keycode
        return self.conn.xproto.get_keyboard_mapping(
                min_keycode,
                max_keycode - min_keycode + 1)

    @cached_property
    def _reply(self):
        return self._cookie.reply()

    def get_keycode(self, keysym):
        """
            return the corresponding keycode for `keysym` or None.
        """
        for j in xrange(self._reply.keysyms_per_keycode):
            for keycode in xrange(self.conn.get_setup().min_keycode, 
                    self.conn.get_setup().max_keycode):

                if self.get_keysym(keycode, j) == keysym:
                    return keycode
        return None

    def get_keysym(self, keycode, col):
        keysyms = self._reply.keysyms
        min_keycode = self.conn.get_setup().min_keycode
        max_keycode = self.conn.get_setup().max_keycode
        per = self._reply.keysyms_per_keycode

        #ptr = (keycode - min_keycode) * per
        keysyms = keysyms[(keycode - min_keycode) * per:]
        # TODO: error checking
        if col < 4:
            if col > 1:
                while (per > 2 and keysyms[per - 1] == NO_SYMBOL):
                    per -= 1
                if per < 3:
                    col -= 2
            if (per < (col|1) or keysyms[col | 1] == NO_SYMBOL):
                lsym, usym = convert_case(keysyms[col & ~1])
                if not col & 1:
                    return lsym
                elif lsym == usym:
                    return 0
                else:
                    return usym
        return keysyms[col]

X_KEYS = ['Home', 'Left', 'Up', 'Right', 'Down', 'Page_Up',
          'Page_Down', 'End', 'Begin', 'BackSpace',
          'Return', 'Escape', 'KP_Enter'] + \
         ['F%d' % i for i in range(1, 36)]

def keysym_to_str(keysym):
    """
        convert a keysym to its equivalent character and return it.
        Should work for most keys.

        Ported from awesome's keygrabber.c:keysym_to_str
    """
    # first, check the X keys
    for xkey in X_KEYS:
        if keysym == getattr(keysymdef, 'XK_%s' % xkey):
            return xkey
    # then check KP_Space
    if keysym == keysymdef.XK_KP_Space:
        return ' '
    # then check the hyphen
    elif keysym == keysymdef.XK_hyphen:
        return '-'
    # it must be a char, return it
    return chr(keysym & 0x7F)
