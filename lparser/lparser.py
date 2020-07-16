#!/usr/bin/env python3

import parsec as ps

lmb_newlines = ps.regex(r'\s*\n\s*', ps.re.MULTILINE)  # new line and spaces
lmb_spaces = ps.regex(r'\s*', ps.re.MULTILINE)  # any number of spaces

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
def arguments():
    yield ps.string('(')
    args = yield ps.sepBy(variable, lmb_spaces)
    yield ps.string(')')
    return args

@ps.generate
def definition():
    '''def func_name(arg1 arg2 arg3): arg1'''
    yield ps.string('def ')
    func_name = yield variable
    args = yield arguments
    yield ps.string(':')
    yield lmb_spaces
    var = yield application ^ variable
    yield lmb_newlines
    return func_name, args, var

@ps.generate
def application():
    '''func(arg1 arg2)'''
    func_name = yield variable
    args = yield arguments
    return func_name, args


@ps.generate
def program():
    yield lmb_spaces
    print("----")
    #defs = yield ps.sepEndBy1(definition, lmb_newlines)
    defs = yield ps.many(definition)
    print("defs")
    app = yield application
    yield lmb_spaces
    return defs, app


def main():
    pass


if __name__ == '__main__':
    main()
