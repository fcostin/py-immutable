from immutable import (replace, replace_index)
import collections


def test_replace_works_for_namedtuples():

    T = collections.namedtuple('T', ['foo'])

    x = T(foo=123)
    y = replace(x, foo=456)
    assert type(y) == type(x)
    assert y.foo == 456


def test_replace_works_for_old_style_classes():

    class T:
        def __init__(self, foo):
            self.foo = foo

    x = T(foo=123)
    y = replace(x, foo=456)

    # it was a copy
    assert y is not x

    # input unmodified
    assert x.__class__ == T
    assert x.foo == 123

    # output as desired
    assert y.__class__ == T
    assert y.foo == 456


def test_replace_works_for_new_style_classes():

    class T(object):
        def __init__(self, foo):
            self.foo = foo

    x = T(foo=123)
    y = replace(x, foo=456)

    # it was a copy
    assert y is not x

    # input unmodified
    assert type(x) == T
    assert x.foo == 123

    # output as desired
    assert type(y) == T
    assert y.foo == 456


def test_replace_uses_replace_magic_method_if_present():

    p_call_counter = [0]

    class T(object):
        def __init__(self, foo):
            self.foo = foo

        def _replace(self, **kwargs):
            p_call_counter[0] += 1
            # in practice, you might want to use a custom replace method to
            # use super-optimized replacement logic, or perform horrible
            # long range side effects, or something.
            return T(**kwargs)

    x = T(foo=123)
    y = replace(x, foo=456)

    # assert custom __replace__ method was called
    assert p_call_counter[0] == 1

    # it was a copy
    assert y is not x

    # input unmodified
    assert type(x) == T
    assert x.foo == 123

    # output as desired
    assert type(y) == T
    assert y.foo == 456


def test_replace_by_index_works_for_namedtuples():

    T = collections.namedtuple('T', ['foo', 'barr'])

    x = T(foo=123, barr=456)
    y = replace_index(x, 1, 654)
    assert type(y) == type(x)
    assert y == T(foo=123, barr=654)


def test_replace_by_index_works_for_tuples():
    x = (1, 2, 3)
    y = replace_index(x, -1, 'coconut')
    assert type(y) == type(x)
    assert y == (1, 2, 'coconut')


def test_replace_by_index_works_for_lists():
    x = ['a', 'b', 'c', 'd', '!']
    y = replace_index(x, -3, 'raca')
    z = replace_index(y, 4, 'abra!')
    assert type(z) == type(y) == type(x)
    assert z == ['a', 'b', 'raca', 'd', 'abra!']


def test_replace_by_index_works_for_new_style_classes():

    class T(object):
        def __init__(self, iterable):
            self._guts = iterable

        def __iter__(self):
            return iter(self._guts)

    arg = [1, 2, 3]
    x = T(arg)
    y = replace_index(x, -1, 'coconut')

    # it was a copy
    assert x is not y

    # input unmodified
    assert type(x) == T
    assert x._guts == [1, 2, 3]
    assert x._guts is arg

    # output as desired
    assert type(y) == T
    assert y._guts == [1, 2, 'coconut']
    assert y._guts is not arg


def test_replace_by_index_works_for_old_style_classes():

    class T:
        def __init__(self, iterable):
            self._guts = iterable

        def __iter__(self):
            return iter(self._guts)

    arg = [1, 2, 3]
    x = T(arg)
    y = replace_index(x, -1, 'coconut')

    # it was a copy
    assert x is not y

    # input unmodified
    assert x.__class__ == T
    assert x._guts == [1, 2, 3]
    assert x._guts is arg

    # output as desired
    assert y.__class__ == T
    assert y._guts == [1, 2, 'coconut']
    assert y._guts is not arg
