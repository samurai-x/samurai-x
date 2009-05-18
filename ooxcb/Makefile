all: xproto xtest render

xproto: ooxcb/xproto.py docs/source/api/xproto.rst

xtest: ooxcb/xtest.py docs/source/api/xtest.rst

render: ooxcb/render.py docs/source/api/render.rst

docs/source/api/xproto.rst: xproto.rst
	cp xproto.rst docs/source/api/xproto.rst

ooxcb/xproto.py: xproto.xml xproto.i
	python ooxcb_client.py xproto > ooxcb/xproto.py

docs/source/api/xtest.rst: xtest.rst
	cp xtest.rst docs/source/api/xtest.rst

ooxcb/xtest.py: xtest.xml xtest.i
	python ooxcb_client.py xtest > ooxcb/xtest.py

docs/source/api/render.rst: render.rst
	cp render.rst docs/source/api/render.rst

ooxcb/render.py: render.xml render.i
	python ooxcb_client.py render > ooxcb/render.py

clean:
	rm -f docs/source/api/{xproto,xtest,render}.rst ooxcb/{xproto,xtest,render}.py

.phony: xproto xtest clean
