import abc
import copy
import logging
import uuid

from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.componentmetaclass import ComponentMetaClass


logger = logging.getLogger(__name__)


class Base(metaclass=ComponentMetaClass):
    
    def __init__(self, data):
        self.data = data
        self._children = []
    
    @classmethod
    def create(cls, *args, **kwargs):
        data = kwargs.pop('data', None)
        if data is None:
            data = cls.type_(*args, **kwargs)
        comp = cls(data)
        return comp

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        return hash(self) == hash(other)

    @property
    def id(self):
        return self.metaobject.id

    @id.setter
    def id(self, value):
        self.metaobject.id = value

    @property
    def type(self):
        return type(self).__name__

    @property
    def parent(self):

        # Return None if the component isn't registered - it may have been
        # detached.
        if self.data not in get_base().scene.objects:
            return None
        return get_base().node_manager.wrap(get_base().scene)

    @parent.setter
    def parent(self, value):
        value.add_child(self)

    @property
    def children(self):
        return self._children

    @abc.abstractmethod
    def detach(self):
        """"""

    @abc.abstractmethod
    def destroy(self):
        """"""

    @abc.abstractmethod
    def add_child(self, child):
        """"""
