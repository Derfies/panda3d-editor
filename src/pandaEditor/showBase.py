import pandac.PandaModules as pm
from direct.showbase import ShowBase as P3dShowBase

import p3d


class ShowBase( P3dShowBase.ShowBase ):
    
    def __init__( self, wxWin, *args, **kwargs ):
        P3dShowBase.ShowBase.__init__( self, *args, **kwargs )
        
        self.wxWin = wxWin
        
    def FinishInit( self ):
        self.SetupEdRender()
        self.SetupEdRender2d()
        self.SetupEdWindow()
        self.SetupEdMouseWatcher()
        self.SetupEdCamera()
        
        # Make additional camera for 2d nodes
        cam2d = self.makeCamera2d( self.win )
        cam2d.reparentTo( self.edRender2d )
        
        # Add the editor window, camera and pixel 2d to the list of forced
        # aspect windows so aspect is fixed when the window is resized.
        self.forcedAspectWins = []
        self.forcedAspectWins.append( (self.win, self.edCamera, self.edPixel2d) )
        
        # Set up masks for camera and render
        self.SetupCameraMask()
        self.SetupRenderMask()
        
    def SetupEdRender( self ):
        """
        Create editor root node behind render node so we can keep editor only
        nodes out of the scene.
        """
        self.edRender = pm.NodePath( 'edRender' )
        self.edRender.setShaderAuto()
        render.reparentTo( self.edRender )
        
    def SetupEdRender2d( self ):
        """
        Creates the render2d scene graph, the primary scene graph for 2-d 
        objects and gui elements that are superimposed over the 3-d geometry 
        in the window.
        """
        self.edRender2d = pm.NodePath( 'edRender2d' )

        # Set up some overrides to turn off certain properties which we 
        # probably won't need for 2-d objects.
        self.edRender2d.setDepthTest( 0 )
        self.edRender2d.setDepthWrite( 0 )
        self.edRender2d.setMaterialOff( 1 )
        self.edRender2d.setTwoSided( 1 )
        
        # This special root, pixel2d, uses units in pixels that are relative
        # to the window. The upperleft corner of the window is (0, 0),
        # the lowerleft corner is (xsize, -ysize), in this coordinate system.
        xsize, ysize = self.getSize()
        self.edPixel2d = self.edRender2d.attachNewNode( pm.PGTop( 'edPixel2d' ) )
        self.edPixel2d.setPos( -1, 0, 1 )
        if xsize > 0 and ysize > 0:
            self.edPixel2d.setScale( 2.0 / xsize, 1.0, 2.0 / ysize )
            
    def SetupEdWindow( self ):
        self.wxWin.Initialize()
        
    def SetupEdMouseWatcher( self ):
        
        # Setup mouse watcher for the editor window
        buttonThrowers, pointerWatcherNodes = self.setupMouseCB( self.win )
        self.edMouseWatcher = buttonThrowers[0].getParent()
        self.edMouseWatcherNode = self.edMouseWatcher.node()
        self.edMouseWatcherParent = self.edMouseWatcher.getParent()
        
    def SetupEdCamera( self ):
        
        # Create editor camera
        self.edCamera = p3d.EditorCamera( 
            'camera', 
            style=p3d.CAM_VIEWPORT_AXES,
            speed=0.5, 
            rootNp=self.edRender,
            rootP2d=self.edPixel2d,
            win=self.win,
            mouseWatcherNode=self.edMouseWatcherNode 
        )
        self.edCamera.reparentTo( self.edRender )
        self.edCamera.Start()
        
        # Modify the existing display region and create a new one for the 
        # editor camera.
        self.dr = base.cam.node().getDisplayRegion( 0 )
        self.dr.setClearColorActive( True )
        self.dr.setClearColor( self.getBackgroundColor() )
        self.dr.setSort( 1 )
        self.dr.setActive( False )
        self.edDr = self.win.makeDisplayRegion( 0, 1, 0, 1 )
        self.edDr.setCamera( self.edCamera )
        
    def windowEvent( self, *args, **kwargs ):
        """
        Overridden so as to fix the aspect ratio of the editor camera and
        editor pixel2d.
        """
        P3dShowBase.ShowBase.windowEvent( self, *args, **kwargs )
        
        for win, cam, pixel2d in self.forcedAspectWins:
            aspectRatio = self.getAspectRatio( win )
            cam.node().getLens().setAspectRatio( aspectRatio )
            
            # Fix pixel2d scale for new window size
            # Temporary hasattr for old Pandas
            if not hasattr( win, 'getSbsLeftXSize' ):
                pixel2d.setScale( 2.0 / win.getXSize(), 1.0, 2.0 / win.getYSize() )
            else:
                pixel2d.setScale( 2.0 / win.getSbsLeftXSize(), 1.0, 2.0 / win.getSbsLeftYSize() )
            
    def GetEditorRenderMasks( self ):
        """
        Return the show, hide and clear masks for objects that are to be 
        rendered only in the editor viewport.
        """
        show = pm.BitMask32()
        show.setRangeTo( True, 28, 4 )
        hide = pm.BitMask32().allOn()
        hide.setRangeTo( False, 28, 4 )
        clear = pm.BitMask32()
        
        return show, hide, clear
            
    def SetupCameraMask( self ):
        """
        Set camera mask to draw all objects but those with the first four bits
        flipped. All editor geometry will use these bits so as to not be
        rendered in the game view.
        """
        bits = self.cam.node().getCameraMask()
        bits.setRangeTo( False, 28, 4 )
        self.cam.node().setCameraMask( bits )
        
        # Set edRender mask
        self.edRender.node().adjustDrawMask( *self.GetEditorRenderMasks() )
            
    def SetupRenderMask( self ):
        """
        Set the draw mask for the render node to be visible to all cameras.
        Since we are adjusting the draw mask of the render node's parent we
        need to manually set this node's mask or it will inherit those 
        properties.
        """
        showMask = pm.BitMask32().allOn()
        hideMask = pm.BitMask32()
        clearMask = pm.BitMask32()
        render.node().adjustDrawMask( showMask, hideMask, clearMask )
            
    def Reset( self ):
        """Remove all default nodes and recreate them."""
        # Remove cam node and camera
        self.cam.removeNode()
        self.cam = None
        self.camera.removeNode()
        self.camera = None
        
        # Recreate all default nodes. Remove the new display region created
        # by makeCamera() and connect the new camera to the existing one.
        self.setupRender()
        self.makeCamera( self.win )
        dr = self.cam.node().getDisplayRegion( 0 )
        self.win.removeDisplayRegion( dr ) 
        self.dr.setCamera( self.cam )
        __builtins__['render'] = self.render
        
        # Set up masks
        self.SetupCameraMask()
        self.SetupRenderMask()
            
    def ResetModelPath( self ):
        """
        Clears the model path, making sure to restore the current working 
        directory (so editor models can still be found).
        """
        pm.getModelPath().clear()
        pm.getModelPath().prependDirectory( '.' )
        
    def DisableEditorMouse( self ):
        self.edMouseWatcher.detachNode()
            
    def EnableEditorMouse( self ):
        self.edMouseWatcher.reparentTo( self.edMouseWatcherParent )