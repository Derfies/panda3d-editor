from panda3d.core import DirectionalLight

import p3d


class Manager( p3d.Object ):
    
    def __init__( self, *args, **kwargs ):
        p3d.Object.__init__( self, *args, **kwargs )
        
        self._gizmos = {}
        self._activeGizmo = None
        
        # Create gizmo manager mouse picker
        self.picker = p3d.MousePicker( 'mouse', *args, **kwargs )
        self.picker.Start()
        
        # Create a directional light and attach it to the camera so the gizmos
        # don't look flat
        dl = DirectionalLight( 'gizmoManagerDirLight' )
        self.dlNp = self.camera.attachNewNode( dl )
        self.rootNp.setLight( self.dlNp )
    
    def AddGizmo( self, gizmo ):
        """Add a gizmo to be managed by the gizmo manager."""
        gizmo.rootNp = self.rootNp
        self._gizmos[gizmo.getName()] = gizmo
        
    def GetGizmo( self, name ):
        """
        Find and return a gizmo by name, return None if no gizmo with the
        specified name exists.
        """
        if name in self._gizmos:
            return self._gizmos[name]
        
        return None
    
    def GetActiveGizmo( self ):
        """Return the active gizmo."""
        return self._activeGizmo
        
    def SetActiveGizmo( self, name ):
        """
        Stops the currently active gizmo then finds the specified gizmo by
        name and starts it.
        """
        # Stop the active gizmo
        if self._activeGizmo is not None:
            self._activeGizmo.Stop()
        
        # Get the gizmo by name and start it if it is a valid gizmo
        self._activeGizmo = self.GetGizmo( name )
        if self._activeGizmo is not None:
            self._activeGizmo.Start()
    
    def RefreshActiveGizmo( self ):
        """Refresh the active gizmo if there is one."""
        if self._activeGizmo is not None:
            self._activeGizmo.Refresh()
        
    def GetGizmoLocal( self, name ):
        """Return the gizmos local mode."""
        gizmo = self.GetGizmo( name )
        if gizmo is not None:
            return gizmo.local
            
    def SetGizmoLocal( self, name, mode ):
        """Set all gizmo local modes, then refresh the active one."""
        gizmo = self.GetGizmo( name )
        if gizmo is not None:
            gizmo.local = mode
        self.RefreshActiveGizmo()
            
    def SetLocal( self, val ):
        for gizmo in self._gizmos.values():
            gizmo.local = val
        self.RefreshActiveGizmo()
        
    def ToggleLocal( self ):
        """Toggle all gizmos local mode on or off."""
        for gizmo in self._gizmos.values():
            gizmo.local = not gizmo.local
        self.RefreshActiveGizmo()
        
    def SetSize( self, factor ):
        """Resize the gizmo by a factor."""
        for gizmo in self._gizmos.values():
            gizmo.SetSize( factor )
            
    def AttachNodePaths( self, nps ):
        """Attach node paths to be transformed by the gizmos."""
        for gizmo in self._gizmos.values():
            gizmo.AttachNodePaths( nps )
                    
    def IsDragging( self ):
        """
        Return True if the active gizmo is in the middle of a dragging
        operation, False otherwise.
        """
        return self._activeGizmo is not None and self._activeGizmo.dragging