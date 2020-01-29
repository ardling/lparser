#!/usr/bin/env python3

import parsec as ps


lmb_spaces = ps.regex(r'\s*')

variable = ps.regex(r'[_a-zA-Z][_a-zA-Z1-9]*')
lmb_none = ps.string('')


@ps.generate
def app():
    func = yield variable
    yield ps.string('(')
    args = yield ps.sepBy(variable, lmb_spaces)
    yield ps.string(')')
    return (func, args)

# lambda_expr = ps.string('\\') >> ps.string('.')

lambda_body = app ^ variable

@ps.generate
def lambda_expr():
    yield ps.string('\\')
    vals = yield ps.sepBy(variable, lmb_spaces)
    yield ps.string('.')
    body = yield lambda_body
    return vals, body


def main():
    pass


if __name__ == '__main__':
    main()
