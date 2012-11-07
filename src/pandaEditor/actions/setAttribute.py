from base import Base


class SetAttribute( Base ):
    
    def __init__( self, nps, attr, val ):
        self.nps = nps
        self.attr = attr
        self.val = val
        
        # Save old values
        self.oldVals = []
        for np in self.nps:
            self.oldVals.append( attr.Get( np ) )
    
    def Undo( self ):
        """Undo the action."""
        for i in range( len( self.nps ) ):
            self.attr.Set( self.nps[i], self.oldVals[i] )
    
    def Redo( self ):
        """Redo the action."""
        for np in self.nps:
            self.attr.Set( np, self.val )