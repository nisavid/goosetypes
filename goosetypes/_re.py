"""Regular-expression-like goose types"""

__copyright__ = "Copyright (C) 2014 Ivan D Vasin"
__docformat__ = "restructuredtext"

import spruce.types as _stypes

from . import _core as _goosetypes_core
from . import _string as _goosetypes_string


def _type_isregexlike(type):
    return issubclass(type, _stypes.regex_class) \
           or _goosetypes_string._type_isstringlike(type)


regexlike = \
    _goosetypes_core.goosetypeclass_fromconverter('regexlike', _stypes.regex,
                                                  type_issubclass=
                                                      _type_isregexlike)
