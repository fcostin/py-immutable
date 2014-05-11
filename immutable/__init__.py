"""
immutable - generic functions for immutable functional programming idioms
"""


import copy


def replace(x, **kwargs):
    """
    Returns a copy of `x` that has the same attribute values as `x`,
    optionally overriding a given dict of named attributes. does not
    modify `x`.

    Intended as a generic non-mutating functional replacement for `setattr`
    aka `obj.attr = new_value` state mutation.

    Types wishing to define their own custom replace behaviour should
    implement a `_replace(self, **kwargs)` method with the semantics stated
    above.

    Notes:

        The magic method called is called `_replace` instead of
        e.g. `__replace__` because that is how `namedtuple` does it.
    """
    if hasattr(x, '_replace'):
        result = x._replace(**kwargs)
    else:
        result = _default_replace(x, kwargs)
    return result


def replace_index(x, index, value):
    """
    returns copy of `x` with `index`-th element replaced by `value`.
    """
    # assume x has a copy-constructor and can be interpreted as a list
    y = list(x)
    y[index] = value
    cctor = copy_constructor(x)
    result = cctor(y)
    return result


def copy_constructor(x):
    """
    Copy constructor of given value/object x.

    If you want to simply make a copy of `x`, do not use this, instead please
    see the `copy` module.

    Desired properties:

        if `x` has value semantics, then
            `copy_constructor(x)(x) == x`
        if `x` is mutable, then
            `copy_constructor(x)(x) is not x`

    Custom types wishing to define copy constructors should:
        1.  define a constructor, that, if called with one argument, works as a
            copy constructor
        2.  failing that, define a custom `_make` method to do the same

    Notes:
        The magic method is named `_make` instead of e.g.
        `__copy_constructor__` because that is what `namedtuple` does.
    """

    if hasattr(x, '_make'):
        # special case for namedtuples and similar types, which don't
        # support calling their constructor with a single argument
        # that is another value of the same type.
        cctor = x._make     # namedtuple case
    elif _is_old_style_class(x):
        cctor = x.__class__
    else:
        # assume new-style class
        cctor = type(x)
    return cctor


def _is_old_style_class(obj):
    # ref: https://docs.python.org/release/2.5.2/ref/node33.html
    return hasattr(obj, '__class__') and (obj.__class__ != type(obj))


def _default_replace(obj, kwargs):
    result = copy.deepcopy(obj)
    for key, value in kwargs.iteritems():
        setattr(result, key, value)
    return result
