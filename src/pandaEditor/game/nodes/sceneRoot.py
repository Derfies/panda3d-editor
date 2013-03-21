from panda3d.bullet import BulletWorld as BW

from base import Base
from game.nodes.attributes import NodePathTargetConnection as Cnnctn


class SceneRoot( Base ):
    
    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Cnnctn( 'PhysicsWorld', BW, base.scene.GetPhysicsWorld, 
                    base.scene.SetPhysicsWorld, base.scene.ClearPhysicsWorld ),
            parent='Scene'
        )
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        return cls( base.scene )
    
    def AddChild( self, comp ):
        self.data.RegisterComponent( comp )
        
    def SetParent( self, pComp ):
        
        # SceneRoot is a special node which shouldn't be parented to anything.
        pass
    
    def SetId( self, id ):
        
        # SceneRoot is a special node doesn't need an id.
        pass