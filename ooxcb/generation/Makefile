all: xproto xtest render composite

xproto: ../ooxcb/xproto.py ../docs/source/api/xproto.rst

../docs/source/api/xproto.rst: xproto.rst
	cp xproto.rst ../docs/source/api/xproto.rst

xproto.rst: ../ooxcb/xproto.py

../ooxcb/xproto.py: xproto.xml xproto.i
	python ooxcb_client.py xproto > ../ooxcb/xproto.py

xtest: ../ooxcb/xtest.py ../docs/source/api/xtest.rst

../docs/source/api/xtest.rst: xtest.rst
	cp xtest.rst ../docs/source/api/xtest.rst

xtest.rst: ../ooxcb/xtest.py

../ooxcb/xtest.py: xtest.xml xtest.i
	python ooxcb_client.py xtest > ../ooxcb/xtest.py

render: ../ooxcb/render.py ../docs/source/api/render.rst

../docs/source/api/render.rst: render.rst
	cp render.rst ../docs/source/api/render.rst

render.rst: ../ooxcb/render.py

../ooxcb/render.py: render.xml render.i
	python ooxcb_client.py render > ../ooxcb/render.py

composite: ../ooxcb/composite.py ../docs/source/api/composite.rst

../docs/source/api/composite.rst: composite.rst
	cp composite.rst ../docs/source/api/composite.rst

composite.rst: ../ooxcb/composite.py

../ooxcb/composite.py: composite.xml composite.i
	python ooxcb_client.py composite > ../ooxcb/composite.py

clean:
	rm -f ../docs/source/api/{xproto,xtest,render,composite}.rst ../ooxcb/{xproto,xtest,render,composite}.py {xproto,xtest,render,composite}.rst

.phony: xproto xtest render composite

