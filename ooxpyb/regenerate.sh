#!/bin/sh
cd generator
cp /usr/share/xcb/xproto.xml .
python oowrap.py xproto.i > ../ooxcb/xproto.py
