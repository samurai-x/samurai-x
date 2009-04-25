ooxcb.xtest
===========

.. module:: ooxcb.xtest

.. class:: GetVersionReply

    .. method:: __init__(self, conn)


    .. attribute:: major_version

    .. attribute:: minor_version

.. class:: xtestExtension

    .. data:: header


    .. method:: get_version(self, major_version, minor_version)


    .. method:: get_version_unchecked(self, major_version, minor_version)


    .. method:: compare_cursor(self, window, cursor)


    .. method:: compare_cursor_unchecked(self, window, cursor)


    .. method:: fake_input_checked(self, type, detail=0, time=0, window=XNone, rootX=0, rootY=0, deviceid=0)


    .. method:: fake_input(self, type, detail=0, time=0, window=XNone, rootX=0, rootY=0, deviceid=0)


    .. method:: grab_control_checked(self, impervious)


    .. method:: grab_control(self, impervious)


.. class:: CompareCursorReply

    .. method:: __init__(self, conn)


    .. attribute:: same

.. class:: CompareCursorCookie

.. class:: Cursor

    .. data:: _None


    .. data:: Current


.. class:: GetVersionCookie

