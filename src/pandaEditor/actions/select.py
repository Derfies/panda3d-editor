from base import Base


class Select( Base ):
    
    def __init__( self, app, nps ):
        self.app = app
        self.nps = nps
    
    def Undo( self ):
        self.app.selection.Remove( self.nps )
        self.app.doc.OnSelectionChanged()
    
    def Redo( self ):
        self.app.selection.Add( self.nps )
        self.app.doc.OnSelectionChanged()