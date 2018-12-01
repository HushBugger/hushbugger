"""A silent alternative to debugging."""

import functools
import random
import sys

__all__ = ["Dummy", "hush"]


class Dummy(object):
    """A Dummy responds to almost everything, usually by returning itself.

    In its repr, it will cleverly pretend to be a mysteriously named object
    from another module.
    """

    def __init__(self, module=random.choice(list(sys.modules))):
        self.__module__ = module

    def __repr__(self):
        return "<{}.Coalescer object at {:#x}>".format(self.__module__, id(self))

    __str__ = __repr__

    def __next__(self):
        if random.random() < 0.05:
            raise StopIteration
        return self

    next = __next__

    def __coerce__(self, other):
        return self, self

    def __int__(self):
        return 4

    __long__ = __int__

    def __float__(self):
        return 4.1

    def __len__(self):
        return 13

    def __hash__(self):
        return id(self)


def _return_self(self, *args, **kwargs):
    return self


def _return_true(self, *args, **kwargs):
    return True


for method in (
    "call getattr delattr getitem setitem delitem enter exit "
    "iter add radd abs and concat floordiv iadd iand "
    "iconcat ifloordiv ilshift imatmul imod imul index inv "
    "invert ior ipow irshift isub itruediv ixor lshift matmul "
    "mod mul ne neg or pos pow rshift sub truediv xor radd "
    "rsub rmul rmatmul rtruediv rfloordiv rmod rdivmod rpow "
    "rlshift rrshift rand rxor ror"
).split():
    setattr(Dummy, "__" + method + "__", _return_self)

for method in "contains eq ge gt le lt not bool nonzero".split():
    setattr(Dummy, "__" + method + "__", _return_true)


def hush(func):
    """A decorator to pretend that a function never fails."""

    @functools.wraps(func)
    def decorated(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if sys.version_info < (3,):
                # Inspectable disassembly isn't available in Python 2
                return Dummy()

            import dis

            traceback = e.__traceback__
            if traceback.tb_next is None:
                return Dummy()
            frame = traceback.tb_next.tb_frame
            prev = None
            for instruction in dis.get_instructions(frame.f_code):
                if instruction.opname == "RETURN_VALUE" and prev is not None:
                    if prev.opname == "LOAD_CONST":
                        return prev.argval
                    elif prev.opname in {"LOAD_FAST", "LOAD_GLOBAL", "LOAD_DEREF"}:
                        for scope in frame.f_locals, frame.f_globals, frame.f_builtins:
                            if prev.argval in scope:
                                return scope[prev.argval]
                prev = instruction
            return Dummy()

    return decorated
