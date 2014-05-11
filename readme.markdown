immutable
=========

generic functions to support immutable functional programming idioms

[![Build Status](https://travis-ci.org/fcostin/immutable.png)](https://travis-ci.org/fcostin/immutable)


### motivation

*   state makes things harder to reason about.
*   most of the time you don't need state, values work fine.

### nomenclature

*   by "value" we mean an immutable value, i.e., a value is something that doesn't change

### suggestions

*   prefer values (ie immutable values) over mutable objects
*   prefer functions over methods
*   prefer namespaces of related functions (in modules) over classes
*   prefer treating a non-value as if it were a value
*   prefer namedtuples over tuples (readability)
*   prefer pure functions over side-effecting functions

These are merely suggestions, not blanket rules.

### refactoring patterns:

*   smell: object has mutable state

    +   factor out state into value type T
    +   methods can now be functions T -> T

*   smell: function mutates an argument

    +   treat argument as immutable
    +   return a modified copy instead

*   smell: code mutates an attribute of an object

    +   instead return a copy constructed with the new attribute value

These smells are not smells if they are merely implementation details and are
properly isolated behind a functional interface.


irritants
---------

In python, there is an established generic syntax to modify an attribute of some object state

    x = Obj(...)
    x.attr = new_value

As far as i am aware, there is no established generic syntax / library function to construct a
new value which is the same as some given value except with one (or more?) of the attributes
replaced by a new attribute value.

If there were such a `replace` function, then we could write *generic* code to create new
values with altered attributes without modifying state. It is already possible to write
non-generic code to do this, case by case, for each type we need to support.

Supposing there was such a `replace` function, then quite often, when we write

    x = Obj(...)
    x.attr = new_value

we could instead write

    x = Obj(...)
    x = replace(x, attr=new_value)

which could be made clearer by writing it in single static assignment form:

    x_0 = Obj(...)
    x_1 = replace(x_0, attr=new_value)

This last form leaves us with the two values, `x_0` and `x_1`, from before and after the
modification.

