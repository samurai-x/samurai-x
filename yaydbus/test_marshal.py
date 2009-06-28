# -*- coding: utf-8 -*-

import py.test

from yaydbus import marshal

def _correct(signature, data, result=None):
    if result is None:
        result = data
    sig = marshal.parse_signature(signature)
    assert sig.unmarshal_simple(sig.marshal_simple(data)) == result

def _dbuscode(signature):
    assert marshal.parse_signature(signature).dbuscode == signature

def test_marshal():
    # Testing the parser ...
    assert marshal.parse_signature('()')
    assert marshal.parse_signature('a{ii}')
    _dbuscode('a{iai}')
    _dbuscode('()')
    _dbuscode('(((((((((((((())))))))))))))')
    _dbuscode('aidaidadiaiaiaiaisdd')
    _dbuscode('yyyy(yyy(yy)yy)yyyyy(yy)a{i(xx)}')
    # Some invalid signatures ...
    py.test.raises(marshal.MarshallingError, marshal.parse_signature, '{}')
    py.test.raises(marshal.MarshallingError, marshal.parse_signature, 'a{}')
    py.test.raises(marshal.MarshallingError, marshal.parse_signature, 'a{()i}')
    py.test.raises(marshal.MarshallingError, marshal.parse_signature, 'a{sii}')
    # Testing the marshaller / unmarshaller
    _correct('yyy', (1, 2, 3))
    _correct('ai', ([3333, 6666, 9999, 63333, 66666, 99999],))
    _correct('(is)', ((65535, 'Hey Guys!'),))
    _correct('a(is)', ([(65535, 'Hey Guys!'), (123, 'Blah'), (51451, 'Blubb')],))
    _correct('aai', ([[1, 2, 3], [4, 5, 6]],))
    _correct('sss', ('I', 'like', 'cookies!'))
    _correct('yay', (123, []))
    _correct('yas', (123, ['Just', 'some', 'stupid', 'stuff']))
    _correct('(((((y)y)y)y)y)', ((((((1,), 2,), 3,), 4,), 5),))
    _correct('a{ss}', ([('Key', 'Value'), ('bla', 'Blubb')],))
    _correct('a{ss}', ({'Hey!': 'Ho.'}.items(),))
    _correct('s', (u'öößßµµ',))
    # fun with variant
    _correct('v', (('s', 'heyho'),), ('heyho',))
    _correct('v', (('(yy)', (1, 2)),), ((1, 2),))
