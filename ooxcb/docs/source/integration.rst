Integration
===========

... with pygtk
--------------

That's the minimal skeleton to integrate ooxcb into the gobject mainloop::

    import sys
    sys.path.append('..')

    import ooxcb
    from ooxcb import xproto

    import gtk
    import gobject

    def ooxcb_callback(source, cb_condition, connection):
        while True:
            if not connection.alive: # `if connection.conn:` for ooxcb 1.0
                break
            evt = connection.poll_for_event()
            if evt is None:
                break
            evt.dispatch()
        # return True so that the callback will be called again.
        return True

    conn = ooxcb.connect()
    # That's the important line. It makes gobject call `ooxcb_callback`
    # when data is available.
    gobject.io_add_watch(
            conn.get_file_descriptor(),
            gobject.IO_IN,
            ooxcb_callback,
            conn)

    gtk.main()


... to be continued ...
