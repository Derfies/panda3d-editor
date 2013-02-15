from base import Base


class Connect( Base ):
    
    def __init__( self, tgtComps, cnnctn, fn ):
        self.tgtComps = tgtComps
        self.cnnctn = cnnctn
        self.fn = fn
        
        # Save old values
        self.oldComps = self.cnnctn.Get()
    
    def Undo( self ):
        self.cnnctn.Set( self.oldComps )
    
    def Redo( self ):
        for tgtComp in self.tgtComps:
            self.fn( tgtComp )