from base import Base


class SceneRoot( Base ):
    
    def Create( self ):
        self.data = base.scene
        return base.scene
    
    def AddChild( self, comp ):
        self.data.RegisterComponent( comp )
        
    def SetParent( self, pComp ):
        
        # SceneRoot is a special node which shouldn't be parented to anything.
        pass