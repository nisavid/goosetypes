"""String-like goose types"""

__copyright__ = "Copyright (C) 2014 Ivan D Vasin"
__docformat__ = "restructuredtext"

from collections import Callable as _Callable
import types as _types

import spruce.types as _stypes

from . import _core as _goosetypes_core


def _type_isstringlike(type):
    try:
        string_method = getattr(type, '__unicode__')
    except AttributeError:
        try:
            string_method = getattr(type, '__str__')
        except AttributeError:
            return issubclass(type, _types.StringTypes)
    return isinstance(string_method, _Callable)


hex_intlike = \
    _goosetypes_core.goosetypeclass_fromconverter('hexlike', _stypes.hex_int,
                                                  type_issubclass=
                                                      _type_isstringlike)


stringlike = \
    _goosetypes_core.goosetypeclass_fromconverter('stringlike', _stypes.string,
                                                  type_issubclass=
                                                      _type_isstringlike)
