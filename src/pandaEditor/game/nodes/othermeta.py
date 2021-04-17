import copy

from collections import OrderedDict

from game.nodes.attributes import Base
from game.nodes.wrappermeta import BaseMetaClass


class ComponentMetaClass(BaseMetaClass):

    pass

    @classmethod
    def get_mro(metacls, cls, mro):
        mro = super().get_mro(cls, mro)

        # HAXX
        class_name = cls.__name__
        path = cls.__module__.split('.')
        if path[0] != 'game':
            return mro

        cls._declared_fields = metacls._get_attributes(mro)
        return mro

    @classmethod
    def _get_attributes(metacls, mro):

        from game.nodes.attributes import Base

        attrs = {}
        for cls in mro:
            for attr_name in dir(cls):
                attr = getattr(cls, attr_name)
                if not isinstance(attr, Base):
                    continue
                attr.category = cls.__name__
                attr.name = attr_name
                attrs[attr_name] = attr

        return attrs

