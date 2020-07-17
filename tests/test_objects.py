from pprint import pprint
import lparser.lparser as lp


program_text_1 = '''
def func1(arg1) {arg1()}
def f1(a) {a()}
def b() {
    def f2() {abc()}
    f2()
}
def abc() {"abc"}
def aaa() {f1(b)}
func1(aaa)
'''


def test_program_1():
    prog = lp.parse(program_text_1)
    pprint(prog)
    pprint('Exec')
    pprint(prog.exec())
    assert prog.exec() == 'abc'



def test_program_2():
    text = '''
    def a() {"result"}
    def b() {a()}
    b()'''
    res = lp.parse(text)
    assert res.exec() == 'result'


def test_program_3():
    text = '''
    def a() {"a"}
    def b() {"b"}
    def c(a) {a()}
    c(b)'''
    res = lp.parse(text)
    assert res.exec() == 'b'


def test_program_4():
    text = '''
    def a() {"a"}
    def b() {"b"}
    def c(g) {a()}
    c(b)'''
    res = lp.parse(text)
    assert res.exec() == 'a'