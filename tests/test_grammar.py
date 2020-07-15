import lparser.lparser as gr


def test_expr_1():
    assert (gr.lambda_expr.parse('\\var1 var2.var1')) == (('var1', 'var2'), 'var1')


def test_expr_2():
    assert (gr.lambda_expr.parse('\\var1.\\var2.var1')) == (('var1',), (('var2',), 'var1'))


def test_application_1():
    assert (gr.application.parse('func(arg1 arg2)') ==
                              ('func', ['arg1', 'arg2']))


def test_definition_1():
    assert (gr.definition.parse('def func(arg1 arg2 arg3): arg1') == 
                                   ('func', ['arg1', 'arg2', 'arg3'], 'arg1'))


def test_definition_2():
    assert (gr.definition.parse('def func(arg1 arg2 arg3): func2(arg1 arg3)') == 
                                ('func', ['arg1', 'arg2', 'arg3'], ('func2', ['arg1', 'arg3'])))


def test_program_1():
    text = '''def func1(arg1): arg1
def f1(a): a
func1(aaa)'''
    res = (
        [
            ('func1', ['arg1'], 'arg1'),
            ('f1', ['a'], 'a')
        ],
        ('func1', ['aaa']))
    assert (gr.program.parse(text) == res)