"""Goose Types core"""

__copyright__ = "Copyright (C) 2014 Ivan D Vasin"
__docformat__ = "restructuredtext"

import __builtin__
from abc import ABCMeta as _ABCMeta, abstractmethod as _abstractmethod
from collections import Callable as _Callable

import spruce.types as _stypes


def goosetypeclass_fromconverter(classname, converter, bases=(),
                                 type_issubclass=None):

    @classmethod
    def _value_isinstance(cls, value):
        try:
            converter(value)
        except (TypeError, ValueError):
            return False
        else:
            return True

    _type_issubclass = None
    if type_issubclass:
        @classmethod
        def _type_issubclass(cls, type):
            return type_issubclass(type)
    elif converter.totype:
        @classmethod
        def _type_issubclass(type):
            return issubclass(type, converter.totype)
    elif any(hasattr(base, '_type_issubclass') for base in bases):
        pass
    else:
        method = None
        for base in bases:
            try:
                method = getattr(base, '_type_issubclass')
            except AttributeError:
                pass
            else:
                if not isinstance(method, _Callable):
                    method = None

        if not method:
            if classname:
                goosetypeclass_description = 'goose type ' + classname
            else:
                goosetypeclass_description = 'a goose type'
            goosetypeclass_description += \
                ' from converter {!r}'.format(converter)
            if bases:
                goosetypeclass_description += ' with bases {}'.format(bases)

            raise ValueError('cannot determine a subclass check function for'
                              ' constructing {}'
                              .format(goosetypeclass_description))

    if not classname:
        classname = converter.annotated_totype.__name__ + '_GooseType'

    goosetypeclass_bases = [converter.annotated_totype]
    goosetypeclass_bases.extend(list(bases or (GooseType,)))
    goosetypeclass_bases = tuple(goosetypeclass_bases)

    goosetypeclass_attrs = {'_value_isinstance': _value_isinstance}
    if _type_issubclass:
        goosetypeclass_attrs['_type_issubclass'] = _type_issubclass

    return type(classname, goosetypeclass_bases, goosetypeclass_attrs)


def instance_of(type, excluded_types=(), displayname=None):

    if displayname is not None:
        def displayname_(cls):
            return displayname
    else:
        def displayname_(cls):
            message = 'instance of {!r}'.format(type)
            if excluded_types:
                message += \
                    ' but not of {{{}}}'\
                     .format(', '.join(repr(type_)
                                       for type_ in excluded_types))
            return message
    displayname_.__name__ = 'displayname'
    displayname_ = classmethod(displayname_)

    @classmethod
    def _excluded_types(cls):
        return excluded_types

    @classmethod
    def _wrapped_type(cls):
        return type

    classname = type.__name__ + '_Instance'
    if excluded_types:
        classname += '_Excluding_' + '_'.join(type_.__name__
                                              for type_ in excluded_types)
    class_attrs = {'_excluded_types': _excluded_types,
                   '_wrapped_type': _wrapped_type}
    if displayname_ is not None:
        class_attrs['displayname'] = displayname_
    return __builtin__.type(classname, (InstanceOfType,), class_attrs)


def subclass_of(type, excluded_types=(), displayname=None):

    if displayname is not None:
        def displayname_(cls):
            return displayname
    else:
        def displayname_(cls):
            message = 'subclass of {!r}'.format(type)
            if excluded_types:
                message += \
                    ' but not of {{{}}}'\
                     .format(', '.join(repr(type_)
                                       for type_ in excluded_types))
            return message
    displayname_.__name__ = 'displayname'
    displayname_ = classmethod(displayname_)

    @classmethod
    def _excluded_types(cls):
        return excluded_types

    @classmethod
    def _wrapped_type(cls):
        return type

    classname = type.__name__ + '_Subclass'
    if excluded_types:
        classname += '_Excluding_' + '_'.join(type_.__name__
                                              for type_ in excluded_types)
    class_attrs = {'_excluded_types': _excluded_types,
                   '_wrapped_type': _wrapped_type}
    if displayname_ is not None:
        class_attrs['displayname'] = displayname_
    return __builtin__.type(classname, (SubclassOfType,), class_attrs)


class GooseTypeMeta(_ABCMeta):

    def __instancecheck__(self, value):
        return self._value_isinstance(value)

    def __subclasscheck__(self, type):
        return self._type_issubclass(type)


class GooseType(_stypes.AnnotatedType):

    __metaclass__ = GooseTypeMeta

    @classmethod
    @_abstractmethod
    def _type_issubclass(cls, type):
        pass

    @classmethod
    @_abstractmethod
    def _value_isinstance(cls, value):
        pass


class InstanceOfType(GooseType):

    __metaclass__ = GooseTypeMeta

    @classmethod
    def convertible_type_description(cls):
        message = repr(cls._wrapped_type())
        if cls._excluded_types:
            message += \
                ' excluding {{{}}}'\
                 .format(', '.join(repr(type_)
                                   for type_ in cls._excluded_types()))
        return message

    @classmethod
    def _excluded_types(cls):
        return ()

    @classmethod
    def _type_issubclass(cls, type):
        return issubclass(type, cls._wrapped_type()) \
               and not issubclass(type, cls._excluded_types())

    @classmethod
    def _value_isinstance(cls, value):
        return isinstance(value, cls._wrapped_type()) \
               and not isinstance(value, cls._excluded_types())

    @classmethod
    @_abstractmethod
    def _wrapped_type(cls):
        pass


class SubclassOfType(GooseType):

    __metaclass__ = GooseTypeMeta

    @classmethod
    def convertible_type_description(cls):
        return 'a metaclass'

    @classmethod
    def convertible_value_description(cls):
        message = 'a subclass of {!r}'.format(cls._wrapped_type())
        if cls._excluded_types:
            message += \
                ' excluding {{{}}}'\
                 .format(', '.join(repr(type_)
                                   for type_ in cls._excluded_types()))
        return message

    @classmethod
    def _excluded_types(cls):
        return ()

    @classmethod
    def _type_issubclass(cls, type):
        return issubclass(type, __builtin__.type)

    @classmethod
    def _value_isinstance(cls, value):
        try:
            return issubclass(value, cls._wrapped_type()) \
                   and not issubclass(value, cls._excluded_types())
        except TypeError:
            return False

    @classmethod
    @_abstractmethod
    def _wrapped_type(cls):
        pass
