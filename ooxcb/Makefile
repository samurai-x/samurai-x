all: xproto

xproto: ooxcb/xproto.py docs/source/api/xproto.rst 

docs/source/api/xproto.rst: xproto.rst
	cp xproto.rst docs/source/api/xproto.rst

ooxcb/xproto.py: xproto.xml xproto.i
	python ooxcb_client.py xproto > ooxcb/xproto.py

.phony: xproto
