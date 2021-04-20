import panda3d.bullet as pb
from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.attributes import Connection
from game.nodes.base import Base
from game.nodes.componentmetaclass import ComponentMetaClass


class PhysicsWorldConnection(Connection):

    def __init__(self):
        super().__init__(pb.BulletWorld)

    def get(self):
        return self.parent.data.physics_world

    def connect(self, physics_world):
        self.parent.data.physics_world = physics_world

    def clear(self):
        self.parent.data.physics_world = None


class SceneRoot(Base, metaclass=ComponentMetaClass):

    physics_world = PhysicsWorldConnection()
    
    @classmethod
    def create(cls, *args, **kwargs):
        return cls(get_base().scene)

    @property
    def id(self):
        return None

    @id.setter
    def id(self, value):
        pass

    @property
    def parent(self):
        return None

    @parent.setter
    def parent(self, value):
        pass

    def add_child(self, comp):
        self.data.register_component(comp)
