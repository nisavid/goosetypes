###########
Goose Types
###########

Goose Types is a Python library for data types that support custom
methods for type checking.

Goose types are classes with custom methods that define the behavior of
`isinstance()`_ and `issubclass()`_ checks against themselves, along
with some related annotations and error handling.  In other words, a
goose type is a frontend for Python's `metaclass hooks for custom
instance and subclass checks`_.


.. _isinstance():
    https://docs.python.org/2.7/library/functions.html#isinstance

.. _issubclass():
    https://docs.python.org/2.7/library/functions.html#issubclass

.. _metaclass hooks for custom instance and subclass checks:
    https://docs.python.org/2.7/reference/datamodel.html#customizing-instance-and-subclass-checks


***********************
Relation to duck typing
***********************

This is related to `duck typing`_, and could even be interpreted as an
implementation of it, but it is subtly different.

In contrast with a type in a nominal_ or structural_ type system, a duck
type is defined by a partial structure or behavior that is checked at
runtime.  In this sense, a goose type is the same.  However, duck typing
is typically associated with one of two approaches that differ from
goose typing.

One approach to duck typing is to apply EAFP: assume that the input
implements the desired structure and behavior, and rely on error
handling (supplementing as needed) to deal with non-compliant input.
This is a fine approach for simple duck types and loose validation
requirements, but for interfaces that require strict checking of complex
type descriptions, the validation and error handling code can be
cumbersome, littering a function and obscuring its essential
functionality.

Another approach is to apply a form of nominal type checking at the
level of attributes or methods, sometimes together with checking the
multiplicity of arguments.  By inspecting an object's attributes, it is
possible to check for a combination of interface conditions, such as
attribute names, method names, and argument multiplicities, before
commencing a destructive or expensive task.

Like the latter approach, goose types are more useful when it is
desirable to perform complex validation up front.  With Goose Types,
complex type checking code to be extracted from a function body into the
body of a goose type, leaving behind an invocation of `isinstance()`_ or
`issubclass()`_.  In the sense that this is runtime checking of
desirable interface behavior, this is like duck typing.  However, unlike
the conventional "walks"/"quacks" tests of duck typing, this can be used
for checks that are exactly as extensive, specific, or generic as
needed, without littering the code of functions that merely need to
invoke a type check.


.. _duck typing: https://en.wikipedia.org/wiki/Duck_typing

.. _isinstance():
    https://docs.python.org/2.7/library/functions.html#isinstance

.. _issubclass():
    https://docs.python.org/2.7/library/functions.html#issubclass

.. _nominal: https://en.wikipedia.org/wiki/Nominal_type_system

.. _structural: https://en.wikipedia.org/wiki/Structural_type_system
