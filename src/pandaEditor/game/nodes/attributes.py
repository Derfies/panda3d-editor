from collections import MutableSequence

import panda3d.core as pc
from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.basemetaclass import BaseMetaClass


class ConnectionTargets(MutableSequence):

    def __init__(self, parent, instance, data):
        self.parent = parent
        self.instance = instance
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value
        self.update()

    def __delitem__(self, index):
        del self.data[index]
        self.update()

    def insert(self, index, value):
        self.__setitem__(slice(index, index), [value])

    def update(self):
        self.parent.clear_all(self.instance)
        for obj in self.data:
            setattr(self.instance, self.parent.name, obj)

    # def remove(self, obj):
    #     print(self.data, 'remove:', obj)
    #     print(obj in self.data)
    #     print(obj.data in [d.data for d in self.data])
    #     print('obj hash:', hash(obj))
    #     print('data hash:', [hash(obj) for obj in self.data])
    #     print('obj hash2:', hash(obj.data))
    #     print('data hash2:', [hash(obj.data) for obj in self.data])


class Base(metaclass=BaseMetaClass):
    
    def __init__(
        self,
        type_,
        # get_fn=None,
        # set_fn=None,
        **kwargs
        # init_arg=None,
        # init_arg_name=None,
        # serialise=True,
    ):
        self.type = type_
        #self.get_fn = kwargs.get('get_fn')
        self.init_arg = kwargs.get('init_arg')
        self.init_arg_name = kwargs.get('init_arg_name')
        self.serialise = kwargs.get('serialise', True)

    def _get_data(self, instance):
        return instance.data

    def __get__(self, instance, owner):
        return self.get_fn(self._get_data(instance))

    def __set__(self, instance, value):
        self.set_fn(self._get_data(instance), value)


class NodeMixin:

    def _get_data(self, instance):
        return super()._get_data(instance).node()


class ReadOnlyAttribute(Base, metaclass=BaseMetaClass):

    def __init__(self, type_, get_fn, **kwargs):
        super().__init__(type_, **kwargs)

        self.get_fn = get_fn


class Attribute(ReadOnlyAttribute, metaclass=BaseMetaClass):

    def __init__(self, type_, get_fn, set_fn, **kwargs):
        super().__init__(type_, get_fn, **kwargs)

        self.set_fn = set_fn


class NodeAttribute(NodeMixin, Attribute, metaclass=BaseMetaClass):

    pass


class ReadOnlyNodeAttribute(NodeMixin, ReadOnlyAttribute, metaclass=BaseMetaClass):

    pass


class Connection(Base, metaclass=BaseMetaClass):

    many = False

    def __init__(self, type_, get_fn, set_fn, clear_fn, **kwargs):
        super().__init__(type_, **kwargs)

        self.get_fn = get_fn
        self.set_fn = set_fn
        self.clear_fn = clear_fn

    def _get_target(self, value):

        # Note that value might be None if we're setting the connection to null.
        return value.data if value is not None else None

    def __get__(self, instance, owner):
        obj = self.get_fn(self._get_data(instance))
        return get_base().node_manager.wrap(obj) if obj is not None else None

    def __set__(self, instance, value):
        super().__set__(instance, self._get_target(value))


class Connections(Connection):

    many = True

    def __init__(self, type_, get_fn, set_fn, clear_fn, clear_all_fn, **kwargs):
        super().__init__(type_, get_fn, set_fn, clear_fn, **kwargs)

        self.clear_all_fn = clear_all_fn

    def __get__(self, instance, owner):

        # This sucks. Some functions return nodes however our architecture
        # expects these to be node paths.
        objs = [
            obj if isinstance(obj, pc.NodePath) else pc.NodePath(obj)
            for obj in self.get_fn(self._get_data(instance))
        ]
        return ConnectionTargets(
            self,
            instance,
            [get_base().node_manager.wrap(obj) for obj in objs]
        )

    def clear_all(self, instance):
        return self.clear_all_fn(self._get_data(instance))


class NodeConnection(NodeMixin, Connection):

    pass


class NodeConnections(Connections, NodeConnection):

    pass


class ToNodeConnection(Connection):

    def _get_target(self, obj):
        return obj.data.node()


class ToNodesConnection(Connections, ToNodeConnection):

    pass


class NodeToNodeConnection(NodeConnection, ToNodeConnection):

    pass


class NodeToNodesConnection(Connections, NodeToNodeConnection):

    pass


class TagAttribute(Attribute):

    def __init__(self, *args, **kwargs):
        self.tag_name = kwargs.pop('tag_name')
        super().__init__(*args, **kwargs)

    def get(self):
        return self.data.get_tag(self.tag_name)

    def set(self, value):
        return self.data.set_tag(self.tag_name, value)


class PyTagAttribute(Attribute):

    def __init__(self, *args, **kwargs):
        self.pytag_name = kwargs.pop('pytag_name')
        super().__init__(*args, **kwargs)

    def __get__(self, instance, owner):
        return instance.data.get_python_tag(self.pytag_name)

    def __set__(self, instance, value):
        instance.data.set_python_tag(self.pytag_name, value)


class ProjectAssetMixin:

    def __init__(self, *args, **kwargs):
        self.directory = kwargs.pop('directory', None)
        super().__init__(*args, **kwargs)

    def __get__(self, *args, **kwargs):
        return get_base().project.get_project_relative_path(
            super().__get__(*args, **kwargs),
            self.directory,
        )


class ReadOnlyNodeProjectAssetAttribute(ProjectAssetMixin, ReadOnlyNodeAttribute):
    pass


class NodeProjectAssetAttribute(ProjectAssetMixin, NodeAttribute):

    pass


class PyTagProjectAssetAttribute(ProjectAssetMixin, PyTagAttribute):

    pass