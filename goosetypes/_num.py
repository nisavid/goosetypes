"""Numeric goose types"""

__copyright__ = "Copyright (C) 2014 Ivan D Vasin"
__docformat__ = "restructuredtext"

from collections import Callable as _Callable
import types as _types

import spruce.types as _stypes

from . import _core as _goosetypes_core


# float-like variants ---------------------------------------------------------


def _type_isfloatlike(type):
    return issubclass(type,
                      tuple([complex, float, int, long]
                            + list(_types.StringTypes)))


floatlike = \
    _goosetypes_core.goosetypeclass_fromconverter('floatlike', _stypes.float,
                                                  type_issubclass=
                                                      _type_isfloatlike)


neg_floatlike = \
    _goosetypes_core.goosetypeclass_fromconverter('neg_floatlike',
                                                  _stypes.neg_float,
                                                  bases=(floatlike,))


nonneg_floatlike = \
    _goosetypes_core.goosetypeclass_fromconverter('nonneg_floatlike',
                                                  _stypes.nonneg_float,
                                                  bases=(floatlike,))


nonpos_floatlike = \
    _goosetypes_core.goosetypeclass_fromconverter('nonpos_floatlike',
                                                  _stypes.nonpos_float,
                                                  bases=(floatlike,))


pos_floatlike = \
    _goosetypes_core.goosetypeclass_fromconverter('pos_floatlike',
                                                  _stypes.pos_float,
                                                  bases=(floatlike,))


# int-like variants -----------------------------------------------------------


def _type_isintlike(type):
    try:
        intmethod = getattr(type, '__int__')
    except AttributeError:
        return issubclass(type, _types.StringTypes)
    else:
        return isinstance(intmethod, _Callable)


intlike = _goosetypes_core.goosetypeclass_fromconverter('intlike', _stypes.int,
                                                        type_issubclass=
                                                            _type_isintlike)


neg_intlike = _goosetypes_core.goosetypeclass_fromconverter('neg_intlike',
                                                            _stypes.neg_int,
                                                            bases=(intlike,))


nonneg_intlike = \
    _goosetypes_core.goosetypeclass_fromconverter('nonneg_intlike',
                                                  _stypes.nonneg_int,
                                                  bases=(intlike,))


nonpos_intlike = \
    _goosetypes_core.goosetypeclass_fromconverter('nonpos_intlike',
                                                  _stypes.nonpos_int,
                                                  bases=(intlike,))


pos_intlike = _goosetypes_core.goosetypeclass_fromconverter('pos_intlike',
                                                            _stypes.pos_int,
                                                            bases=(intlike,))
