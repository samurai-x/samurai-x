# Copyright (c) 2008-2009, samurai-x.org
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the samurai-x.org nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SAMURAI-X.ORG ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL SAMURAI-X.ORG  BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
    This module contains some helper functions for the icccm standard.
"""

from ooxcb.xproto import Window

class WMState(object):
    """
        container class for the WM_STATE property.

        .. attribute:: state

            one member of :class:`ooxcb.xproto.WMState`

        .. attribute:: icon
            
            The icon window, either a :class:`ooxcb.xproto.Window` instance
            or None.
    """
    def __init__(self, state, icon):
        self.state = state
        self.icon = icon

def icccm_get_wm_state(window):
    """
        return a :class:`WMState` instance or None if
        there is no `WM_STATE` property.
    """
    prop = window.get_property('WM_STATE', 'CARDINAL').reply()
    if not prop.exists:
        return None
    else:
        icon = None
        if prop.value[1]:
            prop = window.conn.get_from_cache_fallback(prop.value[1], Window)
        return WMState(prop.value[0], icon)

def mixin():
    from ooxcb.util import mixin_functions
    mixin_functions((
        icccm_get_wm_state,
        ), Window)

