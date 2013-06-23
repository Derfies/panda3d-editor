import os
import traceback

import wx
from direct.directtools.DirectGrid import DirectGrid
from wx.lib.pubsub import Publisher as pub
import pandac.PandaModules as pm
import panda3d.core as pc

import p3d
import wxExtra
import ui
import editor
import gizmos
import actions
import commands as cmds
from project import Project
from showBase import ShowBase
from selection import Selection
from assetManager import AssetManager
from dragDropManager import DragDropManager
    

class App( p3d.wx.App ):
    
    """Base editor class."""
    
    def OnInit( self ):
        self.gizmo = False
        self._xformTask = None
        
        # Bind publisher events
        pub.subscribe( self.OnUpdate, 'Update' )
        
        # Build main frame, start Panda and replace the wx event loop with
        # Panda's.
        self.frame = ui.MainFrame( None, size=(800, 600) )
        ShowBase( self.frame.pnlViewport )
        self.ReplaceEventLoop()
        self.frame.Show()
        wx.CallAfter( self.FinishInit )
        
        return True
    
    def FinishInit( self ):
        base.FinishInit()
        
        # Create project manager
        self.project = Project( self )
        base.project = self.project
        self.frame.SetProjectPath( self.frame.cfg.Read( 'projDirPath' ) )
        
        # Create grid
        self.SetupGrid()
        
        # Create frame rate meter
        self.frameRate = p3d.FrameRate()
        
        # Create shading mode keys
        dsp = p3d.DisplayShading()
        dsp.accept( '4', dsp.Wireframe )
        dsp.accept( '5', dsp.Shade )
        dsp.accept( '6', dsp.Texture )
        
        # Set up gizmos
        self.SetupGizmoManager()
        
        # Bind mouse events
        self.accept( 'mouse1', self.OnMouse1Down )
        self.accept( 'shift-mouse1', self.OnMouse1Down, [True] )
        self.accept( 'control-mouse1', self.OnMouse1Down )
        self.accept( 'mouse2', self.OnMouse2Down )
        self.accept( 'mouse1-up', self.OnMouse1Up )
        self.accept( 'mouse2-up', self.OnMouse2Up )
        
        # Create selection manager
        self.selection = Selection(
            camera=base.edCamera, 
            root2d=base.edRender2d, 
            win=base.win, 
            mouseWatcherNode=base.edMouseWatcherNode 
        )
        base.selection = self.selection
        
        # Create our managers.
        self.assetMgr = AssetManager()
        self.dDropMgr = DragDropManager()
        self.actnMgr = actions.Manager()
        
        # Bind events
        self.accept( 'z', self.Undo )
        self.accept( 'shift-z', self.Redo )
        self.accept( 'f', self.FrameSelection )
        self.accept( 'del', lambda fn: cmds.Remove( fn() ), [self.selection.Get] )
        self.accept( 'backspace', lambda fn: cmds.Remove( fn() ), [self.selection.Get] )
        self.accept( 'control-d', lambda fn: cmds.Duplicate( fn() ), [self.selection.Get] )
        self.accept( 'control-g', lambda fn: cmds.Group( fn() ), [self.selection.Get] )
        self.accept( 'control-s', self.frame.OnFileSave, [None] )
        self.accept( 'arrow_up', lambda fn: cmds.Select( fn() ), [self.selection.SelectParent] )
        self.accept( 'arrow_down', lambda fn: cmds.Select( fn() ), [self.selection.SelectChild] )
        self.accept( 'arrow_left', lambda fn: cmds.Select( fn() ), [self.selection.SelectPrev] )
        self.accept( 'arrow_right', lambda fn: cmds.Select( fn() ), [self.selection.SelectNext] )
        self.accept( 'projectFilesModified', self.OnProjectFilesModified )
        
        # Create a "game"
        self.game = editor.Base()
        self.game.OnInit()
        
        # Start with a new scene
        self.CreateScene()
        self.doc.OnRefresh()
        
        return True
    
    def SetupGrid( self ):
        """Create the grid and set up its appearance."""
        self.grid = DirectGrid( 
            gridSize=20.0,
            gridSpacing=1.0,
            planeColor=(0.5, 0.5, 0.5, 0.0),
            parent=base.edRender
        )
        self.grid.snapMarker.hide()
        self.grid.centerLines.setColor( (0, 0, 0, 0) )
        self.grid.centerLines.setThickness( 2 )
        self.grid.majorLines.setColor( (0.25, 0.25, 0.25, 0) )
        self.grid.majorLines.setThickness( 1 )
        self.grid.minorLines.setColor( (0.5, 0.5, 0.5, 0) )
        self.grid.updateGrid()
    
    def SetupGizmoManager( self ):
        """Create gizmo manager."""
        gizmoMgrRootNp = base.edRender.attachNewNode( 'gizmoManager' )
        kwargs = {
            'camera':base.edCamera, 
            'rootNp':gizmoMgrRootNp, 
            'win':base.win, 
            'mouseWatcherNode':base.edMouseWatcherNode
        }
        self.gizmoMgr = gizmos.Manager( **kwargs )
        self.gizmoMgr.AddGizmo( gizmos.Translation( 'pos', **kwargs ) )
        self.gizmoMgr.AddGizmo( gizmos.Rotation( 'rot', **kwargs ) )
        self.gizmoMgr.AddGizmo( gizmos.Scale( 'scl', **kwargs ) )
        
        # Bind gizmo manager events
        self.accept( 'q', self.SetActiveGizmo, [None] )
        self.accept( 'w', self.SetActiveGizmo, ['pos'] )
        self.accept( 'e', self.SetActiveGizmo, ['rot'] )
        self.accept( 'r', self.SetActiveGizmo, ['scl'] )
        self.accept( 'space', self.ToggleGizmoLocal )
        self.accept( '+', self.gizmoMgr.SetSize, [2] )
        self.accept( '-', self.gizmoMgr.SetSize, [0.5] )
        
    def SetActiveGizmo( self, name ):
        self.gizmoMgr.SetActiveGizmo( name )
        self.frame.OnUpdateXform( None )
        
    def SetGizmoLocal( self, val ):
        self.gizmoMgr.SetLocal( val )
        self.frame.OnUpdateXform( None )
        
    def ToggleGizmoLocal( self ):
        self.gizmoMgr.ToggleLocal()
        self.frame.OnUpdateXform( None )
        
    def OnMouse1Down( self, shift=False ):
        """
        Handle mouse button 1 down event. Start the drag select operation if
        a gizmo is not being used and the alt key is not down, otherwise start 
        the transform operation.
        """
        if ( not self.gizmoMgr.IsDragging() and 
             p3d.MOUSE_ALT not in base.edCamera.mouse.modifiers ):
            self.selection.StartDragSelect( shift )
        elif self.gizmoMgr.IsDragging():
            self.StartTransform()
            
    def OnMouse2Down( self ):
        """
        Handle mouse button 2 down event. Start the transform operation if a
        gizmo is being used.
        """
        if self.gizmoMgr.IsDragging():
            self.StartTransform()
                    
    def OnMouse1Up( self ):
        """
        Handle mouse button 1 up event. Stop the drag select operation if the
        marquee is running, otherwise stop the transform operation if a gizmo
        is being used.
        """
        if self.selection.marquee.IsRunning():
            
            # Don't perform selection if there are no nodes and the selection
            # is currently empty.
            selNodes = self.selection.StopDragSelect()
            if self.selection.comps or selNodes:
                cmds.Select( selNodes )
        elif self.gizmoMgr.IsDragging() or self.gizmo:
            self.StopTransform()
            
    def OnMouse2Up( self ):
        """
        Handle mouse button 2 up event. Stop the transform operation if a 
        gizmo is being used.
        """
        if self.gizmoMgr.IsDragging() or self.gizmo:
            self.StopTransform()
            
    def StartTransform( self ):
        """
        Start the transfrom operation by adding a task to constantly send a
        selection modified message while transfoming.
        """
        self.gizmo = True
        self._xformTask = taskMgr.add( self.doc.OnSelectionModified, 
                                       'SelectionModified' )
            
    def StopTransform( self ):
        """
        Stop the transfrom operation by removing the selection modified 
        message task. Also create a transform action and push it onto the undo 
        queue.
        """
        # Remove the transform task
        if self._xformTask in taskMgr.getAllTasks():
            taskMgr.remove( self._xformTask )
            self._xformTask = None
            
        actGizmo = self.gizmoMgr.GetActiveGizmo()
        actns = []
        for i, np in enumerate( actGizmo.attachedNps ):
            actns.append( actions.Transform( np, np.getTransform(), actGizmo.initNpXforms[i] ) )
        actn = actions.Composite( actns )
        self.actnMgr.Push( actn )
        self.gizmo = False
        
        # Make sure to mark the NodePath as dirty in case it is a child of a
        # model root.
        wrpr = base.game.nodeMgr.Wrap( np )
        wrpr.SetModified( True )
        
        # Call OnModified next frame. Not sure why but if we call it straight
        # away it causes a small jitter when xforming...
        taskMgr.doMethodLater( 0, self.doc.OnModified, 'dragDrop' )
        
    def FrameSelection( self ):
        """
        Call frame selection on the camera if there are some node paths in the 
        selection.
        """
        nps = self.selection.GetNodePaths()
        if nps:
            base.edCamera.Frame( nps )
        else:
            base.edCamera.Frame( [base.scene.rootNp] )
            
    def OnUpdate( self, msg ):
        """
        Subscribed to the update selection message. Make sure that the
        selected nodes are attached to the managed gizmos, then refresh the
        active one.
        """
        nps = self.selection.GetNodePaths()
        self.gizmoMgr.AttachNodePaths( nps )
        self.gizmoMgr.RefreshActiveGizmo()
        self.selection.Update()
                    
    def CreateScene( self, filePath=None, newDoc=True ):
        """
        Create an empty scene and set its root node to the picker's root node.
        """
        # Reset undo queue if creating a new document
        if newDoc:
            self.actnMgr.Reset()
        
        # Close the current scene if there is one
        self.selection.Clear()
        if hasattr( self, 'scene' ):
            self.scene.Close()
            
        # Create a new scene
        self.scene = editor.Scene()
        self.scene.rootNp.reparentTo( base.edRender )
        
        # Set the selection and picker root node to the scene's root node
        self.selection.rootNp = self.scene.rootNp
        self.selection.picker.rootNp = self.scene.rootNp
        self.selection.marquee.rootNp = self.scene.rootNp
        
        # Create the document wrapper if creating a new document
        if newDoc:
            self.doc = ui.Document( filePath, self.scene )
        
    def AddComponent( self, typeStr, *args, **kwargs ):
        wrprCls = base.game.nodeMgr.GetWrapperByName( typeStr )
        wrpr = wrprCls.Create( *args, **kwargs )
        wrpr.SetDefaultValues()
        wrpr.SetParent( wrpr.GetDefaultParent() )
        
        # Bit of a hack. Sometimes a wrapper can create multiple components 
        # when Create is called. Make sure to set default values on all the 
        # components that were created.
        if hasattr( wrpr, 'extraNps' ):
            for np in wrpr.extraNps:
                eWrpr = base.game.nodeMgr.Wrap( np )
                eWrpr.SetDefaultValues()
        cmds.Add( [wrpr.data] )
        
        return wrpr
        
    def OnProjectFilesModified( self, filePaths ):
        self.assetMgr.OnAssetModified( filePaths )
        self.game.pluginMgr.OnProjectFilesModified( filePaths )
        
    def Undo( self ):
        self.actnMgr.Undo()
        self.doc.OnModified()
        
    def Redo( self ):
        self.actnMgr.Redo()
        self.doc.OnModified()
        
    def Group( self ):
        nps = self.selection.GetNodePaths()
        if nps:
            cmds.Group( nps )
        
    def Ungroup( self ):
        nps = self.selection.GetNodePaths()
        if nps:
            cmds.Ungroup( nps )
        
    def Parent( self ):
        pass
        
    def Unparent( self ):
        pass