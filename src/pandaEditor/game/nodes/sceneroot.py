from panda3d.bullet import BulletWorld
from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.attributes import NodePathTargetConnection
from game.nodes.base import Base
from game.nodes.othermeta import ComponentMetaClass


class SceneRoot(Base, metaclass=ComponentMetaClass):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
       #  self.AddAttributes(
       #      NodePathTargetConnection(
       #          'PhysicsWorld',
       #          BulletWorld,
       #          base.scene.GetPhysicsWorld,
       #          base.scene.SetPhysicsWorld,
       #          base.scene.ClearPhysicsWorld
       #      ),
       #      parent='Scene'
       # )
    
    @classmethod
    def create(cls, *args, **kwargs):
        return cls(get_base().scene)
    
    def add_child(self, comp):
        self.data.register_component(comp)

    @property
    def parent(self):
        return get_base().node_manager.wrap(get_base().scene)

    @parent.setter
    def parent(self, value):

        # Render is a default Panda NodePath which shouldn't be parented to
        # anything.
        pass

    @property
    def id(self):
        return None

    @id.setter
    def id(self, value):
        pass
