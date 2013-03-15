import uuid

import p3d


class Scene( p3d.Object ):
        
    cType = 'SceneRoot'
    
    def __init__( self, *args, **kwargs ):
        p3d.Object.__init__( self, *args, **kwargs )
        
        self.comps = {}
        base.scene = self
        self.physicsWorld = None
        self.physicsTask = None
    
    def RegisterComponent( self, comp ):
        id = str( uuid.uuid4() )
        self.comps[comp] = id
        
    def DeregisterComponent( self, comp ):
        if comp in self.comps:
            del self.comps[comp]
            
    def GetPhysicsWorld( self, foo ):
        return self.physicsWorld
    
    def SetPhysicsWorld( self, cookie, phWorld ):
        self.physicsWorld = phWorld
    
    def ClearPhysicsWorld( self, cookie ):
        self.physicsWorld = None