from panda3d.bullet import BulletWorld as BW

#from game.nodes.manager import import_wrapper
from game.nodes.wrappermeta import WrapperMeta

from game.nodes.base import Base
#Cnnctn = import_wrapper('nodes.attributes.NodePathTargetConnection')


class SceneRoot(Base, metaclass=WrapperMeta):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
       #  self.AddAttributes(
       #      Cnnctn(
       #          'PhysicsWorld',
       #          BW,
       #          base.scene.GetPhysicsWorld,
       #          base.scene.SetPhysicsWorld,
       #          base.scene.ClearPhysicsWorld
       #      ),
       #      parent='Scene'
       # )
    
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
