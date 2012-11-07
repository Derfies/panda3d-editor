from base import Base


class Transform( Base ):
    
    def __init__( self, nps, xforms, oldXforms ):
        self.nps = nps
        self.xforms = xforms
        self.oldXforms = oldXforms
    
    def Undo( self ):
        for i in range( len( self.nps ) ):
            self.nps[i].setTransform( self.oldXforms[i] )
    
    def Redo( self ):
        for i in range( len( self.nps ) ):
            self.nps[i].setTransform( self.xforms[i] )