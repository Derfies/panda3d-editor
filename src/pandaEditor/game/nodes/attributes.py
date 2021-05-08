import uuid
from functools import partial
from collections import MutableSequence

import panda3d.core as pc
from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.basemetaclass import BaseMetaClass


class ConnectionTargets(MutableSequence):

    def __init__(self, parent, instance, comps):
        self.parent = parent
        self.instance = instance
        self.comps = comps

    def __len__(self):
        return len(self.comps)

    def __bool__(self):
        return len(self.comps) > 0

    def __getitem__(self, index):
        return self.comps[index]

    def __setitem__(self, index, value):
        self.comps[index] = value
        self.update()

    def __delitem__(self, index):
        del self.comps[index]
        self.update()

    def insert(self, index, value):
        self.__setitem__(slice(index, index), [value])

    def update(self):
        self.parent.clear(self.instance)
        for comp in self.comps:
            setattr(self.instance, self.parent.name, comp)


class Base(metaclass=BaseMetaClass):
    
    def __init__(
        self,
        type_,
        get_fn=None,
        set_fn=None,
        serialise=True,
        node_data=False,
        read_only=False,
        required=False,
    ):
        self.type = type_
        self.get_fn = get_fn
        self.set_fn = set_fn
        self.serialise = serialise
        self.node_data = node_data
        self._read_only = read_only
        self.required = required

    def _get_data(self, instance):
        return instance.data if not self.node_data else instance.data.node()

    def __get__(self, instance, owner):
        return self.get_fn(self._get_data(instance))

    def __set__(self, instance, value):
        self.set_fn(self._get_data(instance), value)

    @property
    def read_only(self):
        return self.set_fn is None or self._read_only


class Attribute(Base, metaclass=BaseMetaClass):

    pass


class Connection(Base, metaclass=BaseMetaClass):

    many = False

    def __init__(self, type_, get_fn, set_fn, clear_fn, **kwargs):
        self.node_target = kwargs.pop('node_target', False)
        super().__init__(type_, get_fn, set_fn, **kwargs)

        self.clear_fn = clear_fn

    def _get_target(self, value):
        if value is None:
            return None
        return value.data if not self.node_target else value.data.node()

    def __get__(self, instance, owner):
        obj = self.get_fn(self._get_data(instance))

        # This sucks. Some functions return nodes however our architecture
        # expects these to be node paths.
        if obj is not None and self.node_target:
            obj = pc.NodePath(obj)
        return get_base().node_manager.wrap(obj) if obj is not None else None

    def __set__(self, instance, value):
        if not value:
            try:
                self.clear_fn(self._get_data(instance))
            except:
                print(self, instance, value)
                raise
        else:
            super().__set__(instance, self._get_target(value))


class Connections(Connection):

    many = True

    def __get__(self, instance, owner):

        # This sucks. Some functions return nodes however our architecture
        # expects these to be node paths.
        objs = self.get_fn(self._get_data(instance))
        if self.node_target:
            objs = [pc.NodePath(obj) for obj in objs]
        return ConnectionTargets(
            self,
            instance,
            [get_base().node_manager.wrap(obj) for obj in objs]
        )

    def clear(self, instance):
        return self.clear_fn(self._get_data(instance))


class TagAttributeBase(Attribute):
    pass


def get_metaobject_tag(attr, data):
    return data.metaobject.tags[attr.name]


def set_metaobject_tag(attr, data, value):
    data.metaobject.tags[attr.name] = value


class MetaobjectTagAttribute(TagAttributeBase):

    def __init__(self, type_, read_only=False, required=False):
        super().__init__(
            type_,
            partial(get_metaobject_tag, self),
            partial(set_metaobject_tag, self),
            read_only=read_only,
            required=required,
        )

    def _get_data(self, instance):
        return instance


def get_tag(attr, data):
    return data.get_tag(attr.name)


def set_tag(attr, data, value):
    data.set_tag(attr.name, value)


class TagAttribute(TagAttributeBase):

    def __init__(self, read_only=False, required=False):
        super().__init__(
            str,
            partial(get_tag, self),
            partial(set_tag, self),
            read_only=read_only,
            required=required,
        )


def get_python_tag(attr, data):
    return data.get_python_tag(attr.name)


def set_python_tag(attr, data, value):
    data.set_python_tag(attr.name, value)


class PythonTagAttribute(TagAttributeBase):

    def __init__(self, type_, read_only=False, required=False):
        super().__init__(
            type_,
            partial(get_python_tag, self),
            partial(set_python_tag, self),
            read_only=read_only,
            required=required,
        )


class ProjectAssetAttribute(Attribute):

    # TODO: Still breaking when we use 'set' from a relative path...

    def __init__(self, *args, **kwargs):
        self.directory = kwargs.pop('directory', None)
        super().__init__(*args, **kwargs)

    # def __get__(self, *args, **kwargs):
    #     return get_base().project.get_project_relative_path(
    #         super().__get__(*args, **kwargs),
    #         self.directory,
    #     )


class ProjectAssetPythonTagAttribute(ProjectAssetAttribute, PythonTagAttribute):

    pass
