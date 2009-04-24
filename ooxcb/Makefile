all: xproto xtest

xproto: ooxcb/xproto.py docs/source/api/xproto.rst

xtest: ooxcb/xtest.py docs/source/api/xtest.rst

docs/source/api/xproto.rst: xproto.rst
	cp xproto.rst docs/source/api/xproto.rst

ooxcb/xproto.py: xproto.xml xproto.i
	python ooxcb_client.py xproto > ooxcb/xproto.py

docs/source/api/xtest.rst: xtest.rst
	cp xtest.rst docs/source/api/xtest.rst

ooxcb/xtest.py: xtest.xml xtest.i
	python ooxcb_client.py xtest > ooxcb/xtest.py

clean:
	rm -f docs/source/api/{xproto,xtest}.rst ooxcb/{xproto,xtest}.py

.phony: xproto xtest clean
