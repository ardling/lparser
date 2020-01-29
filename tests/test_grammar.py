import lparser.lparser as gr

def test_1():
    assert (gr.lambda_expr.parse('\\var1 var2.var1')) == (['var1', 'var2'], 'var1')


def test_2():
    assert (gr.lambda_expr.parse('\\var1 var2.var2(var3 var1)')) == (['var1', 'var2'], ('var2', ['var3', 'var1']))
