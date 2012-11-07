from base import Base


class Deselect( Base ):
    
    def __init__( self, nps ):
        self.nps = nps
    
    def Undo( self ):
        base.selection.Add( self.nps )
    
    def Redo( self ):
        base.selection.Remove( self.nps )