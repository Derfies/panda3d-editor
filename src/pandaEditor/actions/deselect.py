from base import Base


class Deselect( Base ):
    
    def __init__( self, comps ):
        self.comps = comps
    
    def Undo( self ):
        base.selection.Add( self.comps )
    
    def Redo( self ):
        base.selection.Remove( self.comps )