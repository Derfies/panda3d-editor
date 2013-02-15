from base import Base


class SetConnections( Base ):
    
    def __init__( self, tgtComps, cnnctn ):
        self.tgtComps = tgtComps
        self.cnnctn = cnnctn
        
        # Save old values
        self.oldComps = self.cnnctn.Get()
    
    def Undo( self ):
        self.cnnctn.Set( self.oldComps )
    
    def Redo( self ):
        self.cnnctn.Set( self.tgtComps )