all: xproto xtest render composite shape xfixes

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

shape: ../ooxcb/shape.py ../docs/source/api/shape.rst

../docs/source/api/shape.rst: shape.rst
	cp shape.rst ../docs/source/api/shape.rst

shape.rst: ../ooxcb/shape.py

../ooxcb/shape.py: shape.xml shape.i
	python ooxcb_client.py shape > ../ooxcb/shape.py

xfixes: ../ooxcb/xfixes.py ../docs/source/api/xfixes.rst

../docs/source/api/xfixes.rst: xfixes.rst
	cp xfixes.rst ../docs/source/api/xfixes.rst

xfixes.rst: ../ooxcb/xfixes.py

../ooxcb/xfixes.py: xfixes.xml xfixes.i
	python ooxcb_client.py xfixes > ../ooxcb/xfixes.py

clean:
	rm -f ../docs/source/api/{xproto,xtest,render,composite,shape,xfixes}.rst ../ooxcb/{xproto,xtest,render,composite,shape,xfixes}.py {xproto,xtest,render,composite,shape,xfixes}.rst

.phony: xproto xtest render composite shape xfixes

