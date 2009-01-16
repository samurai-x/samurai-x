#!/bin/sh
./ooxcb_client.py > ooxcb/xproto.py
patch -p1 -i configure.patch
