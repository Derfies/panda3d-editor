import pandac.PandaModules as pm
from pandac.PandaModules import Point3, Vec3, Plane, NodePath

import p3d
from p3d import commonUtils as utils
from constants import *


class Base( NodePath, p3d.SingleTask ):
    
    def __init__( self, name, *args, **kwargs ):
        NodePath.__init__( self, name )
        p3d.SingleTask.__init__( self, name, *args, **kwargs )
        
        self.attachedNps = []
        self.dragging = False
        self.local = True
        self.planar = False
        self.size = 1
        
        self.axes = []
        
        # Set this node up to be drawn over everything else
        self.setBin( 'fixed', 40 )
        self.setDepthTest( False )
        self.setDepthWrite( False )
        
    def OnUpdate( self, task ):
        """
        Update method called every frame. Run the transform method if the user
        is dragging, and keep it the same size on the screen.
        """
        if self.dragging:
            self.Transform()
            
        scale = ( self.getPos() - self.camera.getPos() ).length() / 10
        self.setScale( scale )
    
    def OnStart( self ):
        """
        Starts the gizmo adding the task to the task manager, refreshing it
        and deselecting all axes except the default one.
        """
        self.Refresh()
        
        # Select the default axis, deselect all others
        for axis in self.axes:
            if axis.default:
                axis.Select()
            else:
                axis.Deselect()
                
        self.AcceptEvents()
        
    def OnStop( self ):
        """
        Stops the gizmo by hiding it and removing it's update task from the
        task manager.
        """
        # Hide the gizmo and ignore all events
        self.detachNode()
        self.ignoreAll()
        
    def AcceptEvents( self ):
        """Bind all events for the gizmo."""
        self.accept( 'mouse1-up', self.OnMouseUp )
        self.accept( 'mouse2-up', self.OnMouseUp )
        self.accept( 'mouse2', self.OnMouse2Down )
        self.accept( ''.join( [self.name, '-mouse1'] ), self.OnNodeMouse1Down, [False] )
        self.accept( ''.join( [self.name, '-control-mouse1'] ), self.OnNodeMouse1Down, [True] )
        self.accept( ''.join( [self.name, '-mouse-over'] ), self.OnNodeMouseOver )
        self.accept( ''.join( [self.name, '-mouse-leave'] ), self.OnNodeMouseLeave )
            
    def Transform( self ):
        """
        Override this method to provide the gizmo with transform behavior.
        """
        pass
        
    def AttachNodePaths( self, nps ):
        """
        Attach node paths to the gizmo. This won't affect the node's position
        in the scene graph, but will transform the objects with the gizmo.
        """
        self.attachedNps = nps
        
    def SetSize( self, factor ):
        """
        Used to scale the gizmo by a factor, usually by 2 (scale up) and 0.5
        (scale down). Set both the new size for the gizmo also call set size
        on all axes.
        """
        self.size *= factor
        
        # Each axis may have different rules on how to appear when scaled, so
        # call set size on each of them
        for axis in self.axes:
            axis.SetSize( self.size )
        
    def GetAxis( self, collEntry ):
        """
        Iterate over all axes of the gizmo, return the axis that owns the
        solid responsible for the collision.
        """
        for axis in self.axes:
            if collEntry.getIntoNode() in axis.collNodes:
                return axis
        
        # No match found, return None
        return None
    
    def GetSelectedAxis( self ):
        """Return the selected axis of the gizmo."""
        for axis in self.axes:
            if axis.selected:
                return axis
            
    def ResetAxes( self ):
        """
        Reset the default colours and flag as unselected for all axes in the 
        gizmo.
        """
        for axis in self.axes:
            axis.Deselect()
            
    def Refresh( self ):
        """
        If the gizmo has node paths attached to it then move the gizmo into
        position, set its orientation and show it. Otherwise hide the gizmo.
        """
        if self.attachedNps:
            
            # Show the gizmo
            self.reparentTo( self.rootNp )
            
            # Move the gizmo into position
            self.setPos( self.attachedNps[0].getPos( self.rootNp ) )
            
            # Only set the orientation of the gizmo if in local mode
            if self.local:
                self.setHpr( self.attachedNps[0].getHpr( self.rootNp ) )
            else:
                self.setHpr( self.rootNp.getHpr() )
                
        else:
            
            # Hide the gizmo
            self.detachNode()
            
    def OnMouseUp( self ):
        """
        Set the dragging flag to false and reset the size of the gizmo on the
        mouse button is released.
        """
        self.dragging = False
        self.SetSize( 1 )
        
    def OnNodeMouseLeave( self, collEntry ):
        """
        Called when the mouse leaves the the collision object. Remove the
        highlight from any axes which aren't selected.
        """
        for axis in self.axes:
            if not axis.selected:
                axis.Unhighlight()
        
    def OnNodeMouse1Down( self, planar, collEntry ):
        self.planar = planar
        self.dragging = True
        
        # Store the attached node path's transforms.
        self.initNpXforms = [np.getTransform() for np in self.attachedNps]
        
        # Reset colours and deselect all axes, then get the one which the
        # mouse is over
        self.ResetAxes()
        axis = self.GetAxis( collEntry )
        if axis is not None:
            
            # Select it
            axis.Select()
            
            # Get the initial point where the mouse clicked the axis
            self.startAxisPoint = self.GetAxisPoint( axis )
            self.lastAxisPoint = self.GetAxisPoint( axis )
            
    def OnMouse2Down( self ):
        """
        Continue transform operation if user is holding mouse2 but not over
        the gizmo.
        """
        axis = self.GetSelectedAxis()
        if axis is not None and self.attachedNps and self.mouseWatcherNode.hasMouse():
            self.dragging = True
            self.initNpXforms = [np.getTransform() for np in self.attachedNps]
            self.startAxisPoint = self.GetAxisPoint( axis )
            self.lastAxisPoint = self.GetAxisPoint( axis )
        
    def OnNodeMouseOver( self, collEntry ):
        """Highlights the different axes as the mouse passes over them."""
        # Don't change highlighting if in dragging mode
        if self.dragging:
            return
        
        # Remove highlight from all unselected axes
        for axis in self.axes:
            if not axis.selected:
                axis.Unhighlight()
        
        # Highlight the axis which the mouse is over
        axis = self.GetAxis( collEntry )
        if axis is not None:
            axis.Highlight()
            
    def GetMousePlaneCollisionPoint( self, pos, nrml ):
        """
        Return the collision point of a ray fired through the mouse and a
        plane with the specified normal.
        """
        # Fire a ray from the camera through the mouse 
        mp = self.mouseWatcherNode.getMouse()
        p1 = Point3()
        p2 = Point3()
        self.camera.node().getLens().extrude( mp, p1, p2 )
        p1 = self.rootNp.getRelativePoint( self.camera, p1 )
        p2 = self.rootNp.getRelativePoint( self.camera, p2 )
        
        # Get the point of intersection with a plane with the normal
        # specified
        p = Point3()
        Plane( nrml, pos ).intersectsLine( p, p1, p2 )
        
        return p
    
    def GetAxisPoint( self, axis ):
        """
        Return the point of intersection for the mouse picker ray and the axis
        in the gizmo root node space.
        """
        # Get the axis vector - by default this is the selected axis'
        # vector unless we need to use the camera's look vector
        if axis.vector == CAMERA_VECTOR:
            axisVector = self.rootNp.getRelativeVector( self.camera, Vec3(0, -1, 0) )
        else:
            axisVector = self.rootNp.getRelativeVector( self, axis.vector )
            
        # Get the transform plane's normal. If we're transforming in
        # planar mode use the axis vector as the plane normal, otherwise
        # get the normal of a plane along the selected axis
        if self.planar or axis.planar:
            return self.GetMousePlaneCollisionPoint( self.getPos(), axisVector )
        else:
            
            # Get the cross of the camera vector and the axis vector - a
            # vector of 0, 1, 0 in camera space is coming out of the lens
            camVector = self.rootNp.getRelativeVector( self.camera, Vec3(0, 1, 0) )
            camAxisCross = camVector.cross( axisVector )
            
            # Cross this back with the axis to get a plane's normal
            planeNormal = camAxisCross.cross( axisVector )
            p = self.GetMousePlaneCollisionPoint( self.getPos(), planeNormal )
            return utils.ClosestPointToLine( p, self.getPos(), self.getPos() + 
                                             axisVector )