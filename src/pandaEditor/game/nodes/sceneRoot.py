from base import Base
from game.nodes.attributes import NodePathTargetConnection as Cnnctn


class SceneRoot( Base ):
    
    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Cnnctn( 'PhysicsWorld', None, base.scene.GetPhysicsWorld, base.scene.SetPhysicsWorld, base.scene.ClearPhysicsWorld )
        )
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        wrpr = cls( base.scene )
        return wrpr
    
    def AddChild( self, comp ):
        self.data.RegisterComponent( comp )
        
    def SetParent( self, pComp ):
        
        # SceneRoot is a special node which shouldn't be parented to anything.
        pass