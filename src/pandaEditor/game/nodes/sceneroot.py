import panda3d.bullet as pb
from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.attributes import Connection
from game.nodes.nongraphobject import NonGraphObject
from game.nodes.componentmetaclass import ComponentMetaClass


def get_physics_world(scene):
    return scene.physics_world


def set_physics_world(scene, world):
    scene.physics_world = world


class SceneRoot(NonGraphObject, metaclass=ComponentMetaClass):

    physics_world = Connection(
        pb.BulletWorld,
        get_physics_world,
        set_physics_world,
        None,
    )
    
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

    def add_child(self, child):
        self.data.register_component(child)
