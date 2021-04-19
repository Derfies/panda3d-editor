from panda3d.bullet import BulletWorld
from direct.showbase.PythonUtil import getBase as get_base

# from game.nodes.attributes import NodePathTargetConnection
from game.nodes.base import Base
from game.nodes.othermeta import ComponentMetaClass


class SceneRoot(Base, metaclass=ComponentMetaClass):

    # TODO: Move bullet world stuff into bullet context.
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.AddAttributes(
    #         NodePathTargetConnection(
    #             'PhysicsWorld',
    #             BulletWorld,
    #             base.scene.GetPhysicsWorld,
    #             base.scene.SetPhysicsWorld,
    #             base.scene.ClearPhysicsWorld
    #         ),
    #         parent='Scene'
    #    )
    
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
