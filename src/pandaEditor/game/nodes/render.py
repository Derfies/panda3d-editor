from nodePath import NodePath


class Render( NodePath ):
    
    def Create( self ):
        self.SetupNodePath( render )
        self.Wrap( render )
        return render