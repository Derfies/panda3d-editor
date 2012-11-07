from base import Base


class Add( Base ):
    
    def __init__( self, nps ):
        self.nps = nps
    
    def Undo( self ):
        base.scene.DeleteNodePaths( self.nps )
    
    def Redo( self ):
        base.scene.AddNodePaths( self.nps )