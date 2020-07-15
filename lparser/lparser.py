#!/usr/bin/env python3

import parsec as ps

lmb_spaces = ps.regex(r'\s*')  # any number of spaces

variable = ps.regex(r'[_a-zA-Z][_a-zA-Z1-9]*')
lmb_none = ps.string('')


@ps.generate
def app():
    '''application: a(b c d)'''
    func = yield variable
    yield ps.string('(')
    args = yield ps.sepBy(variable, lmb_spaces)
    yield ps.string(')')
    return func, tuple(args)

# lambda_expr = ps.string('\\') >> ps.string('.')

lambda_body = app ^ variable


@ps.generate
def lambda_expr():
    '''expression: \a b.b a'''
    yield ps.string('\\')
    vals = yield ps.sepBy(variable, lmb_spaces)
    yield ps.string('.')
    body = yield lambda_body
    return tuple(vals), body


def main():
    pass


if __name__ == '__main__':
    main()
