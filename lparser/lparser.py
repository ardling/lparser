#!/usr/bin/env python3

import lparser.objects as obs

import parsec as ps


lmb_newlines = ps.regex(r'\s*\n\s*', ps.re.MULTILINE)  # new line and spaces
lmb_spaces = ps.regex(r'\s*', ps.re.MULTILINE)  # any number of spaces

variable = ps.regex(r'[_a-zA-Z][_a-zA-Z1-9]*')
lmb_none = ps.string('')


@ps.generate
def lmb_string():
    yield ps.string('"')
    string = yield ps.many(ps.none_of('"'))
    yield ps.string('"')
    return obs.String(''.join(string))


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
def block():
    '''{st1 \nst2 \nst3}'''
    yield ps.string('{')
    yield lmb_spaces
    defs = yield ps.many(definition)
    val = yield lmb_value
    yield lmb_spaces
    yield ps.string('}')
    return obs.Block(obs.Context(defs), val)


@ps.generate
def arguments():
    '''(a b c)'''
    yield ps.string('(')
    args = yield ps.sepBy(variable, lmb_spaces)
    yield ps.string(')')
    return args


@ps.generate
def application():
    '''func(arg1 arg2)'''
    func_name = yield variable
    args = yield arguments
    return obs.Application(func_name, args)


@ps.generate
def definition():
    '''def func_name(arg1 arg2 arg3): {block}'''
    yield ps.string('def ')
    app = yield application
    yield lmb_spaces
    var = yield block
    yield lmb_newlines
    return app, var


lmb_value = lmb_string ^ application ^ variable


@ps.generate
def program():
    yield lmb_spaces
    defs = yield ps.many(definition)
    app = yield application
    yield lmb_spaces
    return obs.Block(obs.Context(defs), app)


def parse(text):
    return program.parse(text)