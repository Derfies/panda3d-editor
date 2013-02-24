from base import Base


class Connect( Base ):
    
    def __init__( self, tgtComps, cnnctn, fn ):
        self.tgtComps = tgtComps
        self.cnnctn = cnnctn
        self.fn = fn
        
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
        for tgtComp in self.tgtComps:
            self.fn( tgtComp )
        wrpr = base.game.nodeMgr.Wrap( self.cnnctn.srcComp )
        wrpr.SetModified( True )