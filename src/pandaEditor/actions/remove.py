from base import Base


class Remove( Base ):
    
    def __init__( self, nps ):
        self.nps = nps
    
    def Undo( self ):
        base.scene.AddNodePaths( self.nps )
    
    def Redo( self ):
        base.scene.DeleteNodePaths( self.nps )