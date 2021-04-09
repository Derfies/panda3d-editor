from pandac.PandaModules import NodePath, CardMaker, LineSegs, Point2

import p3d


TOLERANCE = 1e-3


class Marquee( NodePath, p3d.SingleTask ):
    
    """Class representing a 2D marquee drawn by the mouse."""
    
    def __init__( self, *args, **kwargs ):
        colour = kwargs.pop( 'colour', (1, 1, 1, .2) )


        # Create a card maker
        cm = CardMaker( 'foo' )
        cm.setFrame( 0, 1, 0, 1 )
        
        # Init the node path, wrapping the card maker to make a rectangle
        NodePath.__init__( self, cm.generate() )
        p3d.SingleTask.__init__(self, *args, **kwargs)
        self.setColor( colour )
        self.setTransparency( 1 )
        self.reparentTo( self.root2d )
        self.hide()
        
        # Create the rectangle border
        ls = LineSegs()
        ls.moveTo( 0, 0, 0 )
        ls.drawTo( 1, 0, 0 )
        ls.drawTo( 1, 0, 1 )
        ls.drawTo( 0, 0, 1 )
        ls.drawTo( 0, 0, 0 )
        
        # Attach border to rectangle
        self.attachNewNode( ls.create() )
        
    def OnUpdate( self, task ):
        """
        Called every frame to keep the marquee scaled to fit the region marked
        by the mouse's initial position and the current mouse position.
        """
        # Check for mouse first, in case the mouse is outside the Panda window
        if self.mouseWatcherNode.hasMouse():
        
            # Get the other marquee point and scale to fit
            pos = self.mouseWatcherNode.getMouse() - self.initMousePos
            self.setScale( pos[0] if pos[0] else TOLERANCE, 1, pos[1] if pos[1] else TOLERANCE )
            
    def OnStart( self ):
        
        # Move the marquee to the mouse position and show it
        self.initMousePos = Point2( self.mouseWatcherNode.getMouse() )
        self.setPos( self.initMousePos[0], 1, self.initMousePos[1] )
        self.show()
                    
    def OnStop( self ):
        
        # Hide the marquee
        self.hide()
    
    def IsNodePathInside( self, np ):
        """Test if the specified node path lies within the marquee area."""
        npWorldPos = np.getPos( self.rootNp )
        p3 = self.camera.getRelativePoint( self.rootNp, npWorldPos )

        # Convert it through the lens to render2d coordinates
        p2 = Point2()
        if not self.camera.GetLens().project( p3, p2 ):
            return False
        
        # Test point is within bounds of the marquee
        min, max = self.getTightBounds()
        if ( p2.getX() > min.getX() and p2.getX() < max.getX() and 
             p2.getY() > min.getZ() and p2.getY() < max.getZ() ):
            return True
        
        return False