import types

from game.nodes.attributes import Base, Attribute, Connection, ReadOnlyAttribute
from game.nodes.basemetaclass import BaseMetaClass


class ComponentMetaClass(BaseMetaClass):

    def __new__(metacls, name, bases, attrs):
        cls = super().__new__(metacls, name, bases, attrs)

        cls.properties  # HAXXOR need to init properties at least once.

        return cls

    @property
    def properties(cls):

        results = {}
        for base in cls.mro():
            for key, value in base.__dict__.items():
                if not isinstance(value, Base):
                    continue

                # TODO: Need a better way to set category / name data.
                value.category = base.__name__
                value.name = key
                results[key] = value
        return results

        '''

        mro = cls.mro()
        results = {}
        names = dir(cls)
        # :dd any DynamicClassAttributes to the list of names if object is a class;
        # this may result in duplicate entries if, for example, a virtual
        # attribute with the same name as a DynamicClassAttribute exists
        try:
            for base in cls.__bases__:
                for k, v in base.__dict__.items():
                    if isinstance(v, types.DynamicClassAttribute):
                        names.append(k)
                    else:
                        print('ignore:', k)
        except AttributeError as e:
            print('error:', e)

        print('cls:', cls)
        for key in names:
            print('found key:', key)
            # First try to get the value via getattr.  Some descriptors don't
            # like calling their __get__ (see bug #1785), so fall back to
            # looking in the __dict__.
            for base in mro:
                print('    base:', base, base.__dict__)
                if key in base.__dict__:
                    value = base.__dict__[key]
                    if isinstance(value, Base):
                        value.category = base.__name__  # HAXXOR
                    break

            if not isinstance(value, Base):
                continue
            results[key] = value

        return results
        '''

    @property
    def attributes(cls):
        return {
            key: value
            for key, value in cls.properties.items()
            if isinstance(value, ReadOnlyAttribute)
        }

    @property
    def connections(cls):
        return {
            key: value
            for key, value in cls.properties.items()
            if isinstance(value, Connection)
        }

    @property
    def create_attributes(cls):
        return {
            key: value
            for key, value in cls.attributes.items()
            if value.init_arg is not None
        }
