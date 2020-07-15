#!/usr/bin/env python3

import parsec as ps

lmb_spaces = ps.regex(r'\s*')  # any number of spaces

variable = ps.regex(r'[_a-zA-Z][_a-zA-Z1-9]*')
lmb_none = ps.string('')


# lambda_expr = ps.string('\\') >> ps.string('.')

@ps.generate
def lambda_expr():
    '''expression: \a b.b a'''
    yield ps.string('\\')
    vals = yield ps.sepBy(variable, lmb_spaces)
    yield ps.string('.')

    # body is expr (\a.\b.a b) or variable (\a. a)
    body = yield lambda_expr ^ variable
    return tuple(vals), body


@ps.generate
def definition():
    '''def func_name(arg1 arg2 arg3): arg1'''
    yield ps.string('def ')
    func_name = yield variable
    yield ps.string('(')
    args = yield ps.sepBy(variable, lmb_spaces)
    yield ps.string('):')
    yield lmb_spaces
    var = yield variable
    return func_name, args, var


def main():
    pass


if __name__ == '__main__':
    main()
