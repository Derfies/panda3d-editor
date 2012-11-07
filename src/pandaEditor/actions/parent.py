from base import Base


class Parent( Base ):
    
    def __init__( self, nps, parent ):
        self.nps = nps
        self.parent = parent
        
        self.oldParents = [np.getParent() for np in self.nps]
    
    def Undo( self ):
        for i in range( len( self.nps ) ):
            self.nps[i].wrtReparentTo( self.oldParents[i] )
    
    def Redo( self ):
        for np in self.nps:
            np.wrtReparentTo( self.parent )