from base import Base


class Transform( Base ):
    
    def __init__( self, app, nps, xforms, oldXforms ):
        self.app = app
        self.nps = nps
        self.xforms = xforms
        self.oldXforms = oldXforms
    
    def Undo( self ):
        for i in range( len( self.nps ) ):
            self.nps[i].setTransform( self.oldXforms[i] )
        self.app.doc.OnModified()
        self.app.doc.OnSelectionChanged()
    
    def Redo( self ):
        for i in range( len( self.nps ) ):
            self.nps[i].setTransform( self.xforms[i] )
        self.app.doc.OnModified()
        self.app.doc.OnSelectionChanged()