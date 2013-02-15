from nodePath import NodePath


class Render( NodePath ):
    
    def Create( self, parent=None ):
        self.SetupNodePath( render )
        self.data = render
        return render
    
    def SetParent( self, pComp ):
        
        # Render is a default Panda NodePath which shouldn't be parented to
        # anything.
        pass