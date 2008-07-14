from pyglet.window.xlib import xlib 
from ctypes import POINTER

xlib.XModifierKeymap_p = POINTER(xlib.XModifierKeymap)
xlib.Window_p = POINTER(xlib.Window)
xlib.RevertToPointerRoot = xlib.PointerRoot

BUTTONMASK = (xlib.ButtonPressMask | xlib.ButtonReleaseMask)
MOUSEMASK = (xlib.ButtonPressMask | xlib.ButtonReleaseMask | xlib.PointerMotionMask)
def CLEANMASK(mask):
     return (mask & ~(xlib.NumLockMask | xlib.LockMask))

