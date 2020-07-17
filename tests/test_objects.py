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