import copy
import types

from collections import OrderedDict

from game.nodes.attributes import Base
from game.nodes.basemetaclass import BaseMetaClass


class ComponentMetaClass(BaseMetaClass):

    @property
    def frobulate(cls):

        mro = cls.mro()
        results = {}
        #processed = set()
        names = dir(cls)
        # :dd any DynamicClassAttributes to the list of names if object is a class;
        # this may result in duplicate entries if, for example, a virtual
        # attribute with the same name as a DynamicClassAttribute exists
        try:
            for base in cls.__bases__:
                for k, v in base.__dict__.items():
                    if isinstance(v, types.DynamicClassAttribute):
                        names.append(k)
        except AttributeError:
            pass

        for key in names:
            # First try to get the value via getattr.  Some descriptors don't
            # like calling their __get__ (see bug #1785), so fall back to
            # looking in the __dict__.
            for base in mro:
                if key in base.__dict__:
                    value = base.__dict__[key]
                    break

            if not isinstance(value, Base):
                continue
            results[key] = value

        #print(results)

        return results
    '''
    pass

    @classmethod
    def get_mro(metacls, cls, mro):
        mro = super().get_mro(cls, mro)

        # HAXX
        class_name = cls.__name__
        path = cls.__module__.split('.')
        if path[0] != 'game':
            return mro

        #cls._declared_fields = metacls._get_attributes(mro)
        return mro

    @classmethod
    def _get_attributes(metacls, mro):

        from game.nodes.attributes import Base



        attrs = {}
        # for cls in reversed(mro):
        #     print(cls)
        #     print('    ', cls.__dict__)
            # for attr_name in dir(cls):
            #     print(cls, attr_name, getattr(cls, attr_name))
                # if attr_name in attrs:
                #     continue
                # attr = getattr(cls, attr_name)
                # if not isinstance(attr, Base):
                #     #print('SKIPPING ATTRIBUTE:', attr)
                #     continue
                # attr.category = cls.__name__
                # attr.name = attr_name
                # attrs[attr_name] = attr

        return attrs
    '''
    @property
    def create_attributes(cls):
        # return list(
        #     filter(lambda a: a.init_arg is not None, cls._declared_fields.values())
        # )
        # for key, value in cls.frobulate.items():
        #     print(key, value, value.init_arg)
        return {
            key: value
            for key, value in cls.frobulate.items()
            if isinstance(value, Base) and value.init_arg is not None
        }
