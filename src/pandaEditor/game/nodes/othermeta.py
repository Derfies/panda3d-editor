import copy

from collections import OrderedDict

from game.nodes.attributes import Base
from game.nodes.wrappermeta import BaseMetaClass


class ComponentMetaClass(BaseMetaClass):

    pass
    #
    # def __new__(cls, name, bases, attrs):
    #     attrs['_declared_fields'] = cls._get_declared_fields(name, bases, attrs)
    #     out_cls = super().__new__(cls, name, bases, attrs)
    #     return out_cls
    #
    # @classmethod
    # def _get_declared_fields(cls, name, bases, attrs):
    #     fields = []
    #     for field_name, obj in list(attrs.items()):
    #         if not isinstance(obj, Base):
    #             continue
    #         field = attrs.pop(field_name)
    #         field.category = name
    #         fields.append((field_name, field))
    #
    #     # Ensures a base class field doesn't override cls attrs, and maintains
    #     # field precedence when inheriting multiple parents. e.g. if there is a
    #     # class C(A, B), and A and B both define 'field', use 'field' from A.
    #     known = set(attrs)
    #
    #     def visit(name):
    #         known.add(name)
    #         return name
    #
    #     base_fields = [
    #         (visit(name), f)
    #         for base in bases if hasattr(base, '_declared_fields')
    #         for name, f in base._declared_fields.items() if name not in known
    #     ]
    #
    #     print(f'Component: {name} fields: {fields}')
    #
    #     # print('DO COPY')
    #     #
    #     # return OrderedDict(
    #     #     copy.deepcopy(base_fields) +
    #     #     copy.deepcopy(fields)
    #     # )
    #     return OrderedDict(
    #         base_fields +
    #         fields
    #     )

    @classmethod
    def get_mro(metacls, cls, mro):
        mro = super().get_mro(cls, mro)

        # HAXX
        class_name = cls.__name__
        path = cls.__module__.split('.')
        if path[0] != 'game':
            return mro

        cls._declared_fields = metacls._get_attributes(mro)
        #print('FINAL:', cls, '->', cls._declared_fields)

        # for foo, bar in cls._declared_fields.items():
        #     cls.

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
                #print('    ->', cls, 'attr:', attr_name, cls.__name__)
                attr.category = cls.__name__
                attr.name = attr_name
                attrs[attr_name] = attr
            # print('->', cls, )
            # for field_name, obj in dir(cls):
            #     if not isinstance(obj, Base):
            #         continue
            #     #field = attrs.pop(field_name)
            #     field.category = cls.__name__
            #     fields.append((field_name, field))

        return attrs
        # fields = []
        #
        # for field_name, obj in list(attrs.items()):
        #     if not isinstance(obj, Base):
        #         continue
        #     field = attrs.pop(field_name)
        #     field.category = name
        #     fields.append((field_name, field))

        # Ensures a base class field doesn't override cls attrs, and maintains
        # field precedence when inheriting multiple parents. e.g. if there is a
        # class C(A, B), and A and B both define 'field', use 'field' from A.
        # known = set(attrs)
        #
        # def visit(name):
        #     known.add(name)
        #     return name
        #
        # base_fields = [
        #     (visit(name), f)
        #     for base in bases if hasattr(base, '_declared_fields')
        #     for name, f in base._declared_fields.items() if name not in known
        # ]
        #
        # print(f'Component: {name} fields: {fields}')
        #
        # # print('DO COPY')
        # #
        # # return OrderedDict(
        # #     copy.deepcopy(base_fields) +
        # #     copy.deepcopy(fields)
        # # )
        # return OrderedDict(
        #     base_fields +
        #     fields
        # )
