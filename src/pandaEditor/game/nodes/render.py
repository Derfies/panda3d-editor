from nodePath import NodePath


class Render( NodePath ):
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        wrpr = cls( render )
        wrpr.SetupNodePath()
        return wrpr
    
    def SetParent( self, pComp ):
        
        # Render is a default Panda NodePath which shouldn't be parented to
        # anything.
        pass