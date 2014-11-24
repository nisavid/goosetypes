"""Duck types miscellany"""

__copyright__ = "Copyright (C) 2014 Ivan D Vasin"
__docformat__ = "restructuredtext"

from collections import Callable as _Callable

import spruce.types as _stypes

from . import _core as _goosetypes_core


def _type_isboollike(type):
    try:
        nonzero_method = getattr(type, '__nonzero__')
    except AttributeError:
        return False
    return isinstance(nonzero_method, _Callable)


boollike = _goosetypes_core.goosetypeclass_fromconverter('boollike',
                                                         _stypes.bool,
                                                         type_issubclass=
                                                             _type_isboollike)
