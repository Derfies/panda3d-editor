from panda3d.bullet import BulletWorld

from game.nodes.attributes import NodePathTargetConnection
from game.nodes.base import Base
from game.nodes.wrappermeta import WrapperMeta


class SceneRoot(Base, metaclass=WrapperMeta):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.AddAttributes(
            NodePathTargetConnection(
                'PhysicsWorld',
                BulletWorld,
                base.scene.GetPhysicsWorld,
                base.scene.SetPhysicsWorld,
                base.scene.ClearPhysicsWorld
            ),
            parent='Scene'
       )
    
    @classmethod
    def Create(cls, *args, **kwargs):
        return cls(base.scene)
    
    def AddChild(self, comp):
        self.data.RegisterComponent(comp)
        
    def GetParent(self):
        return None
        
    def SetParent(self, pComp):
        
        # SceneRoot is a special node which shouldn't be parented to anything.
        pass
    
    def SetId(self, id):
        
        # SceneRoot is a special node doesn't need an id.
        pass
