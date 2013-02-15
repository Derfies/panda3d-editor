import uuid

import p3d


class Scene( p3d.Object ):
    
    def __init__( self, *args, **kwargs ):
        p3d.Object.__init__( self, *args, **kwargs )
        
        self.comps = {}
        base.scene = self
    
    def RegisterComponent( self, comp ):
        id = str( uuid.uuid4() )
        self.comps[comp] = id
        
    def DeregisterComponent( self, comp ):
        if comp in self.comps:
            del self.comps[comp]