from base import Base


class Parent( Base ):
    
    def __init__( self, app, nps, parent ):
        self.app = app
        self.nps = nps
        self.parent = parent
        
        self.oldParents = [np.getParent() for np in self.nps]
    
    def Undo( self ):
        for i in range( len( self.nps ) ):
            self.nps[i].wrtReparentTo( self.oldParents[i] )
        self.app.doc.OnModified()
    
    def Redo( self ):
        for np in self.nps:
            np.wrtReparentTo( self.parent )
        self.app.doc.OnModified()