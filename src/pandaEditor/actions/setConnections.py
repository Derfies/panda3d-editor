from base import Base


class SetConnections( Base ):
    
    def __init__( self, tgtComps, cnnctn ):
        self.tgtComps = tgtComps
        self.cnnctn = cnnctn
        
        # Save old values
        self.oldComps = self.cnnctn.Get()
        
        # Make sure to mark the NodePath as dirty in case it is a child of
        # a model root.
        wrpr = base.game.nodeMgr.Wrap( self.cnnctn.srcComp )
        self.modded = wrpr.GetModified()
    
    def Undo( self ):
        self.cnnctn.Set( self.oldComps )
        wrpr = base.game.nodeMgr.Wrap( self.cnnctn.srcComp )
        wrpr.SetModified( self.modded )
    
    def Redo( self ):
        self.cnnctn.Set( self.tgtComps )
        wrpr = base.game.nodeMgr.Wrap( self.cnnctn.srcComp )
        wrpr.SetModified( True )