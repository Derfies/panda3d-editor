import panda3d.core as pm
from direct.showbase.ShowBase import ShowBase

import p3d
from direct.showbase import ShowBaseGlobal
from pandaEditor.ui.mainFrame import MainFrame


class App(ShowBase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.forcedAspectWins = []

        self.startWx()
        self.frame = MainFrame(None, size=(800, 600))
        self.frame.Show()
        self.frame.pnlViewport.Initialize()

        self.SetupEdRender()
        self.SetupEdRender2d()
        self.SetupEdMouseWatcher()
        self.SetupEdCamera()

        # Make additional camera for 2d nodes
        cam2d = self.makeCamera2d( self.win )
        cam2d.reparentTo( self.edRender2d )

        # Add the editor window, camera and pixel 2d to the list of forced
        # aspect windows so aspect is fixed when the window is resized.
        self.forcedAspectWins.append((self.win, self.edCamera, self.edPixel2d))

        self.Reset()
        self.frame.app.FinishInit()
        self.windowEvent(None)
        
    def SetupEdRender( self ):
        """
        Create editor root node behind render node so we can keep editor only
        nodes out of the scene.
        """
        self.edRender = pm.NodePath( 'edRender' )
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
            pos=(56, 56, 42),
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
        self.dr.setActive( False )
        self.dr.setSort( 20 )
        
        self.dr2d = base.cam2d.node().getDisplayRegion( 0 )
        self.dr2d.setActive( False )
        self.dr2d.setSort( 21 )
        
        self.edDr = self.win.makeDisplayRegion( 0, 1, 0, 1 )
        self.edDr.setCamera( self.edCamera )
        self.edDr.setClearColorActive( True )
        self.edDr.setClearColor( (0.63, 0.63, 0.63, 0) )
        
    def windowEvent(self, *args, **kwargs):
        """
        Overridden so as to fix the aspect ratio of the editor camera and
        editor pixel2d.
        """
        super().windowEvent(*args, **kwargs)

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
            
    def Reset(self):


        """Remove all default nodes and recreate them."""
        # Remove all default nodes and set them to None so they are recreated
        # properly.
        for name in ('cam', 'camera', 'cam2d', 'camera2d'):
            np = getattr(self, name)
            np.removeNode()
            setattr(self, name, None)
        
        # Set up render and render2d again, forcing their new values into
        # builtins.
        self.setupRender()

        # This is kinda lame imho. These default nodes are created by importing
        # the showbase global module, which makes it difficult to recreate these
        # nodes for our purposes.
        render2d = pm.NodePath('render2d')
        aspect2d = render2d.attachNewNode(pm.PGTop('aspect2d'))
        ShowBaseGlobal.render2d = render2d
        ShowBaseGlobal.aspect2d = aspect2d
        self.setupRender2d()

        __builtins__['render'] = self.render
        __builtins__['render2d'] = self.render2d
        __builtins__['aspect2d'] = self.aspect2d
        __builtins__['pixel2d'] = self.pixel2d
        
        self.makeCamera( self.win )
        self.makeCamera2d( self.win )
        __builtins__['camera'] = self.camera
        
        for cam, dr in {self.cam:self.dr, self.cam2d:self.dr2d}.items():
            defaultDr = cam.node().getDisplayRegion( 0 )
            self.win.removeDisplayRegion( defaultDr ) 
            dr.setCamera( cam )
        
        # Set up masks
        self.SetupCameraMask()
        self.SetupRenderMask()
        
        # Set auto shader.
        render.setShaderAuto()
            
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
        
    def LayoutGameView( self ):
        """Deactivate both display regions and enable mouse."""
        self.DisableEditorMouse()
        
        self.dr.setActive( True )
        self.dr.setDimensions( 0, 1, 0, 1 )
        self.dr2d.setActive( True )
        self.dr2d.setDimensions( 0, 1, 0, 1 )
        
        self.edRender2d.hide()
        self.edPixel2d.hide()
            
    def LayoutEditorView( self ):
        """Deactivate both display regions and enable mouse."""
        self.EnableEditorMouse()
        
        self.dr.setActive( False )
        self.dr2d.setActive( False )
        
        self.edDr.setActive( True )
        self.edRender2d.show()
        self.edPixel2d.show()
            
    def LayoutBothView( self ):
        """Deactivate both display regions and enable mouse."""
        self.EnableEditorMouse()
        
        self.dr.setActive( True )
        self.dr.setDimensions( 0.65, 1, 0.65, 1 )
        
        self.dr2d.setActive( True )
        self.dr2d.setDimensions( 0.65, 1, 0.65, 1 )
        
        self.edDr.setActive( True )
        self.edRender2d.show()
        self.edPixel2d.show()