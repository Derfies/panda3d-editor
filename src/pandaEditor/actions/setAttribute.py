from base import Base


class SetAttribute( Base ):
    
    def __init__( self, nps, attr, val ):
        self.nps = nps
        self.attr = attr
        self.val = val
        
        # Save old values. I've had to cast the value back into its own type
        # so as to get a copy - undo doesn't seem to work otherwise.
        self.modded = []
        self.oldVals = []
        for np in self.nps:
            self.oldVals.append( attr.type( attr.Get( np ) ) )
            
            # Make sure to mark the NodePath as dirty in case it is a child of
            # a model root.
            wrpr = base.game.nodeMgr.Wrap( np )
            self.modded.append( wrpr.GetModified() )
    
    def Undo( self ):
        """Undo the action."""
        for i in range( len( self.nps ) ):
            self.attr.Set( self.nps[i], self.oldVals[i] )
            wrpr = base.game.nodeMgr.Wrap( self.nps[i] )
            wrpr.SetModified( self.modded[i] )
    
    def Redo( self ):
        """Redo the action."""
        for np in self.nps:
            self.attr.Set( np, self.val )
            wrpr = base.game.nodeMgr.Wrap( np )
            wrpr.SetModified( True )