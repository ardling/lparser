import lparser.lparser as gr
import lparser.objects as obs
import parsec
import pprint
import pytest


def test_expr_1():
    assert (gr.lambda_expr.parse('\\var1 var2.var1')) == (('var1', 'var2'), 'var1')


def test_expr_2():
    assert (gr.lambda_expr.parse('\\var1.\\var2.var1')) == (('var1',), (('var2',), 'var1'))


def test_string_1():
    assert gr.lmb_string.parse('"abc cbd"') == obs.String("abc cbd")
    assert gr.lmb_string.parse('" \n "') == obs.String(" \n ")
    with pytest.raises(parsec.ParseError):
        gr.lmb_string.parse('"abc')


def test_application_1():
    assert (gr.application.parse('func(arg1 arg2)') == obs.Application('func', ['arg1', 'arg2']))


def test_definition_1():
    print(gr.definition.parse('def func(arg1 arg2 arg3) { arg1() }\n'))
    assert (gr.definition.parse('def func(arg1 arg2 arg3) { arg1() }\n') ==
                                (obs.Application('func', ['arg1', 'arg2', 'arg3']),
                                 obs.Block(obs.Context(), obs.Application('arg1', []))))


def test_definition_2():
    assert (gr.definition.parse('def func(arg1 arg2 arg3) {func2(arg1 arg3)\n}\n') ==
                                (obs.Application('func', ['arg1', 'arg2', 'arg3']),
                                 obs.Block(obs.Context(), obs.Application('func2', ['arg1', 'arg3']))))


def test_definition_3():
    assert gr.definition.parse('def func(arg1) {"abc"}\n') == (obs.Application('func', ['arg1']),
                                                               obs.Block(obs.Context(), obs.String("abc")))


def test_program_1():
    text = '''def func1(arg1){arg1()}
def f1(a){a()}
func1(aaa)'''
    res = gr.program.parse(text)
    assert res == obs.Block(
        obs.Context([(obs.Application('func1', ['arg1']),
                      obs.Block(obs.Context(),
                                obs.Application('arg1', []))),
                     (obs.Application('f1', ['a']),
                       obs.Block(obs.Context(),
                                 obs.Application('a', [])))
                    ]),
        obs.Application('func1', ['aaa'])
    )


program_text_1 = '''
def func1(arg1){arg1()}

 def f1(a){a()}


func1(aaa)
'''

def test_program_2():
    res = gr.program.parse(program_text_1)
    assert res == obs.Block(
        obs.Context([(obs.Application('func1', ['arg1']),
                      obs.Block(obs.Context(),
                                obs.Application('arg1', []))),
                     (obs.Application('f1', ['a']),
                       obs.Block(obs.Context(),
                                 obs.Application('a', [])))
                    ]),
        obs.Application('func1', ['aaa'])
    )
