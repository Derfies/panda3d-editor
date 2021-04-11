from panda3d.bullet import BulletWorld as BW

try:
    from pandaEditor.editor.nodes.attributes import NodePathTargetConnection as Cnnctn
    from pandaEditor.editor.nodes.base import Base
except ImportError:
    print('import failed')
    from pandaEditor.game.nodes.attributes import NodePathTargetConnection as Cnnctn
    from pandaEditor.game.nodes.base import Base


class SceneRoot(Base):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.AddAttributes(
            Cnnctn('PhysicsWorld', BW, base.scene.GetPhysicsWorld, 
                    base.scene.SetPhysicsWorld, base.scene.ClearPhysicsWorld),
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
