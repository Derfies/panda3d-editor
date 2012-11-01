from base import Base


class Deselect( Base ):
    
    def __init__( self, app, nps ):
        self.app = app
        
        # Adjust node path list to represent only those which are selected
        # at the time this class is instanced
        self.nps = list( set( nps ) & set( self.app.selection.nps ) )
    
    def Undo( self ):
        self.app.selection.Add( self.nps )
        self.app.doc.OnSelectionChanged()
    
    def Redo( self ):
        self.app.selection.Remove( self.nps )
        self.app.doc.OnSelectionChanged()