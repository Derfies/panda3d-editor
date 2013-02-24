from base import Base


class Transform( Base ):
    
    def __init__( self, nps, xforms, oldXforms ):
        self.nps = nps
        self.xforms = xforms
        self.oldXforms = oldXforms
        
        # Make sure to mark the NodePath as dirty in case it is a child of a
        # model root.
        self.modded = []
        for np in self.nps:
            wrpr = base.game.nodeMgr.Wrap( np )
            self.modded.append( wrpr.GetModified() )
    
    def Undo( self ):
        for i in range( len( self.nps ) ):
            self.nps[i].setTransform( self.oldXforms[i] )
            wrpr = base.game.nodeMgr.Wrap( self.nps[i] )
            wrpr.SetModified( self.modded[i] )
    
    def Redo( self ):
        for i in range( len( self.nps ) ):
            self.nps[i].setTransform( self.xforms[i] )
            wrpr = base.game.nodeMgr.Wrap( self.nps[i] )
            wrpr.SetModified( True )