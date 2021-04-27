from game.nodes.attributes import Base, Attribute, Connection
from game.nodes.basemetaclass import BaseMetaClass


class ComponentMetaClass(BaseMetaClass):

    def __new__(metacls, name, bases, attrs):
        cls = super().__new__(metacls, name, bases, attrs)

        cls.properties = metacls.get_properties(cls)

        return cls

    def get_properties(cls):
        results = {}
        for base in reversed(cls.mro()):
            for key, value in base.__dict__.items():
                if not isinstance(value, Base):
                    continue

                # TODO: Need a better way to set category / name data.
                value.category = base.__name__
                value.name = key
                results[key] = value
        return results

    @property
    def attributes(cls):
        return {
            key: value
            for key, value in cls.properties.items()
            if isinstance(value, Attribute)
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
