import lparser.lparser as gr

import pprint
import logging
import functools


log = logging.getLogger(__name__)


def mlog(func):
    @functools.wraps(func)
    def __new(*args, **kwargs):
        log.error('%s\n%s\n%s', func.__qualname__, pprint.pformat(args[1:]), kwargs)
        return func(*args, **kwargs)

    return __new


class Context:
    def __init__(self, defs=()):
        log.error(defs)
        self.defs = {a.func_name: Function(a.args, b) for a, b in defs}

    def __repr__(self):
        return f'<Context {pprint.pformat(self.defs)}>'

    def __eq__(self, other):
        return (type(self) == type(other)) and (self.defs == other.defs)

    def __getitem__(self, key):
        try:
            return self.defs[key]
        except KeyError:
            raise KeyError(f'No element "{key}" in context')

    def update(self, context, args):
        new = Context()
        new.defs.update(context.defs)
        new.defs.update(self.defs)
        new.defs.update(args)
        return new


class Function():
    def __init__(self, args, block):
        self.args = args
        self.block = block

    def __repr__(self):
        return (f'<Function {self.args} -> {self.block}')

    def __eq__(self, other):
        return (type(other) == type(self)) and (self.args == other.args) and (self.block == self.block)

    def exec(self, context):
        # args = {self.args[i]: val for i, val in enumerate(args)}
        # log.error('Func exec: (%s)', pprint.pformat(args))

        return self.block.exec(context)


class Application:
    def __init__(self, func_name, args):
        self.func_name = func_name
        self.args = args

    def __repr__(self):
        return f'<Application {self.func_name}{self.args}>'

    def __eq__(self, other):
        return (type(other) == type(self)) and (self.func_name == other.func_name) and (self.args == other.args)

    # @mlog
    def exec(self, context):
        log.error('Exec %s(%s)', self.func_name, ' '.join(self.args))

        func = context[self.func_name]
        args = {func.args[i]: context[a] for i, a in enumerate(self.args)}
        lcontext = context.update(Context(), args)

        return func.exec(lcontext)


class Block:
    def __init__(self, context, app):
        self.context = context
        self.app = app

    def __repr__(self):
        return f'<Block {self.app} {pprint.pformat(self.context)}>'

    def __eq__(self, other):
        return (type(other) == type(self)) and (self.context == other.context) and (self.app == other.app)

    def exec(self, context=Context()):
        new = context.update(Context(), self.context.defs)
        return self.app.exec(new)


class String:
    def __init__(self, val):
        self._str = val

    def __repr__(self):
        return f'String({self._str})'

    def __eq__(self, other):
        return self._str == other._str

    def exec(self, _):
        return self._str
